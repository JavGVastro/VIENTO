"""Read and visualize the ideal GSTools PARAMETERS FITS convention.

Rows are [LM value, upper offset, lower offset]. Interval endpoints are
value-lower_offset and value+upper_offset, including signed offsets.
No observational seeing/noise parameters or custom fitting modules are needed.
"""
from pathlib import Path
import re
import warnings

import numpy as np
import pandas as pd
from astropy.io import fits
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

PARAMETERS = ("sig2", "r0", "m")
BATCH_KEYS = ("grid_size", "length_scale", "spatial_bin", "seed")
LABELS = {"sig2": r"$\sigma_{\mathrm{pos}}^2$ [velocity units$^2$]",
          "r0": r"$r_0$ [map length units]", "m": r"$m$"}
TITLES = {"sig2": r"$\sigma_{\mathrm{pos}}^2$", "r0": r"$r_0$", "m": r"$m$"}
_NUM = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def _match(pattern, value):
    match = re.search(pattern, value, re.I)
    return _number(match.group(1)) if match else np.nan


def _header_number(header, *keys):
    for key in keys:
        value = _number(header.get(key))
        if np.isfinite(value):
            return value
    return np.nan


def _prefer(a, b):
    return a if np.isfinite(a) else b


def _metadata(path, root, header):
    stem = re.sub(r"\.fits(?:\.gz)?$", "", path.name, flags=re.I)
    tag = re.search(r"_L(\d{3})$", stem, re.I)
    filename_fraction = int(tag.group(1)) / 100 if tag else np.nan
    header_fraction = _header_number(header, "FITFRAC")
    if np.isfinite(filename_fraction) and np.isfinite(header_fraction):
        if not np.isclose(filename_fraction, header_fraction, rtol=0, atol=1e-8):
            raise ValueError("FITFRAC and _Lnnn filename disagree")
    fraction = _prefer(header_fraction, filename_fraction)
    if np.isfinite(fraction) and not 0 < fraction <= 1:
        raise ValueError("Fitting fraction must be in (0, 1]")
    base = stem[:tag.start()] if tag else stem
    relative = path.relative_to(root)
    family = re.search(r"(?:^|_)(exponential|gaussian|stable)(?:_|$)", base, re.I)
    model = str(header.get("MODEL", family.group(1) if family else "unknown")).lower().strip()
    alpha = _prefer(_header_number(header, "ALPHA"), _match(r"(?:^|_)alpha(" + _NUM + r")(?=_|$)", base))
    grid = _prefer(_header_number(header, "GRID_N", "NGRID", "N"), _match(r"(?:^|_)N(\d+)(?=_|$)", base))
    # SHAPE may be a string such as '(64, 64, 64)'. Never use primary NAXIS.
    if not np.isfinite(grid):
        dimensions = re.findall(r"\d+", str(header.get("SHAPE", "")))
        if dimensions and len(set(dimensions)) == 1:
            grid = float(dimensions[0])
    length = _prefer(_header_number(header, "L_SCALE", "LENX"), _match(r"(?:^|_)L(" + _NUM + r")(?=_|$)", base))
    sig_e = _prefer(_header_number(header, "SIGE", "SIG_E"), _match(r"(?:^|_)sigE(" + _NUM + r")(?=_|$)", base))
    bin_value = _match(r"(?:^|_)bin(\d+)(?=_|$)", base)
    # Filenames without a bin suffix are treated as native bin 0.
    bin_value = _prefer(bin_value, _header_number(header, "BIN", "BIN_LEVEL"))
    spatial_bin = int(bin_value) if np.isfinite(bin_value) else 0
    label = f"stable (alpha={alpha:g})" if model == "stable" and np.isfinite(alpha) else model
    return dict(file_name=path.name, file_path=str(path), relative_path=relative.as_posix(),
                source_dir=relative.parent.as_posix(),
                sample_id=(relative.parent / base).as_posix(), model=model, alpha=alpha,
                model_label=label, grid_size=grid, length_scale=length,
                spatial_bin=spatial_bin, sigE=sig_e,
                seed=_header_number(header, "SEED_V", "VSEED", "SEED"),
                fit_limit=fraction, fit_kind="fraction" if np.isfinite(fraction) else "baseline",
                fraction_source="FITFRAC" if np.isfinite(header_fraction) else ("filename" if tag else "unknown"),
                fit_model=str(header.get("FITMODEL", "unrecorded")),
                box_size=_header_number(header, "BOX_SIZE"),
                relative_uncertainty=_header_number(header, "RELUNC"),
                n_fit=_header_number(header, "NFIT"), redchi=_header_number(header, "REDCHI"),
                m3d=_header_number(header, "M3D"), m2d=_header_number(header, "M2D"))


def load_results(fits_dir, *, recursive=True, reference_keys=None, metadata_overrides=None):
    """Read every fitted .fits/.fits.gz once; return (tidy rows, file/row issues).

    Default reference headers are SIG2, R0 and M2D. They are labelled header
    references, not guaranteed truth. No M3D or L_SCALE fallback is applied.
    Overrides are indexed by relative_path, e.g. {'map_L020.fits': {'sigE': 0}}.
    Original maps without PARAMETERS are reported as skipped, not fabricated.
    """
    root = Path(fits_dir).expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"FITS directory does not exist: {root}")
    reference_keys = reference_keys or {"sig2": "SIG2", "r0": "R0", "m": "M2D"}
    metadata_overrides = metadata_overrides or {}
    iterator = root.rglob("*") if recursive else root.glob("*")
    paths = sorted(p for p in iterator if p.is_file() and re.search(r"\.fits(?:\.gz)?$", p.name, re.I))
    rows, issues = [], []
    for path in paths:
        try:
            with fits.open(path, memmap=False) as hdul:
                matches = [h for h in hdul if h.name.upper() == "PARAMETERS"]
                if not matches:
                    issues.append(dict(file_name=path.name, severity="skipped", detail="No PARAMETERS extension"))
                    continue
                if len(matches) != 1:
                    raise ValueError("Multiple PARAMETERS extensions")
                hdu = matches[0]
                if hdu.data is None or len(hdu.data) != 3:
                    raise ValueError("Expected exactly 3 rows: value, upper offset, lower offset")
                names = {s.lower(): s for s in hdu.columns.names}
                missing = set(PARAMETERS) - names.keys()
                if missing:
                    raise ValueError(f"Missing ideal-fit columns: {sorted(missing)}")
                if {"noise", "s0"} & names.keys():
                    raise ValueError("This is a seeing/noise fit; expected an ideal 3-parameter table")
                header = hdul[0].header
                meta = _metadata(path, root, header)
                meta.update(metadata_overrides.get(meta["relative_path"], {}))
                if meta["model"] == "unknown" or not np.isfinite(meta["sigE"]):
                    raise ValueError("Cannot identify MODEL or sigE; provide metadata_overrides")
                if meta["model"] == "stable" and not np.isfinite(meta["alpha"]):
                    raise ValueError("Stable ALPHA missing; provide metadata_overrides")
                meta["model_label"] = (f"stable (alpha={meta['alpha']:g})"
                                       if meta["model"] == "stable" else meta["model"])
                ci_level = _number(hdu.header.get("CILEVEL"))
                new_rows = []
                for param in PARAMETERS:
                    values = np.asarray(hdu.data[names[param]], dtype=float).reshape(-1)
                    if values.size != 3 or not np.isfinite(values[0]):
                        raise ValueError(f"Invalid scalar values in {param}")
                    value, upper, lower = values
                    low, high = value - lower, value + upper
                    valid_ci = bool(np.isfinite(low) and np.isfinite(high) and low <= high)
                    outside = bool(valid_ci and not low <= value <= high)
                    refkey = reference_keys.get(param)
                    ref = _number(header.get(refkey)) if refkey else np.nan
                    new_rows.append(dict(meta, parameter=param, value=value,
                                         err_upper=upper, err_lower=lower,
                                         interval_low=low, interval_high=high,
                                         interval_valid=valid_ci, center_outside_interval=outside,
                                         ci_level=ci_level, reference=ref,
                                         reference_key=refkey or "none", summary_kind="individual"))
                    if not valid_ci or outside:
                        issues.append(dict(file_name=path.name, severity="warning",
                                           detail=f"{param}: " + ("invalid/missing interval; plot center only" if not valid_ci
                                                                   else "LM value outside posterior interval; preserve endpoints")))
                rows.extend(new_rows)
        except Exception as exc:
            issues.append(dict(file_name=path.name, severity="error", detail=str(exc)))
    table = pd.DataFrame(rows)
    if not table.empty:
        duplicated = table.duplicated(["sample_id", "fit_kind", "fit_limit", "parameter"], keep=False)
        if duplicated.any():
            files = table.loc[duplicated, "relative_path"].unique().tolist()
            raise ValueError(f"Duplicate fits for the same sample/fraction (possibly .fits + .fits.gz): {files}")
        table = table.sort_values(["sample_id", "fit_limit", "parameter"], na_position="first").reset_index(drop=True)
    return table, pd.DataFrame(issues, columns=["file_name", "severity", "detail"])


def filter_results(table, **filters):
    """Filter metadata; None means all. Numeric selection uses isclose."""
    result = table.copy()
    if result.empty:
        return result
    for key, value in filters.items():
        if value is None:
            continue
        if key not in result:
            raise KeyError(key)
        values = value if isinstance(value, (tuple, list, set, np.ndarray)) else [value]
        mask = np.zeros(len(result), dtype=bool)
        for item in values:
            if pd.api.types.is_numeric_dtype(result[key]) and isinstance(item, (int, float, np.number)):
                mask |= np.isclose(result[key].to_numpy(dtype=float), item, rtol=0, atol=1e-8, equal_nan=True)
            else:
                mask |= result[key].eq(item).to_numpy()
        result = result.loc[mask].copy()
    return result


def select_fraction(table, fraction):
    """None explicitly selects untagged baselines; no assumed 0.6 fraction."""
    if table.empty:
        return table.copy()
    if fraction is None:
        return table.loc[table.fit_kind == "baseline"].copy()
    return filter_results(table.loc[table.fit_kind == "fraction"], fit_limit=float(fraction))


def inventory(table):
    if table.empty:
        return table.copy()
    columns = ["sample_id", "model_label", "sigE", *BATCH_KEYS, "fit_kind", "fit_limit",
               "relative_uncertainty", "fit_model", "redchi", "n_fit", "relative_path"]
    return table.drop_duplicates("file_path")[columns].reset_index(drop=True)


def fraction_coverage(table, expected=(.2, .3, .4, .5, .6, .7, .8, .9, .99)):
    """Availability for discovered samples only; not a prediction of absent models."""
    output = []
    if table.empty:
        return pd.DataFrame()
    for sample, data in table.groupby("sample_id", sort=True):
        row = {"sample_id": sample}
        found = data.fit_limit.dropna().unique()
        for fraction in expected:
            row[f"L{round(100*fraction):03d}"] = bool(np.isclose(found, fraction, rtol=0, atol=1e-8).any())
        output.append(row)
    return pd.DataFrame(output).set_index("sample_id")


def iter_batches(table, keys=BATCH_KEYS):
    """Yield (title, table) without mixing sizes, length scales, bins or seeds."""
    if table.empty:
        return
    for values, group in table.groupby(list(keys), dropna=False, sort=True):
        if not isinstance(values, tuple):
            values = (values,)
        title = ", ".join(f"{key}={value:g}" if isinstance(value, (int, float)) and np.isfinite(value)
                          else f"{key}={value}" for key, value in zip(keys, values))
        yield title, group.copy()


def summarize_fractions(table, selected=(.4, .5, .6), *, by_sample=None, require_all=True):
    """Descriptive average and interval envelope; NOT combined posterior errors.

    Nested SF fits are dependent. Export scatter and span of centers separately
    from [minimum lower bound, maximum upper bound]. A single fraction retains
    its original bounds. Missing requested fractions are explicitly reported.
    """
    output, issues = [], []
    if table.empty:
        return pd.DataFrame(), pd.DataFrame()
    fractions = table.loc[table.fit_kind == "fraction"]
    for sample, original in fractions.groupby("sample_id", sort=True):
        chosen = tuple(sorted(set((by_sample or {}).get(sample, selected))))
        if not chosen or any(not 0 < x <= 1 for x in chosen):
            raise ValueError(f"Invalid selected fractions for {sample}: {chosen}")
        found = original.fit_limit.unique()
        missing = [x for x in chosen if not np.isclose(found, x, rtol=0, atol=1e-8).any()]
        if missing:
            issues.append(dict(sample_id=sample, missing_fractions=tuple(missing),
                               action="omitted" if require_all else "partial summary"))
            if require_all:
                continue
        selected_data = filter_results(original, fit_limit=chosen)
        for param, data in selected_data.groupby("parameter", sort=False):
            row = data.iloc[0].to_dict()
            mean = float(data.value.mean())
            all_ci = bool(data.interval_valid.all())
            low = float(data.interval_low.min()) if all_ci else np.nan
            high = float(data.interval_high.max()) if all_ci else np.nan
            refs = data.reference.to_numpy(dtype=float)
            # A reference must belong to this exact sample and remain unchanged across fits.
            same_ref = np.isfinite(refs).all() and np.allclose(refs, refs[0], rtol=1e-8, atol=1e-12)
            if np.isfinite(refs).any() and not same_ref:
                issues.append(dict(sample_id=sample, missing_fractions=(), action=f"{param}: reference varies; summary reference omitted"))
            row.update(value=mean, interval_low=low, interval_high=high,
                       err_lower=mean-low, err_upper=high-mean, interval_valid=all_ci,
                       center_outside_interval=bool(all_ci and not low <= mean <= high),
                       fit_limit=np.nan, fit_kind="selected_summary", summary_kind="mean + interval envelope",
                       fit_limits_used=tuple(sorted(data.fit_limit)), n_fractions=len(data),
                       fraction_std=float(data.value.std(ddof=1)) if len(data) > 1 else 0.0,
                       value_min=float(data.value.min()), value_max=float(data.value.max()),
                       relative_span=float(np.ptp(data.value)/abs(mean)) if mean else np.nan,
                       reference=float(refs[0]) if same_ref else np.nan,
                       file_path="; ".join(data.file_path), relative_path="; ".join(data.relative_path),
                       file_name="selected summary", redchi=np.nan, n_fit=np.nan,
                       ci_level=np.nan, relative_uncertainty=np.nan)
            output.append(row)
    return pd.DataFrame(output), pd.DataFrame(issues)


def _one_batch(table):
    for key in BATCH_KEYS:
        if table[key].nunique(dropna=False) > 1:
            raise ValueError(f"Multiple {key} values: use iter_batches or filter_results before plotting")


def _models(table, model_order):
    present = list(table.model_label.unique())
    if model_order:
        return [m for m in model_order if m in present] + sorted(set(present)-set(model_order))
    rank = {"exponential": 0, "stable": 1, "gaussian": 2}
    return sorted(present, key=lambda m: (rank.get(m.split(" ")[0], 9), m))


def _values(data, normalize):
    data = data.copy()
    if normalize:
        valid = np.isfinite(data.reference) & (data.reference > 0)
        if not valid.all():
            warnings.warn(f"Omitting {int((~valid).sum())} values without a positive header reference", stacklevel=2)
        data = data.loc[valid].copy()
        for column in ("value", "interval_low", "interval_high"):
            data[column] /= data.reference
        data["reference"] = 1.0
    return data


def _intervals(ax, x, data, color):
    """Draw actual endpoints independently of the LM marker (signed offsets safe)."""
    good = data.interval_valid.to_numpy(dtype=bool)
    xx = np.asarray(x)[good]
    ax.vlines(xx, data.interval_low.to_numpy()[good], data.interval_high.to_numpy()[good], color=color, alpha=.75, lw=1.4)
    ax.plot(xx, data.interval_low.to_numpy()[good], linestyle="none", marker="_", color=color, ms=7)
    ax.plot(xx, data.interval_high.to_numpy()[good], linestyle="none", marker="_", color=color, ms=7)
    outside = data.center_outside_interval.to_numpy(dtype=bool)
    ax.scatter(np.asarray(x)[outside], data.value.to_numpy()[outside], s=85, facecolors="none", edgecolors="crimson", zorder=6)


def _legend(fig, levels, references, selected=False, summary=False, outside=False):
    cmap = plt.get_cmap("tab10")
    handles = [Line2D([], [], color=cmap(i % 10), marker="o", label=rf"$\sigma_E={level:g}$")
               for i, level in enumerate(levels)]
    handles += [Line2D([], [], color="0.4", marker="|", linestyle="none", markersize=13,
                       label="Interval envelope" if summary else "Stored posterior interval")]
    if references:
        handles += [Line2D([], [], color="0.4", linestyle="--", label="Header reference (same map)")]
    if selected:
        handles += [Line2D([], [], marker="o", color="k", markerfacecolor="none", linestyle="none", label="Selected fractions")]
    if outside:
        handles += [Line2D([], [], marker="o", color="crimson", markerfacecolor="none", linestyle="none", label="LM outside interval")]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, 1.0), ncol=min(4,len(handles)), frameon=False)


def plot_parameters(table, *, params=PARAMETERS, model_order=None, sigE_levels=(0,1,2),
                    reference=True, normalize=False, labels=None, ylims=None,
                    figsize=(15,5.6), title=None, markersize=6, jitter=.18):
    """One row, models on x, sigE colors; pass one fraction or a selected summary."""
    if table.empty:
        raise ValueError("No results to plot")
    _one_batch(table)
    if table.duplicated(["model_label", "sigE", "parameter"]).any():
        raise ValueError("Multiple results per model/sigE: select one fraction and realization, or summarize_fractions first")
    levels = [x for x in sigE_levels if np.isclose(table.sigE, x).any()]
    if not levels:
        raise ValueError("No requested sigE levels found")
    models = _models(table, model_order)
    fig, axs = plt.subplots(1,len(params),figsize=figsize,squeeze=False)
    axes=axs.ravel()
    for ax,param in zip(axes,params):
        for i,level in enumerate(levels):
            data = _values(filter_results(table,parameter=param,sigE=level), normalize)
            color=plt.get_cmap("tab10")(i % 10)
            x=np.array([models.index(m) for m in data.model_label],dtype=float)+(i-(len(levels)-1)/2)*jitter
            _intervals(ax,x,data,color)
            ax.plot(x,data.value,marker="o",ls="none",color=color,ms=markersize,zorder=4)
            if reference:
                for xx,ref in zip(x,data.reference):
                    if np.isfinite(ref):
                        ax.hlines(ref,xx-.055,xx+.055,color=color,linestyle="--",lw=2.2)
        tick_labels = [re.sub(r"stable \(alpha=([^)]+)\)",
                              lambda match: "stable\n" + rf"$\alpha={match.group(1)}$", m)
                       for m in models]
        ax.set_xticks(range(len(models)), tick_labels)
        ax.tick_params(axis="x", labelsize=10)
        ax.set_title(TITLES.get(param,param))
        ax.set_ylabel("Fit / header reference" if normalize else (labels or LABELS).get(param,param))
        ax.grid(axis="y",alpha=.2)
        if ylims and param in ylims: ax.set_ylim(*ylims[param])
    _legend(fig,levels,reference,summary=bool((table.summary_kind != "individual").any()),
            outside=bool(table.center_outside_interval.any()))
    fig.supxlabel(title or "Ideal GSTools fit parameters",y=.015)
    fig.tight_layout(rect=(0,.045,1,.86))
    return fig,axes


def plot_fraction_grid(table, *, selected=(.4,.5,.6), selected_by_sample=None, summary=None,
                       params=PARAMETERS, model_order=None, sigE_levels=(0,1,2), reference=True,
                       normalize=False, labels=None, ylims=None, title=None, figsize=None):
    """Rows=models, columns=parameters, colored curves=sigE. One batch per figure."""
    table=table.loc[table.fit_kind == "fraction"].copy()
    if table.empty: raise ValueError("No fraction fits to plot")
    _one_batch(table)
    if table.duplicated(["model_label","sigE","fit_limit","parameter"]).any():
        raise ValueError("Duplicate model/sigE/fraction; filter one realization or source_dir")
    # Different realizations with disjoint fractions must not be connected, either.
    counts=table.groupby(["model_label","sigE"]).sample_id.nunique()
    if (counts>1).any(): raise ValueError("Multiple sample_ids per model/sigE; filter one realization/source_dir")
    models=_models(table,model_order)
    levels=[x for x in sigE_levels if np.isclose(table.sigE,x).any()]
    if not levels: raise ValueError("No requested sigE levels found")
    figsize=figsize or (15,3.5*len(models)+1.0)
    fig,axes=plt.subplots(len(models),len(params),figsize=figsize,squeeze=False)
    for row,model in enumerate(models):
        for col,param in enumerate(params):
            ax=axes[row,col]
            for i,level in enumerate(levels):
                data=_values(filter_results(table,model_label=model,parameter=param,sigE=level),normalize).sort_values("fit_limit")
                if data.empty: continue
                color=plt.get_cmap("tab10")(i % 10)
                x=data.fit_limit.to_numpy()
                _intervals(ax,x,data,color)
                ax.plot(x,data.value,"o-",color=color,ms=4,lw=1)
                chosen=(selected_by_sample or {}).get(data.sample_id.iloc[0],selected)
                mask=np.array([any(np.isclose(v,f,rtol=0,atol=1e-8) for f in chosen) for v in x])
                ax.scatter(x[mask],data.value.to_numpy()[mask],s=75,facecolors="none",edgecolors="k",zorder=5)
                if reference:
                    refs=data.reference.to_numpy()
                    good=np.isfinite(refs)
                    if good.any():
                        ax.plot(x[good],refs[good],"--",color=color,alpha=.65,lw=1.2)
                if summary is not None and not summary.empty:
                    adopted=_values(filter_results(summary,sample_id=data.sample_id.iloc[0],parameter=param),normalize)
                    if len(adopted)==1:
                        a=adopted.iloc[0]
                        ax.axhline(a.value,color=color,ls=":",lw=1.5)
                        if a.interval_valid:
                            ax.axhspan(a.interval_low,a.interval_high,color=color,alpha=.06)
            ticks=np.sort(table.fit_limit.unique())
            ax.set_xticks(ticks)
            ax.tick_params(axis="x",labelsize=9,rotation=45 if len(ticks)>7 else 0)
            ax.set_xlabel(r"$L_{\rm fracc}$")
            ax.set_ylabel("Fit / header reference" if normalize else (labels or LABELS).get(param,param))
            ax.set_title(f"{model} — {TITLES.get(param,param)}",fontsize=11)
            ax.grid(alpha=.2)
            if ylims and param in ylims: ax.set_ylim(*ylims[param])
    _legend(fig,levels,reference,selected=True,outside=bool(table.center_outside_interval.any()))
    caption=title or "Ideal GSTools fits versus fitting fraction"
    if summary is not None and not summary.empty:
        caption+="\nDotted lines: selected means; faint bands: interval envelopes (descriptive)."
    fig.supxlabel(caption,y=.01,fontsize=10)
    top=1-.85/figsize[1]
    fig.tight_layout(rect=(0,.07,1,top))
    return fig,axes


def save_figure(fig, output_dir, name, formats=("pdf","png"), dpi=180):
    directory=Path(output_dir); directory.mkdir(parents=True,exist_ok=True)
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",name).strip("_")
    paths=[]
    for extension in formats:
        path=directory/f"{safe}.{extension}"
        fig.savefig(path,dpi=dpi,bbox_inches="tight")
        paths.append(path)
    return paths
