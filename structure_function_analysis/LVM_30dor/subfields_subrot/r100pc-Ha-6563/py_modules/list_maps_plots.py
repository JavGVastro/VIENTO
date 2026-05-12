# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 06:53:57 2026

@author: ZAINTEL2
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
from astropy.wcs import WCS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib import cm

def plot_list_pdfs_circles(
    dfs,
    col,
    *,
    labels=None,
    center="none",          # "none" | "mean" | "zscore"
    method="kde",           # "kde" | "hist_curve" | "hist_step"
    bins="auto",
    grid_points=500,
    bw_scale=1.0,
    figsize=(8, 4),
    annotate=False,
    legend_mode="auto",     # "auto" | "inside" | "outside" | "none"
    legend_max=8,
    cmap="viridis",
    color_values=None,      # optional list/array of values used to map colors
    return_stats=True,
    sort_key=None,
    linewidth=1.8,
    alpha=1.0,
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
    method : {"kde","hist_curve","hist_step"}
    bins : int | str | sequence
    grid_points : int
    bw_scale : float
    annotate : bool
        If True, put stats text inside plot. Not recommended for many curves.
    legend_mode : {"auto","inside","outside","none"}
    legend_max : int
        Max number of entries before auto legend is suppressed.
    cmap : str
        Matplotlib colormap name.
    color_values : array-like or None
        If provided, must have same length as valid series. Used to assign colors.
    return_stats : bool
        If True, also return a DataFrame of sample statistics.
    sort_key : callable or None
        Applied to labels before plotting, e.g. sort_key=lambda x: x.
    linewidth : float
    alpha : float
    """
    # ----------------------------
    # normalize input into (label, df) pairs
    # ----------------------------
    if isinstance(dfs, dict):
        items = list(dfs.items())
    else:
        if labels is None:
            labels = [f"df{i+1}" for i in range(len(dfs))]
        items = list(zip(labels, dfs))

    if sort_key is not None:
        items = sorted(items, key=lambda t: sort_key(t[0]))

    fig, ax = plt.subplots(figsize=figsize)

    # ----------------------------
    # prepare all valid series
    # ----------------------------
    series = []
    stats_rows = []

    for name, df in items:
        if col not in df.columns:
            print(f"[skip] {name}: column '{col}' not found")
            continue

        x = df[col].dropna().to_numpy()
        if x.size == 0:
            print(f"[skip] {name}: no valid values in '{col}'")
            continue

        mu = x.mean()
        sigma = x.std(ddof=1) if x.size > 1 else 0.0
        sigma2 = x.var(ddof=1) if x.size > 1 else 0.0

        if center == "mean":
            y = x - mu
        elif center == "zscore":
            y = (x - mu) / sigma if sigma > 0 else np.zeros_like(x)
        else:
            y = x

        series.append((name, x, y, mu, sigma, sigma2))
        stats_rows.append({
            "name": name,
            "N": x.size,
            "mean": mu,
            "std": sigma,
            "var": sigma2,
            "xmin": y.min(),
            "xmax": y.max(),
        })

    if not series:
        raise ValueError("No valid series to plot (check column name / NaNs).")

    stats_df = pd.DataFrame(stats_rows)

    # ----------------------------
    # common x-range
    # ----------------------------
    all_y = np.concatenate([s[2] for s in series])
    xmin, xmax = all_y.min(), all_y.max()
    pad = 0.05 * (xmax - xmin) if xmax > xmin else 1.0
    xmin, xmax = xmin - pad, xmax + pad

    # ----------------------------
    # color assignment
    # ----------------------------
    n = len(series)
    cmap_obj = cm.get_cmap(cmap)

    if color_values is None:
        if n == 1:
            colors = [cmap_obj(0.6)]
        else:
            colors = [cmap_obj(v) for v in np.linspace(0.1, 0.9, n)]
    else:
        color_values = np.asarray(color_values, dtype=float)
        vmin, vmax = color_values.min(), color_values.max()
        if vmax == vmin:
            normed = np.full_like(color_values, 0.6, dtype=float)
        else:
            normed = (color_values - vmin) / (vmax - vmin)
            normed = 0.1 + 0.8 * normed
        colors = [cmap_obj(v) for v in normed]

    # ----------------------------
    # plot each dataset
    # ----------------------------
    for (name, x, y, mu, sigma, sigma2), color in zip(series, colors):
        if method == "kde":
            kde = gaussian_kde(y)
            kde.set_bandwidth(bw_method=kde.factor * bw_scale)
            grid = np.linspace(xmin, xmax, grid_points)
            pdf = kde(grid)
            ax.plot(grid, pdf, linewidth=linewidth, alpha=alpha, color=color, label=name)

        else:
            dens, edges = np.histogram(y, bins=bins, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])

            if method == "hist_curve":
                ax.plot(centers, dens, linewidth=linewidth, alpha=alpha, color=color, label=name)
            elif method == "hist_step":
                ax.step(edges[:-1], dens, where="post", linewidth=linewidth, alpha=alpha, color=color, label=name)
            else:
                raise ValueError("method must be 'kde', 'hist_curve', or 'hist_step'")

    # ----------------------------
    # labels / title
    # ----------------------------
    if center == "mean":
        ax.set_xlabel(f"{col} - mean")
    elif center == "zscore":
        ax.set_xlabel(f"({col} - mean) / std")
    else:
        ax.set_xlabel(col)

    ax.set_ylabel("PDF")
    ax.set_title(f"PDFs of '{col}' ({method}, center={center})")

    # ----------------------------
    # legend control
    # ----------------------------
    if legend_mode == "auto":
        if len(series) <= legend_max:
            ax.legend()
    elif legend_mode == "inside":
        ax.legend()
    elif legend_mode == "outside":
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=True)
    elif legend_mode == "none":
        pass
    else:
        raise ValueError("legend_mode must be 'auto', 'inside', 'outside', or 'none'")

    # ----------------------------
    # optional stats annotations
    # ----------------------------
    if annotate:
        lines = []
        for name, x, y, mu, sigma, sigma2 in series:
            lines.append(f"{name}: N={x.size}, std={sigma:.4g}, var={sigma2:.4g}")
        ax.text(
            0.01, 0.99, "\n".join(lines),
            transform=ax.transAxes,
            ha="left", va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="gray")
        )

    plt.tight_layout()

    if return_stats:
        return fig, ax, stats_df
    return fig, ax

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

def plot_panels_log(line_df, *, mark_func=None, s=25,
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
        sc1 = ax[0].scatter(line_df[xcol], line_df[ycol], s=s, c=line_df[flux_col], cmap=flux_cmap, norm="log")
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

def plot_panels_log_title(line_df, *, mark_func=None, s=25,
                     xcol="RAdeg", ycol="DEdeg",
                     flux_col="log_F", vcol="V_mean",
                     flux_cmap="magma", v_cmap="RdBu_r",
                     invert_ra=True, figsize=(14, 7),
                     titles=("Log Flux", "V_mean - <V_mean>"),
                     cbar_labels=("Flux", "V_mean - mean"),
                     figure_title=None):
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
    figure_title : str or None
        General title for the whole figure.
    """

    required = [xcol, ycol, flux_col, vcol]
    missing = [c for c in required if c not in line_df.columns]
    if missing:
        raise ValueError(f"Missing columns in line_df: {missing}")

    with sns.axes_style("darkgrid"):
        fig, ax = plt.subplots(1, 2, figsize=figsize, constrained_layout=True)

        # General title
        if figure_title is not None:
            fig.suptitle(figure_title, fontsize=16)

        # Panel 1: log flux
        sc1 = ax[0].scatter(
            line_df[xcol],
            line_df[ycol],
            s=s,
            c=line_df[flux_col],
            cmap=flux_cmap,  norm="log"
        )
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

def plot_panels_wcs(line_df, wcs, *, mark_func=None, s=25,
                          xcol="RAdeg", ycol="DEdeg",
                          flux_col="log_F", vcol="V_mean",
                          flux_cmap="magma", v_cmap="RdBu_r",
                          invert_ra=True, figsize=(14, 7),
                          titles=("Log Flux", "V_mean - <V_mean>"),
                          cbar_labels=("Flux", "V_mean - mean"),
                          figure_title=None):
    """
    Plot two panels for a given line DataFrame using WCSAxes:
      (1) flux_col map
      (2) mean-subtracted vcol map

    Parameters
    ----------
    line_df : pandas.DataFrame
        Must contain xcol, ycol, flux_col, vcol.
    wcs : astropy.wcs.WCS
        WCS object used to create world-coordinate axes.
    mark_func : callable or None
        Function like mark_points(ax) to annotate points on each axis.
        If it plots RA/Dec values, it should also use
        transform=ax.get_transform("world").
    s : float
        Marker size for scatter.
    invert_ra : bool
        If True, invert x-axis (RA convention).
    figure_title : str or None
        General title for the whole figure.
    """

    required = [xcol, ycol, flux_col, vcol]
    missing = [c for c in required if c not in line_df.columns]
    if missing:
        raise ValueError(f"Missing columns in line_df: {missing}")

    with sns.axes_style("darkgrid"):
        fig = plt.figure(figsize=figsize, constrained_layout=True)

        ax0 = fig.add_subplot(1, 2, 1, projection=wcs)
        ax1 = fig.add_subplot(1, 2, 2, projection=wcs)
        ax = [ax0, ax1]

        if figure_title is not None:
            fig.suptitle(figure_title, fontsize=16)

        # Panel 1: log flux
        sc1 = ax[0].scatter(
            line_df[xcol],
            line_df[ycol],
            s=s,
            c=line_df[flux_col],
            cmap=flux_cmap,
            norm="log",
            transform=ax[0].get_transform("world")
        )
        if invert_ra:
            ax[0].invert_xaxis()
        ax[0].set_xlabel("RA")
        ax[0].set_ylabel("Dec")
        ax[0].set_title(titles[0])
        if callable(mark_func):
            mark_func(ax[0])
        fig.colorbar(sc1, ax=ax[0], label=cbar_labels[0])

        # Panel 2: mean-subtracted velocity
        v1 = line_df[vcol] - line_df[vcol].mean()
        sc2 = ax[1].scatter(
            line_df[xcol],
            line_df[ycol],
            s=s,
            c=v1,
            cmap=v_cmap,
            transform=ax[1].get_transform("world")
        )
        if invert_ra:
            ax[1].invert_xaxis()
        ax[1].set_xlabel("RA")
        ax[1].set_ylabel("Dec")
        ax[1].set_title(titles[1])
        if callable(mark_func):
            mark_func(ax[1])
        fig.colorbar(sc2, ax=ax[1], label=cbar_labels[1])

    return fig, ax    