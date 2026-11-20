# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:00:14 2025

@author: ZAINTEL2
"""

import numpy as np
from astropy.wcs import WCS

def get_radec_from_map(data_map, pix_arcsec, ra_star, dec_star, scale=3600 ):
    """
    Compute RA/Dec coordinates for a map. It asumes the star is at the center of the observations.

    Parameters
    ----------
    data_map : 2D numpy array
        Full image array (e.g., surface brightness map).
    pix_arcsec : float
        Pixel scale in arcseconds/pixel.
    ra_star : float
        RA of the center pixel in degrees.
    dec_star : float
        Dec of the center pixel in degrees.

    Returns
    -------
    ra : 2D numpy array
        Right Ascension in degrees.
    dec : 2D numpy array
        Declination in degrees.
    """

    x_star = data_map.shape[1] / 2
    y_star = data_map.shape[0] / 2
    
    pixel_scale_deg = pix_arcsec / scale

    w = WCS(naxis=2)
    w.wcs.crpix = [x_star, y_star]
    w.wcs.crval = [ra_star, dec_star]
    w.wcs.cdelt = np.array([-pixel_scale_deg, pixel_scale_deg])
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]

    ny, nx = data_map.shape
    x = np.arange(nx)
    y = np.arange(ny)
    xx, yy = np.meshgrid(x, y)

    ra, dec = w.wcs_pix2world(xx, yy, 0)
    
    return ra, dec, w, x_star, y_star