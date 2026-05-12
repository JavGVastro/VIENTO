# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 07:09:49 2025

@author: ZAINTEL2
"""

import numpy as np
from matplotlib import pyplot as plt

def plot_param_comp(*dicts, labels=None, decimals=4):
    """
    Plot parameter dictionaries with asymmetric error bars.

    Parameters
    ----------
    *dicts : one or more dict objects
        Each dict must have keys mapping to lists of [value, upper, lower] for error bar plotting.
    labels : list of str, optional
        Labels for each dictionary. If None, will use "Set 1", "Set 2", etc.
    decimals : int, optional
        Number of decimals to round values (default: 4).
    """
    n_sets = len(dicts)
    param_keys = list(dicts[0].keys())
    n_params = len(param_keys)

    # Prepare labels
    if labels is None:
        labels = [f"Set {i+1}" for i in range(n_sets)]

    x = np.arange(n_params)  # positions on x axis

    width = 0.8 / n_sets  # Bar width
    plt.figure(figsize=(max(6, n_params * 1.3), 5))

    for idx, d in enumerate(dicts):
        y = [round(d[k][0], decimals) for k in param_keys]
        # Set negative uncertainties to zero
        yerr_upper = [max(0, round(d[k][1], decimals)) for k in param_keys]
        yerr_lower = [max(0, round(d[k][2], decimals)) for k in param_keys]
        # Offset for multiple sets
        x_offset = x + (idx - n_sets/2) * width + width/2

        plt.errorbar(
            x_offset,
            y,
            yerr=[yerr_lower, yerr_upper],
            fmt='o',
            label=labels[idx],
            capsize=5,
            elinewidth=2,
        )

    plt.xticks(x, param_keys, rotation=45)
    plt.ylabel('Value')
    plt.title('Parameter values with asymmetric uncertainties')
    plt.legend()
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.show()
    


def plot_param_comp_obs(*dicts, labels=None, decimals=4, obs=None, obs_linestyle="--", obs_alpha=0.6):
    """
    Plot parameter dictionaries with asymmetric error bars.
    Optionally plot one horizontal reference line per dictionary (obs).

    Parameters
    ----------
    *dicts : one or more dict objects
        Each dict must have keys mapping to lists of [value, upper, lower].
    labels : list of str, optional
        Labels for each dictionary. If None, will use "Set 1", "Set 2", etc.
    decimals : int, optional
        Number of decimals to round values (default: 4).
    obs : array-like, optional
        One reference value per input dict. Must have length == number of dicts.
        If provided, draws one horizontal line per dict at y = obs[idx].
    obs_linestyle : str, optional
        Linestyle for obs lines (default "--").
    obs_alpha : float, optional
        Alpha for obs lines (default 0.6).
    """
    n_sets = len(dicts)
    if n_sets == 0:
        raise ValueError("Provide at least one parameter dictionary.")

    param_keys = list(dicts[0].keys())
    n_params = len(param_keys)

    # Prepare labels
    if labels is None:
        labels = [f"Set {i+1}" for i in range(n_sets)]
    if len(labels) != n_sets:
        raise ValueError(f"labels must have length {n_sets} (got {len(labels)}).")

    # Validate obs: must match number of dicts (not number of parameters)
    if obs is not None:
        obs = np.asarray(obs, dtype=float)
        if obs.ndim != 1 or len(obs) != n_sets:
            raise ValueError(
                f"obs must be 1D with length == number of sets ({n_sets}); got shape {obs.shape}."
            )

    x = np.arange(n_params)
    width = 0.8 / n_sets
    plt.figure(figsize=(max(6, n_params * 1.3), 5))

    for idx, d in enumerate(dicts):
        # (Optional but recommended) enforce same keys/order across dicts
        if list(d.keys()) != param_keys:
            raise ValueError("All dictionaries must have the same keys in the same order.")

        y = [round(d[k][0], decimals) for k in param_keys]
        yerr_upper = [max(0, round(d[k][1], decimals)) for k in param_keys]
        yerr_lower = [max(0, round(d[k][2], decimals)) for k in param_keys]

        x_offset = x + (idx - n_sets/2) * width + width/2

        eb = plt.errorbar(
            x_offset,
            y,
            yerr=[yerr_lower, yerr_upper],
            fmt="o",
            label=labels[idx],
            capsize=5,
            elinewidth=2,
        )

        # Draw one horizontal obs line for this set (if provided)
        if obs is not None:
            color = eb.lines[0].get_color()  # match marker color
            plt.axhline(
                obs[idx],
                linestyle=obs_linestyle,
                alpha=obs_alpha,
                color=color,
            )

    plt.xticks(x, param_keys, rotation=45)
    plt.ylabel("Value")
    plt.title("Parameter values with asymmetric uncertainties")
    plt.legend()
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.show()


def plot_param(*dicts, labels=None, decimals=4, true=None):
    """
    For each key in the input dicts, plot the values (with error bars) on a separate plot.
    Optionally plot reference 'true' values as horizontal lines.

    Parameters
    ----------
    *dicts : one or more dict objects
        Each dict must have keys mapping to lists of [value, upper, lower] for error bar plotting.
    labels : list of str, optional
        Labels for each dictionary. If None, will use "Set 1", "Set 2", etc.
    decimals : int, optional
        Number of decimals to round values (default: 4).
    true : list, tuple, or dict, optional
        If list/tuple: reference values for keys ['sig2', 'r0', 'm'] in that order.
        If dict: maps key names to reference values.
    """
    n_sets = len(dicts)
    param_keys = list(dicts[0].keys())
    n_params = len(param_keys)

    # Prepare labels
    if labels is None:
        labels = [f"Set {i+1}" for i in range(n_sets)]

    x = np.arange(n_sets)  # one spot for each set (dict)

    # Prepare "true" as a mapping from param_keys to values
    if true is not None:
        if isinstance(true, dict):
            true_map = true
        elif isinstance(true, (list, tuple)):
            # Map for sig2, r0, m if present
            true_keys = ['sig2', 'r0', 'm']
            true_map = {k: v for k, v in zip(true_keys, true)}
        else:
            true_map = {}
    else:
        true_map = {}

    for key in param_keys:
        values = []
        yerr_upper = []
        yerr_lower = []
        for d in dicts:
            values.append(round(d[key][0], decimals))
            yerr_upper.append(max(0, round(d[key][1], decimals)))
            yerr_lower.append(max(0, round(d[key][2], decimals)))

        plt.figure(figsize=(max(4, n_sets * 1.2), 5))
        plt.errorbar(
            x,
            values,
            yerr=[yerr_lower, yerr_upper],
            fmt='o',
            capsize=5,
            elinewidth=2,
            label=key,
        )
        plt.xticks(x, labels, rotation=30)
        plt.ylabel(key)
        plt.title(f"{key} value with asymmetric uncertainties")
        plt.grid(alpha=0.3)
        # Optionally add value labels on points:
        for xi, val in zip(x, values):
            plt.text(xi, val, f"{val}", ha="center", va="bottom", fontsize=9)
        # Draw "true" value line if provided
        if key in true_map and true_map[key] is not None:
            plt.axhline(true_map[key], color='red', linestyle='--', label='Reference')
            #plt.legend()
        plt.tight_layout()
        plt.show()