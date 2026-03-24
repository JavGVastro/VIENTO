import numpy as np
import matplotlib.pyplot as plt
import lmfit

def fit_structure_function(
    data_in,
    N,
    bfunc,
    bplot,
    name='name',
    data='data',
    pc_per_arcsec=1,
    relative_uncertainty=0.07,
    emcee_steps=50000,
    emcee_burn=500,
    emcee_thin=50,
    emcee_workers=16,
):
    """
    Fits a structure function model to the input data and performs MCMC sampling.
    
    Parameters
    ----------
    sf_noise_2 : dict or DataFrame-like
        Must have keys: 'N pairs', 'Unweighted B(r)', 'log10 r'
    N : float
        Box size parameter.
    bfunc : module or object
        Must have attribute bfunc03s (model function).
    bplot : module or object
        Must provide corner_plot and strucfunc_plot functions.
    name : str
        Name identifier for plots.
    data : str
        Data identifier for plots.
    pc_per_arcsec : float
        Conversion factor for arcsec to pc.
    relative_uncertainty : float
        Relative uncertainty for weighting.
    emcee_steps : int
        Number of MCMC steps.
    emcee_burn : int
        Number of MCMC burn-in steps.
    emcee_thin : int
        MCMC thinning factor.
    emcee_workers : int
        Number of parallel workers for emcee.
    
    Returns
    -------
    results : dict
        Contains 'result' (LMFit minimize result) and 'result_emcee' (MCMC result).
    """

    # Mask valid data
    mask     = np.array(data_in["N pairs"]) > 0
    B        = np.array(data_in['Unweighted B(r)'])[mask]
    r        = np.array(10 ** np.array(data_in['log10 r']))[mask]
    box_size = N

    # Model
    model = lmfit.Model(bfunc.bfunc03s)

    # Set parameter hints
    model.set_param_hint("r0",    value=0.1 * box_size,      min=0.01 * box_size,     max=2.0 * box_size)
    model.set_param_hint("sig2",  value=0.5 * B.max(),       min=0.25 * B.max(),      max=2.0 * B.max())
    model.set_param_hint("m",     value=1.0,                 min=0.5,                 max=2.0)
    model.set_param_hint("s0",    value=0.5 * pc_per_arcsec, min=0.1 * pc_per_arcsec, max=1.5 * pc_per_arcsec)
    model.set_param_hint("noise", value=0.5 * B.min(),       min=0.0, max=3 * B.min())
    # model.set_param_hint("box_size", value=box_size, vary=False)

    # Weights
    weights = 1.0 / (relative_uncertainty * B)
    large_scale = r > 0.5 * box_size
    # Optional: weights[large_scale] /= 1.25
    # Optional: weights[:1] /= 2.0

    to_fit = r <= 0.6 * box_size
    result = model.fit(B[to_fit], weights=weights[to_fit], r=r[to_fit])

    # MCMC with emcee
    emcee_kws = dict(
        steps=emcee_steps,
        burn=emcee_burn,
        thin=emcee_thin,
        is_weighted=True,
        progress=False,
        workers=emcee_workers,
    )
    emcee_params = result.params.copy()
    # Optionally add lnsigma parameter here if needed

    result_emcee = model.fit(
        data=B[to_fit],
        r=r[to_fit],
        weights=weights[to_fit],
        params=emcee_params,
        method="emcee",
        nan_policy="omit",
        fit_kws=emcee_kws,
    )

    # Plot acceptance fraction
    plt.figure()
    plt.plot(result_emcee.acceptance_fraction, "o")
    plt.xlabel("walker")
    plt.ylabel("acceptance fraction")
    plt.title("MCMC Acceptance Fraction")
    plt.show()

    # Print autocorrelation times
    if hasattr(result_emcee, "acor"):
        print("Autocorrelation time for the parameters:")
        print("----------------------------------------")
        for i, p in enumerate(result_emcee.params):
            try:
                print(f"{p} = {result_emcee.acor[i]:.3f}")
            except IndexError:
                pass

    # Corner plot
    bplot.corner_plot(
        result_emcee, result, name, data, data_ranges=[0.95, 0.99, 0.995, 0.997, 0.999]
    )

    # Structure function plot
    bplot.strucfunc_plot(
        result_emcee, result, r, B, to_fit, name, data, box_size, large_scale
    )

    # Return fit results
    return {'result': result, 'result_emcee': result_emcee}

def fit_structure_function_ideal(
    data_in,
    N,
    bfunc,
    bplot_ideal,
    name='name',
    data='data',
    pc_per_arcsec=1,
    relative_uncertainty=0.07,
    emcee_steps=50000,
    emcee_burn=500,
    emcee_thin=50,
    emcee_workers=16,
):
    """
    Fits a structure function model to the input data and performs MCMC sampling.
    
    Parameters
    ----------
    sf_noise_2 : dict or DataFrame-like
        Must have keys: 'N pairs', 'Unweighted B(r)', 'log10 r'
    N : float
        Box size parameter.
    bfunc : module or object
        Must have attribute bfunc00s (ideal model function).
    bplot : module or object
        Must provide corner_plot and strucfunc_plot functions.
    name : str
        Name identifier for plots.
    data : str
        Data identifier for plots.
    pc_per_arcsec : float
        Conversion factor for arcsec to pc.
    relative_uncertainty : float
        Relative uncertainty for weighting.
    emcee_steps : int
        Number of MCMC steps.
    emcee_burn : int
        Number of MCMC burn-in steps.
    emcee_thin : int
        MCMC thinning factor.
    emcee_workers : int
        Number of parallel workers for emcee.
    
    Returns
    -------
    results : dict
        Contains 'result' (LMFit minimize result) and 'result_emcee' (MCMC result).
    """

    # Mask valid data
    mask     = np.array(data_in["N pairs"]) > 0
    B        = np.array(data_in['Unweighted B(r)'])[mask]
    r        = np.array(10 ** np.array(data_in['log10 r']))[mask]
    box_size = N

    # Model
    model = lmfit.Model(bfunc.bfunc00s)

    # Set parameter hints
    model.set_param_hint("r0",    value=0.1 * box_size,      min=0.01 * box_size,     max=2.0 * box_size)
    model.set_param_hint("sig2",  value=0.5 * B.max(),       min=0.25 * B.max(),      max=2.0 * B.max())
    model.set_param_hint("m",     value=1.0,                 min=0.5,                 max=2.0)
    #model.set_param_hint("s0",    value=0.5 * pc_per_arcsec, min=0.1 * pc_per_arcsec, max=1.5 * pc_per_arcsec)
    #model.set_param_hint("noise", value=0.5 * B.min(),       min=0.0, max=3 * B.min())
    # model.set_param_hint("box_size", value=box_size, vary=False)

    # Weights
    weights = 1.0 / (relative_uncertainty * B)
    large_scale = r > 0.5 * box_size
    # Optional: weights[large_scale] /= 1.25
    # Optional: weights[:1] /= 2.0

    to_fit = r <= 0.6 * box_size
    result = model.fit(B[to_fit], weights=weights[to_fit], r=r[to_fit])

    # MCMC with emcee
    emcee_kws = dict(
        steps=emcee_steps,
        burn=emcee_burn,
        thin=emcee_thin,
        is_weighted=True,
        progress=False,
        workers=emcee_workers,
    )
    emcee_params = result.params.copy()
    # Optionally add lnsigma parameter here if needed

    result_emcee = model.fit(
        data=B[to_fit],
        r=r[to_fit],
        weights=weights[to_fit],
        params=emcee_params,
        method="emcee",
        nan_policy="omit",
        fit_kws=emcee_kws,
    )

    # Plot acceptance fraction
    plt.figure()
    plt.plot(result_emcee.acceptance_fraction, "o")
    plt.xlabel("walker")
    plt.ylabel("acceptance fraction")
    plt.title("MCMC Acceptance Fraction")
    plt.show()

    # Print autocorrelation times
    if hasattr(result_emcee, "acor"):
        print("Autocorrelation time for the parameters:")
        print("----------------------------------------")
        for i, p in enumerate(result_emcee.params):
            try:
                print(f"{p} = {result_emcee.acor[i]:.3f}")
            except IndexError:
                pass

    # Corner plot
    bplot_ideal.corner_plot(
        result_emcee, result, name, data, data_ranges=[0.95, 0.99, 0.995, 0.997, 0.999]
    )

    # Structure function plot
    bplot_ideal.strucfunc_plot(
        result_emcee, result, r, B, to_fit, name, data, box_size, large_scale
    )

    # Return fit results
    return {'result': result, 'result_emcee': result_emcee}