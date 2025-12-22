
- [Turbustat VCA](https://turbustat.readthedocs.io/en/latest/tutorials/statistics/vca_example.html#vca-tutorial)
- **Velocity Channel Analysis (VCA)** investigates how the spatial power spectrum of intensity fluctuations in a spectral cube varies with the thickness of the velocity slices. This method distinguishes between the contributions of velocity and density fluctuations to the observed emission. A major advantage of a spectral-line data cube, rather than an integrated two-dimensional image, is that it captures aspects of both the density and velocity fluctuations in the field of observation ([Turbustat VCA](https://turbustat.readthedocs.io/en/latest/tutorials/statistics/vca_example.html#vca-tutorial)). 
	- [Lazarian & Pogosyan 2000](https://ui.adsabs.harvard.edu/#abs/2000ApJ...537..720L/abstract) and [Lazarian & Pogosyan 2004](https://ui.adsabs.harvard.edu/#abs/2004ApJ...616..943L/abstract) derived how the power spectrum from a cube depends on the statistics of the density and velocity fields for the 21-cm Hydrogen line, allowing for each of their properties to be examined (provided the data have sufficient spectral resolution). 
	- The Lazarian & Pogosyan theory predicts two regimes based on the the power-spectrum slope: the *shallow* ($n < -3$) and the *steep* ($n > -3$) regimes. In the case of optically thick line emission, [Lazarian & Pogosyan 2004](https://ui.adsabs.harvard.edu/#abs/2004ApJ...616..943L/abstract) show that the slope saturates to (see [Burkhart et al. 2013](https://ui.adsabs.harvard.edu/#abs/2013ApJ...771..123B/abstract) as well). The VCA predictions in these different regimes are shown in Table 1 of [Chepurnov & Lazarian 2009](https://ui.adsabs.harvard.edu/#abs/2009ApJ...693.1074C/abstract) (also see Table 3 in [Lazarian 2009](https://ui.adsabs.harvard.edu/#abs/2009SSRv..143..357L/abstract)). The complementary [Velocity Coordinate Spectrum](https://turbustat.readthedocs.io/en/latest/tutorials/statistics/vca_example.html#vca-tutorial) can be used in tandem with VCA.
- **Velocity Channel Analysis (VCA)** consists of taking the spatial power spectrum of the emission intensity (or brightness) in velocity channels of spectroscopic PV data. First, the PV data re binned into velocity channels of width $\delta v .$ The relative contribution of velocity fluctuations to fluctuations in the total intensity decreases as the width of the velocity slices increases, because thicker velocity slices averages our the contribution of many velocity fluctuations. The bery thickest velocity slice gives information only on the density spectral index. A velocity slice has a width $\delta v = (v_\text{max} - v_\text{min})/N$, where $N$ is the number of channels ([[Arthur et al. 2016]]). 
## Theoretical Background

Given a spectral cube $I(x,y,v)$, VCA studies the 2D spatial power spectrum $P(k)$ of velocity channel maps. The slope of the power spectrum depends on whether the velocity slice is thin or thick:

- For **thin** velocity slices:

$$\beta_{\text{thin}} \approx \beta_n + \frac{\beta_v - 3}{2}$$

- For **thick** velocity slices:

$$\beta_{\text{thick}} \approx \beta_n$$


### Application

By measuring how the power spectrum slope changes with velocity slice thickness, VCA provides constraints on both the density and velocity structure of the turbulent medium.