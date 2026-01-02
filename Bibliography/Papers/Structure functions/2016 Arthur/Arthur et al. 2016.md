---
Priority: 
Status: 
Area: 
Subject: 
Notes: 
tags:
  - Structure_Function
Complete: 
url: https://ui.adsabs.harvard.edu/abs/2016MNRAS.463.2864A/abstract
Title: Turbulence in the ionized gas of the Orion nebula
Action: 
Journal: 
Authors: 
Topic: Structure Function
Data: 
Class: Article
Observations: true
Project: true
---


# Abstract

- Study of velocity fluctuations in [[M 42]] applying statistical techniques to observed cubes.
- The cubes are derived from high resolving power longlist spectroscopy.
- From VCA they found that observations match Kolmogorov from $8$ to $22 \text{ arcsec}$ or $0.02 - 0.05 \text{ pc}$.
- Outer scale which is the dominant scale fo density fluctuations in the nebula approximately coincides with the autocorrelation length. *It is propose that this is the principal driving scale of the turbulence, which originates in the dense cores of the Orion molecular filament.*
- non-thermal linewidths with trends of velocity centroid versus ionization contribute in equal measure to the total velocity dispersion.
- The turbulence is subsonic and can can account for only one half to the derived variance in ionized density, with the remaining variance provided by density gradients in photoevaporation flows form globules and filaments.
- Intercomparison with results from simulations implies that the ionized gas is confined to thick shell and does not fill the interior of the nebula.

# 1 Introduction

- Complex velocity structure in H II regions: Studies reveal that spectral lines are broadened beyond thermal broadening, indicating disordered motion in the gas, even after accounting for systematic motions like expansion and rotation.
- Turbulence in photoionized gas: The remaining random velocity component is attributed to turbulence, analyzed through statistical methods in both Galactic and extragalactic H II regions, focusing on point-to-point radial velocity variations with scale.
- Structure functions of velocity centroids have become a standard statistical tool since von [[von Hoerner 1951]] investigated the projection of a three-dimensional correlation function on to the plane of the sky. **They mesure the variation of the mean velocity integrated along the line-of-sight as a function of the plane-of-sky separation**.
- This can be realized by multiple **high-velocity-resolution longlist spectroscopic** observation of an optically thin emission line at a variety of position across an H II region or by **Fabry-Perot interferometry**, which has much lower velocity resolution.
- Observationally [[M 42]] fill the requirements of high velocity resolution with high spatial resolution, and its kinematic features and stellar population are well known. The inner part of the nebula measures some $3 \times 5 \text{ arcmin}^2$ and is bright in optical emission lines. The principal ionizing star is $\theta^1 \text{ Ori C}$ (spectra type $\sim \text{O}7$), which also posses a fast stellar wind, and there are also 3 B-type stars. The early stars are the Trapezium cluster. M42 is a site of ongoing star formation on the nearside of the Orion Molecular Cloud (OMC-1) and there is a large population of young stars, some of which are the sources of stellar jets and Herbig-Haro objects and some proplyds. M 42 is an example of a blister H II region and the photoionized gas is streaming away from the background molecular cloud with a blueshifted velocities of the order of $10 \text{ km/s} .$
- VCA vs structure function

# 2 Methods

## 2.1 Observational data

- The total observed area is from 5ʰ35ᵐ10ˢ.4 to 5ʰ35ᵐ23ˢ.2 in right ascension and from −5°21′36″ to −5°26′10″ in declination. The position of θ¹ Ori C is R.A. 5ʰ35ᵐ16ˢ.5 Dec. −5°23′23″ (J2000). [[M 42 observations.png|1]]
- The spectral line data were presented in the emission line atlas of García-Díaz et al. (2008). 
- In this paper, we use the Hα, \[S II\] 6716, 6731 Å, \[N II\] 6583 Å and \[O III\] 5007 Å data obtained with the echelle spectrograph attached to the 4 m telescope at Kitt Peak National Observatory ([[KPNO]]; for observational details see Doi, O’Dell & Hartigan 2004), with supplementary \[S II\] data observed with the Manchester Echelle Spectrometer attached to the 2.1 m telescope at the Observatorio Astronómico Nacional at San Pedro Mártir ([[OAN]]-SPM), Mexico. 
- The data cover the 3 × 5 arcmin² [[Arthur 2016 KPNO M42 S.png|central (Huygens) region of the Orion nebula]]  and the Hα, \[N II\] and \[O III\] data consist of 96 approximately 300 arcsec North–South orientated slits at 2 arcsec intervals, where the slit width corresponds to 0.8 arcsec. The velocity resolution of these observations is 8 km s⁻¹. 
- The \[S II\] 6716, 6731 Å data set has a total of 92 North–South pointings covering the same region, consisting of 37 positions observed at KPNO and 55 positions observed at OAN-SPM. The KPNO \[S II\] data consist of two disjoint regions, one in the east and one in the west of the nebula, while the OAN-SPM data consist of 35 pointings with a slit width corresponding to 2 arcsec and 12 km s⁻¹ velocity resolution, and 20 pointings with a 0.9 arcsec slit width and 6 km s⁻¹ velocity resolution. The slit length at OAN-SPM is 312 arcsec.
- We use the calibrated position-velocity (PV) arrays obtained by Garcia from each individual longlist spectrum fo the VCA of each emission line.
- For the second-order structure functions, we work with the velocity moment maps. particularly the mean velocity map reconstructed from the PV arrays by garcia.

## 2.2 Statistical methods
### Velocity channel analysis
- VCA consists of taking the spatial power spectrum of the emission intensity (or brightness) in the velocity channels of spectroscopic PV data.
- The PV are binned into velocity channels of width $\delta v$. As the width of the velocity slices increases, the contribution of velocity fluctuations decreases. 
- A velocity slice has a width $\delta v = (v_\text{max} - v_\text{min})/N$, where $N$ is the number of channels. In this work $v_\text{max} = 70 \ \text{km/s}, v_\text{min} = -40 \ \text{km/s}$. 
- The thickest velocity channel corresponds to $N=1$ and the thinnest velocity slice to $\delta v = 4 \ \text{km/s}$. 

### Second-order structure function
- The second-order structure function of the velocity centroids is: $$S_2(l) = \frac{\sum_{\text{pairs}} \left[V_c(r) - V_c(r + l)\right]^2}{\sigma_{V_c}^2 N(l)},$$ where $r$ is the two-dimensional position vector in the plane of the sky, while $l$ is the separation vector. The normalization is by the number of pairs of points at each separation, $N(l)$, and the variance of centroid velocity fluctuations, $\sigma_{V_c}^2$, is defined by $$\sigma_{V_c}^2 = \frac{\sum_{\text{pixels}} \left[V_c(r) - \langle V_c \rangle\right]^2}{N}.$$
- Here, $\langle V_c \rangle$ is the mean centroid velocity: $$\langle V_c \rangle = \frac{\sum_{\text{pixels}} V_c(r)}{N}.$$
- We also define an intensity-weighted structure function by: $$S_2(l) = \frac{\sum_{\text{pairs}} \left[V_c(r) - V_c(r + l)\right]^2 I(r) I(r + l)}{\sigma_{V_c}^2 W(l)},$$ where $W(l) = \sum_{\text{pairs}} I(r) I(r + l)$ is the sum of the weights for each separation, and $I(r), I(r + l)$ are the weights (i.e., intensities) at each pair of pixels. This form favors bright structures and reduces the contribution of fainter regions. this is one way to reduce the contribution of noise to the structure function.
- The structure function is affected by small-scale, high-velocity features such as Herbig-Haro objects. The first step is to examine the probability density function of the velocity centroids. In practice, a 2 per cent threshold was uniformly applied to the pdf binned at $1 \ \text{km/s}$ resolution to eliminate the small number of pixels with anomalously high values [[Arthur 2016 fig 1 pdfs.png|1]].
- It can be seen in X that pixels corresponding to objects as HH 201, 202, 203, 204 and 529 are masked along numerical artefacts. 

### Application to the Orion nebula

- For VCA bootstrap Monte Carlo method, resampling with replacement of the ser of PV arrays. The power-law indices of the power spectra resulting from 10 different resampling of the set of PV arrays are obtained using a leat-squares fitting procedure. The variation of these sample power-law indices provides an estimate of the confidence bounds for the power-law index across the Orion nebula.

# 3 Results

## 3.1 Velocity Channel analysis

- The 1D, normalized, compensated power spectra for thin and thick velocity channels is shown and the coloured points represent the average power spectrum of 96 distinct slits.
- In the case of the two \[SII\], only the 20 highest's resolution slits are used.
- By plotting the 1D, normalized, compensated power spectra $k^3 P(k)$ for thin and thick velocity channels is very apparent a break at $k = 0.124 \ \text{arcsec}^{-1} = 7 - 8 \ \text{arcsec}$.
- The power spectrum can be divided into four ranges, where regimes I and II correspond to wavenumbers smaller than the break point, and III and IV regimes larger.
- For wavenumbers in regimes II, the power-law indicies of all the power spectra for all the emission lines are $\gamma > -3$. The power laws for the thin channels are less steep than those of the thick channels.
- For wavenumber in regimes III, the power-law indicies are all steeper than the critical value $\gamma = -3$, indicating there is very little power at small spatial scales.
- Noise dominates regime IV.
- The spectral indices in regime I and IV are similar and both shallow indicating that the velocity fluctuations at small y large scales are uncorrelated.
- Since the break in the slope always occurs at the same scales, this must be a feature of the emissivity fluctuations in the nebula.
- The power-law of the think slices is generally shallower (less negative) than that of the thick slices, indicative of the additional effect of velocity fluctuations.

## 3.2 Second-order structure function
### Shape and sope of structure function for each emission line

- The structure function is shown in [[Arthur 2016 fig 8 m structure functions.png|Fig8]].
- The fit to the power-law index of the structure function is performed over the spatial separations corresponding to regime II of the VCA, $8 < l < 22 \ \text{arcsec}$.
- The structure function show no clear break. The power-law fit to scales $> 8 \ \text{arcsec}$ is not too bad a fit to smaller scales also.
- The structure function has a slight negative curvature, giving gradually steeper slopes at smaller scales. The more pronounced steepening below $2 \ \text{arcsec}$ is due to the spatial resolution of the observation and corresponds to the region where the seeing and inter-slit separation become important.
- The steepest power-law indices over the fit range are for the Ha and \[O III\] lines. The form of the structure function is the same for both emission lines with an index of $1.2 \pm0.1$.
- The two \[S II\]emission lines have very similar structure functions to each other. Their slopes are shallower than others with an index of $0.8 \pm0.1$.
- The structure function for \[N II\] can be divided into two distinct populations: one set correspond to grames selected from the upper part of the velocity map, and the other to frames from the lower half. One set has an index similar to \[S II\] while the other between \[S II\] and Ha cases.
- The lower panes in [[Arthur 2016 fig 8 m structure functions.png|Fig8-9]] show the structure function when all pixels are used. There is little difference for Ha, \[O III\] and \[N II\] but for \[S II\] shows considerably differences.
- Difference between weighted structure functions for lines like \[S II\] and \[N II\].

## 3.3 Analysis of the power-law indices

- Use observed power-law indices from the VCA and second-order sf to recover the three-dimensional velocity statistics of the ionized gas in the Orion nebula. 
- Relationships between the observationally derived powe-law spectrum indices and the underlying 3D density and velocity fluctuations.
- The VCA gives us the power-law indices of the average power spectra of thin and thick velocity slices. The **thickest velocity slice corresponds to the velocity-integrated surface brightness** and the power-law indices of the spectra of the thick slices are predicted to be equal to the those of the 3D power spectra of the respective emissivity, $\gamma_T = n_E$.
- The critical value $n_E \sim -3$ divides 'seetp' from 'shallow' power spectra.
- A steep emissivity spectrum, $n_E < -3$ means that the emissivity is dominated by fluctuations at intermediate to large scales, while a 'shallow' spectrum, $n_E > -3$, indicates tat emissivity is dominated by fluctuations at small scales.
- As the velocities slices become thinner, velocity fluctuations dominate the spectra. 
- By using a combination of thick s lice and thin slice spectral indices, we can recover the velocity power-law index.
	- Steep case (VCA) $\gamma_t = -3 + \frac{1}{2}m_{3D}$:
	- Shallow case (VCA): $\gamma_t - \gamma_T = \frac{1}{2}m_{3D}.$
	- Projection smoothing: $m_{2D} = m_{3D} + 1$
	- Sheet-like case: $m_{2D} \approx m_{3D}$
	- Three-dimensional structure function: $m_{3D} = -3 - n,$ where $n = -\frac{11}{3}$ for homogeneous, incompressible turbulence (i.e., Kolmogorov spectrum).
	
### VCA: regime II

- For wave numbers $k < 0.124 \ \text{arcsec}^{-1}$ (spatial scales $r > 8 \ \text{arcsec}$) [[Arthur 2016 Table 2.png|Table 2]]:
	- \[S II\] show the critical value of separation between steep and shallow (lower ionization). These lines are least affected by thermal broadening and have the highest resolution of the observational data.
	- \[N II\] falls into the shallow regime and as \[S II\] shows the Kolmogorov value.
	- For Ha, there is little difference between the thin and thick power-law indices since thermal broadening is important. It is therefore not possible ro recover a meaningful value of $n$.
	- \[O III\] also shows the Kolmogorov behavior. 

### VCA: regime III
- For wave numbers $k > 0.124 \ \text{arcsec}^{-1}$ (spatial scales $l < 8 \ \text{arcsec}$) [[Arthur 2016 Table 3.png|Table 3]]:
	- \[S II\] power spectra have 'thick' slice power-law indices steeper than their 'thin' slice power-law indices. Negative values to structure function power index.
	- The \[N II\], Ha and \[O III\] have opposite behavior and their power-law indices cannot be accommodated by the theory.
### Structure function power indices

- We fit the structure functions over the separation range corresponding to VCA regime II. $m_{2D} \sim 1.2$ for the H$\alpha$ and \[O III\] lines, and  $m_{2D} < 1$ for the \[S II\] and \[N II\] lines  [[Arthur 2016 Table 4.png|Table 4]].
- In the range $l < 8 \ \text{arcsec}$ the structure function falls off very steeply due to the effects of seeing and the interslit separation.
- In the range $l > 100 \ \text{arcsec}$ the structure function flattens.
- The 3D structure function index must lie between the two limits given by projection smoothing and a sheet-like distribution of emitters: $m_{2D} - 1 < m_{3D} < m_{2D}$
- The lowest value of $m_{2D}$ is $m_{2D} \simeq 0.80,$ and the highest value is: $m_{2D} \simeq 1.18.$ Therefore, $m_{3D}$ must lie in the range: $0.18 < m_{3D} < 0.80.$ This is consistent with the results of the VCA, for which: $m_{3D} \simeq 0.67$ but is such a wide range of values that is not a useful diagnostic.

## 3.4 Line-of-sight velocity dispersions

- Spectral lines are broadened beyond the thermal component by a combination of ordered (expansion, contraction, rotation) and disordered motion (random motions loosely to 'turbulence') along the LOS.
- The lines often do not have Gaussian profiles and can sometimes be separated into distinct components with different kinematic characteristics.
- The non-thermal line of-sight velocity dispersion $\sigma$ may be estimated by correcting the observed linewidths for the contributions from the spectrograph resolution, fine-structure splitting, and thermal Doppler broadening.
- A striking fact about the nebular line profiles is that the los velocity dispersion is several times larger than the POS dispersion in mean velocities.
- This is illustrated in Fig X, which shows flux weighted histograms of the non-thermal rms linewidths versus mean velocity for all lines.
- The LOS rms velocity dispersion is $9-10 \ \text{ km/s}$, whereas the rms plane of sky dispersion of the mean velocities is only $2-4 \ \text{ km/s}$.
- Additional broadening due to dust scattering which gives an extended red wing to the line profile. By means of fitting multiple Gaussian components to each line profile, it is possible to effectively remove this scattered component. It is more difficult to perform this for lower ionization lines sine the back-scattered component is not as cleanly separated from the core component.
- An alternative method of suppressing the effects of scattering on the linewidths is to use the FWHM instead of the rms width. 
- Even a weak component with a velocity that is very different from the line centroid can have a large effect on the $\sigma_{\text{los}}$ due to the $(u - \bar{u})^2$ dependence of the second velocity moment. But the same component will have almost no effect on the FWHM if its amplitude is less than half of that of the line core.
- We therefore define a FWHM-based effective $\sigma$ as: $\hat{\sigma}_{\text{los}} = \frac{\text{FWHM}}{\sqrt{8 \ln 2}} \approx \frac{\text{FWHM}}{2.355},$ with the constant of proportionality being chosen so that $\sigma_{\text{los}} = \sigma_{\text{los}}$ for a Gaussian profile.
- The results are shown in Fig. 12, where it can be seen that nearly all the lines show substantial reductions in the line-of-sight linewidths with respect to the moment-derived values of Fig. 10. The exception is H$\alpha$, where larger thermal broadening means that $\hat{\sigma}_{\text{los}}$ is still contaminated by the back-scattered component due to blending.
- Note that $\hat{\sigma}_{\text{los}}$ is insensitive to not only the scattered component, but also to any other weak component that is not blended with the line core. For low ionization lines, this includes the kinematic component known as the Diffuse Blue Layer, which produces lines splitting in the SE and N regions of our observed maps.

# 4 Discussion

## 4.1 Comparison with previous structure function determinations

- The most promising range of length scales for measuring turbulence velocity spectrum is between a few times the seeing width and about half the correlation length, $l_0$, of the turbulence.
- At scales larger tan $l_0$, the structure function flattens as it tends toward the asymptotic value of $2$ for a homogenous random field. If there is a linear velocity gradient across the map, then the structure function will steepen again at the largest scales.
- Alternatively, if the turbulent velocity dispersion is inhomogeneous, being larger in the centre of the map than in the periphery, then the structure function slope will become negative at the largest scales.
- The Figure does not include the effects of noise, but that is easily dealt with in the case that the noise is 'white' (spatially uncorrelated) since the effect is to simply add a constant value to the structure function at all scales. 
- Previous studies of the velocity structure function in Orion have been carried out based on slit spectra [[Castañeda 1988]], \cite{Odell1992}, \cite{Wen1993}). 
- [[Arthur 2016 Table 5.png|Table 5]] compares these results with our own for different emission lines, ordered from lower to higher ionization. In spite of the differences in methodology, a broad agreement is seen, with both the magnitude of the velocity dispersion and the steepness of the structure function slope increasing with ionization.
- The most directly comparable methodology is \cite{Odell1992}, \cite{Wen1993}
- [[Castañeda 1988]] is based on multi-component Gaussian fits.
- Mc Leod et al. 2016 obtained flat structure function. Probably because of the noise in the observations.

## 4.2 Comparison with previous simulation results

- Simulations ($n \sim -3.1$)
- VCA of the emission lines of the heavier ions, the measured values of the thin velocity slice spectral index agree to within $0.1$ . 
- On the other hand, the second-order structure functions we calculated from our simulations proved less capable of reliably recovering the 3D power spectrum.
- In the simulation a single power law is sufficient to cover most of the wavenumber range. In contrast, our observationally derived power spectra can be split into different regimes.
- With regard to the power-law indices of the second-order structure functions, our simulations found a clear sequence: $1 > m_{2D}(\text{[O III]}) > m_{2D}(\text{H}\alpha) > m_{2D}(\text{[N II]}) > m_{2D}(\text{[S II]}).$ The simulation structure function follows a clear power law over a wide range of spatial separations whereas the observational structure function has a slowly varying power law as a function of separation scale.
- **The simulation results give very different values for the NII and OIII thick-slice spectral indices, suggesting a very different spatial distribution for these two emission regions**.

## 4.3 Turbulent contribution to spectral line broadening



- Other questions require consideration of the magnitude of the velocity fluctuations, as measured by different techniques than the structure function and power spectra. Such questions include whether turbulence alone is sufficient to account for the non-thermal line broadening observed in the nebula, and whether that turbulence is driven primarily by the large-scale thermal expansion of the nebula, or by smaller scale photoevaporation flows, and to what extent stellar winds play a role.
- The plane-of-sky dispersion in centroid velocities $\sigma_{\text{pos}}(\bar{u})$ is the rms width of the marginal distribution along the $\bar{u}$-axis of Fig. 10, which is the same as the quantity $\sigma_c$ used to normalize the structure functions in Section 2. Fig. 14(a) summarizes the observational determination of $\sigma_{\text{los}}$ and $\sigma_{\text{pos}}$, while Fig. 14(b) shows the same quantities calculated for the turbulent H II region simulation of Paper I.
- ==The fact that the line-of-sight velocity dispersion is roughly twice the plane-of-sky velocity dispersion can be interpreted in at least two different ways.== 
- **Case I:** In the case of a homogeneous turbulent velocity field with characteristic correlation length $l_0$, the projection from three to two dimensions over a line-of-sight depth $H$ reduces the plane-of-sky amplitude of fluctuations if $l_0 \ll H$, a phenomenon known as **projection smearing** (von Hoerner 1951; Scalo 1984).
- Our $l_0$ and $\sigma_{\text{pos}}/\sigma_{\text{los}}$ correspond to $s_0$ and $\sigma_{\text{los}}/\sigma_{\text{true}}$ in Fig. 1 of Scalo (1984), from where it can be seen that a value of 0.5 requires $l_0/H \approx 0.02-0.1$, depending on the steepness of the velocity fluctuation spectrum. The results from our structure function analysis (Section 3.2) imply a correlation length $l_0 \approx 0.1-0.2$ pc for all lines, which would require a very large line-of-sight depth $H > 1$ pc in order to explain the observed $\sigma_{\text{pos}}/\sigma_{\text{los}}$ by projection smoothing. **This is inconsistent with independent evidence** (Baldwin et al. 1991; O'Dell 2001; García-Díaz \& Henney 2007) that the emitting layer thickness is much smaller than this in the region covered by our maps: $H \approx 0.01-0.3$ pc, being thinner on the West side and for the lower ionization lines. The same discrepancy arises when the projection smearing argument is applied to our simulated H II region. Therefore, projection smearing of the large-scale fluctuations is negligible and cannot explain the difference between $\sigma_{\text{pos}}$ and $\sigma_{\text{los}}$.
- **Case II:** A second, contrasting interpretation of the evidence would be in terms of large-scale, ordered motions. Consider an emission shell that expands at velocity $v$. If the shell emissivity is homogeneous, then the integrated line profile is rectangular, with mean velocity $\bar{u} = 0$ and velocity width $\sigma_{\text{los}} = v/2$. Furthermore, the spatially resolved line profile at any point will also have $\bar{u} = 0$, so that $\sigma_{\text{pos}} = 0$. However, if there are **emissivity fluctuations between different parts of the shell, then $\bar{u}$ will fluctuate on the plane of the sky, according to the relative brightness of the redshifted and blueshifted hemispheres**. The required rms fractional variation in emissivity on the scale of the shell diameter is found to be $\sigma_{\text{fluc}} \approx \sigma_{\text{pos}}/\sigma_{\text{los}}$.
- The observed large-scale ($>9$ arcsec) brightness fluctuations are illustrated in Fig. 15, which shows log-normal fits to the PDFs of surface brightness, $S$, after normalizing by the mean, $S_0$, and binning the maps at 16 $\times$ 16 pixels. The rms width of the log-normal PDF, $\sigma_{\text{nS}/S_0}$ is seen to be in the range 0.45-0.6 for all lines. This is related to the rms fractional brightness fluctuation as $\sigma^2_{\text{nS}/S_0} = \ln(1 + \sigma_{\text{nS}/S_0})$, which implies $\sigma_{\text{nS}/S_0} \approx \sigma_{\text{S}/S_0}$ if $\sigma_{\text{nS}/S_0} < 1$. The relationship between $\sigma_{\text{E}/E_0}$ and $\sigma_{\text{S}/S_0}$ depends on both line-of-sight projection (Brunt, Federens \& Price 2010a), which tends to make $\sigma_{\text{S}/S_0} < \sigma_{\text{E}/E_0}$, and fluctuations in the foreground dust extinction, which have the opposite effect of increasing $\sigma_{\text{S}/S_0}$. The first effect dominates, so that the surface brightness PDFs imply $\sigma_{\text{E}/E_0} \geq 2\sigma_{\text{S}/S_0} \sim 1$ (see Section 4.5 for details). **This is larger than the value derived in the previous paragraph, which implies that emissivity fluctuations combined with an ordered velocity field are entirely sufficient to explain the observed plane-of-sky variation in mean velocities, without requiring any fluctuations in the velocity field itself.**
- Although it is a priori unlikely that there are no velocity fluctuations in the ionized gas, this is yet another reason why the structure function of the mean velocity is not an effective diagnostic of these fluctuations in the presence of strongly inhomogeneous emissivity and large-scale velocity gradients.
- In Orion, the ordered large-scale expansion of the nebula is an asymmetrical champagne flow away from the background molecular cloud (Zuckerman 1973), which produces systematically larger blueshifts with increasing ionization (e.g. fig. 11 of Baldwin et al. 2000). This offers a simple method for estimating the relative contribution of ordered versus turbulent motions to the total velocity dispersion. The mean systematic difference between the \[O I\] and \[O III\] centroid velocities is $\delta u = 9.4$ km s$^{-1}$ (table 2 of García-Díaz et al. 2008), which gives a champagne-flow contribution to the velocity dispersion of $\sigma_{\text{cham}} \approx 0.5 \delta u = 4.7$ km s$^{-1}$. The turbulent contribution to the velocity dispersion is then $\sigma_{\text{turb}} \left( \sigma^2_{\text{los}} - \sigma^2_{\text{cham}} \right)^{1/2} = 3.7$ km s$^{-1}$. The uncertainties in this analysis are large, so that all that can be confidently asserted is that the ordered and turbulent velocity dispersions are roughly equal with $\sigma_{\text{cham}} \approx \sigma_{\text{turb}} = 4-5$ km s$^{-1}$.

## 4.4 What is the significance of the 22 and 8 arcsec length scales?

- The outer scale of 22 arcsec coincides with scale where the structure functions reach a value of unity (Fig. 8), which corresponds to the correlation length, $l_0$, of the velocity fluctuations (see Fig. 13). It is therefore plausible to associate this scale, which corresponds to a physical size of $\approx 0.05$ parsec, with the driving scale of turbulence in the nebula. The inner scale of 8 arcsec, corresponding to a physical size of $\approx 0.02$ parsec, is harder to associate with any particular process since the structure functions (Fig. 8) show no apparent feature at this scale.

## 4.5  Does velocity turbulence causes the surface brightness fluctuations?

- The surface brightness fluctuations on the plane of the sky are primarily caused by emissivity fluctuations within the nebular volume, which are in turn caused by fluctuations in electron density, temperature, and ionization. The temperature and ionization dependence of the emissivity is very different for each line, but the electron density dependence is similar in all cases, being $\propto N_e^2$ in the low-density limit, which is appropriate for all the \[S II] lines. **It therefore seems likely that any commonalities in the statistics between all the different emission lines will give us information about the electron density fluctuations within the nebula.**
- In Section 4.3, it was shown that the rms fractional surface brightness variation in 2D is $\sigma_{\text{S}/S_0} \approx 0.5$ for all lines, and the rms emissivity variation in 3D is predicted to be $\sigma_{\text{E}/E_0} = \xi \sigma_{\text{S}/S_0}$, where the ‘de-projection factor’ is $\xi = 2-3$ (Brunt, Federath \& Price 2010b). On the other hand, if the emissivity fluctuations are due to variations in the density squared, then the rms fractional 3D density variation is $\sigma_{\rho/\rho_0} = 0.5 \sigma_{\text{E}/E_0}$, which approximately cancels out the de-projection factor so that $\sigma_{\rho/\rho_0} \approx \sigma_{\text{S}/S_0} \approx 0.5$. **If the density fluctuations are caused by the turbulent velocity fluctuations,** then numerical simulations (Konstandin et al. 2012) show that there is a linear relationship between $\sigma_{\rho/\rho_0}$ and the rms Mach number, $M$, of the turbulence: $\sigma_{\rho/\rho_0} = bM$, where $b = 1/3$ to $b = 1$, depending on whether the turbulent driving is primarily solenoidal or compressive. The rms Mach number is the ratio of the velocity dispersion to the constant isothermal sound speed $M = \sigma_{\rho/\rho_0}/c_i$, where $c_i = \sqrt{kT/m_H}$ is the ion sound speed and $T \approx 104$ K and $c_i \approx 11$ km s$^{-1}$. Thus, $M \approx 0.36$ so that, given $b < 1$, an input into the turbulent contribution to the density fluctuations is $\sigma_{\rho/\rho_0} \approx 0.36$.
- We therefore require a further mechanism to explain the roughly 50 per cent of the variance in ionized density that cannot be accounted for by turbulent velocity fluctuations. This could plausibly be provided by the bright-rimmed structure of the photoevaporation flows away from dense molecular globules and filaments (e.g. Bertoldi \& McKee 1990; Mellema et al. 2006; Henney et al. 2009; Arthur et al. 2011), which are responsible for driving the turbulence. We have calculated the emissivity-weighted density PDF for a simple model of a single spherically divergent, isothermal evaporation flow from a D-critical ionization front (Dyson 1968) and find $\sigma_{\rho/\rho_0} = 0.56$. For an ensemble of such flows with varying peak densities the $\sigma_{\rho/\rho_0}$ would be even higher, so that in order for their global contribution to rival that of the velocity fluctuations it is sufficient that a fraction 0.1–0.5 of the total emission should come from such flows.
# 5 Speculation

- We offer a speculative account of the complex web of physical processes that give rise to the velocity and brightness fluctuations that we observe in the Orion nebula. This is illustrated in Fig. 16, where the most important causal links are shown by thick arrows and secondary processes by thin arrows. The principal origin of all structure in the H II region is the highly filamentary and clumpy density structure in the molecular cloud from which it is emerging, which in turn has its origin in some combination of thermal and gravitational instability and supersonic turbulence (Padoan \& Nordlund 2002; Ballesteros-Paredes et al. 2011). In the molecular gas, thermal pressure is negligible compared with magnetic pressure, turbulent ram pressure, and the gravitational potential. However, the large temperature increase that accompanies photoionization means that thermal pressure dominates in the H II region, so that density gradients are converted into pressure gradients that can accelerate the gas. The fractal nature of the molecular density means that gas acceleration occurs on multiple scales, from the global outward radial expansion of the H II region (which in Orion is a highly one-sided champagne flow) down to photoevaporation flows from individual globules. **One piece of evidence for a direct connection between molecular density fluctuations and ionized velocity fluctuations is that Kainulainen et al. (2016) find correlation lengths of the order of 0.08 pc for the separations of molecular cores along the ridge that lies behind the Orion nebula, which is similar to the correlation lengths we find for the velocity fluctuations in the nebula.**
- Ionized density fluctuations can arise directly from the molecular density fluctuations, such as the bright rims at the edges of photoionized globules (Mellema et al. 2006; Henney et al. 2009; Arthur et al. 2011), and this is most important in **the lower ionization zones near the ionization front** where the \[S II] and \[N II] emission is strong. 
- In the more **highly ionized interior of the nebula**, it is collisions between opposing velocity streams that produce the ionized density fluctuations, but these fluctuations are less extreme than those seen in regions where the turbulence is subsonic.
- Finally, a variety of other processes, such as O star winds, radiation pressure, and bipolar jets from young stars can play a secondary role in stirring up gas motions.
- In the case of the Orion nebula, evidence for the influence of stellar wind interactions is restricted to the central 0.05 pc (García-Arredondo, Henney \& Arthur 2001) and the low-density western outskirts (Güdel et al. 2008), and they seem to have little influence on the bulk of the nebular gas. Stellar wind effects are more important in older and more massive regions that contain LBV and Wolf–Rayet stars (e.g. Smith \& Brooks 2007). Similarly, radiation pressure, although unimportant in Orion, becomes much more important in higher luminosity regions (Krumholz \& Matzner 2009). Herbig–Haro jets and bowshocks dominate the far wings ($\delta u \sim 50$ km s$^{-1}$) of the velocity distribution in Orion (Henney et al. 2007), but the total kinetic energy of these high-velocity flows is relatively low, so that the effect on the global velocity statistics is minor.

# 6 Summary

We have used statistical analysis of high-resolution spectroscopic observation of optical emission lines in the central $0.4 \times 0.6 \ \text{arcsec}$ of the Orion nebula in order to characterize the turbulence in the ionized gas. The analysis has been guided and informed by radiation hydrodynamic simulations of H II region evolution, the techniques that we have applied are as follows:
	1. Second-order structure function of velocity centroids (Section 2.2.2), which gives the variation as a function of plane-of-sky separation of the differences in average line-of-sight velocity.
	2. VCA (Section 2.2.1), which compares the spatial power spectrum slope of velocity-resolved and velocity-integrated emission profiles of the same line.
	3. Linewidth analysis (Section 3.4), which is sensitive to velocity fluctuations along the line of sight.
	4. PDF (Section 4.3) of the surface brightness in different lines.
Our principal empirical findings are as follows:
- The VCA technique is the most reliable means of determining the spectrum of velocity fluctuations in the ionized gas (Section 3.3.1), and we find consistent evidence from both low and high ionization lines for a Kolmogorov-type spectrum ($\delta u \sim l^{1/3}$) for length scales, $l$, between 0.05 pc ($\approx 22$ arcsec) and 0.02 pc ($\approx 8$ arcsec). Unfortunately, VCA cannot be applied if the thermal or instrumental linewidth is larger than the velocity differences of interest (Appendix C), which rules out its application to the H$\alpha$ line and to scales smaller than 0.02 pc.
- **The structure functions show systematic trends with degree of ionization (Section 3.3.3). Higher ionization lines tend to show steeper autocorrelation scales, larger total plane-of-sky velocity dispersions, and steeper slopes than lower ionization lines.** The changes are subtle and difficult to interpret because of the influence of projection effects and sensitivity to details of the observational methodology (Section 4.1.1).
- **The characteristic length of 0.05 pc is special in at least two ways, corresponding to both the autocorrelation scale of velocity differences for low-ionization lines (Figs 6, 8 and 13) and also a break in the power spectrum of surface brightness fluctuations in all lines (Figs 5–7).** We suggest that this is the dominant scale for density fluctuations in the nebula (Section 4.4) and is also the main driving scale of the turbulence. A further break in the surface brightness power spectra occurs at the smaller scale of 0.02 pc ($\approx 8$ arcsec), but there is no obvious feature in the structure functions at this scale.
- Comparison of the application of turbulent diagnostics to numerical simulations (Paper I) with application of the same diagnostics to Orion leads us to conclude (Section 4.2) that even the high-ionization line emission (e.g. \[O III]) is confined to a thick shell and does not fill the interior of the nebula. Furthermore, the underlying power spectrum is shallower in the simulations, implying that small-scale turbulent driving is less important in the nebula than it is in the simulations.
- There are three lines of evidence suggesting that the velocity fluctuations are not homogeneous on the largest scales, but rather that the turbulent conditions themselves vary, both across the sky and along the line of sight, on scales larger than the velocity autocorrelation length of 0.05–0.15 pc:
	- The structure function slope of the \[N II] line is significantly steeper in the southern half of our observed field than in the northern half (Fig. 8).
	- The plane-of-sky velocity dispersion $\sigma_v$ increases with increasing ionization (Table 5), implying an increasing amplitude of fluctuations towards the interior of the nebula
	- The line-of-sight non-thermal velocity dispersion (after removing the confounding effect of dust scattering; Section 3.4) is typically twice as large ($\approx 6$ km s$^{-1}$) as the plane-of-sky velocity dispersion ($\approx 3$ km s$^{-1}$). In order to explain this ratio in terms of a homogeneous turbulent layer, the line-of-sight depth of the layer would need to be at least 10 times the velocity autocorrelation length, which is unrealistically large (Section 4.3). Instead, the result is more naturally explained by large-scale velocity gradients (such as radial expansion), combined with emissivity fluctuations along the line of sight.
- The turbulent and ordered components of the velocity dispersion ($\sigma_{\text{turb}}$ and $\sigma_{\text{cham}}$, respectively) are of similar magnitude: estimated to be 4–5 km s$^{-1}$ (Section 4.3).
- The PDF of surface brightness fluctuations is approximately log-normal with a fractional width of 0.4–0.5 in all lines (Section 4.3). Turbulent velocity fluctuations can only account for half of the variance in surface brightness. The remaining part may be due to density gradients in photoevaporation flows (Section 4.5).

# Appendix

## A: Positions of high-resolution \[S II] observations

- The \[S II] 6716, 6731 Å observations consist of 92 North–South pointings, 37 observed at KPNO with the same characteristics as the H$\alpha$, \[N II] and \[O III] observations used in this paper and 55 observed at OAN-SPM. Of this latter group, 20 pointings have a high-velocity resolution of 6 km s$^{-1}$ and the remaining 35 pointings have a lower velocity resolution of 12 km s$^{-1}$.
- All 92 data sets are used to construct the velocity maps, however only the 20 highest resolution observations are useful for VCA calculation, since the other observations are too affected by noise at high wavenumber.

## B: Position of \[O III] horizontal slits

- The main data set consists of North-South oriented longslit spectra. We test if the orientation affects the VCA by examining supplementary data set perpendicular to the main data set made at OAN-SPM. 
- 15 spectra were obtained in steps of $1.4 \ \text{arcsec}$ starting at $23 \ \text{arcsec}$ south of $\theta^1$Ori C and proceeding south.

## C: Are the thin slices really thin?

## D: Plane-of-sky versus Line-of-sight variations in velocity from simulated region

- For two representative times, [[Arthur 2016 fig D1.png|Fig D1]] shows the joint distribution of mean velocity $\bar{u}$ and non-thermal linewidth $\sigma_{\text{los}}$, calculated from the line profiles of synthetic position–position–velocity cubes for the simulated turbulent H II region of Medina et al. (2014). [[Arthur 2016 fig D1.png|Fig D1]]  shows the temporal evolution of the plane-of-sky average and Standard deviation of the same two quantities for the [O III] line. Results from the upper-right and lower-left panels of [[Arthur 2016 fig D1.png|Fig D1]] , respectively, provide the data that go into the horizontal and vertical axes of Fig. 14(b) in Section 3.4. 
- At late times ([[Arthur 2016 fig D1.png|Fig D1]] c d), when dust absorption is relatively unimportant, the average line centroid velocity (upper left panel of[[Arthur 2016 fig D1.png|Fig D1]] ) reflects the champagne flow due to the largest-scale density gradients in our simulation box. This leads to both blue and red shifts, since opposite viewing directions (e.g. $+x$ and $-x$) have roughly equal but opposite mean velocities, so that pairs of PDFs in [[Arthur 2016 fig D1.png|Fig D1]] c d are rough mirror images. At earlier times ([[Arthur 2016 fig D1.png|Fig D1]]  a b), radial expansion dominates and the dust optical depth is larger, which leads to selectively greater absorption of receding regions of the nebula. This produces predominantly blueshifted mean velocities from all viewing directions.

![[Arthur 2016 fig D1.png|500]]
## E: Toy Model of surface brightness profiles

# Images

![[Arthur 2016 KPNO M42 S.png]]


![[Arthur 2016 fig 1 pdfs.png]]

![[Arthur 2016 fig 5.png]]

![[Arthur 2016 fig 6.png]]

![[Arthur 2016 fig 8 m structure functions.png]]
![[Arthur 2016 fig 10 12.png]]

![[Arthur 2016 fig 13.png|400]]

![[Arthur 2016 fig 14.png|600]]

![[Arthur 2016 fig 15.png|400]]

![[Arthur 2016 fig 16.png|500]]
# Tables

![[Arthur 2016 Table 1.png|500]]
![[Arthur 2016 Table 2.png|600]]

![[Arthur 2016 Table 3.png|600]]

![[Arthur 2016 Table 4.png|400]]

![[Arthur 2016 Table 5.png|600]]