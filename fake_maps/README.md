- The objective is to develop a more accurate way to represent real observations, from our perspective, through synthetic maps with the end to use them as our laboratory.
- Here we explore the current state of the synthetic maps (a.k.a. fake maps) created using the [Turbustat](https://turbustat.readthedocs.io/en/latest/index.html) Python package. 
- We review our initial modification for the [[#2D-case mod|2D-case]] and 3D-case to:
	- `make_extended`[1](https://turbustat.readthedocs.io/en/latest/api/turbustat.simulator.make_extended.html#turbustat.simulator.make_extended) and
	- `make_3dfield`[2](https://turbustat.readthedocs.io/en/latest/api/turbustat.simulator.make_3dfield.html#make-3dfield)
- The modification add a tapered behavior to the structure function through adding the parameter ~~`r0`~~ `r_a`, so the *original code* and results would be referred as **non-tapered**.The correlation length used as input for the synthetic map is called **artificial correlation length**, $r_a :$
 $$e^{-\dfrac{1}{2 \pi k r_a}} .$$

- Do not confuse with $r_0$ which is the correlation length recovered through the fit.
- For the fake maps experiments:
	- I decided to only work with the 3D case using sigE = 0,1,2 cases, eliminating the need of working with 2D maps.
	- Since cubes are used a lot of kb for storage, the [moment0 and moment1](https://spectral-cube.readthedocs.io/en/latest/api/spectral_cube.SpectralCube.html#spectral_cube.SpectralCube.moment) are going to be exported to a fits file with all the parameters in the header. (see pipeline X).
	- In the phd we didn't elaborate on analyzing the fitting and the recovers parameters of the synthetic structure functions. So as first approach we elaborate on that.
- Creating 3D cubes must take into consideration the fluctuations in the emissivity field and the velocity field.
	- Constant density (emissivity fluctuations, $\sigma_E = 0$)
	- Low density fluctuations (emissivity fluctuations, $\sigma_E = 1$)
	- High density fluctuations (emissivity fluctuations, $\sigma_E = 2$)
- Experiments with fake maps
	- vary m, ra, etc.
	- Seeing effect
	- Box size effect
	- Noise effect
	- Binning
- PhD repository biblio
	- Dr. Will's original [Jupyter file](https://github.com/JavGVastro/PhD.Paper/blob/main/Fake-Maps/fake-maps-seeing.ipynb) with the first comment about the mod from PhD  repository.
	- [Fake maps to illustrate different features of structure function](https://github.com/JavGVastro/PhD.Paper/blob/main/Fake-Maps/fake-maps-complete.ipynb)
	- [Effects of the finite map size](https://github.com/JavGVastro/PhD.Paper/blob/main/Fake-Maps/fake-maps-finite.ipynb)
	- [Fake maps with fake seeing](https://github.com/JavGVastro/PhD.Paper/blob/main/Fake-Maps/fake-maps-seeing.ipynb)
# To-Do

- [ ] Redo in the new pipeline/project (phd stuff, seeing, large-effects)
	- [!] Emissivity fluctuations (review the way I originally compute them since I think is wrong - create issue)
	- [ ] seeing
	- [ ] finite box effects
- [x] Add Discussion to Git: State of the art ✅ 2025-12-16
- [ ] Poisson Noise
- [ ] Add init and experimental notebook version

# Power law law's for fake maps

- Since fake maps are created using the spectral exponent $\kappa$ it is necessary to consider all the necessary stuff to recover the slope of the structure function $m$.

From: https://github.com/JavGVastro/PhD.Paper/issues/18

As suggestion from somewhere, the power spectra is in terms of numbers of dimensions (ND) and the N-dimensional slope structure function.

$$\kappa = \text{ND} + m_\text{ND}$$

``` python
# Physical parameters
m_obs = 1.0    # The projected slope of the structure function we measure
m2D   = 0.85   # for recovering m as 1.00 in the projected field (k = 2 + m2D) non emissivity fluctuation case
m3D   = 0   # for recovering m as 1.00 in the projected field (k = 3 + m3D) non emissivity fluctuation case
m3D = 0.30   # for recovering m as 1.00 in the projected field (k = 3 + m3D) light fluctuations
m3D = 0.55   # for recovering m as 1.00 in the projected field (k = 3 + m3D) heavy fluctuations
```

# 2D-case mod 

``` python
    if ellip < 1:
        # Apply a rotation and scale the x-axis (ellip).
        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        xprime = ellip * (xx * costheta - yy * sintheta)
        yprime = xx * sintheta + yy * costheta

        rr2 = xprime ** 2 + yprime ** 2

        rr = rr2 ** 0.5
        # Also save circular version to use with correlation_length <-----------
        rcirc = np.hypot(xx, yy)   <-----------
        rcirc[rcirc == 0.0] = np.nan  <-----------
    else:
        # Circular whenever ellip == 1
        rr = (xx ** 2 + yy ** 2) ** 0.5

    # flag out the bad point to avoid warnings
    rr[rr == 0] = np.nan

    if correlation_length is not None:     <-----------
        # Taper the power spectrum at large separations (low spatial   <-----------
        # frequencies) so that the field is uncorrelated at the <-----------
        # largest scales. <-----------
        #
        # rcirc is spatial frequency: 1 / r, measured in pixels <-----------
        output *= np.exp(-1.0 / (2 * np.pi * rcirc * correlation_length)) <-----------
```

# 3D-case mod 

#TBD