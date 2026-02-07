# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 06:50:51 2025

@author: ZAINTEL2
"""

import numpy as np

def ci_results_compiler(
    a
):
    """
    Compile the results from the confidence interval analysis. We recover the 
    turbulent parameters results value from the LM analysis and the
    the confidence intervals from the MCMC analysis.
    
    Parameters
    ----------
    reslm   : lmfit.model.ModelResult
        LMFit minimize result.
    resmcmc : lmfit.model.ModelResult
        MCMC results.

    Returns
    -------
    results_2sig : dict
        Contains turbulent parameter with its confidence intervals.
    """
    
    result = a['result']
    result_emcee = a['result_emcee']


    LM = {
        'sig2': [result.params['sig2'].value,result.params['sig2'].stderr],
        'r0': [result.params['r0'].value,result.params['r0'].stderr],
        'm' : [result.params['m'].value,result.params['m'].stderr],
        's0': [result.params['s0'].value,result.params['s0'].stderr],
        'noise' : [result.params['noise'].value,result.params['noise'].stderr]
    }


    MCMC = {
        'sig2': [result_emcee.params['sig2'].value,result_emcee.params['sig2'].stderr],
        'r0': [result_emcee.params['r0'].value,result_emcee.params['r0'].stderr],
        'm' : [result_emcee.params['m'].value,result_emcee.params['m'].stderr],
        's0': [result_emcee.params['s0'].value,result_emcee.params['s0'].stderr],
        'noise' : [result_emcee.params['noise'].value,result_emcee.params['noise'].stderr]
    }

    sig2s2 = np.percentile(result_emcee.flatchain['sig2'],[2.5, 97.5])
    r0s2 = np.percentile(result_emcee.flatchain['r0'],[2.5, 97.5])
    ms2 = np.percentile(result_emcee.flatchain['m'],[2.5, 97.5])
    s0s2 = np.percentile(result_emcee.flatchain['s0'],[2.5, 97.5])
    b0s2 = np.percentile(result_emcee.flatchain['noise'],[2.5, 97.5])
    
    sig2s2p = sig2s2[1]-result.params['sig2'].value
    sig2s2m = result.params['sig2'].value-sig2s2[0]
    
    r0s2p = r0s2[1]-result.params['r0'].value
    r0s2m = result.params['r0'].value-r0s2[0]
    
    ms2p = ms2[1]-result.params['m'].value
    ms2m = result.params['m'].value-ms2[0]
    
    s0s2p = s0s2[1]-result.params['s0'].value
    s0s2m = result.params['s0'].value-s0s2[0]
    
    b0s2p = b0s2[1]-result.params['noise'].value
    b0s2m = result.params['noise'].value-b0s2[0]

    results_2sig = {
        'sig2': [result.params['sig2'].value,sig2s2p,sig2s2m],
        'r0': [result.params['r0'].value,r0s2p,r0s2m],
        'm' : [result.params['m'].value,ms2p,ms2m],
        's0': [result.params['s0'].value,s0s2p,s0s2m],
        'noise' : [result.params['noise'].value,b0s2p,b0s2m] 
        
    }
        
    return results_2sig

def ci_results_compiler_ideal(
    a
):
    """
    Compile the results from the confidence interval analysis. We recover the 
    turbulent parameters results value from the LM analysis and the
    the confidence intervals from the MCMC analysis.
    
    Parameters
    ----------
    reslm   : lmfit.model.ModelResult
        LMFit minimize result.
    resmcmc : lmfit.model.ModelResult
        MCMC results.

    Returns
    -------
    results_2sig : dict
        Contains turbulent parameter with its confidence intervals.
    """
    
    result = a['result']
    result_emcee = a['result_emcee']


    LM = {
        'sig2': [result.params['sig2'].value,result.params['sig2'].stderr],
        'r0': [result.params['r0'].value,result.params['r0'].stderr],
        'm' : [result.params['m'].value,result.params['m'].stderr],
   #     's0': [result.params['s0'].value,result.params['s0'].stderr],
   #     'noise' : [result.params['noise'].value,result.params['noise'].stderr]
    }


    MCMC = {
        'sig2': [result_emcee.params['sig2'].value,result_emcee.params['sig2'].stderr],
        'r0': [result_emcee.params['r0'].value,result_emcee.params['r0'].stderr],
        'm' : [result_emcee.params['m'].value,result_emcee.params['m'].stderr],
    #    's0': [result_emcee.params['s0'].value,result_emcee.params['s0'].stderr],
    #    'noise' : [result_emcee.params['noise'].value,result_emcee.params['noise'].stderr]
    }

    sig2s2 = np.percentile(result_emcee.flatchain['sig2'],[2.5, 97.5])
    r0s2 = np.percentile(result_emcee.flatchain['r0'],[2.5, 97.5])
    ms2 = np.percentile(result_emcee.flatchain['m'],[2.5, 97.5])
  #  s0s2 = np.percentile(result_emcee.flatchain['s0'],[2.5, 97.5])
  #  b0s2 = np.percentile(result_emcee.flatchain['noise'],[2.5, 97.5])
    
    sig2s2p = sig2s2[1]-result.params['sig2'].value
    sig2s2m = result.params['sig2'].value-sig2s2[0]
    
    r0s2p = r0s2[1]-result.params['r0'].value
    r0s2m = result.params['r0'].value-r0s2[0]
    
    ms2p = ms2[1]-result.params['m'].value
    ms2m = result.params['m'].value-ms2[0]
    
 #   s0s2p = s0s2[1]-result.params['s0'].value
 #   s0s2m = result.params['s0'].value-s0s2[0]
    
 #   b0s2p = b0s2[1]-result.params['noise'].value
 #   b0s2m = result.params['noise'].value-b0s2[0]

    results_2sig = {
        'sig2': [result.params['sig2'].value,sig2s2p,sig2s2m],
        'r0': [result.params['r0'].value,r0s2p,r0s2m],
        'm' : [result.params['m'].value,ms2p,ms2m],
 #       's0': [result.params['s0'].value,s0s2p,s0s2m],
 #       'noise' : [result.params['noise'].value,b0s2p,b0s2m] 
        
    }
        
    return results_2sig

