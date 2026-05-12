import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.visualization.wcsaxes.patches import SphericalCircle


def load_circle_catalog(catalog_path, name_file, frame="icrs"):
    """
    Load a circle catalog CSV and rebuild the `circles` list used in the notebooks.

    Required columns in the CSV
    ---------------------------
    label, ring, angle_deg, ra_deg, dec_deg, radius_arcsec
    """
    circles_df = pd.read_csv(catalog_path).copy()
    if "name" not in circles_df.columns:
        circles_df["name"] = [f"{name_file}_{lab}" for lab in circles_df["label"]]

    circles = []
    for _, row in circles_df.iterrows():
        center = SkyCoord(
            ra=row["ra_deg"] * u.deg,
            dec=row["dec_deg"] * u.deg,
            frame=frame,
        )
        circles.append({
            "name": row["name"],
            "label": row["label"],
            "ring": row["ring"],
            "angle_deg": row["angle_deg"],
            "center": center,
            "ra_deg": row["ra_deg"],
            "dec_deg": row["dec_deg"],
            "radius_arcsec": row["radius_arcsec"],
        })
    return circles_df, circles


def build_circle_results_df(circles, dfs_fit, radius=None, radius_arcsec=None, pc=None, param_row=0):
    """
    Build one summary row per circle from the fit tables.

    Parameters
    ----------
    circles : list[dict]
        Circle catalog.
    dfs_fit : dict[str, pd.DataFrame]
        Dictionary keyed by circle export name.
    radius : astropy quantity, optional
        Common circle radius. Used only if `radius_arcsec` is not provided.
    radius_arcsec : float, optional
        Common circle radius in arcsec. If provided, this takes priority over
        `radius`. If neither is provided, the function tries to infer it from
        circles[0]["radius_arcsec"].
    pc : float, optional
        Conversion factor in pc per arcsec.
    param_row : int
        Row to use as the representative fit value, default 0.

    Notes
    -----
    If `pc` is provided, the function computes a projected ring-center
    distance in parsecs using the assumed ring geometry:

        center -> 0
        inner  -> 2*r
        middle -> 4*r
        outer  -> 6*r

    where r is the common circle radius in arcsec.
    """
    rows = []

    ring_to_dist_pc = None
    if pc is not None:
        r_arcsec = None

        # Option 1: explicit radius in arcsec
        if radius_arcsec is not None:
            r_arcsec = radius_arcsec

        # Option 2: explicit astropy quantity
        elif radius is not None:
            r_arcsec = radius.to(u.arcsec).value

        # Option 3: infer from circle catalog
        elif len(circles) > 0 and "radius_arcsec" in circles[0]:
            r_arcsec = circles[0]["radius_arcsec"]

        if r_arcsec is not None:
            ring_to_dist_pc = {
                "center": 0.0,
                "inner": 2 * r_arcsec * pc,
                "middle": 4 * r_arcsec * pc,
                "outer": 6 * r_arcsec * pc,
            }

    for item in circles:
        name = item["name"]
        if name not in dfs_fit:
            continue

        df_fit = dfs_fit[name]
        if df_fit.empty:
            continue

        row = {
            "name": name,
            "label": item["label"],
            "ring": item["ring"],
            "angle_deg": item["angle_deg"],
            "ra_deg": item["ra_deg"],
            "dec_deg": item["dec_deg"],
            "radius_arcsec": item["radius_arcsec"],
        }

        for col in df_fit.columns:
            try:
                row[col] = df_fit[col].iloc[param_row]
            except Exception:
                row[col] = np.nan

        if "sig2" in row and pd.notna(row["sig2"]):
            row["sig"] = np.sqrt(row["sig2"])
        else:
            row["sig"] = np.nan

        if ring_to_dist_pc is not None:
            row["radius_pc"] = ring_to_dist_pc.get(item["ring"], np.nan)

        rows.append(row)

    return pd.DataFrame(rows)


def compute_group_stats(results_df, param, group_col="ring", xcol=None, order=None):
    """
    Compute count/mean/std/median for a parameter grouped by ring or any other column.
    """
    group_cols = [group_col]
    if xcol is not None and xcol != group_col:
        group_cols.append(xcol)

    stats_df = (
        results_df
        .groupby(group_cols)[param]
        .agg(["count", "mean", "std", "median"])
        .reset_index()
    )

    if order is not None and group_col in stats_df.columns:
        stats_df[group_col] = pd.Categorical(stats_df[group_col], categories=order, ordered=True)
        sort_cols = [group_col]
        if xcol is not None and xcol != group_col:
            sort_cols.append(xcol)
        stats_df = stats_df.sort_values(sort_cols)

    if xcol is not None and xcol in stats_df.columns:
        stats_df = stats_df.sort_values(xcol)

    return stats_df


def _format_fit_triplet(df_fit, param, fmt="{:.2f}", text_mode="stacked"):
    vals = df_fit[param].tolist()[:3]
    vals_fmt = [fmt.format(v) for v in vals]

    if text_mode == "inline":
        return vals_fmt[0] + "".join([f"({v})" for v in vals_fmt[1:]])
    return "\n".join([vals_fmt[0]] + [f"({v})" for v in vals_fmt[1:]])


def plot_circle_fit_map(
    wcs,
    circles,
    dfs_fit,
    param,
    *,
    figsize=(7, 6),
    cmap="viridis",
    fmt="{:.2f}",
    fontsize=8,
    linewidth=1.5,
    text_mode="stacked",
    text_color="black",
    title=None,
    colorbar=True,
    anchor_alpha=0.01,
    anchor_color="white",
    edge_only=True,
    face_alpha=0.25,
):
    """
    Plot circles on a WCS axis and write the selected fit parameter values inside each circle.
    The first row of each fit table is used for coloring and the first 3 rows are written as text.
    """
    fig = plt.figure(figsize=figsize, constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection=wcs)

    ra_vals = [item["ra_deg"] for item in circles]
    dec_vals = [item["dec_deg"] for item in circles]

    # Anchor the WCS plot using nearly invisible points, following the working notebook pattern.
    ax.scatter(
        ra_vals,
        dec_vals,
        s=1.0,
        color=anchor_color,
        alpha=anchor_alpha,
        transform=ax.get_transform("world")
    )

    main_vals = [dfs_fit[item["name"]][param].iloc[0] for item in circles if item["name"] in dfs_fit]
    norm = mpl.colors.Normalize(vmin=min(main_vals), vmax=max(main_vals))
    cmap_obj = plt.cm.get_cmap(cmap)

    for item in circles:
        name = item["name"]
        if name not in dfs_fit:
            continue

        df_fit = dfs_fit[name]
        color = cmap_obj(norm(df_fit[param].iloc[0]))
        txt = _format_fit_triplet(df_fit, param, fmt=fmt, text_mode=text_mode)

        if edge_only:
            facecolor = "none"
            alpha = 1.0
        else:
            facecolor = color
            alpha = face_alpha

        circle = SphericalCircle(
            (item["center"].ra, item["center"].dec),
            item["radius_arcsec"] * u.arcsec,
            edgecolor=color,
            facecolor=facecolor,
            alpha=alpha,
            linewidth=linewidth,
            transform=ax.get_transform("world")
        )
        ax.add_patch(circle)

        ax.text(
            item["ra_deg"],
            item["dec_deg"],
            txt,
            transform=ax.get_transform("world"),
            ha="center",
            va="center",
            fontsize=fontsize,
            color=text_color
        )

    ax.set_xlabel("RA")
    ax.set_ylabel("Dec")
    ax.set_title(title or f"{param} by circle")

    if colorbar:
        sm = plt.cm.ScalarMappable(cmap=cmap_obj, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label(param)

    return fig, ax


def plot_parameter_by_radius(
    results_df,
    param,
    *,
    radius_col="radius_pc",
    group_col="ring",
    figsize=(7, 4),
    show_points=True,
    jitter=0.0,
    errorbar=True,
    title=None,
    ylabel=None,
    rng_seed=42,
):
    """
    Plot a parameter as a function of projected ring-center distance.
    """
    if radius_col not in results_df.columns:
        raise ValueError(f"Column '{radius_col}' not found in results_df.")

    stats_df = (
        results_df
        .groupby([group_col, radius_col])[param]
        .agg(["count", "mean", "std", "median"])
        .reset_index()
        .sort_values(radius_col)
    )

    fig, ax = plt.subplots(figsize=figsize)

    if show_points:
        xvals = results_df[radius_col].to_numpy(dtype=float)
        if jitter and jitter > 0:
            rng = np.random.default_rng(rng_seed)
            xvals = xvals + rng.normal(0, jitter, size=len(xvals))

        ax.scatter(
            xvals,
            results_df[param],
            s=35,
            alpha=0.8,
            label="subfields"
        )

    if errorbar:
        ax.errorbar(
            stats_df[radius_col],
            stats_df["mean"],
            yerr=stats_df["std"],
            fmt="o-",
            color="black",
            capsize=4,
            label="ring mean ± std"
        )

    ax.set_xlabel("Distance from center [pc]")
    ax.set_ylabel(ylabel or param)
    ax.set_title(title or f"{param} vs projected radius")
    ax.grid(True, alpha=0.3)

    if show_points or errorbar:
        ax.legend()

    return fig, ax, stats_df


def plot_parameter_by_ring(
    results_df,
    param,
    *,
    group_col="ring",
    order=("center", "inner", "middle", "outer"),
    figsize=(7, 4),
    show_points=True,
    errorbar=True,
    title=None,
    ylabel=None,
):
    """
    Plot a parameter grouped by ring name rather than physical radius.
    """
    stats_df = compute_group_stats(results_df, param, group_col=group_col, order=list(order))

    fig, ax = plt.subplots(figsize=figsize)

    ring_to_x = {name: i for i, name in enumerate(order)}

    if show_points:
        xvals = [ring_to_x[r] for r in results_df[group_col]]
        ax.scatter(
            xvals,
            results_df[param],
            s=35,
            alpha=0.8,
            label="subfields"
        )

    if errorbar:
        xstats = [ring_to_x[r] for r in stats_df[group_col]]
        ax.errorbar(
            xstats,
            stats_df["mean"],
            yerr=stats_df["std"],
            fmt="o-",
            color="black",
            capsize=4,
            label="ring mean ± std"
        )

    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order)
    ax.set_xlabel("Ring")
    ax.set_ylabel(ylabel or param)
    ax.set_title(title or f"{param} by ring")
    ax.grid(True, alpha=0.3)

    if show_points or errorbar:
        ax.legend()

    return fig, ax, stats_df

def plot_parameter_by_radius_multi(
    results_df_dict,
    param,
    *,
    radius_col="radius_pc",
    figsize=(7, 4),
    show_points=True,
    jitter=0.0,
    errorbar=True,
    title=None,
    ylabel=None,
    rng_seed=42,
):
    """
    Plot one parameter vs projected ring-center distance for multiple runs.

    Parameters
    ----------
    results_df_dict : dict[str, pd.DataFrame]
        Dictionary keyed by run label, for example:
        {"50pc": results_df_50pc, "100pc": results_df_100pc}
    param : str
        Parameter to plot, e.g. "sig", "r0", "m".
    radius_col : str
        Column containing the projected ring-center distance in pc.
    figsize : tuple
    show_points : bool
        If True, plot individual subfield values.
    jitter : float
        Gaussian jitter applied to x values for the individual points.
    errorbar : bool
        If True, plot mean ± std for each run.
    title : str or None
    ylabel : str or None
    rng_seed : int

    Returns
    -------
    fig, ax, stats_dict
        stats_dict is keyed by run label and contains the grouped stats table.
    """
    fig, ax = plt.subplots(figsize=figsize)
    rng = np.random.default_rng(rng_seed)

    stats_dict = {}

    for i, (run_label, df) in enumerate(results_df_dict.items()):
        if radius_col not in df.columns:
            raise ValueError(f"Column '{radius_col}' not found in results_df for run '{run_label}'.")
        if param not in df.columns:
            raise ValueError(f"Column '{param}' not found in results_df for run '{run_label}'.")

        stats_df = (
            df.groupby(radius_col)[param]
            .agg(["count", "mean", "std", "median"])
            .reset_index()
            .sort_values(radius_col)
        )

        stats_dict[run_label] = stats_df
        color = f"C{i}"

        if show_points:
            xvals = df[radius_col].to_numpy(dtype=float)
            if jitter and jitter > 0:
                xvals = xvals + rng.normal(0, jitter, size=len(xvals))

            ax.scatter(
                xvals,
                df[param],
                s=35,
                alpha=0.7,
                color=color,
                label=f"{run_label} subfields"
            )

        if errorbar:
            ax.errorbar(
                stats_df[radius_col],
                stats_df["mean"],
                yerr=stats_df["std"],
                fmt="o",
                capsize=4,
                linewidth=1.5,
                color=color,
                label=f"{run_label} mean ± std"
            )

    ax.set_xlabel("Projected radius [pc]")
    ax.set_ylabel(ylabel or param)
    ax.set_title(title or f"{param} vs projected radius")
    ax.grid(True, alpha=0.3)
    ax.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    frameon=True
    )

    return fig, ax, stats_dict