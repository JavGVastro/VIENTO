- The integral scale measures the **total spatial extent of the correlation**, accounting for how strongly different points remain correlated as their separation increases. 

# Correlation function

Considering a statistically homogeneous random field $v(\mathbf{x})$, e.g., turbulent velocity field. The velocity fluctuations is defined as $$\delta v(\mathbf{x}) = v(\mathbf{x}) - \langle v \rangle. $$
The spatial covariance is defined as $$c(r) = \langle \delta v(\mathbf{x}) \delta v(\mathbf{x}+\mathbf{r}) \rangle.$$
For isotropic statistics, this depended only on the separation magnitude $r=|r|.$ 

Normalizing: $$C(r) = \dfrac{c(r)}{c(0)} = \dfrac{\langle \delta v(\mathbf{x}) \delta v(\mathbf{x}+\mathbf{r}) \rangle}{\sigma^2_v}$$ Consequently:
- $C(0) = 1:$ the field is perfectly correlated with itself at zero separation.
- $C(r) = 0.8:$ fluctuations separated by $r$ retain a strong positive correlation.
- $C(0) = 0:$ the fluctuations have zero linear covariance at that separation.
- $C(0) < 0:$ the fluctuations are anticorrelated.

$C(0) = 0$ does not necessarily imply statistical independence. It means that linear covariance vanishes.

The **integral correlation length**, or integral scale, is then defined as: $$\boxed{L_\text{int} = \int_0^\infty C(r)dr}.$$
The normalized definition is important to get units of length.

# Geometrical interpretation: an integral as accumulated area

The correlation at each separation determines how much that small interval contributes to the integral. Replacing the entire correlation function with a rectangle that has:
- Height $1$, corresponding to perfect normalized correlation.
- Width $L_\text{int}$.
- The same are as the actual correlation curve.
- $\text{Area} = 1 \times L_\text{int} = L_\text{int}$ therefore, the integral scale is the width of an idealized region of perfect correlation that would contain the same accumulated correlations as the actual field.

# Mathematical example: exponential correlation

Consider $$C(r) = \exp^{-r/l}$$ where $l$ is a characteristic length.

This function never reaches zero at any finite separation. It only approaches zero asymptotically. Yet it posses a perfectly well-defined integral scale: $$\boxed{L_\text{int} = l}.$$
The integral transforms the continuously decaying correlation function into one characteristic length.

What does it mean to accumulate correlation?

$$A(R)=\int_0^R C(R)dr$$

Considering a partial integral (instead of intgrating to infinity) we can ask, how much of the total correlation has accumulated b a given distance?
- $R=l=63.2\%$
- $R=2l=86.5\%$
- $R=3l=95\%$

Even though correlation persist at arbitrarily large separations, most of their accumulated contribution is concentrated within a finite spatial region.

That is exactly what the integral scale captures.

**The integral scale measures accumulated correlation, whereas the zero-crossing distance identifies where the correlation first vanishes.**

For measured turbulent correlations, the first zero crossing is sometimes used as a practical upper integration limit, particularly when the correlation at larger separations becomes noisy or oscillatory. This is an estimation convention, not the same mathematical definition as integration to infinity.

# Statistical interpretation: how far does information remain correlated?

Consider two points in a turbulent velocity field $v(x)$ and $v(x+r)$. At small separations, their velocity fluctuations tend to be similar because they belong to the same spatially correlated field.

As $r$ increases, that statistical similarity generally weakens.

The correlation function describes this loss of similarity at each separation. The integral scale compresses the entire decay into a single characteristic distance. 

This is useful since the integral scale determines how quickly spatial averaging reduces the variance of a field.

# Physical interpretation in turbulence

The integral scale is not automatically the diameter of the largest eddy, nor is it necessarily identical to the turbulence driving or injection scale.

It is a statistical measure derived from two-point correlations. Its relationship to physical eddy sizes depends on the turbulence model, geometry, and observable.

In three-dimensional velocity turbulence, one commonly distinguishes longitudinal and transverse correlations. their integral scales need not be identical, even under isotropic turbulence.
# Correlation length definitions

The correlation length, $\mathcal{L}$, (also called *integral length scale* [Pope](<../Bibliography/Books/Turbulent Flows.md>)) is defined in terms of the auto correlation function  $C(r)$: 

$$\mathcal{L} \equiv \int_0^\infty C(r)\ dr . \tag1 $$


[Tennekes and Lumley](<../Bibliography/Books/A First Course in Turbulence.md>) define the correlation length as:

$$\Lambda_{t}=\dfrac{1}{C(0)} \int_{0}^{\infty} C(r) dr$$

[Jaupart and Chabrier 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...663A.113J/abstract) define the correlation length as:

$$\ell_c^2 = \frac{1}{4} \int C(r) \, d^2 r= \frac{\pi}{2} \int_0^\infty r C(r) \, dr \tag2$$