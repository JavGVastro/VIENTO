
# To-Do

- [ ] Integrate $B(r)$ table with .fits file (now it exported as an numpy array into a .json file)
- [ ] Elaborate on Papermill on make_file inject parameters and run stuff
# 1. Purpose and Scope

The VIENTO pipeline aims to provide a reproducible, modular workflow to:

- Compute the observational second-order structure function of the velocity field of an H II region from astronomical observations (typically in [FITS](https://docs.astropy.org/en/stable/io/fits/index.html) format).
- Fit a parametric model to the observational structure function:
  - Either a 5-parameter “proposed” model, or
  - A 3-parameter “ideal” model.
- Estimate confidence intervals for all fitted parameters.
- Produce:
  - Publication-quality plots of the velocity field.
  - Diagnostic and final plots of the structure function and fitted model(s).
  - Corner plots of the model parameter posteriors.
  - Machine-readable files containing the structure function and parameter estimates.

This document describes the current state of the pipeline, including the main stages, notebooks, custom modules, inputs/outputs, and a preliminary to-do list for the first upload to Git.

---

# 2. High-Level Workflow

At a high level, the pipeline takes as input a velocity field (optionally accompanied by a surface brightness/emission map for weighting) and produces:

- A structure function B(r) (possibly weighted).
- Best-fit parameters for a chosen model (3- or 5-parameter).
- Confidence intervals for each parameter.
- Plots:
  - Velocity field.
  - Observational structure function with fitted model(s) and confidence intervals.
  - Corner plot of the parameter posteriors.
- A results file summarizing all relevant numerical outputs.

The pipeline is currently organized into three stages, each associated with a Jupyter notebook:

1. Stage 1: Raw FITS → pipeline-ready velocity map FITS, with complete header metadata.
2. Stage 2: Structure function computation and model fitting (including MCMC).
3. Stage 3: Results compilation and visualization (plots, parameter summaries).

The medium-term goal is to minimize interactive steps and run as much as possible through Python scripts orchestrated by a single Makefile, while retaining Jupyter notebooks only where interactive inspection is essential.

---

# 3. Stage 1 – Velocity Map Preparation

## 3.1 Objective

Convert reduced observational FITS data into a pipeline-ready velocity map FITS file, with:

- A clean velocity field (after masking outliers, dead pixels, bad regions).
- A rich FITS header containing all metadata needed for subsequent stages.

## 3.2 Current Implementation

- Implemented in a Jupyter notebook (Stage 1 notebook).
- Used interactively to:
  - Load reduced observational FITS files (from the instrument reduction pipeline).
  - Inspect and correct:
    - Dead pixels.
    - Outliers.
    - Bad regions or artifacts.
  - Define and apply masks where necessary.
  - Extract or compute:
    - The velocity field.
    - Any additional map(s) (e.g. surface brightness/emission) that may later be used as weights.

## 3.3 Metadata in the Pipeline-Ready FITS Header

The pipeline-ready FITS file contains the velocity map in the data array and several key header entries, for example:

- AUTHOR: file creator.
- m2D: exponent parameter related to the 2D structure function slope (k = 2D + m2D).
- ra: artificial correlation length.
- sig: standard deviation of the artificial map.
- sig2: variance of the artificial map.
- s0: atmospheric seeing.
- noise: instrumental noise.
- box_size: observational box size.
- pc: parsec conversion (physical scale).
- pix: pixel scale of the instrument.
- LINE: emission line name (e.g. H_I-6563).
- BINSIZE: spatial binning factor (0 for native resolution, 2, 4, 8, etc. for binned maps).

Notes:

- These values are intended to be carried throughout the entire pipeline, particularly into the structure function and fitting stages.
- Some keys (e.g. m2D, ra, sig, noise) may be specific to artificial or test maps, but the mechanism is the same for observational data.
- LINE specifies the emission line (e.g. H_I-6563).
- BINSIZE indicates the spatial binning factor.

## 3.4 Output of Stage 1

- A FITS file containing:
  - The velocity field in the data array.
  - All required metadata in the header.

This file is referred to as the pipeline-ready velocity map FITS and is the standard input for Stage 2.

---

# 4. Stage 2 – Structure Function and Model Fitting

## 4.1 Objective

From the pipeline-ready velocity map FITS, compute the observational structure function and perform model fitting and confidence interval estimation.

## 4.2 Current Implementation: `pipeline_computations` Notebook

Stage 2 is implemented in a Jupyter notebook named `pipeline_computations`. The notebook is designed so that, once the user specifies the name of the pipeline-ready FITS file, the rest of the process runs automatically as far as possible.

#### 4.2.1 Input Handling

- The notebook takes as input the FITS filename (without requiring manual re-entry of metadata).
- Tasks:
  - Load the FITS image (velocity field).
  - Read and organize header information.

To-do: implement a dedicated helper function in a user module (for example, `load_velocity_map_and_header`) to centralize this logic.

#### 4.2.2 Structure Function Computation

- The observational structure function is computed using a custom library (referred to here as `strucfunc`).
  - This library is envisioned to be a separate project or module.
  - It should support:
    - Unweighted structure functions.
    - Weighted structure functions when a surface brightness/emission map is available.

- The results (e.g. lag distances, structure function values, uncertainties) are exported to a JSON file.

Potential improvement: replace or complement the JSON output with a FITS table extension that stores the structure function results and is linked directly to the original velocity map FITS.

#### 4.2.3 Model Fitting and Confidence Intervals

- A user function (for example, `fit_structure_function`) is called to:
  - Read the structure function data from the JSON file.
  - Choose the model:
    - 3-parameter ideal model, or
    - 5-parameter proposed model.
  - Perform the parametric fit using the `bfunc` module and `lmfit`:
    - `bfunc` contains the mathematical forms of all supported structure function models.
    - `lmfit` is used for nonlinear least-squares fitting and for defining parameter bounds and constraints.
  - Run MCMC (emcee) via `lmfit` to estimate posterior distributions and confidence intervals.

- The fitting stage produces:
  - A standard `lmfit.ModelResult` object for the deterministic fit.
  - A MCMC result for the parameter posteriors.

Both results are saved using a utility such as `save_modelresult` (or equivalent).

#### 4.2.4 Outputs of Stage 2

From a single pipeline-ready velocity map FITS, Stage 2 produces:

- A JSON file with the structure function B(r) and related information.
- One or more saved `lmfit` result files:
  - Deterministic fit result.
  - MCMC (emcee) result.

## 4.3 Notes and To-Dos for Stage 2

- Fitting procedure improvements:
  - Tuning of priors, number of walkers, burn-in length, and chain length for MCMC.
  - Assessment of parameter degeneracies and robust error estimation.
- Alternative storage:
  - Evaluate using FITS tables instead of (or in addition to) JSON for B(r) and associated quantities.
- Weighted structure function:
  - Formalize how a surface brightness or emission map is used as a weight in the structure function computation and document the required inputs.

## Fit and confidence interval details

### Prior

| Parameter          | Lower                         | Upper                      |
| ------------------ | ----------------------------- | -------------------------- |
| $\sigma^2$         | $0.25$ max $[B_{\text{obs}}]$ | $2$ max $[B_{\text{obs}}]$ |
| $r_0$              | $0.01 L$                      | $2 L$                      |
| $m$                | $0.5$                         | $2.0$                      |
| $s_0$              | $0.1$ arcsec                  | $1.5$ arcsec               |
| $B_{\text{noise}}$ | $0$                           | $3$ min $[B_{\text{obs}}]$ |
|                    |                               |                            |
**Note**: max $[B_{\text{obs}}]$ and min $[B_{\text{obs}}]$ are over all bins in the observed structure function with $r < L/2$.
**Note**: Mayores incertidumbres a los primeros puntos (antes de la relación lineal)
# 5. Stage 3 – Results Compilation and Visualization

## 5.1 Objective

Collect all products from previous stages and generate:

- Publication-quality velocity field plots.
- Diagnostic and final structure function plots, including:
  - Observational data.
  - Overplotted model(s).
  - Confidence interval bands.
- Corner plots of the parameter posteriors.
- A compact numerical summary of best-fit parameters and errors.

## 5.2 Current Implementation: `pipeline_results_compiling` Notebook

Stage 3 is implemented in a Jupyter notebook named `pipeline_results_compiling`.

#### 5.2.1 Loading Data and Metadata

The notebook loads:

- The pipeline-ready velocity map FITS to recover both the data and header metadata.
- The structure function JSON file produced in Stage 2.
- The saved `lmfit` fit and MCMC result files.

To-do: implement a user function to load the velocity field and all relevant properties from the FITS file in a single call, returning a structured object or dictionary.

#### 5.2.2 Velocity Field Plot

From the FITS data and header, the notebook creates a paper-ready plot of the velocity field:

- Axes in physical units (e.g. parsecs).
- Proper labels, colorbar, and units.
- Orientation, scale bars, and any required annotations.

This figure is intended to be close to publication quality, with only minor cosmetic refinements needed later.

#### 5.2.3 Structure Function Visualization (Diagnostic)

- Load the structure function from the JSON file and convert it into an array or structured object.

To-do: clarify and standardize the array structure (for example, columns for radius, B(r), uncertainties, mask flags, etc.).

- Plot:
  - The observational structure function.
  - The ideal and proposed models, using “ideal” or reference values for comparison.

These plots are currently diagnostic, not final publication figures, but are scientifically informative.

#### 5.2.4 Fit and Confidence Interval Compilation

- Load the fit and MCMC results from the saved `lmfit` files.
- Apply the user function `ci_results_compiler` to:
  - Extract model parameters (either 3 or 5) from the MCMC output.
  - Construct a dictionary where each parameter has a list with three elements:
    1. Best-fit value.
    2. Positive error.
    3. Negative error.

This dictionary serves as the central numerical summary of the fit and its uncertainties.

#### 5.2.5 Final Plots: Corner Plot and SF with Confidence Intervals

- Use the `bplot` Python module to:
  - Generate a corner plot from the MCMC chains.
  - Plot the structure function with:
    - The best-fit model curve.
    - Confidence interval bands around the model.

Current status:

- `bplot` is fully functional for the 5-parameter model.
- There is no current support for the 3-parameter model within `bplot`.

Planned action:

- Request an update from Dr. Will to extend `bplot` to handle the 3-parameter model, as this would be time-consuming to implement independently.

#### 5.2.6 Outputs of Stage 3

From the inputs of Stages 1 and 2, Stage 3 produces:

- Publication-ready velocity field plot.
- Diagnostic structure function plot with ideal/proposed models.
- Final structure function plus confidence interval plot.
- Corner plot of the model parameters.
- A dictionary summarizing best-fit parameters and asymmetric errors.

---

# 6. Data Flow and File Types

## 6.1 Main Data Flow

1. Raw reduced FITS (instrument output)  
   ↓ Stage 1  
2. Pipeline-ready velocity map FITS (velocity field plus metadata in header)  
   ↓ Stage 2  
3. Structure function JSON plus `lmfit` fit files (deterministic plus MCMC)  
   ↓ Stage 3  
4. Plots (velocity field, SF with fit and CI, corner plot) plus parameter dictionary

## 6.2 File Types

- FITS:
  - Raw reduced observations.
  - Pipeline-ready velocity maps (with extended metadata).
- JSON:
  - Structure function results B(r).
- Model result files:
  - Saved `lmfit.ModelResult` (format to be standardized; for example, pickle, JSON, or custom).
  - Saved MCMC results.
- Plots:
  - Static image files (for example, PNG, PDF) in a `figures/` directory.
- Python:
  - Custom modules for structure function (`strucfunc`), models (`bfunc`), plotting (`bplot`), and utilities.

---

# 7. Custom Python Modules (Current and Planned)

## 7.1 `strucfunc` (Structure Function Library)

Purpose:

- Compute observational structure functions from velocity maps.

Status:

- Conceptually defined; intended as a separate module or project.

To-do:

- Finalize the API for:
  - Unweighted structure functions.
  - Weighted structure functions using brightness/emission.

## 7.2 `bfunc` (Structure Function Models)

Purpose:

- Provide analytic structure function models, including:
  - 3-parameter ideal model.
  - 5-parameter proposed model.
  - Potential additional models.

Usage:

- Called by `fit_structure_function` in Stage 2 via `lmfit`.

## 7.3 `bplot` (Plotting Utilities)

Purpose:

- Create:
  - Corner plots for MCMC results.
  - Structure function plots with model fits and confidence band overlays.

Status:

- Currently implemented for the 5-parameter model.

To-do:

- Extend to support the 3-parameter model.

## 7.4 Utility Functions (Planned)

Suggested utility functions to centralize repeated tasks:

- `load_velocity_map_and_header(fits_filename)`  
  Load velocity data and relevant header information into a dictionary or small object.

- `load_structure_function(json_filename)`  
  Load structure function results into a well-defined array or structured object.

- `fit_structure_function(sf_data, model_type="5p" or "3p")`  
  Wrapper that calls `bfunc`, performs `lmfit` fitting and MCMC, and saves results.

- `ci_results_compiler(lmfit_result, mcmc_result)`  
  Build the parameter dictionary with best values and asymmetric errors.

---

# 8. External Dependencies (Preliminary)

A non-exhaustive list of external Python packages used or planned:

- Numerical and scientific computing:
  - numpy
  - scipy
- Astronomical I/O and FITS handling:
  - astropy.io.fits
  - possibly astropy.wcs for coordinate handling
- Fitting and statistics:
  - lmfit
  - emcee (via lmfit for MCMC)
- Visualization:
  - matplotlib
- Data serialization:
  - json
  - possibly pickle (if used for model results)

These dependencies should be consolidated later into a `requirements.txt` or `environment.yml`.

---

# 9. Project Folder Structure (Current Working Model)

```
- pipeline_VIENTO (Folder outline, general)
	- fits_ready (.fits files ready for observations. NOTE: Matrix/Scatter, SB True/False, ideal True/False)
	- results_fit
	- results_Br
	- py_modules
	- Imgs
	- computations.ipynb (run using Make_file or all samples)
	- res_compilation.ipynb (Manual)  
```


The precise structure will be refined, but the pipeline currently assumes or is compatible with a layout similar to:

- `observations/`  
  Raw and reduced FITS files from the instrument.

- `velocity_fields_maps/`  
  Pipeline-ready velocity map FITS files (Stage 1 outputs).

- `structure_function/`  
  JSON files or FITS tables containing structure function results (Stage 2 outputs).

- `confidence_intervals/`  
  Saved `lmfit` deterministic and MCMC results, and possibly compiled CI dictionaries.

- `results_files/`  
  Aggregated results, summary tables, and master files combining multiple runs.

- `figures/`  
  Plots produced in Stage 3 (velocity fields, SF plots, corner plots).

- `py_modules/`  
  Custom Python modules:
  - `strucfunc`, `bfunc`, `bplot`, and utility modules.

- `notebooks/`
  Jupyter notebooks:
  - Stage 1 preparation notebook.
  - `pipeline_computations` (Stage 2).
  - `pipeline_results_compiling` (Stage 3).

This layout will be adjusted and formalized as part of the first stable Git version.

## Folder structure Fake Maps Experiments

```
- pipeline_fake (Fake Maps Experiments)
	- fits_ready (Fits files ready for the pipeline and .txt files with names of all files) 
		  Fake maps batch test: (Matrix, SB: True, ideal: True)
	- Imgs
	- py_modules
	- results_fit
	- results_Br
	- pipeline_computations.ipynb (run using Make_file or all samples)
	- pipeline_results_compiling.ipynb (Manual)  
	- pipeline_config.py (Pahts and folders for the current runt) - TO MODIFY INITIALLY!!
```

# 10. Known Limitations and To-Do List

## 10.1 Jupyter vs. Scripted Pipeline

Current state:

- Stages 1–3 rely heavily on Jupyter notebooks.

Goal:

- Implement a single Makefile that orchestrates the entire pipeline via Python scripts, with notebooks reserved for data exploration and ad-hoc diagnostics.

To-do:

- Extract core logic from notebooks into modules and scripts.
- Define clear command-line interfaces for each stage.

## 10.2 Structure Function Library (`strucfunc`)

To-do:

- Stabilize the API.
- Implement weighted structure function computation.
- Document all assumptions and units.

## 10.3 Model Fitting and Confidence Intervals

To-do:

- Optimize MCMC settings (walkers, steps, burn-in).
- Conduct convergence diagnostics.
- Standardize the storage format of `lmfit` and MCMC outputs.
- Clarify the choice of priors and bounds for each parameter.

## 10.4 Plotting (`bplot`)

To-do:

- Extend to support the 3-parameter model.
- Uniform style and formatting for:
  - Velocity field plots.
  - SF plus CI plots.
  - Corner plots.
- Ensure plots are easily reusable in LaTeX manuscripts.

## 10.5 Data Formats and Metadata

To-do:

- Decide whether to:
  - Use JSON only, or
  - Introduce FITS table extensions for structure functions and CI results.
- Ensure that all critical metadata (for example, line name, binning, physical scale) is:
  - Carried consistently from Stage 1 to Stage 3.
  - Documented in the FITS header and/or separate configuration files.

## 10.6 Multi-Run and Multi-Region Comparison

Future work:

- Extend the pipeline to handle:
  - Multiple velocity maps (different regions or lines).
  - Systematic comparison of structure function parameters across runs.
- Create higher-level scripts to:
  - Aggregate results.
  - Produce summary plots and tables.

---

# 11. Summary

The VIENTO pipeline currently consists of three main stages:

1. Preparation of a pipeline-ready velocity map FITS with all necessary metadata in the header.
2. Computation of the observational structure function, followed by model fitting (3- or 5-parameter) and MCMC-based confidence interval estimation.
3. Compilation of results and generation of plots, including:
   - Paper-ready velocity field images.
   - Structure function plots with model fits and confidence intervals.
   - Corner plots of parameter posteriors.
   - A numerical summary of best-fit parameters and their errors.

The immediate next steps are to:

- Consolidate the core logic into reusable Python modules.
- Introduce a Makefile-driven scripted workflow.
- Finalize data formats and plotting tools.
- Prepare the codebase and documentation for a clean and coherent first upload to Git.

This document serves as the initial reference for the repository and will be refined as the pipeline evolves.
