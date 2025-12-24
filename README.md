# VIENTO
Velocity and Ionization Examination in Nebular Turbulent Observations (*Velocidad e Ionización: Estudios en Nebulosa de la Turbulencia Observada*)

A research initiative (IRyA-UNAM / Mexico) to characterize [turbulent](<Turbulence ISM/Turbulence.md>) velocity fields in [H II regions](<H II regions/README.md>) using emission-line observations and derived radial-velocity maps using the second-order structure function. We systematically measure key turbulent parameters such as velocity dispersion in the plane of the sky, the correlation length (energy injection scale), and the spectral slope characterizing the turbulence.

Two pillars:
- [Numerical methods](<Turbulence Statistics/README.md>) and [archive](<Turbulent archive/README.md>) that standardizes turbulent parameters across many regions.
	- Using the [VIENTO pipeline](pipeline_VIENTO/README.md) we compute the structure function, fit a model and recover the turbulent parameters with their confidence intervals using Bayesian statistics.
- Follow-up analyses connecting [turbulence to H II region properties](<Turbulence ISM/Turbulence in H II regions.md>) (luminosity, size, line-of-sight σ, multi-phase gas, etc.).

Scientific goals:
- Measure, for each region/line/map version the following **turbulent parameters**:
	- Velocity dispersion (plane-of-sky), $\sigma_\text{POS}$
	- [Correlation length](<Turbulence ISM/Correlation length in H II Regions>), $r_0$
	- [Power-law index](<Turbulence ISM/Power law slope in H II regions.md>), $m$
- Our analysis will yield robust correlations between turbulence properties and physical parameters (e.g., luminosity, diameter, and line-of-sight velocity dispersion) of numerous H II regions.
	- [Projection effects](<Turbulence ISM/Projection smearing.md>) and compressibility:
		- $\sigma_\text{POS}$ vs $\sigma \rho$ [1](<Turbulence ISM/Compressibility in H II regions.md>)
		- $\sigma_\text{POS}$ vs $\sigma_\text{LOS}$
		- $r_0 \ \text{vs} \ \text{Diam}$
	- Theoretical vs observed power law index
	- Velocity dispersion - Luminosity, $\sigma_\text{POS} \ \text{vs} \ I$
- Analyze the [Non-turbulent](<Turbulence ISM/Non Turbulence/Emissivity fluctuations produce POS velocity fluctuations.md>) option for the observed velocity fluctuations.
- [Fake maps experiments](<fake_maps/README.md>).
---
- Muti-scale studies of inhomogeneous turbulence in star forming regions. Such as the fact that the turbulent intensity in Orion seems to be larger in the center than in the outskirts.
- Gas and stars kinematics. Insights into the kinematic relationships between different gas phases. 
- Compare methods (e.g., structure function vs. power spectrum vs. SCF/VCA/VCS/Δ-variance) and quantify consistency, biases, and uncertainty.

# Published papers

- https://ui.adsabs.harvard.edu/abs/2023MNRAS.523.4202G/abstract