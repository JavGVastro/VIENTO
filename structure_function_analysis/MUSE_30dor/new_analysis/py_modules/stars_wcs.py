# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:00:14 2025

@author: ZAINTEL2
"""

from astropy.wcs import WCS

x_star = sb.shape[1]/2
y_star = sb.shape[0]/2

pixel_scale_deg = pix / 3600

w = WCS(naxis=2)

w.wcs.crpix = [x_star, y_star]
w.wcs.crval = [83.8187500 , -5.3897222]  # RA and Dec in degrees
w.wcs.cdelt = np.array([pixel_scale_deg, pixel_scale_deg])
w.wcs.ctype = ["RA---TAN", "DEC--TAN"]

ny, nx = sb[trim].shape
x = np.arange(nx)
y = np.arange(ny)
xx, yy = np.meshgrid(x, y)
ra, dec = w.wcs_pix2world(xx, yy, 0)