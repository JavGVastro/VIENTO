
- **Covariance** measures the joint variability of two variables ($X$ and $Y$), i.e. the relationship between two variables (correlation) or the same variable across different points in time or space (autocorrelation)
- **Correlation** is the standardized version of covariance that measures the strength and direction of the linear relationship between two variables. It is dimensionless and scaled to lie between $-1$ and $1$.
- **Autocorrelation** is the correlation of a variable with itself ($X$ and $X$).
---
- The **Autocovariance** is the covariance of a variable with itself at some other time, measured by a time lag $\tau$.

Given a continuous function $x(t)$, defined in the interval $t_1 < t < t_2$, the **autocovariance function** is:

$$\phi(\tau) = \frac{1}{t_2 - t_1 - \tau} \int_{t_1}^{t_2-\tau} x'(t)x'(t + \tau) \, dt $$

 where primes indicate deviations from the mean values.

In the discrete case where $x$ is defined at equally spaced points, $k = 1, 2, \dots, N,$ we can calculate the **autocovariance at $\text{lag} \ L$**:

$$\phi(L) = \frac{1}{N - 2L} \sum_{k=L}^{N-L} x'_k x'_{k+L} = \overline{x'_k x'_{k+L}} \quad \text{for } L = 0, \pm 1, \pm 2, \pm 3, \ldots \tag1$$

 Note $\phi(0) = \overline{x' ^2}$, so that the **autocovariance** at *lag zero* is just the variance of the variable.

- The **autocorrelation function** is the *normalized* **autocovariance** function, eq. $(1)$, which has the following properties:
	- $\phi(\tau) / \phi(0) = r(\tau);$
	- $-1 \leq r(\tau) \leq ; r(0) = 1.$
	- If $x$ is not periodic $r(t) \rightarrow 0$, as $r \rightarrow \infty$.
	- It is normally assumed that data sets subjected to tome series analysis are stationary: implying that the true mean of the variable and its higher-order statistical moments are independents of the particular time.
	- This implies that the **autocorrelation function** can be assumed symmetric, $r(\tau) = r(-\tau)$.
	- The correlation length is the value of $\tau$ in which. $r(\tau) = 0$.
- The **correlation length** is a concept used in the study of autocorrelation functions to quantify the characteristic scale over which a variable exhibits significant correlation with itself. It represents the "distance" (in time, space, or another domain) over which the values of a field, process, or time series are correlated. Beyond this scale, the correlations diminish and become negligible. The autocorrelation function usually decays as $k$ increases, reflecting that values further apart in time or space are less likely to be correlated
	- In turbulence theory the correlation length is interpreted as the physical scale where the energy input take place. 
- The red noise (an auto regressive model ) is a signal-time series that has characteristics allowing its autocorrelation function to be modeled as an exponential and can be used to characterize velocity fluctuations in the context of turbulence.

# Definitions
$$
  C(r) = \frac{1}{\sigma^2}\left\langle
  \bigl[
  V_{c}(\boldsymbol{x}_j) \  V_{c}(\boldsymbol{x}_i)
 \bigr] \right \rangle_{ |{\boldsymbol{x}_j - \boldsymbol{x}_i} | \ \approx \ r} \ .
$$

## Other definitions

$$\text{ACF}(k) = \frac{\text{Cov}(X_t, X_{t-k})}{\text{Var}(X_t)}
$$
or 

$$\text{ACF}(k) = \frac{\mathbb{E}[(X_t - \mu)(X_{t-k} - \mu)]}{\sigma^2} .$$


Sample definition: 

$$\text{ACF}(k) = \frac{\sum_{t=k+1}^{n} (X_t - \bar{X})(X_{t-k} - \bar{X})}{\sum_{t=1}^{n} (X_t - \bar{X})^2}$$


[[Aller 1951]]

$$g(r) = \frac{\sum I'(x) I'(x + r)}{\sum I'(x)^2}$$