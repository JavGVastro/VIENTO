- Here we explore the current state of the synthetic maps (a.k.a. fake maps) created using the turbustat package. 
- We review how they are created, which modifications are made to the original code and  analyze the results of the structure function and the process of recovering of turbulent parameters through the fit.
- We take as a starting point what was done in my phd, and our goal to develop more accurate ways to represent real observations through the synthetic maps with the end to use them as our laboratory.
- [ ] Finish current state of the art of our modifications (phd stuff, no-small / large-effects)
- [ ] Upload Fake maps to Git
- [ ] Add Git link
- [ ] noise
- [ ] seeing
- [ ] finite box effects



- Dr. Will's original Jupyter file from PhD [repository](https://github.com/JavGVastro/PhD.Paper/blob/main/Fake-Maps/fake-maps-seeing.ipynb):
- The modification is done to the function `make_extended`[1](https://turbustat.readthedocs.io/en/latest/api/turbustat.simulator.make_extended.html#turbustat.simulator.make_extended) and `make_3dfield`[2](https://turbustat.readthedocs.io/en/latest/api/turbustat.simulator.make_3dfield.html#make-3dfield) adding to the code that the curve follows the behavior of: $$e^{-\dfrac{1}{2 \pi k r_0}} .$$
- The modification add a tapered behavior to the structure function so the *original code* and results would be referred as **non-tapered**.

# Power law law's

``` python
# Physical parameters
m_obs = 1.0    # The projected slope of the structure function we measure
m2D   = 0.85   # for recovering m as 1.00 in the projected field (k = 2D + m2D) non emissivity fluctuation case
m3D_1 = 0.30   # for recovering m as 1.00 in the projected field (k = 3D + m3D) light fluctuations
m3D_2 = 0.55   # for recovering m as 1.00 in the projected field (k = 3D + m3D) heavy fluctuations
```
# 2D case
## Modification

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
