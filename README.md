# VIENTO
Velocity and Ionization Examination in Nebular Turbulent Observations (*Velocidad e Ionización: Estudios en Nebulosa de la Turbulencia Observada*)

A research initiative to characterize turbulent velocity fields in H II regions using emission-line observations and derived radial-velocity maps using the second-order structure function.

Two pillars:
- Methods and [database](https://github.com/JavGVastro/VIENTO/tree/main/Turbulent%20parameters%20archive) that standardizes turbulent parameters across many regions.
- Follow-up analyses connecting turbulence to region properties (luminosity, size, line-of-sight σ, multi-phase gas, etc.).

Scientific goals:
- Measure, for each region/line/map version:
	- Velocity dispersion (plane-of-sky), $\sigma_\text{POS}$
	- Correlation length, $r_0$
	- Power-law index, $m$
- Our analysis will yield robust correlations between turbulence properties and physical parameters (e.g., luminosity, diameter, and line-of-sight velocity dispersion) of numerous H II regions, as well as insights into the kinematic relationships between different gas phases. These results will refine existing turbulence theories and enhance our understanding of interstellar medium dynamics. 
	- Projection effects and compressibility:
		- $\sigma_\text{POS}$ vs $\rho$
		- $\sigma_\text{POS}$ vs $\sigma_\text{LOS}$
		- $r_0 \ \text{vs} \ \text{Diam}$
	- Theoretical vs observed power law index
	- Velocity dispersion - Luminosity, $\sigma_\text{POS} \ \text{vs} \ I$
- Analyze the [Non-turbulent](<Turbulence ISM/Non Turbulence/Emissivity fluctuations produce POS velocity fluctuations.md>) option for the observed velocity fluctuations.
- Muti-scale studies of inhomogeneous turbulence in star forming regions. Such as the fact that the turbulent intensity in Orion seems to be larger in the center than in the outskirts.
- Compare methods (e.g., structure function vs. power spectrum vs. SCF/VCA/VCS/Δ-variance) and quantify consistency, biases, and uncertainty.

# Project Overview

- The VIENTO project aims to provide a comprehensive study of turbulent velocity fields in H II regions by analyzing high-resolution radial velocity maps obtained from emission-line observations.
- By applying statistical methods—primarily the second-order structure function and a previously developed turbulence model—we systematically measure key turbulent parameters such as velocity dispersion in the plane of the sky, the correlation length (energy injection scale), and the spectral slope characterizing the turbulence.
- The statistical functions are computed using our algorithm in Python and different packages are used to fit the observational results with a theoretical model and obtain the confidence interval. 


# Published papers

- https://ui.adsabs.harvard.edu/abs/2023MNRAS.523.4202G/abstract