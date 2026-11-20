# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 16:39:45 2025

@author: ZAINTEL2
"""

import numpy as np

# Region properties: INPUT
distance   = 410                              # Distance to object [parsecs]
ra_star    = 83.818750                        # Right ascenscion reference star
dec_star   = -5.3897222                       # Declination reference star
name_star = r'$\theta^1$ Ori C'

# Observations properties: INPUT
seeing      = 0.9                              # FWHM seeing [arcsec] 
pixel_scale = 0.2                              # Spatial scale of the instrument [arcsec per pixel]

# Conversions to parsecs
pc = distance * (2 * np.pi) / (360 * 60 * 60)  # arcsec to parsecs [parsecs]
s0 = (seeing * pc) / 2.355                     # RMS seeing [parsecs]
   