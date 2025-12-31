
# Correlation length definitions

The correlation length, $\mathcal{L}$, (also called *integral length scale* [Pope](<../Bibliography/Books/Turbulent Flows.md>)) is defined in terms of the auto correlation function  $C(r)$: 

$$\mathcal{L} \equiv \int_0^\infty C(r)\ dr . \tag1 $$


[Tennekes and Lumley](<../Bibliography/Books/A First Course in Turbulence.md>) define the correlation length as:

$$\Lambda_{t}=\dfrac{1}{C(0)} \int_{0}^{\infty} C(r) dr$$

[Jaupart and Chabrier 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...663A.113J/abstract) define the correlation length as:

$$\ell_c^2 = \frac{1}{4} \int C(r) \, d^2 r= \frac{\pi}{2} \int_0^\infty r C(r) \, dr \tag2$$
# Correlation length in H II Regions



Using the model proposed in the project: 

$$ C_{\text{mod}}(r;\ r_0, m) = 2^{- \left( r/r_0 \right)^m} =e^{[- \ln2 (r/r_0)^m]}$$

the solution for the Pope definition of the correlation length is:

$$ \mathcal{L}\equiv \int_0^\infty C(r)\ dr =\int_0^\infty e^{[- \ln2 (r/r_0)]^m} \ dr = \boxed{ \frac{\Gamma \left( \frac{1}{m} \right)}{m(\ln 2)^{1/m}} r_0} $$

with a particular solution for $m =1$: 

$$ \mathcal{L}\approx \boxed{1.44 r_0 }$$


The solution for the Jaupart and Chabrier 2022 definition of the correlation length is:

$$\ell_c^2 = \frac{\pi}{2} \int_0^\infty r C(r) \, dr  =\frac{\pi}{2}\int_0^\infty re^{[- \ln2 (r/r_0)^m]} \ dr = \boxed{\frac{ \pi \Gamma(2/m)}{2m(\ln2)^{2/m}}r_0^2} $$


with a particular solution for $m =1$:  

$$\ell_c^2  \approx \boxed{ 1.808 r_0} $$



# Correlation length values



VIENTO 

$$C(r_0) = \frac{1}{2} =0.5$$

 [Miville-Deschenes et al. 1995](https://ui.adsabs.harvard.edu/abs/1995ApJ...454..316M/abstract):

$$C(r_0) = e^{-1} \sim 0.36$$

 [Lagrois and Joncas 2011](https://ui.adsabs.harvard.edu/abs/2011MNRAS.413..721L/abstract) (*Total decorrelation length*): 

$$C(\tau_0) = 0$$

 