# Spatial Power Spectrum

- A common analysis technique for two-dimensiona images is the spatial power spectrum -the square of the 2D Fourier transform of an image. A radial profile of the 2D power spectrum gives the 1D power spectrum. The slope of this 1D power spectrum ban be compared to the expected indices indifferent physical limits. For example, the velocity field of Kolmogorov turbulence follows $k^{-5/3} ,$ while Burgers' turbulence has $k^{-2} .$
- However, observations are a combination of both velocity and density fluctuations, and the measured index from and integrated intensity map depend on both components, as well as optical depth effects. For a turbulent optical thin traces, and integrated intensity image (or zeroth moment) will have $k^{-11/3} ,$while and optically thick tracer saturates to $k^{-3} .$ 

## Definition

$$\tilde{I}(k_x, k_y) = \iint I(x, y) \, e^{-2\pi i (k_x x + k_y y)} \, dx \, dy$$

$$P(k_x, k_y) = |\tilde{I}(k_x, k_y)|^2
$$

$$P(k) = \langle P(k_x, k_y) \rangle_{k = \sqrt{k_x^2 + k_y^2}}$$

$$P(k) \propto k^{-\beta}$$

## Relation to Structure Function

$$S_2(\ell) = \langle |I(x+\ell, y) - I(x, y)|^2 \rangle$$

$$S_2(\ell) \propto \ell^{\gamma}, \quad \text{with} \quad \gamma = \beta - 2$$

# Power spectrum spectral index $\kappa$

$$p_N(k) \propto k ^{-\kappa_{N\text{D}}} $$

- [[Medina et al 2014]], Stutzki et al 1998, Miville-Deschenes et al. 2003, Brunt et al. 2003

# Energy and power spectrum relation

$$P(k) \propto k^{-\kappa}$$

$$p_n(k) = \int e^{i \mathbf{k} \cdot \mathbf{l}} \langle a(\mathbf{r}) a(\mathbf{r} + \mathbf{l}) \rangle  dl $$


The energy spectrum is the angle integral of the power spectrum over shells of radius $k = |\mathbf{k}|$ such that  

$$E_N(k) \propto k^{n-1} p_n(k)$$

$$E(k) \, dk = P(k) \, dk^P$$


$$E(k) = 4\pi k^2 P(k)$$

Energy Spectrum for n=3
$$E_n(k) \propto k^{n-1} p_n(k)$$
$$E_3(k) \propto k^{3-1} p_3(k)$$
$$E_3(k) \propto k^2 p_3(k)$$

Kolmogorov
$$\kappa = -\frac{11}{3}$$

Power spectrum
$$p_3(k) \propto k^{-\frac{11}{3}}$$$$E_3(k) \propto k^2 k^{-\frac{11}{3}}$$$$E_3(k) \propto k^{-\frac{5}{3}}$$



# Power Spectral Density (PSD)

- [ ] One-dimensional power spectral density

$$S_{xx}(\omega) = \lim_{T \to \infty} E\left[ \frac{|X_T(\omega)|^2}{2T} \right]
$$