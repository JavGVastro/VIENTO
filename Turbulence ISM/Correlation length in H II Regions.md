
# Correlation length

- The correlation length, $\mathcal{L}$, (also called *integral length scale* [Pope](<../Bibliography/Books/Turbulent Flows.md>)) is defined in terms of the auto correlation function  $C(r)$: 
	$$\mathcal{L} \equiv \int_0^\infty C(r)\ dr . \tag1 $$
- [Jaupart and Chabrier 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...663A.113J/abstract) define the correlation length as:
	$$\ell_c^2 = \frac{1}{4} \int C(r) \, d^2 r= \frac{\pi}{2} \int_0^\infty r C(r) \, dr \tag2$$

---

- Values
	- VIENTO 
		$$C(r_0) = \frac{1}{2} =0.5 \tag3$$
	-  [[Miville-Deschenes et al. 1995]]: 
		$$C(r_0) = e^{-1} \sim 0.36 \tag4$$
	- Total decorrelation length [[Lagrois and Joncas 2011]]: 
		$$C(\tau_0) = 0 \tag5$$

 
# Correlation length in H II Regions



Cálculo de los valores de la longitud de correlación, $r_0$, utilizando el modelo propuesto utilizado en [[Posdoc/Posgrado/Posgrado]]: :
$$ C_{\text{mod}}(r;\ r_0, m) = 2^{- \left( r/r_0 \right)^m} = \tag{4.1}$$
$$C(r)=e^{[- \ln2 (r/r_0)^m]} \tag{4.2} $$


La equivalencia entre definiciones es:
- Para la [[#^correlation-length-definition|ec. (2)]]: 
- $$\ell_c^2 = \frac{\pi}{2} \int_0^\infty r C(r) \, dr  =\frac{\pi}{2}\int_0^\infty re^{[- \ln2 (r/r_0)^m]} \ dr = \boxed{\frac{ \pi \Gamma(2/m)}{2m(\ln2)^{2/m}}r_0^2} \tag{5}$$

- *Solución particular* con $m=1$ para $(1)$: 
$$\ell_c^2 = \frac{\pi}{2} \int_0^\infty r C(r) \, dr  =\int_0^\infty re^{[- \ln2 (r/r_0)]} \ dr \approx \boxed{ 1.808 r_0} \tag{5.1}$$

- **Solución general** para [[#^correlation-length-definition|ec. (1)]]: 
$$ \mathcal{L}\equiv \int_0^\infty C(r)\ dr =\int_0^\infty e^{[- \ln2 (r/r_0)]^m} \ dr = \boxed{ \frac{\Gamma \left( \frac{1}{m} \right)}{m(\ln 2)^{1/m}} r_0} \tag{6}$$

- Solución particular con $m =1$ para $(2)$: 
-$$ \mathcal{L}\equiv \int_0^\infty C(r)\ dr =\int_0^\infty 2^{- \left( r/r_0 \right)} \ dr \approx \boxed{1.44 r_0 }\tag{6.1} $$

