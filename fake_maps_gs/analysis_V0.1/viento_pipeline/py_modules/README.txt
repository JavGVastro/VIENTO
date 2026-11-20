# py_modules

The `py_modules` directory contains all custom Python modules developed for this project. These modules include functions and classes written either by myself or kindly provided by Dr. Will Henney, and they encapsulate specific routines used throughout the data import, processing, export, and analysis steps.

- **astronomical_instruments**: Classes and metadata for observational instruments used in the project, including properties such as telescope, site, wavelength coverage, spectral resolution, and observational modes.
- **astronomical_objects**: Classes and metadata for astronomical objects and regions analyzed in the project, including catalog/common names, distances, and points of interest.
- **astrometry_utils**: Computes RA/Dec coordinates for a particular map using a reference star. It assumes that the star is at the center of the observations.
- **bfunc**: Structure function theoretical models.
- **bplot**: Plotting routines for the paper.
- **logerr**: Computation of the error (uncertainty) for logarithmic values.
- **rebin_utils**: `Tetrablock` downsampling and oversampling package.
- **region_observations_props**: General metadata and helper utilities related to H II region observations.
- **results**: TBD
- **spectral_lines**: Classes and metadata for spectral lines used in the analysis, including plot labels, rest wavelengths, elements, ions, and transition identifiers.
- **stars_wcs**: TBD
- **strucfunc**: Dr. Will Henney’s structure function code.
- **turb_utils**: Lightly edited versions of functions from `turbustat.simulator` to generate fields that are uncorrelated at large scales.
