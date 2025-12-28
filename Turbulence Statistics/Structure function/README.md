- The structure function in the VIENTO project is referred as $B(r)$. 
# Definition



$$ B(r) = \left\langle 
\bigl[
V_{c}(\boldsymbol{x}_j) - V_{c}(\boldsymbol{x}_i) 
\bigr]^{2} 
\right\rangle_{ | \boldsymbol{x}_j - \boldsymbol{x}_i | \ \approx \ r} \ .
$$


- Relation with the autocorrelation function $C(r)$

$$ B(r) = 2\sigma^2 \bigl[   1 - C(r)\bigr] .$$

## Other definitions

$$B(r)=\langle {\vert \vec{v}(\vec{x}+\vec{r})-\vec{v}(\vec{x}) \vert}^{2} \rangle  $$

- From [Arthur et al 2016](https://ui.adsabs.harvard.edu/abs/2016MNRAS.463.2864A/abstract)

$$S_2(l) = \frac{\sum_{\text{pairs}} [V_c(r) - V_c(r + l)]^2}{\sigma^2_\text{vc} N(l)}.$$


- $r$ is the two-dimensional position vector in the plan of the sky.
- $l$ is the separation vector.
- $N(l)$ Number of pair of points at each separation.
- $\sigma^2_\text{vc}$ the variance of the centroid velocity fluctuations: 

$$\sigma^2_{v_c} = \frac{\sum_{\text{pixels}} [V_c(r) - (V_c)]^2}{N}.
 $$


- $V_c$ is the mean centroid velocity: 

$$V_c = \frac{\sum_{\text{pixels}} V_c(r)}{N}.$$


**Intensity weighted** structure function by 

$$S_2(l) = \frac{\sum_{\text{pairs}} [V_c(r) - V_c(r + l)]^2 I(r) I(r + l)}{\sigma^2_{v_c} W(l)},$$

where $W(l)$: 

$$W(l) = \sum_{\text{pairs}} I(r) I(r + l),$$
# Structure function relation with turbulence


$$B(r)\propto (\varepsilon r )^{2 / 3} $$

# Heuristic model for H II regions



