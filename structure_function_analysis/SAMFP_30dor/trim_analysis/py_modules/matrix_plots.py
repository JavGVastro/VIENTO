# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 06:53:57 2026

@author: ZAINTEL2
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde

def plot_pdfs(
    arrays,
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
    Plot PDF estimates from multiple numpy arrays (matrices / tensors).

    Parameters
    ----------
    arrays : list[np.ndarray] or dict[str, np.ndarray]
        Arrays to plot. If dict, keys are used as labels.
        Each array can be any shape; it will be flattened to 1D.
    labels : list[str] | None
        Labels if `arrays` is a list. Ignored if `arrays` is a dict.
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
        If True, annotate N/mean/std/var per dataset (stacked on the plot).
    """

    # --- normalize input into (label, array) pairs ---
    if isinstance(arrays, dict):
        items = list(arrays.items())
    else:
        if labels is None:
            labels = [f"arr{i+1}" for i in range(len(arrays))]
        items = list(zip(labels, arrays))

    fig, ax = plt.subplots(figsize=figsize)

    # --- precompute transformed series so we can share x-range ---
    series = []
    for name, arr in items:
        if arr is None:
            print(f"[skip] {name}: array is None")
            continue

        a = np.asarray(arr).ravel()

        # keep only finite values (drops NaN and +/-Inf)
        a = a[np.isfinite(a)]
        if a.size == 0:
            print(f"[skip] {name}: no finite values")
            continue

        mu = float(a.mean())
        sigma = float(a.std(ddof=1)) if a.size > 1 else 0.0
        var = float(a.var(ddof=1)) if a.size > 1 else 0.0

        # transform
        if center == "mean":
            y = a - mu
        elif center == "zscore":
            y = (a - mu) / sigma if sigma > 0 else a * 0.0
        elif center == "none":
            y = a
        else:
            raise ValueError("center must be 'none', 'mean', or 'zscore'")

        series.append((name, a, y, mu, sigma, var))

    if not series:
        raise ValueError("No valid arrays to plot (all empty or non-finite).")

    # --- common x-range ---
    all_y = np.concatenate([s[2] for s in series])
    xmin, xmax = float(all_y.min()), float(all_y.max())
    pad = 0.05 * (xmax - xmin) if xmax > xmin else 1.0
    xmin, xmax = xmin - pad, xmax + pad

    # --- plot each dataset ---
    for name, a, y, mu, sigma, var in series:
        if method == "kde":
            if y.size < 2:
                print(f"[skip] {name}: need >=2 samples for KDE")
                continue

            kde = gaussian_kde(y)
            kde.set_bandwidth(bw_method=kde.factor * bw_scale)

            grid = np.linspace(xmin, xmax, grid_points)
            pdf = kde(grid)
            ax.plot(grid, pdf, linewidth=2, label=name)

        elif method in ("hist_curve", "hist_step"):
            dens, edges = np.histogram(y, bins=bins, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])

            if method == "hist_curve":
                ax.plot(centers, dens, marker="o", linewidth=2, label=name)
            else:  # hist_step
                ax.step(edges[:-1], dens, where="post", linewidth=2, label=name)

        else:
            raise ValueError("method must be 'kde', 'hist_curve', or 'hist_step'")

    # --- labels / title ---
    if center == "mean":
        ax.set_xlabel("value - mean")
    elif center == "zscore":
        ax.set_xlabel("(value - mean) / std")
    else:
        ax.set_xlabel("value")

    ax.set_ylabel("PDF")
    ax.set_title(f"PDFs ({method}, center={center})")
    ax.legend()

    # --- optional stats annotations ---
    if annotate:
        lines = []
        for name, a, y, mu, sigma, var in series:
            lines.append(
                f"{name}: N={a.size}, mean={mu:.4g}, std={sigma:.4g}, var={var:.4g}"
            )
        ax.text(
            0.01, 0.99, "\n".join(lines),
            transform=ax.transAxes,
            ha="left", va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="gray"),
        )

    plt.tight_layout()
    return fig, ax