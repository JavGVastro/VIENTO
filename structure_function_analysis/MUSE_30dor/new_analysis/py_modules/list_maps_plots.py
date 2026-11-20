# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 06:53:57 2026

@author: ZAINTEL2
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde

def plot_list_pdfs(
    dfs,
    col,
    *,
    labels=None,
    center="none",          # "none" | "mean" | "zscore"
    method="kde",           # "kde" | "hist_curve" | "hist_step"
    bins="auto",
    grid_points=500,
    bw_scale=1.0,           # KDE bandwidth multiplier (1.0 = default Scott)
    figsize=(8, 4),
    annotate=True,
):
    """
    Plot PDF estimates of the same column from multiple DataFrames.

    Parameters
    ----------
    dfs : list[pd.DataFrame] or dict[str, pd.DataFrame]
        DataFrames to plot. If dict, keys are used as labels.
    col : str
        Column name present in each DataFrame.
    labels : list[str] | None
        Labels if `dfs` is a list. Ignored if `dfs` is a dict.
    center : {"none","mean","zscore"}
        Center/normalize each dataset before PDF estimation.
    method : {"kde","hist_curve","hist_step"}
        "kde" uses scipy gaussian_kde.
        "hist_curve" connects bin tops (bin centers).
        "hist_step" draws a step outline histogram.
    bins : int | str | sequence
        Binning strategy for histogram methods (passed to np.histogram).
    grid_points : int
        Number of x points for KDE curve evaluation.
    bw_scale : float
        Multiply KDE bandwidth by this factor. Smaller -> less smoothing.
    annotate : bool
        If True, annotate N/mean/std per dataset (stacked on the plot).
    """
    # --- normalize input into (label, df) pairs ---
    if isinstance(dfs, dict):
        items = list(dfs.items())
    else:
        if labels is None:
            labels = [f"df{i+1}" for i in range(len(dfs))]
        items = list(zip(labels, dfs))

    fig, ax = plt.subplots(figsize=figsize)

    # To put all curves on comparable x-axis, we compute all transformed arrays first
    series = []
    for name, df in items:
        if col not in df.columns:
            print(f"[skip] {name}: column '{col}' not found")
            continue

        x = df[col].dropna().to_numpy()
        if x.size == 0:
            print(f"[skip] {name}: no valid values in '{col}'")
            continue

        mu     = x.mean()
        sigma  = x.std(ddof=1) if x.size > 1 else 0.0
        sigma2 = x.var(ddof=1) 


        # transform
        if center == "mean":
            y = x - mu
        elif center == "zscore":
            y = (x - mu) / sigma if sigma > 0 else x * 0.0
        else:
            y = x

        series.append((name, x, y, mu, sigma))

    if not series:
        raise ValueError("No valid series to plot (check column name / NaNs).")

    # --- choose a common x-range for all curves ---
    all_y = np.concatenate([s[2] for s in series])
    xmin, xmax = all_y.min(), all_y.max()
    pad = 0.05 * (xmax - xmin) if xmax > xmin else 1.0
    xmin, xmax = xmin - pad, xmax + pad

    # --- plot each dataset ---
    for name, x, y, mu, sigma in series:
        if method == "kde":
            kde = gaussian_kde(y)
            kde.set_bandwidth(bw_method=kde.factor * bw_scale)
            grid = np.linspace(xmin, xmax, grid_points)
            pdf = kde(grid)
            ax.plot(grid, pdf, linewidth=2, label=name)

        else:
            dens, edges = np.histogram(y, bins=bins, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])

            if method == "hist_curve":
                ax.plot(centers, dens, marker="o", linewidth=2, label=name)
            elif method == "hist_step":
                ax.step(edges[:-1], dens, where="post", linewidth=2, label=name)
            else:
                raise ValueError("method must be 'kde', 'hist_curve', or 'hist_step'")

    # --- labels / title ---
    if center == "mean":
        ax.set_xlabel(f"{col} - mean")
    elif center == "zscore":
        ax.set_xlabel(f"({col} - mean) / std")
    else:
        ax.set_xlabel(col)

    ax.set_ylabel("PDF")
    ax.set_title(f"PDFs of '{col}' ({method}, center={center})")
    ax.legend()

    # --- optional stats annotations (one per dataset) ---
    if annotate:
        lines = []
        for name, x, y, mu, sigma in series:
            lines.append(f"{name}: N={x.size}, std={sigma:.4g}, var={sigma**2:.4g}")
        ax.text(
            0.01, 0.99, "\n".join(lines),
            transform=ax.transAxes,
            ha="left", va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="gray")
        )

    plt.tight_layout()
    return fig, ax


def plot_panels(line_df, *, mark_func=None, s=25,
                     xcol="RAdeg", ycol="DEdeg",
                     flux_col="log_F", vcol="V_mean",
                     flux_cmap="magma", v_cmap="RdBu_r",
                     invert_ra=True, figsize=(14, 7),
                     titles=("Log Flux", "V_mean - <V_mean>"),
                     cbar_labels=("Flux", "V_mean - mean")):
    """
    Plot two panels for a given line DataFrame:
      (1) flux_col map
      (2) mean-subtracted vcol map

    Parameters
    ----------
    line_df : pandas.DataFrame
        Must contain xcol, ycol, flux_col, vcol.
    mark_func : callable or None
        Function like mark_points(ax) to annotate points on each axis.
    s : float
        Marker size for scatter.
    invert_ra : bool
        If True, invert x-axis (RA convention).
    """

    required = [xcol, ycol, flux_col, vcol]
    missing = [c for c in required if c not in line_df.columns]
    if missing:
        raise ValueError(f"Missing columns in line_df: {missing}")

    with sns.axes_style("darkgrid"):
        fig, ax = plt.subplots(1, 2, figsize=figsize, constrained_layout=True)

        # Panel 1: log flux
        sc1 = ax[0].scatter(line_df[xcol], line_df[ycol], s=s, c=line_df[flux_col], cmap=flux_cmap)
        if invert_ra:
            ax[0].invert_xaxis()
        ax[0].set_xlabel("RA (deg)")
        ax[0].set_ylabel("Dec (deg)")
        ax[0].set_title(titles[0])
        if callable(mark_func):
            mark_func(ax[0])
        fig.colorbar(sc1, ax=ax[0], label=cbar_labels[0])

        # Panel 2: mean-subtracted velocity
        v1 = line_df[vcol] - line_df[vcol].mean()
        sc2 = ax[1].scatter(line_df[xcol], line_df[ycol], s=s, c=v1, cmap=v_cmap)
        if invert_ra:
            ax[1].invert_xaxis()
        ax[1].set_xlabel("RA (deg)")
        ax[1].set_ylabel("Dec (deg)")
        ax[1].set_title(titles[1])
        if callable(mark_func):
            mark_func(ax[1])
        fig.colorbar(sc2, ax=ax[1], label=cbar_labels[1])

    return fig, ax
