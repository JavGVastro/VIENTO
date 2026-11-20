"""Load, average, convert, and plot emission-line fit results.

The functions in this module use the result structure returned by
``results_comp.load_line_bundle_mat`` in the accompanying notebooks.  A fit
parameter is represented as ``[central_value, upper_error, lower_error]``.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Iterable, Mapping, Sequence
import warnings

import numpy as np
import pandas as pd


DEFAULT_PARAMS = ("sig2", "r0", "m", "noise", "s0")
DEFAULT_PARAM_TITLES = {
    "sig2": r"$\sigma^2$",
    "r0": r"$r_0$",
    "m": r"$m$",
    "noise": r"$B_\mathrm{noise}$",
    "s0": r"$s_0$",
}
DEFAULT_PARAM_LABELS = {
    "sig2": r"$\sigma^2$ [km$^2$ s$^{-2}$]",
    "r0": r"$r_0$ [pc]",
    "m": r"$m$",
    "noise": r"$B_\mathrm{noise}$ [km$^2$ s$^{-2}$]",
    "s0": r"$s_0$ [pc]",
}


def fit_limit_tag(fit_limit: float, decimals: int = 1) -> str:
    """Return the filename tag used by the original notebooks (0.3 -> '03')."""
    scale = 10**decimals
    width = decimals + 1
    return f"{int(round(float(fit_limit) * scale)):0{width}d}"


def build_fraction_sample_grid(
    dataset_configs: Sequence[Mapping],
    fit_limits: Iterable[float],
) -> list[dict]:
    """Build explicit file specifications for every dataset/bin/line/fraction.

    Each dataset configuration accepts these keys:

    ``group`` (required), ``dataset_prefix`` (required), ``bin_levels``
    (required), ``line_order`` (required), ``filename_template`` (optional),
    and ``file_line_ids`` (optional).  The filename template can use
    ``{dataset_prefix}``, ``{line}``, ``{file_line}``, ``{bin}``,
    ``{fit_limit}``, and ``{fit_tag}``.
    """
    samples: list[dict] = []
    limits = tuple(float(value) for value in fit_limits)

    for config in dataset_configs:
        group = config["group"]
        prefix = config["dataset_prefix"]
        line_order = tuple(config["line_order"])
        bin_levels = tuple(config["bin_levels"])
        file_line_ids = dict(config.get("file_line_ids", {}))
        template = config.get(
            "filename_template",
            "{dataset_prefix}-{file_line}-bin{bin}_{fit_tag}",
        )

        for bin_level in bin_levels:
            for line in line_order:
                file_line = file_line_ids.get(line, line)
                for fit_limit in limits:
                    tag = fit_limit_tag(fit_limit)
                    fields = {
                        "dataset_prefix": prefix,
                        "group": group,
                        "line": line,
                        "file_line": file_line,
                        "bin": bin_level,
                        "fit_limit": fit_limit,
                        "fit_tag": tag,
                    }
                    file_name = template.format(**fields)
                    samples.append(
                        {
                            "file_name": file_name,
                            "internal_name": (
                                f"{group}_{line}_bin{bin_level}_{tag}_line"
                                .replace(" ", "_")
                                .replace("-", "_")
                            ),
                            "label": f"{group} {line} bin{bin_level} {tag}",
                            "group": group,
                            "line": line,
                            "file_line": file_line,
                            "bin": bin_level,
                            "fit_limit": fit_limit,
                            "fit_limit_label": (
                                rf"$r_\mathrm{{max}} = {fit_limit:.1f}L$"
                            ),
                        }
                    )
    return samples


def load_explicit_result_samples(
    results_comp,
    maps_dir,
    samples: Sequence[Mapping],
    *,
    read_header: bool = True,
    fit_key: str = "fit",
    on_error: str = "raise",
    return_failures: bool = False,
):
    """Load explicit result specifications and attach their plotting metadata.

    Set ``on_error='warn'`` or ``'skip'`` when a grid may contain files that
    have not been produced yet.  With ``return_failures=True``, return
    ``(loaded_entries, failures)`` where each failure records its sample and
    exception message.
    """
    if on_error not in {"raise", "warn", "skip"}:
        raise ValueError("on_error must be 'raise', 'warn', or 'skip'.")

    loaded: list[dict] = []
    failures: list[dict] = []

    for sample_in in samples:
        sample = dict(sample_in)
        file_name = sample["file_name"]
        label = sample.get("label", file_name)
        internal_name = sample.get(
            "internal_name",
            f"{label}_line".replace(" ", "_").replace("-", "_"),
        )
        try:
            bundle = results_comp.load_line_bundle_mat(
                file_name,
                internal_name,
                maps_dir,
                read_header=read_header,
            )
            fit = bundle[fit_key]
            fit_dict = fit.to_dict(orient="list")
        except Exception as exc:
            if on_error == "raise":
                raise
            failure = {
                "file_name": file_name,
                "sample": sample,
                "error": f"{type(exc).__name__}: {exc}",
            }
            failures.append(failure)
            if on_error == "warn":
                warnings.warn(
                    f"Skipping {file_name!r}: {failure['error']}",
                    RuntimeWarning,
                    stacklevel=2,
                )
            continue

        entry = dict(sample)
        entry.update(
            {
                "label": label,
                "internal_name": internal_name,
                "bundle": bundle,
                "fit": fit,
                "fit_dict": fit_dict,
                "meta": dict(bundle.get("meta", {})),
            }
        )
        loaded.append(entry)

    return (loaded, failures) if return_failures else loaded


def load_multi_line_bin_fraction_results(
    results_comp,
    maps_dir,
    *,
    dataset_configs: Sequence[Mapping],
    fit_limits: Iterable[float] = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8),
    read_header: bool = True,
    fit_key: str = "fit",
    on_error: str = "raise",
    return_failures: bool = False,
):
    """Load the full dataset x bin x line x fit-limit grid."""
    samples = build_fraction_sample_grid(dataset_configs, fit_limits)
    return load_explicit_result_samples(
        results_comp,
        maps_dir,
        samples,
        read_header=read_header,
        fit_key=fit_key,
        on_error=on_error,
        return_failures=return_failures,
    )


def load_multi_line_bin_results(
    results_comp,
    maps_dir,
    *,
    dataset_prefix: str = "MUSE-M42",
    line_order: Sequence[str] = ("H", "N", "O", "S", "Ar"),
    bin_levels: Sequence[int] = (0, 1, 2, 3, 4),
    group: str | None = None,
    filename_template: str = "{dataset_prefix}-{file_line}-bin{bin}",
    file_line_ids: Mapping[str, str] | None = None,
    read_header: bool = True,
    fit_key: str = "fit",
    on_error: str = "raise",
    return_failures: bool = False,
):
    """Load non-fraction results while retaining the original function name."""
    file_line_ids = dict(file_line_ids or {})
    samples = []
    for line in line_order:
        file_line = file_line_ids.get(line, line)
        for bin_level in bin_levels:
            file_name = filename_template.format(
                dataset_prefix=dataset_prefix,
                line=line,
                file_line=file_line,
                bin=bin_level,
            )
            samples.append(
                {
                    "file_name": file_name,
                    "internal_name": f"{line}_bin{bin_level}_line",
                    "label": f"{line}{bin_level}",
                    "line": line,
                    "file_line": file_line,
                    "bin": bin_level,
                    "group": group or dataset_prefix,
                }
            )
    return load_explicit_result_samples(
        results_comp,
        maps_dir,
        samples,
        read_header=read_header,
        fit_key=fit_key,
        on_error=on_error,
        return_failures=return_failures,
    )


def _selected_limit(entry: Mapping, fit_limits: Sequence[float] | None) -> bool:
    if fit_limits is None:
        return entry.get("fit_limit") is not None
    value = entry.get("fit_limit")
    return value is not None and any(
        np.isclose(float(value), float(limit)) for limit in fit_limits
    )


def average_fit_results(
    data_in: Sequence[Mapping],
    *,
    fit_limits: Sequence[float] | None = None,
    params: Sequence[str] = DEFAULT_PARAMS,
    group_keys: Sequence[str] = ("group", "bin", "line"),
    require_all_fit_limits: bool = True,
) -> list[dict]:
    """Average selected fractions and retain their full uncertainty envelope.

    For every unique set of ``group_keys``, the central value is the arithmetic
    mean.  The lower/upper bounds are the minimum/maximum limits among the
    selected fits, matching the convention in ``plot_parameters-Lfrac_test``.
    By default, groups missing any requested fit limit are reported and skipped
    so a partial set cannot silently become the final average.
    """
    selected = [entry for entry in data_in if _selected_limit(entry, fit_limits)]
    grouped: dict[tuple, list[Mapping]] = {}
    for entry in selected:
        key = tuple(entry.get(name) for name in group_keys)
        grouped.setdefault(key, []).append(entry)

    averaged: list[dict] = []
    for key, entries in grouped.items():
        if fit_limits is not None and require_all_fit_limits:
            present = tuple(float(entry["fit_limit"]) for entry in entries)
            missing = [
                float(limit)
                for limit in fit_limits
                if not any(np.isclose(float(limit), value) for value in present)
            ]
            if missing:
                warnings.warn(
                    f"Skipping average for {dict(zip(group_keys, key))}: "
                    f"missing fit limits {missing}.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                continue
        fit_dict_average: dict[str, list[float]] = {}
        for param in params:
            central_values = []
            lower_limits = []
            upper_limits = []
            for entry in entries:
                values = entry.get("fit_dict", {}).get(param)
                if values is None or len(values) < 3:
                    continue
                central, err_upper, err_lower = map(float, values[:3])
                if not np.all(np.isfinite([central, err_upper, err_lower])):
                    continue
                central_values.append(central)
                lower_limits.append(central - max(0.0, err_lower))
                upper_limits.append(central + max(0.0, err_upper))

            if not central_values:
                fit_dict_average[param] = [np.nan, np.nan, np.nan]
                continue

            mean_value = float(np.mean(central_values))
            err_lower = max(0.0, mean_value - float(np.min(lower_limits)))
            err_upper = max(0.0, float(np.max(upper_limits)) - mean_value)
            fit_dict_average[param] = [mean_value, err_upper, err_lower]

        first = entries[0]
        result = {
            name: value for name, value in zip(group_keys, key)
        }
        result.update(
            {
                "label": " / ".join(str(value) for value in key) + " average",
                "file_name": None,
                "bundle": None,
                "fit": pd.DataFrame(fit_dict_average),
                "fit_dict": fit_dict_average,
                "fit_limit": None,
                "selection_mode": "average",
                "fit_limits_used": tuple(
                    sorted({float(entry["fit_limit"]) for entry in entries})
                ),
                "meta": {
                    **dict(first.get("meta", {})),
                    "aggregation": "mean with full confidence-interval envelope",
                    "n_samples": len(entries),
                },
            }
        )
        averaged.append(result)
    return averaged


def _normalize_fit_limits(value) -> tuple[float, ...]:
    """Normalize a scalar or iterable fit-limit selection to a float tuple."""
    if np.isscalar(value):
        limits = (float(value),)
    else:
        limits = tuple(float(limit) for limit in value)
    if not limits:
        raise ValueError("Each group must select at least one fit limit.")
    if not np.all(np.isfinite(limits)):
        raise ValueError(f"Fit limits must be finite; received {limits!r}.")
    if len(set(limits)) != len(limits):
        raise ValueError(f"Fit limits must be unique; received {limits!r}.")
    return limits


def select_or_average_fit_results(
    data_in: Sequence[Mapping],
    *,
    fit_limits_by_group: Mapping[str, float | Sequence[float]],
    params: Sequence[str] = DEFAULT_PARAMS,
    group_key: str = "group",
    group_keys: Sequence[str] = ("group", "bin", "line"),
    require_all_fit_limits: bool = True,
) -> list[dict]:
    """Apply a different fit-limit selection to each sample group.

    A group assigned one limit is returned directly without averaging. A group
    assigned two or more limits is combined with :func:`average_fit_results`,
    retaining the full asymmetric confidence-interval envelope.

    Examples
    --------
    ``{"MUSE": (0.4, 0.5, 0.6), "MUSE trim": (0.5, 0.6, 0.7),
    "KPNO": 0.5}``
    """
    if group_key not in group_keys:
        raise ValueError(f"group_key {group_key!r} must be included in group_keys.")

    output: list[dict] = []
    for group, selection in fit_limits_by_group.items():
        limits = _normalize_fit_limits(selection)
        group_entries = [
            entry for entry in data_in if entry.get(group_key) == group
        ]
        if not group_entries:
            warnings.warn(
                f"No loaded results found for {group_key}={group!r}.",
                RuntimeWarning,
                stacklevel=2,
            )
            continue

        if len(limits) == 1:
            limit = limits[0]
            selected = [
                entry
                for entry in group_entries
                if entry.get("fit_limit") is not None
                and np.isclose(float(entry["fit_limit"]), limit)
            ]
            if not selected:
                warnings.warn(
                    f"No results found for {group_key}={group!r} at fit limit "
                    f"{limit}.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                continue
            for entry in selected:
                result = dict(entry)
                result["fit_dict"] = deepcopy(entry.get("fit_dict", {}))
                if isinstance(entry.get("fit"), pd.DataFrame):
                    result["fit"] = entry["fit"].copy(deep=True)
                result["meta"] = {
                    **dict(entry.get("meta", {})),
                    "aggregation": "single fit limit; not averaged",
                    "n_samples": 1,
                }
                result["fit_limits_used"] = (limit,)
                result["selection_mode"] = "single"
                result["label"] = (
                    f"{entry.get('label', group)} — fit limit {limit:.1f}"
                )
                output.append(result)
            continue

        group_average = average_fit_results(
            group_entries,
            fit_limits=limits,
            params=params,
            group_keys=group_keys,
            require_all_fit_limits=require_all_fit_limits,
        )
        for entry in group_average:
            entry["selection_mode"] = "average"
            entry["meta"]["fit_limits_selected"] = limits
        output.extend(group_average)

    return output


def convert_s0_pc_to_arcsec(
    data_in: Sequence[Mapping],
    *,
    parameter: str = "s0",
    pc_key: str = "PC",
    arcsec_per_pixel: float = 2.35,
    copy: bool = True,
) -> list[dict]:
    """Convert ``s0`` and both errors from pc to arcsec using metadata ``PC``.

    The conversion follows the notebooks: ``s0_arcsec = s0_pc * 2.35 / PC``.
    Set ``copy=False`` to modify the supplied entries in place.
    """
    output = deepcopy(list(data_in)) if copy else list(data_in)
    for entry in output:
        meta = entry.get("meta", {})
        if pc_key not in meta:
            raise KeyError(
                f"{entry.get('label', entry.get('file_name'))!r} has no "
                f"meta[{pc_key!r}] value."
            )
        pc_scale = float(meta[pc_key])
        if not np.isfinite(pc_scale) or pc_scale <= 0:
            raise ValueError(f"Invalid {pc_key} scale: {pc_scale!r}")
        values = entry.get("fit_dict", {}).get(parameter)
        if values is None or len(values) < 3:
            continue
        scale = float(arcsec_per_pixel) / pc_scale
        converted = [max(0.0, float(values[0]) * scale)]
        converted.extend(max(0.0, float(value) * scale) for value in values[1:3])
        entry["fit_dict"][parameter] = converted
        if isinstance(entry.get("fit"), pd.DataFrame) and parameter in entry["fit"]:
            entry["fit"].loc[:, parameter] = converted
        entry.setdefault("meta", {})[f"{parameter}_unit"] = "arcsec"
    return output


def results_to_dataframe(
    data_in: Sequence[Mapping],
    *,
    params: Sequence[str] = DEFAULT_PARAMS,
) -> pd.DataFrame:
    """Return one tidy row per result and parameter."""
    rows = []
    for entry in data_in:
        for param in params:
            values = entry.get("fit_dict", {}).get(param)
            if values is None or len(values) < 3:
                continue
            central, err_upper, err_lower = map(float, values[:3])
            rows.append(
                {
                    "group": entry.get("group"),
                    "bin": entry.get("bin"),
                    "line": entry.get("line"),
                    "fit_limit": entry.get("fit_limit"),
                    "fit_limits_used": entry.get("fit_limits_used"),
                    "selection_mode": entry.get("selection_mode"),
                    "parameter": param,
                    "value": central,
                    "err_lower": err_lower,
                    "err_upper": err_upper,
                    "lower_limit": central - err_lower,
                    "upper_limit": central + err_upper,
                    "n_samples": entry.get("meta", {}).get("n_samples"),
                }
            )
    return pd.DataFrame(rows)


def _label_map(order, labels, argument_name):
    if labels is None:
        return {value: str(value) for value in order}
    if isinstance(labels, Mapping):
        return {value: labels.get(value, str(value)) for value in order}
    if isinstance(labels, (list, tuple)) and len(labels) == len(order):
        return dict(zip(order, labels))
    raise ValueError(f"{argument_name} must map values or match the order length.")


def _plot_setup(
    *,
    figsize,
    param_labels,
    param_titles,
    param_ylims,
    row_titles,
    row_title_fontsize,
    row_title_y,
):
    from matplotlib import pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=figsize, sharex=False)
    axes = axes.ravel()
    labels = {**DEFAULT_PARAM_LABELS, **(param_labels or {})}
    titles = {**DEFAULT_PARAM_TITLES, **(param_titles or {})}
    ylims = dict(param_ylims or {})
    if row_titles is not None:
        if len(row_titles) != 2:
            raise ValueError("row_titles must contain exactly two entries.")
        for axis, title in ((axes[1], row_titles[0]), (axes[4], row_titles[1])):
            axis.annotate(
                title,
                xy=(0.5, row_title_y),
                xycoords="axes fraction",
                ha="center",
                va="center",
                fontsize=row_title_fontsize,
                fontweight="bold",
            )
    return fig, axes, labels, titles, ylims


def _finish_figure(fig, save, savepath, subplot_adjust=None):
    fig.tight_layout()
    if subplot_adjust is not None:
        if not isinstance(subplot_adjust, Mapping):
            raise TypeError("subplot_adjust must be None or a mapping.")
        fig.subplots_adjust(**dict(subplot_adjust))
    if save:
        path = Path(savepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, bbox_inches="tight")


def plot_param_grid_lines_bins(
    data_in: Sequence[Mapping],
    *,
    params: Sequence[str] = DEFAULT_PARAMS,
    line_order: Sequence[str] = ("H", "N", "O", "S", "Ar"),
    bin_levels: Sequence[int] = (0, 1, 2, 3, 4),
    group: str | None = None,
    xtick_labels=None,
    line_legend_labels=None,
    param_labels=None,
    param_titles=None,
    param_ylims=None,
    row_titles=("Physical parameters", "Nuisance parameters"),
    row_title_fontsize=16,
    row_title_y=1.22,
    decimals=4,
    figsize=(15, 8),
    color_palette="Greys_d",
    markers=("o", "s", "^", "D", "P"),
    jitter=0.08,
    capsize=4,
    elinewidth=1.8,
    markersize=6,
    legend_fontsize=13,
    legend_title_fontsize=14,
    show_values=False,
    true=None,
    subplot_adjust=None,
    save=False,
    savepath="fit_parameters_grid.pdf",
):
    """Plot averaged line results against binning level."""
    import seaborn as sns

    if not data_in:
        raise ValueError("data_in is empty.")
    filtered = [entry for entry in data_in if group is None or entry.get("group") == group]
    keys = [(entry.get("line"), entry.get("bin")) for entry in filtered]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate line/bin entries remain; select one group first.")

    fig, axes, labels, titles, ylims = _plot_setup(
        figsize=figsize,
        param_labels=param_labels,
        param_titles=param_titles,
        param_ylims=param_ylims,
        row_titles=row_titles,
        row_title_fontsize=row_title_fontsize,
        row_title_y=row_title_y,
    )
    param_axes = dict(zip(DEFAULT_PARAMS, axes[:5]))
    colors = sns.color_palette(color_palette, n_colors=len(line_order))[::-1]
    color_map = dict(zip(line_order, colors))
    marker_map = {line: markers[i % len(markers)] for i, line in enumerate(line_order)}
    offsets = np.linspace(-jitter, jitter, len(line_order)) if len(line_order) > 1 else [0.0]
    offset_map = dict(zip(line_order, offsets))
    bin_position = {value: i for i, value in enumerate(bin_levels)}
    tick_map = _label_map(bin_levels, xtick_labels, "xtick_labels")
    legend_map = _label_map(line_order, line_legend_labels, "line_legend_labels")
    lookup = {(entry.get("line"), entry.get("bin")): entry["fit_dict"] for entry in filtered}
    true_map = dict(true or {}) if isinstance(true, Mapping) else dict(zip(("sig2", "r0", "m"), true or ()))

    for param in params:
        if param not in param_axes:
            continue
        ax = param_axes[param]
        for line in line_order:
            points = []
            for bin_level in bin_levels:
                values = lookup.get((line, bin_level), {}).get(param)
                if values is not None and len(values) >= 3:
                    points.append((bin_position[bin_level] + offset_map[line], *map(float, values[:3])))
            if not points:
                continue
            x, y, upper, lower = map(np.asarray, zip(*points))
            ax.errorbar(
                x, y, yerr=[np.maximum(0, lower), np.maximum(0, upper)],
                fmt=marker_map[line], color=color_map[line],
                markerfacecolor=color_map[line], markeredgecolor="black",
                markeredgewidth=0.6, markersize=markersize, capsize=capsize,
                elinewidth=elinewidth, linestyle="none", label=legend_map[line],
            )
            if show_values:
                for xp, yp in zip(x, y):
                    ax.text(xp, yp, f"{yp:.{decimals}f}", ha="center", va="bottom", fontsize=8)
        if param in true_map and true_map[param] is not None:
            ax.axhline(true_map[param], color="red", linestyle="--", linewidth=1.2)
        ax.set_title(titles[param] + " vs binning level")
        ax.set_ylabel(labels[param])
        ax.grid(alpha=0.3)
        if param in ylims and ylims[param] is not None:
            ax.set_ylim(ylims[param])

    positions = np.arange(len(bin_levels))
    for ax in axes[:5]:
        ax.set_xticks(positions, [tick_map[value] for value in bin_levels], rotation=45)
        ax.set_xlim(-0.5, len(bin_levels) - 0.5)
        ax.set_xlabel("Binning level")
    axes[5].axis("off")
    handles, legend_labels = axes[0].get_legend_handles_labels()
    if handles:
        axes[5].legend(handles, legend_labels, loc="center", frameon=False, title="Line",
                       fontsize=legend_fontsize, title_fontsize=legend_title_fontsize)
    _finish_figure(fig, save, savepath, subplot_adjust=subplot_adjust)
    return fig, axes


def plot_param_grid_lines_as_x(
    data_in: Sequence[Mapping],
    *,
    params: Sequence[str] = DEFAULT_PARAMS,
    line_order: Sequence[str] = ("H", "N", "O", "S", "S2", "Ar"),
    group_order: Sequence = ("KPNO", "MUSE trim", "MUSE"),
    group_key: str = "group",
    line_labels=None,
    group_labels=None,
    param_labels=None,
    param_titles=None,
    param_ylims=None,
    row_titles=("Physical parameters", "Nuisance parameters"),
    row_title_fontsize=16,
    row_title_y=1.22,
    decimals=4,
    figsize=(15, 8),
    color_palette="Greys_d",
    markers=("o", "s", "^", "D", "P", "X"),
    jitter=0.10,
    capsize=4,
    elinewidth=1.8,
    markersize=7,
    legend_fontsize=13,
    legend_title_fontsize=14,
    legend_title="Sample",
    show_values=False,
    true=None,
    subplot_adjust=None,
    save=False,
    savepath="fit_parameters_lines_as_x.pdf",
):
    """Plot emission lines on x and encode samples (or fractions) by style."""
    import seaborn as sns
    from matplotlib import pyplot as plt

    if not data_in:
        raise ValueError("data_in is empty.")
    fig, axes, labels, titles, ylims = _plot_setup(
        figsize=figsize,
        param_labels=param_labels,
        param_titles=param_titles,
        param_ylims=param_ylims,
        row_titles=row_titles,
        row_title_fontsize=row_title_fontsize,
        row_title_y=row_title_y,
    )
    param_axes = dict(zip(DEFAULT_PARAMS, axes[:5]))
    colors = sns.color_palette(color_palette, n_colors=len(group_order))[::-1]
    color_map = dict(zip(group_order, colors))
    marker_map = {value: markers[i % len(markers)] for i, value in enumerate(group_order)}
    offsets = np.linspace(-jitter, jitter, len(group_order)) if len(group_order) > 1 else [0.0]
    offset_map = dict(zip(group_order, offsets))
    line_position = {line: i for i, line in enumerate(line_order)}
    line_label_map = _label_map(line_order, line_labels, "line_labels")
    group_label_map = _label_map(group_order, group_labels, "group_labels")
    true_map = dict(true or {}) if isinstance(true, Mapping) else dict(zip(("sig2", "r0", "m"), true or ()))

    for param in params:
        if param not in param_axes:
            continue
        ax = param_axes[param]
        for entry in data_in:
            line = entry.get("line")
            group_value = entry.get(group_key)
            values = entry.get("fit_dict", {}).get(param)
            if line not in line_position or group_value not in color_map or values is None or len(values) < 3:
                continue
            central, upper, lower = map(float, values[:3])
            x = line_position[line] + offset_map[group_value]
            ax.errorbar(
                x, central, yerr=[[max(0.0, lower)], [max(0.0, upper)]],
                fmt=marker_map[group_value], color=color_map[group_value],
                markerfacecolor=color_map[group_value], markeredgecolor="black",
                markeredgewidth=0.6, markersize=markersize, capsize=capsize,
                elinewidth=elinewidth, linestyle="none",
            )
            if show_values:
                ax.text(x, central, f"{central:.{decimals}f}", ha="center", va="bottom", fontsize=8)
        if param in true_map and true_map[param] is not None:
            ax.axhline(true_map[param], color="red", linestyle="--", linewidth=1.2)
        ax.set_title(titles[param] + " vs emission line")
        ax.set_ylabel(labels[param])
        ax.grid(alpha=0.3)
        if param in ylims and ylims[param] is not None:
            ax.set_ylim(ylims[param])

    positions = np.arange(len(line_order))
    for ax in axes[:5]:
        ax.set_xticks(positions, [line_label_map[line] for line in line_order], rotation=45)
        ax.set_xlim(-0.5, len(line_order) - 0.5)
        ax.set_xlabel("Emission line")
    axes[5].axis("off")
    used = {entry.get(group_key) for entry in data_in}
    handles = [
        plt.Line2D(
            [0], [0], marker=marker_map[value], color="none",
            markerfacecolor=color_map[value], markeredgecolor="black",
            markersize=markersize + 2, label=group_label_map[value],
        )
        for value in group_order if value in used
    ]
    if handles:
        axes[5].legend(handles=handles, loc="center", frameon=False,
                       title=legend_title, fontsize=legend_fontsize,
                       title_fontsize=legend_title_fontsize)
    _finish_figure(fig, save, savepath, subplot_adjust=subplot_adjust)
    return fig, axes


def select_results(data_in: Sequence[Mapping], **criteria) -> list[dict]:
    """Filter entries by exact metadata values; iterable values mean membership."""
    selected = []
    for entry in data_in:
        keep = True
        for key, expected in criteria.items():
            if isinstance(expected, (set, list, tuple)) and not isinstance(expected, str):
                keep &= entry.get(key) in expected
            else:
                keep &= entry.get(key) == expected
        if keep:
            selected.append(entry)
    return selected


__all__ = [
    "DEFAULT_PARAMS",
    "average_fit_results",
    "build_fraction_sample_grid",
    "convert_s0_pc_to_arcsec",
    "fit_limit_tag",
    "load_explicit_result_samples",
    "load_multi_line_bin_fraction_results",
    "load_multi_line_bin_results",
    "plot_param_grid_lines_as_x",
    "plot_param_grid_lines_bins",
    "results_to_dataframe",
    "select_results",
    "select_or_average_fit_results",
]

