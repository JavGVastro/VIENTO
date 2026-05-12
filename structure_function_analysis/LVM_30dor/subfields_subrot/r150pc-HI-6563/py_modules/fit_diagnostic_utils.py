"""
fit_diagnostic_utils.py

Utility functions for quality control of structure-function model fits.

These functions are designed to be used after fitting an observational
structure function with lmfit and, optionally, after running emcee.
"""

import numpy as np


def near_bound(param, frac=0.05):
    """
    Check whether an lmfit parameter is close to its lower or upper bound.

    Parameters
    ----------
    param : lmfit.Parameter
        Parameter object from result.params.
    frac : float, optional
        Fraction of the allowed parameter range used to define "near bound".
        For example, frac=0.05 means the parameter is flagged if it lies
        within 5% of either boundary.

    Returns
    -------
    bool
        True if the parameter is close to its lower or upper bound.
    """
    value = param.value
    pmin = param.min
    pmax = param.max

    if pmin is None or pmax is None:
        return False

    if not np.isfinite(pmin) or not np.isfinite(pmax):
        return False

    width = pmax - pmin

    if width <= 0:
        return False

    return (value - pmin < frac * width) or (pmax - value < frac * width)

def near_bound_relative(param, lower_factor=1.5, upper_fraction=0.9):
    """
    Check whether an lmfit parameter is close to its bounds using
    relative criteria instead of a fixed fraction of the full linear range.

    This is useful for positive parameters with wide allowed ranges,
    such as r0.

    Parameters
    ----------
    param : lmfit.Parameter
        Parameter object from result.params.
    lower_factor : float, optional
        The parameter is flagged as near the lower bound if:

            value < lower_factor * pmin

        For example, lower_factor=1.5 means the value is considered
        near the lower bound if it is less than 1.5 times the minimum.
    upper_fraction : float, optional
        The parameter is flagged as near the upper bound if:

            value > upper_fraction * pmax

        For example, upper_fraction=0.9 means the value is considered
        near the upper bound if it is above 90% of the maximum.

    Returns
    -------
    bool
        True if the parameter is close to the lower or upper bound.
    """
    value = param.value
    pmin = param.min
    pmax = param.max

    if pmin is None or pmax is None:
        return False

    if not np.isfinite(value) or not np.isfinite(pmin) or not np.isfinite(pmax):
        return False

    if pmin <= 0 or pmax <= 0:
        return False

    if pmax <= pmin:
        return False

    near_lower = value < lower_factor * pmin
    near_upper = value > upper_fraction * pmax

    return near_lower or near_upper


def frac_uncertainty(value, err_plus, err_minus):
    """
    Compute the maximum fractional uncertainty from asymmetric errors.

    Parameters
    ----------
    value : float
        Central parameter value.
    err_plus : float
        Positive uncertainty.
    err_minus : float
        Negative uncertainty.

    Returns
    -------
    float
        Maximum fractional uncertainty.

    Notes
    -----
    If the value is zero or non-finite, the function returns np.inf.
    """
    if value == 0 or not np.isfinite(value):
        return np.inf

    return max(abs(err_plus), abs(err_minus)) / abs(value)


def abs_uncertainty(err_plus, err_minus):
    """
    Compute the maximum absolute uncertainty from asymmetric errors.

    Parameters
    ----------
    err_plus : float
        Positive uncertainty.
    err_minus : float
        Negative uncertainty.

    Returns
    -------
    float
        Maximum absolute uncertainty.
    """
    return max(abs(err_plus), abs(err_minus))


def max_run_same_sign(x):
    """
    Compute the longest run of consecutive values with the same sign.

    This is useful for identifying systematic residual patterns.

    Parameters
    ----------
    x : array-like
        Residual array or any signed quantity.

    Returns
    -------
    int
        Maximum number of consecutive values with the same sign.
    """
    x = np.asarray(x)

    if x.size == 0:
        return 0

    signs = np.sign(x)
    signs = signs[signs != 0]

    if len(signs) == 0:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(signs)):
        if signs[i] == signs[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run


def get_bound_flags(params, param_names=None, frac=0.05):
    """
    Check which parameters are close to their bounds.

    Parameters
    ----------
    params : lmfit.Parameters
        Parameter collection, usually result.params.
    param_names : list of str or None, optional
        Names of parameters to check. If None, all parameters are checked.
    frac : float, optional
        Fraction of the allowed parameter range used to define "near bound".

    Returns
    -------
    dict
        Dictionary with parameter names as keys and boolean flags as values.
    """
    if param_names is None:
        param_names = list(params.keys())

    flags = {}

    for name in param_names:
        if name in params:
            flags[name] = near_bound(params[name], frac=frac)
        else:
            flags[name] = False

    return flags


def summarize_acceptance_fraction(result_emcee):
    """
    Summarize the emcee acceptance fraction.

    Parameters
    ----------
    result_emcee : lmfit ModelResult
        Result returned by lmfit using method='emcee'.

    Returns
    -------
    dict
        Dictionary with median, minimum, and maximum acceptance fraction.
        Returns NaN values if acceptance_fraction is unavailable.
    """
    summary = {
        "acceptance_fraction_median": np.nan,
        "acceptance_fraction_min": np.nan,
        "acceptance_fraction_max": np.nan,
    }

    if not hasattr(result_emcee, "acceptance_fraction"):
        return summary

    acceptance_fraction = np.asarray(result_emcee.acceptance_fraction)

    summary["acceptance_fraction_median"] = np.nanmedian(acceptance_fraction)
    summary["acceptance_fraction_min"] = np.nanmin(acceptance_fraction)
    summary["acceptance_fraction_max"] = np.nanmax(acceptance_fraction)

    return summary


def summarize_autocorrelation_time(result_emcee):
    """
    Summarize the maximum autocorrelation time from an emcee result.

    Parameters
    ----------
    result_emcee : lmfit ModelResult
        Result returned by lmfit using method='emcee'.

    Returns
    -------
    float
        Maximum autocorrelation time. Returns np.nan if unavailable.
    """
    if not hasattr(result_emcee, "acor"):
        return np.nan

    try:
        return np.nanmax(result_emcee.acor)
    except Exception:
        return np.nan


def get_bound_flags(params, param_names, frac=0.05):
    """
    Check whether several lmfit parameters are close to their bounds.

    Parameters
    ----------
    params : lmfit.Parameters
        Parameter collection, usually result.params.
    param_names : list of str
        Names of parameters to check.
    frac : float, optional
        Fraction of the allowed parameter range used to define "near bound".

    Returns
    -------
    dict
        Dictionary with parameter names as keys and boolean flags as values.
    """
    flags = {}

    for name in param_names:
        if name in params:
            flags[name] = near_bound(params[name], frac=frac)
        else:
            flags[name] = False

    return flags


def frac_uncertainty(value, err_plus, err_minus):
    """
    Compute the maximum fractional uncertainty from asymmetric errors.

    Parameters
    ----------
    value : float
        Central parameter value.
    err_plus : float
        Positive uncertainty.
    err_minus : float
        Negative uncertainty.

    Returns
    -------
    float
        Maximum fractional uncertainty.

    Notes
    -----
    If value is zero or non-finite, the function returns np.inf.
    """
    if value == 0 or not np.isfinite(value):
        return np.inf

    return max(abs(err_plus), abs(err_minus)) / abs(value)


def max_run_same_sign(x):
    """
    Compute the longest run of consecutive values with the same sign.

    This is useful for identifying systematic residual patterns. For example,
    if several consecutive residuals are all positive or all negative, the
    model may be systematically above or below the data over that range.

    Parameters
    ----------
    x : array-like
        Residual array or any signed quantity.

    Returns
    -------
    int
        Maximum number of consecutive values with the same sign.
    """
    x = np.asarray(x)

    if x.size == 0:
        return 0

    signs = np.sign(x)
    signs = signs[signs != 0]

    if len(signs) == 0:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(signs)):
        if signs[i] == signs[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run