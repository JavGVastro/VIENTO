"""Intensity-weighted second-order structure functions for scattered sky data.

Dependencies: numpy, pandas. Coordinates X/Y must be RA/Dec in degrees;
RV is velocity and I is LINEAR intensity (not its logarithm).

Notebook usage (put this file in py_modules):
    from strucfunc_scattered import sosflog
    table = sosflog(data_frame, 0.05, 3600, weight_col="I")
    s = 0.5 * (table['s', 'min'] + table['s', 'max']) * pc
    b2 = table['dV2', 'mean']
    b2w = table['dV2', 'weighted_mean']

Each unique pair i<j with positive separation contributes once. Sky distances
use the original small-angle approximation, with wrapped RA differences.
Time is O(N**2); temporary pair storage is O(N), plus per-bin accumulators.
No spatial interpolation or gridding is performed.

The default lower-bin policy preserves the old sosflog convention: all
separations below 10**log_s_min join bin zero. Set below_min='drop' to enforce
that lower cutoff. Bin k otherwise spans [10**(log_s_min+k*dlog),
10**(log_s_min+(k+1)*dlog)). Only occupied bins are returned.

Both SFs use the same finite, positive-intensity sample. Negative finite
intensities raise an error; zero/nonfinite intensities and nonfinite coordinates
or velocities are excluded with a warning. weight_col=None uses unit weights.

Pair weights are (I_i/I_max)*(I_j/I_max), for numerical scaling. This has no
effect on the weighted SF. Sum-weight columns therefore use normalized units;
table.attrs['intensity_scale'] records I_max. No noise correction is applied.

std is the sample scatter of pair dv**2 (ddof=1). weighted_std is the weighted
population scatter. sem_naive=std/sqrt(N) is provided only for compatibility:
pairs share observations and are not independent. N_eff=(sum w)**2/sum(w**2)
diagnoses weight concentration, NOT the number of independent measurements.
No weighted error bar is claimed. Use a suitable spatial resampling analysis
for scientific uncertainties. Quartiles from the old describe() are not kept.

Metadata in DataFrame.attrs is not automatically preserved by FITS export.
"""

import warnings
import numpy as np
import pandas as pd


def _merge(a, b):
    """Merge (total weight, mean, central sum of squares)."""
    if a[0] == 0:
        return b
    total = a[0] + b[0]
    delta = b[1] - a[1]
    return (total, a[1] + delta * b[0] / total,
            a[2] + b[2] + delta**2 * a[0] * b[0] / total)


def sosflogw(df, dlog=0.05, c=3600, weight_col="I", *,
            log_s_min=1.0, below_min="merge"):
    """Return a MultiIndex-column table of unweighted and weighted SFs.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns X (RA deg), Y (Dec deg), RV, and weight_col.
    dlog : float
        Separation bin width in dex.
    c : float
        Angular conversion from degrees; 3600 produces arcseconds.
    weight_col : str or None
        Linear nonnegative intensity column, or None for unit weights.
    log_s_min : float
        Log10 lower edge in the separation units set by c.
    below_min : {'merge', 'drop'}
        Merge smaller positive separations into bin zero, or discard them.

    Returns
    -------
    pandas.DataFrame
        Existing notebook keys ('s', 'min/max') and ('dV2', 'mean/count/std')
        remain available. New keys include ('dV2', 'weighted_mean'),
        ('weights', 'sum'), ('weights', 'sum_sq'), ('weights', 'n_eff'),
        ('dV2', 'sum'), and ('dV2', 'weighted_sum').
    """
    if not np.isfinite(dlog) or dlog <= 0:
        raise ValueError('dlog must be finite and positive')
    if not np.isfinite(c) or c <= 0 or not np.isfinite(log_s_min):
        raise ValueError('c must be finite and positive; log_s_min finite')
    if below_min not in ('merge', 'drop'):
        raise ValueError("below_min must be 'merge' or 'drop'")
    xyz = df[['X', 'Y', 'RV']].to_numpy(dtype=float)
    intensity = (np.ones(len(df)) if weight_col is None
                 else df[weight_col].to_numpy(dtype=float))
    if np.any(np.isfinite(intensity) & (intensity < 0)):
        raise ValueError('Negative intensities: select a valid sample explicitly')
    good = np.isfinite(xyz).all(axis=1) & np.isfinite(intensity) & (intensity > 0)
    dropped = int((~good).sum())
    if dropped:
        warnings.warn(f'Excluded {dropped} invalid/zero-intensity rows from both SFs',
                      RuntimeWarning, stacklevel=2)
    xyz, intensity = xyz[good], intensity[good]
    if len(xyz) < 2:
        raise ValueError('At least two valid positive-weight observations required')
    if np.any(np.abs(xyz[:, 1]) > 90):
        raise ValueError('Y must be declination in degrees within [-90, 90]')
    intensity_scale = float(intensity.max())
    w = intensity / intensity_scale
    x, y, v = xyz.T
    bins = {}
    zero_pairs = 0
    below_pairs = 0
    for i in range(len(x) - 1):
        dx = (x[i+1:] - x[i] + 180) % 360 - 180
        r = c * np.hypot(dx * np.cos(np.deg2rad((y[i+1:] + y[i])/2)),
                         y[i+1:] - y[i])
        q = (v[i+1:] - v[i])**2
        pw = w[i] * w[i+1:]
        if not (np.isfinite(r).all() and np.isfinite(q).all()):
            raise ValueError('Separation or squared velocity overflow')
        zero_pairs += int((r == 0).sum())
        keep = r > 0
        if below_min == 'drop':
            small = np.zeros(len(r), dtype=bool)
            small[keep] = np.log10(r[keep]) < log_s_min
            below_pairs += int(small.sum())
            keep &= ~small
        r, q, pw = r[keep], q[keep], pw[keep]
        if np.any(pw <= 0):
            raise ValueError('Intensity dynamic range causes pair-weight underflow')
        k = np.maximum(0, np.floor((np.log10(r)-log_s_min)/dlog)).astype(np.int64)
        for key in np.unique(k):
            take = k == key
            rr, qq, ww = r[take], q[take], pw[take]
            n, sw = len(qq), float(ww.sum())
            qm, rm = float(qq.mean()), float(rr.mean())
            wm = float(np.dot(ww, qq)/sw)
            part = ((n, qm, float(np.sum((qq-qm)**2))),
                    (sw, wm, float(np.dot(ww, (qq-wm)**2))),
                    (n, rm, float(np.sum((rr-rm)**2))))
            if key not in bins:
                bins[key] = [part[0], part[1], part[2], rr.min(), rr.max(),
                             float(np.dot(ww, ww))]
            else:
                b = bins[key]
                for j in range(3):
                    b[j] = _merge(b[j], part[j])
                b[3], b[4] = min(b[3], rr.min()), max(b[4], rr.max())
                b[5] += float(np.dot(ww, ww))
    if not bins:
        raise ValueError('No positive-separation pairs remain in the chosen bins')
    rows = []
    for key in sorted(bins):
        u, wt, sep, rmin, rmax, sw2 = bins[key]
        n, mean, m2 = u
        sw, wm, wm2 = wt
        std = np.sqrt(m2/(n-1)) if n > 1 else np.nan
        rows.append({('s', 'count'): n, ('s', 'mean'): sep[1],
                     ('s', 'std'): np.sqrt(sep[2]/(n-1)) if n > 1 else np.nan,
                     ('s', 'min'): rmin, ('s', 'max'): rmax,
                     ('dV2', 'count'): n, ('dV2', 'mean'): mean,
                     ('dV2', 'std'): std, ('dV2', 'sem_naive'): std/np.sqrt(n),
                     ('dV2', 'sum'): n*mean,
                     ('dV2', 'weighted_mean'): wm,
                     ('dV2', 'weighted_std'): np.sqrt(wm2/sw),
                     ('dV2', 'weighted_sum'): sw*wm,
                     ('weights', 'sum'): sw, ('weights', 'sum_sq'): sw2,
                     ('weights', 'n_eff'): sw/(sw2/sw)})
    table = pd.DataFrame(rows, index=pd.Index(sorted(bins), name='ils'))
    table.columns = pd.MultiIndex.from_tuples(table.columns)
    vw = float(np.average(v, weights=w))
    table.attrs.update(n_input=len(df), n_used=len(x), n_dropped=dropped,
                       zero_separation_pairs=zero_pairs, below_min_pairs=below_pairs,
                       intensity_scale=intensity_scale, weight_col=weight_col,
                       dlog=dlog, c=c, log_s_min=log_s_min, below_min=below_min,
                       mean_velocity=float(v.mean()), sigma2=float(np.var(v)),
                       weighted_mean_velocity=vw,
                       weighted_sigma2=float(np.average((v-vw)**2, weights=w)))
    return table
