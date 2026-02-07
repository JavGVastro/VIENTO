

 https://ui.adsabs.harvard.edu/abs/1987ApJ...317..686O/abstract

>[!warning]
>- Reconciliation between values of $w$ and $W$ between different works still needs to be solved. Scale problem maybe?
>- We can compare our observations with the predictions of von Hoerner's theory in a straightforward manner. This can be done by comparison of the agreement of theory and observation in: [[#Structure function]], [[#Dispersion analysis]] and [[#Line broadening]].
>- We have done our best to provide unambiguous and insightful observational data, and even though more good observations are still needed, it seems that the ball is now in the court of theoreticians.
# Abstract


- Determination of **velocity dispersions** and **structures functions** for galactic H II regions:
>	- 
- Dependence of the random velocities upon scale; arguing the presence of turbulence but in poor agreement with the Kolmogorov turbulence [[von Hoerner 1951]].
- No single power law: energy entering at different scales.
- *"We also find that the velocity broadening of the observed line is significantly greater that would be inferred from **scatter of velocities across the face of the nebulae**, this arguing that the apparent velocity differences are reduces by integration along the lines of sight passing into the nebulae."*
- Reassessment of the assumptions of turbulence theory in H II regions.


- The aim is to interpret the data using existing theories and models, finding that they do not fully explain the observation.
- The paper aims to guide the development of new theories and models for turbulence in H II regions, recognizing the significant role of turbulence in these regions
- [[Theory/Turbulence#^theory-Kolmogorov|Turbulence Kolmogorov Theory]]
- The expected one-third power dependence of the dispersion of velocities and the corresponding $2/3$ power dependence for the structure function are only points of reference.


- [[von Hoerner 1951]] has shown that the observed relation of velocity and distance can be very object geometry dependent.
- The goal of the model was to relate *Kolmogorov's solution for turbulent motion to predictions* of **FWHM (or the dispersion of velocities in a sampled area on the face of a nebulae) and the relation between angular separation across the face of a nebula and the measured radial velocity.**
- Von Hoerner introduces a parameter $$l = \Lambda / R ,$$ where $\Lambda$ is the distance across the face of the nebula for the two lines of sight being considered and depth $R$ is sufficiently great that a given LOS through the nebula intersects several turbulent elements.
	- Von Hoerner divides his solution for the structure function into two parts, when $l$ is greater or less than about $0.2$.

# Methods
## Prediction of theory

- **Model 0**  (not consider by von Hoerner) is where the nebula is of a size that all turbulent elements are seen and that there is not an overlapping of their spectra. Model 0 predicts $1/3$ power dependence of the **velocity dispersion with angular distance**, a $2/3$ power dependence of the **structure function**, and that the observed emission lines would be very narrow, having **only thermal broadening** width.
- **Model I** is for an **optically thin, plane parallel nebula**, ==no internal extinction of the observed emission line==, of depth $R$ and the observed line is broadened correspondingly. After correction of thermal broadening, the model predicts 

$$\text{FWHM}  = 1.580 C R ^{1/3} , $$

when observed with a resolution size small compared with $R$, where $C$ is the constant of proportionality in Kolmogorov's relation $V=Cr^{1/3}.$ The **most probable turbulent velocity** will be 

$$w = \frac{\text{FWHM}}{ 2\sqrt{\ln 2}} = \frac{1.580 C R ^{1/3}}{ 2\sqrt{\ln 2}}.$$


- In the case of $l$ large, the structure function is 

 $$B = C^2 \Lambda^{2/3} H_1(l)^2 ,$$
 
  where $H_1(l)$ is a smoothly varying function ranging from $0.671$ at $l = 0.5$ to $1$ at $l=\infty$.
	- In the case of $l$ small: 
	
	$$B = C^2 \Lambda^{5/3} H_2(l)^2R^{-1} ,$$
	
	 where $H_2(l)$ varies from $1.707$ at $l=0$ to $1.147$ at $l=0.2$

- **Model II** is one of an **optically thick nebula**, that is, where the ==emission lines are subject to extinction==. The formulations and solutions are essentially identical to model I, except now $R$ is the distance at which the optical depth becomes $1$. The solutions are 

$$w = \frac{1.776 C R ^{1/3}}{2 \sqrt{\ln 2}}$$

and the functions $H(l)$ change in value.
- **General formulation**: Assume that the relationship of velocity $v$ and separation $r$ is $v^2 = C^2 r^n$, where $C$ is an arbitrary scale factor, then the basic approach for the **observed structure function** is: 

$$B = C^2 \Lambda^n \left[ 2 l \left\{ \int_0^{1/l} \left[ (1 + x^2)^{n/2} - x^n \right] dx - l   \times\int_0^{1/l} x \left[ (1 + x^2)^{n/2} - x^n \right] dx \right\}\right] ,$$

where $x$ is an artificial parameter for integration in depth. The terms following $C^2 \Lambda^n$ are a ==correction factor $F(l,n)$ which takes into consideration the integration of the velocity differences along all steps in both lines of sight.==
	- When $l$ is large $F(l,n)=1$, as the apparent separation $l$ becomes characteristic of the separation of all of the elements of each of the lines of sight. 
	- When $l \ll$ 1, then  $F(l,n)$, is quite dependent of $l$ and $n$.
		- Kaplan and Pikelner imply that  $F(l,n) = 2l$, for all values of $n$, but actually it is $F(l,n) = 2lf(l,n)$, where 
		
		$$f(l,n)=(\ln2-\ln l),1/2l,1/6l^3$$
		 for values of $l^{-2} \ll 1$, and $n = 1, 2,$ and $4$, respectively.
		- For $l \ll 1$, $f(l, \frac{2}{3}) \approx 1$; Kaplan and Pikelener.
	- For $l \ll 1$, $n \ll 1$, $F(l,n)= 7 \pi nl/8$
	- ==Small values of $F(l,n)$ indicate that the **velocity differences averaged over the lines of sight** *are much less than the values corresponding to a distance of $\Lambda$*==.
	- The solution of the general formulation was done by numerical integration for various values of $l$ and $n=2/3, 1/96$. [[#^ODCast87-table1-model|Table 1]] [[#^ODCast87-fig1-model|Fig 1. Model]]
- The **structure function** and the **dispersion of velocities** are related functions, but a separate function treatment of the two is necessary. In particular, we need a solution for dispersion within a sample size. Neither a specific, $n=2/3$, or general formulation of the solution for the most probable three dimensional turbulent velocity $w$ has ben made; ==however, a general consideration must apply, i.e., the differences of velocities of lines of sight will be less than that corresponding to the separation $\Lambda$.==, only approaching those velocities as $l$ becomes very large. this would lead us to expect a dependence rising more rapidly than $\Lambda^{n/2}$ for $l \ll 1$.
	- Von Hoerner's general formulation of the expected line width ca be form. He worked in terms of the *line half-width* at the $e^{-1/2}$ instensity point $\Delta$, which is related to fe FWHM by $\text{FWHM} = (8 \ln 2) \Delta^2$. For an optically thin nebula the general integral to be resolved is
	
	$$\Delta^2 = C^2 \Lambda^n 21 \left( \int_0^{1/l}  x^{n} dx - l \int_0^{1/l} x^{n+1} dx  \right) $$
	
	 in the case of high spatial resolution, which is analogous to von Hoerner's equation (II, 69).
	- The solution to our equation is $\Delta^2 = 2C^2R^2 / (n^2 + 3n + 2)$ , which means that in general: 
	
$$\text{FWHM} = \left[ 16(\ln 2) / (n^2 + 3n + 2) \right]^{1/2} CR^{n/2}$$


## Comparison with observations

>[!info] This section discusses analytical results in random motions H II regions by comparing them with previous similar investigations and theoretical models.

### State Art

- [[Munch 1958]] - [[M 42]]
- [[Catañeda (1985)]] - [[M 42]] - Triple component
- [[Louise and Monnet (1970)]] - Fabry Perot - [[M 8|NGC 6523]] - inherently broad Ha line, they don't detect the double velocity structure.
- [[Bohuski (1973)]] - Fabry-Perot - [[M 20]] / [[M 8|NGC 6523]]- resolution was insufficient to detect the two components in [[M 8|NGC 6523]]
- [[Roy and Joncas 1985]] - [[S142]] - these results are not used in the discussion because they did not accurately determine the instrumental dispersion of velocities.
- [[Roy et al. (RAJ) 1986]] - [[M 17]] - these results are not used in the discussion because they did not accurately determine the instrumental dispersion of velocities.
- Data from [[O'Dell (1986)]]  - Echelle spectrograph - [[NGC 1499]] / [[NGC 7000]] / [[S252]] and recent studies includes  of [[M 20]] and [[M 8]] was used from [[O'Dell, Townsley, and Castañeda (1987)]]. [[#^ODCast87-fig2-sfs|Fig. 2]]

- Reconciliation between values of $w$ and $W$ between different works still needs to be solved. Scale problem maybe?
- Similar slopes through their main bodies but show an appreciable scatter in the absolute scale of the turbulent velocities, more visible in [[#^ODCast87-fig2-sfs|Fig. 2]]
- We can compare our observations with the predictions of von Hoerner's theory in a straightforward manner. This can be done by comparison of the agreement of theory and observation in: ==[[#Structure function]], [[#Dispersion analysis]] and [[line broadening]].==

### Structure function

- The [[Structure Function]] is the most attractive means of studying the statistical correlations of velocity data because many more data points are directly used in determining the velocity properties at a given distance. This in turn allows the use of higher spatial resolution than in the dispersion approach. A final advantage lies in its larger value, which makes it less sensitive to correction for instrumental dispersion.
- ==None of the velocity systems come close to resembling the expectations of the simples application of Kolmogorov theory.==
- The three objects studied over their entire surfaces would be expected to have slopes of about $5/4$ since they cover the range of $0.1<l<1$. **Optically thin**.
- Assuming that the total apparent sizes of **NGC 6514** and **NGC 6523** are $15'$ and $25'$, respectively, then the slope for their velocity systems should be about $3/2$ for the range of $l$ covered by those observations, and if they are even larger, then slopes would be even closer $5/3$.
- [[#^ODCast87-fig2-sfs|Fig. 2]] also shows the theoretical results for $n = 1/96$ fitted to the data for **NGC 7000** and **NGC 6523 A** (inner region of the nebula).
- Not only is the most typical index of $1/96$ much different from Kolmogorov theory, the SF shows variations from the expected smooth slope far beyond the probable error of the determinations and does not fit the observations over the entire range. The energy source driving the turbulence is input at several scales, as indicated by the variations from the expected smooth slope in the structure function. **This argues that the energy source driving the turbulence is input at several scales.** 
- The question of a limited scale of correlation has been discussed by Kaplan and Pikelner. They show that if one assumes that the velocities are not correlated above distances of the nebular thickness $R$, that the observed SF should become flat for $l \gg 1$ and approach the slope for $l \ll 1$ that is calculated for this regime by the general formulation of von Hoerner's approach.
- This assumption of turbulence only cascading downward in size could certainly account for plateaus in the observed structure functions.


### Dispersion analysis

- Summary in [[#^ODCast87-fig3-W|Fig. 3]] and [[#^ODCast87-table2-dispersion|Table 2]]
- NGC 6514 and NGC 6523 A average $0.41 \pm 0.12$ and the others $0.23 \pm 0.03$ (NGC 6523 A, NGC 7000, NGC 1499)
- Steepening of the slope at the small end.
- A **meaningful discussion** of the dispersion data awaits a theoretical treatment such as von Hoerner's discussion of the structure function.

### Line broadening

- The line broadening is essentially due to integration along the line of sight into the nebula, an effect first pointed out by von Hoerner.
- Table 3 gives the summary of FWHM values and the derived values of the most probable three-dimensional turbulent velocities $w$ (FWHM) derived for an electron temperature of $10^4 \text{ K}$.
- For a spherically symmetric nebula one would expect $w$ to decrease near the edge of the nebula as the LSO path through the nebula decreases for a positive index in the expression $v^2 = C^2 r^n$. This effect is not seen.
- This means that not only are the emission lines broadened more than is expected from the dispersion values, but also that the broadening continues to the edge of the object in a fashion which is stronger than expected.
- ==Temperatures at the edge of the nebulae.==
- The $\sqrt{3}$ factor is necessary sine the value of $W$ determined from the dispersion is in one direction only, so that $\sqrt{3} W$ is a measure of the total most probable velocity as determined along a line of sight.
- For the three nebulae studied by the echelle spectrograph $W$ (dispersion) was simply the value derived for the data set enclosing the entire nebulae. 
- In most cases $w$(FWHM) is greater than $\sqrt{3} W$(dispersion) $$\frac{w}{\sqrt{3}W}= 1.6\pm 0.3 $$ and an average of $2.1 \pm 0.3$ for three objects mapped entirely and are free of uncertainties in extrapolation. 
- If the observed velocities were characteristic of the LOS masses, then we would expect this ratio to be about one, if the nebula is optically thin, and to be less than one if the nebula is optically thick.
- ==This result is an apparent dilemma, as it argues that somehow we are seeing **more random velocities being built up over a line of sight distance** that is certainly no greater than the size of the nebula, assuming that nature has not been so unkind as to have made all of the object studied cylinders elongated along our LOS.==
- Gilles Joncas argues that the extra line broadening could be due to **large-scale flow of material along the LOS**, which certainly must contribute to the width. Argument supported by two line components.
- Resolution of this problem also awaits the general formulation of the analytical expression for $W$, so that one can then isolate the effects of large-scale flow.
- **Using dust to work with the optical depth.**
- Mathis (1983) has found that in EHIIR the optical depth can be large, but these are selectively very large objects, much larger than the nebulae considered here and are much more likely to have large optical depths.
- A universally large optical depth would also require that the optical surface brightness would be smooth for all nebulae, which is no acceptable for any of these nebulae.
- ==If nebulae are really optically thick and were are observing them in the $l \gg 1$ regime, then $w$ should be constant across the largest part of the nebula. Since this is not the case this is yet another argument against a model with large optical depth.==
- Two velocity system component against optical depth. If the less optically thick region is very optically thick, then we should not be able to see the other velocity system.
 


## Discussion

- In this work the central regions of the objects were examined
- Fleck has argued that compressibility could vitiate many of the expectations of a turbulence theory bases on al incompressible gas. He argues that the slopes could be flatter than expected if the injection of energy occurs at the small size scale.
- Energy been feeding in several scales, again.
- If this is the case, then the most natural assumption is that the input at the **smallest scale** arises from *free expansion around small knots which are only incompletely ionized and shedding material to the general H II region at high velocities*. The **larger scale inputs** are equally uncertain, possible being instabilities or flow around naturally occurring obstacles.
- The differences in the absolute scale of the six velocity systems is to be expected, as they should depend upon the rate of input of energy into turbulence. 
- If the ultimate source of the energy driving the turbulence is photoionization, then we can rate $\epsilon$  to $N$, the local atomic density. The total radiation power absorbed by an ionization bounded H II region will be $\overline{E}\eta$, where $\overline{E}$ is the mean energy of the absorbed photoionizing photon and $\eta$, their number. The total mass $M$ of the nebula will be $M = (4 \pi /3)S^3 N m_H$, where $S$ is the radius of the Strömgren sphere and $m_H$ is the mas of the hydrogen atom.
- Since the total number of photoionization must equal the total number of recombinations and the latter is $(4\pi / 3)S^3 \alpha N^2$, then $\epsilon =\overline{E} \eta / M \approx N$. The same relation would apply if the nebula is radiation bounded.
- ==It is possible to estimate the relative energies in the turbulen and thermal motion of the gas. In [[O'Dell (1986)]] it was shown that the ratio of energies will be $$\frac{E\text{(turbulence)}}{E\text{(thermal)}} = 5.1 \times 10^{-3} w^2/t .$$==
- ==The values of $w$ derived in Table 3 indicate that $w^2 = 95.7 (\text{ km/s})^2$ , so that the average ratio of energies here is $0.5 \pm 0.2$, which is less but still indication that turbulence carries a large fraction of the energy in these H II regions.== 
- The true importance of this energy awaits resolution in the questions of the origin and dissipation.
- "We have done our best to provide unambiguous and insightful observational data, and even though **more good observations are still needed, it seems that the ball is now in the court of theoreticians.**"

# Data 

## OG
### Tables

| $l$  | $F(l, n)$ (n = 2/3) | $l^nF$ (n = 2/3) | $F(l, n)$ (n = 1/96) | $l^nF$ (n = 1/96) |
| ---- | ------------------- | ---------------- | -------------------- | ----------------- |
| 16   | 0.9294              | 5.901            | 0.04352              | 0.04480           |
| 8    | 0.8884              | 3.153            | 0.03648              | 0.03728           |
| 4    | 0.8249              | 2.079            | 0.02960              | 0.03003           |
| 2    | 0.7430              | 1.176            | 0.02292              | 0.02288           |
| 1    | 0.5997              | 0.5997           | 0.01618              | 0.01618           |
| 1/2  | 0.4470              | 0.2818           | 0.01160              | 0.01148           |
| 1/4  | 0.3023              | 0.1200           | 0.006250             | 0.006160          |
| 1/8  | 0.1885              | 0.04711          | 0.003488             | 0.003404          |
| 1/16 | 0.1107              | 0.01743          | 0.001862             | 0.001809          |
| 1/32 | 0.0668              | 0.006179         | 0.0009681            | 0.0009338         |
^ODCast87-table1-model

| Object     | Slope              | Intercept$^a$ | Weight |
|------------|--------------------|---------------|--------|
| NGC 1499   | 0.21 ± 0.05        | 0.07          | 3      |
| NGC 6514   | 0.39 ± 0.15$^b$    | 0.11          | 1      |
| NGC 6523A  | 0.42 ± 0.10$^c$    | 0.04          | 2      |
| NGC 6523B  | 0.15 ± 0.07        | 0.47          | 2      |
| NGC 7000   | 0.28 ± 0.04        | 0.21          | 3      |
| S252       | 0.30 ± 0.15        | 0.21          | 1      |
^ODCast87-table2-dispersion

* $^a$ log $W$ at log $D(\text{pc}) = 0$.
* $^b$ Uses largest four samples.
* $^c$ Excludes smallest sample.

| Object     | FWHM (km s$^{-1}$) | Line  | $w(\text{FWHM})^a$ (km s$^{-1}$) | $3^{1/2}W(\text{Dispersion})$ |
|------------|---------------------|-------|---------------------------------|------------------------------|
| NGC 1499   | 26.1 ± 1.1          | Hα    | 8.9 ± 1.1                       | 3.5                          |
| NGC 6514   | 15.6 ± 0.3          | N I   | 8.4 ± 0.2                       | 4.8$^b$                      |
| NGC 6523A  | 9.6 ± 0.1           | N I   | 4.0 ± 0.1                       | 5.4$^c$                      |
| NGC 6523B  | 12.9 ± 0.3          | N I   | 6.3 ± 0.2                       | 7.3$^c$                      |
| NGC 7000   | 29.4 ± 0.8          | Hα    | 12.1 ± 0.7                      | 7.4                          |
| S252       | 32.8 ± 0.9          | Hα    | 14.9 ± 0.8                      | 6.8                          |
^ODCast87-table3-losbroadening

* $^a$ $t = 1$ is assumed for all objects.
* $^b$ Assumes an angular size of 15'.
* $^c$ Assumes an angular size of 25'.

### Images

![[ODCast87_fig1_model.png|400]] ^ODCast87-fig1-model




![[ODCast87_fig2_sfs.png|600]]^ODCast87-fig2-sfs

![[ODCast87_fig3_w.png|600]] ^ODCast87-fig3-W

## Reproduce

>[!info] Structure function data



# Cite

```
@ARTICLE{1987ApJ...317..686O,
       author = {{O'Dell}, C.~R. and {Castaneda}, Hector O.},
        title = "{Evidence for Turbulence in H II Regions}",
      journal = {\apj},
     keywords = {Gas Dynamics, H Ii Regions, Nebulae, Turbulence, Velocity Distribution, Astronomical Models, Kolmogoroff Theory, Astrophysics, NEBULAE: H II REGIONS, TURBULENCE},
         year = 1987,
        month = jun,
       volume = {317},
        pages = {686},
          doi = {10.1086/165314},
       adsurl = {https://ui.adsabs.harvard.edu/abs/1987ApJ...317..686O},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

```
# Bibliograby

- [ ] [[Chandrasekhar (1949)]] provided an early summary of the theoretical work on turbulence.
- [ ] [[von Hoerner 1951]] Applied Kolmogorov theory to H II regions and compared with observations.
- [ ] [[Munch 1958]] Extended Van Hoerner's analysis with improved data.
- [ ] [[Interstellar Gas Dynamics|Kaplan (1966)]] and [[Kaplan and Pikelner (1970)]] expanded the theory to the interstellar medium and H II regions.
- [ ] [[Louise and Monnet (1970)]] Identified early issues with Fabry-Perot observations and their implications for turbulence models.
- [ ] [[Fleck (1983)]] Argued that compressibility affects turbulence theory expectations.
- [ ] [[Castañeda (1985)]] Investigated the velocity structure of M42, revealing a triple structure.
- [ ] [[Roy and Joncas 1985]] Provided modern data on Fabry-Perot observations of S142 and M17.
- [ ] [[Roy et al. (RAJ) 1986]] Continued the study of velocity structures in nebulae.
- [ ] [[ODell (1986)]] Showed the discrepancy between observed and expected FWHM values, indicating significant turbulence.
- [ ] [[ODell, Townsley, and Castañeda (1987)]] Investigated the velocity structures in NGC 6514 and NGC 6523.

