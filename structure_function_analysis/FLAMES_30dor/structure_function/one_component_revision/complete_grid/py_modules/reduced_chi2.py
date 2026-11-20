# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 06:34:16 2026

@author: javas
"""

import numpy as np


def make_weights(
    r,
    B,
    box_size,
    relative_uncertainty,
    large_scale_limit=0.10,
    fit_limit=0.15,
    large_scale_factor=1.0,
    first_points_factor=1.0,
    n_first_points=3,
):
    """
    Create weights and fitting masks for lmfit.

    The assumed uncertainty is:

        sigma_B = relative_uncertainty * B

    and the lmfit weights are:

        weights = 1 / sigma_B

    Parameters
    ----------
    r : array-like
        Separation values.

    B : array-like
        Observed structure-function values.

    box_size : float
        Size of the observed field.

    relative_uncertainty : float
        Fractional uncertainty assigned to B.

    large_scale_limit : float, optional
        Fraction of box_size used to identify large scales.

    fit_limit : float, optional
        Fraction of box_size used to select points for fitting.

    large_scale_factor : float, optional
        Factor used to reduce the weights at large scales.

    first_points_factor : float, optional
        Factor used to reduce the weights of the first points.

    n_first_points : int, optional
        Number of first points affected by first_points_factor.

    Returns
    -------
    weights_fit : ndarray
        Weights only for the fitted points.

    to_fit : ndarray of bool
        Boolean mask selecting fitted points.

    weights : ndarray
        Full weights array.

    large_scale : ndarray of bool
        Boolean mask selecting large-scale points.
    """

    r = np.asarray(r)
    B = np.asarray(B)

    weights = 1.0 / (relative_uncertainty * B)

    large_scale = r > large_scale_limit * box_size
    weights[large_scale] /= large_scale_factor

    weights[:n_first_points] /= first_points_factor

    to_fit = r <= fit_limit * box_size

    weights_fit = weights[to_fit]

    return weights_fit, to_fit, weights, large_scale

def tune_relative_uncertainty(
    fit_function,
    r,
    B,
    box_size,
    initial_relative_uncertainty=0.05,
    target_redchi_min=0.5,
    target_redchi_max=1.0,
    max_iter=30,
    step_factor=1.2,
    verbose=True,
    **weight_kwargs,
):
    """
    Automatically find a relative_uncertainty that gives reduced chi-square
    inside a desired interval.

    Parameters
    ----------
    fit_function : callable
        Function that performs the lmfit fit.

        It must have the form:

            result = fit_function(r_fit, B_fit, weights_fit)

        and it must return an lmfit result object with result.redchi.

    r, B : arrays
        Data arrays.
    box_size : float
        Observational box size.
    initial_relative_uncertainty : float
        Starting value for the fractional uncertainty.
    target_redchi_min, target_redchi_max : float
        Desired interval for reduced chi-square.
    max_iter : int
        Maximum number of iterations.
    step_factor : float
        Multiplicative factor used to update relative_uncertainty.
    verbose : bool
        Print progress if True.
    weight_kwargs :
        Extra arguments passed to make_weights.

    Returns
    -------
    best_result : lmfit result
        Final lmfit result.
    best_relative_uncertainty : float
        Final relative uncertainty.
    history : list of dict
        Iteration history.
    """

    relative_uncertainty = initial_relative_uncertainty
    history = []

    r = np.asarray(r)
    B = np.asarray(B)

    for i in range(max_iter):
    
        weights_fit, to_fit, weights, large_scale = make_weights(
            r,
            B,
            box_size,
            relative_uncertainty,
            **weight_kwargs,
        )
    
        r_fit = r[to_fit]
        B_fit = B[to_fit]
    
        result = fit_function(r_fit, B_fit, weights_fit)
        redchi = result.redchi

        history.append(
            {
                "iteration": i,
                "relative_uncertainty": relative_uncertainty,
                "redchi": redchi,
            }
        )

        if verbose:
            print(
                f"iter {i:02d}: "
                f"relative_uncertainty = {relative_uncertainty:.5f}, "
                f"redchi = {redchi:.4f}"
            )

        if target_redchi_min <= redchi <= target_redchi_max:
            if verbose:
                print("Accepted relative_uncertainty.")
            return result, relative_uncertainty, history

        if redchi > target_redchi_max:
            # chi-square too large: errors are too small
            relative_uncertainty *= step_factor

        elif redchi < target_redchi_min:
            # chi-square too small: errors are too large
            relative_uncertainty /= step_factor

    if verbose:
        print("Maximum number of iterations reached.")

    return result, relative_uncertainty, history