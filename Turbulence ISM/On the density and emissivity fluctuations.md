
- [ ] Review $R \approx 0.2$ value


- For ionized regions it is assumed that the relative fluctuations in surface brightness $S$ and density $\rho$ are equal: $$\sigma_S \approx \sigma_\rho $$

- Note that literature on turbulence in molecular clouds discuss fluctuations of **density** since they are mainly concerned with emission lines whose *emissivity is approximately linearly proportional to density*.
- In the case of photoionized regions, the emissivity of important lines such as $\text{H}\alpha$ (completely ionized hydrogen sin most transitions are $n=3 \rightarrow 2$) is proportional to **density-squared** $n_e^2$, so in adopting the results of [Brunt:2004a](https://ui.adsabs.harvard.edu/abs/2004ApJ...604..196B) we substitute **emission measure** (or its proxy, $\text{H}\alpha$ surface brightness) in place of column density: $$EM = \int n_e^2dl$$
- We calculate $\langle \delta S^2  \rangle / S_0$ by fitting a log-normal function to the probability distribution function of the surface brightness map after filtering out fluctuations on scales smaller than the velocity correlation length.
- The relative fluctuations in surface brightness, $\sigma_{S / S_0} \equiv \langle \delta S^2  \rangle / S_0 ,$ and density, $\sigma_{\rho / \rho_0} \equiv \langle \delta \rho^2  \rangle / \rho_0$, are equal $$\sigma_{S/S_0} \approx \sigma_{\rho / \rho_0} , \tag1$$which is a result of the cancellation between two effects:
	1. That the volumetric $\text{H}\alpha$ emissivity $E$ is proportional to density squared, so that,  $$\sigma_{E/E_0} = 2 \sigma_{\rho / \rho_0} . \tag2$$
	2. Second, that fluctuations in surface brightness $S$ are related to those in emissivity by 
	$$\sigma_{S/S_0} = R^{1/2} \sigma_{E/E_0}, \tag3$$where $R$ is the 2D-to-3D variance ratio [Brunt, Federrath & Price 2010](https://academic.oup.com/mnras/article/403/3/1507/1050035) .  For an emissivity power spectrum  $P(k) \sim k^{-3}$ and assuming a ratio of map size to correlation length of $L/r_0 = 10$, we have $R \approx 0.2$ and hence: 
	$$\sigma_{S/S_0} \approx \sigma_{\rho / \rho_0}$$ 
- Substituting ec. $(3)$ in $(2)$ and solving for $\sigma_S$:
 
	 $$\frac{\sigma_S}{R^{1/2}} =\sigma_E= 2 \sigma_\rho $$
	 
	$$\frac{\sigma_S}{0.2^{1/2}} = 2 \sigma_\rho $$
	
	$$\frac{\sigma_S}{0.447} = 2 \sigma_\rho $$
	
	$$\sigma_S = 0.894 \sigma_\rho$$
	
$$\boxed{\sigma_S \approx \sigma_\rho} \quad \text{Q.E.D} \tag4$$
