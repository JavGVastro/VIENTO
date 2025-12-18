
- Here we review the literature regarding the index of the observational structure function.
- We address some problems regarding the observational  power law index of the structure function (two-dimensional and projected), and its relation to its three-dimensional counterpart, and with index of the power and energy spectrum. 
- Relevant when using simulations and synthetic maps  [1](https://github.com/JavGVastro/VIENTO/tree/main/fake_maps) .
- **Relationship between power spectra and observed structure function indexes** results (see below):
	- non-emissivity fluctuations: $\kappa_{3\text{D}} =  m_{2\text{D}}  + 2$ and for
	- strong emissivity fluctuations: $\kappa_{3\text{D}} =  m_{2\text{D}}  + 3$

 
# Structure function turbulence index values
 

- Subsonic incompressible flow (Kolmogorov theory)
	- $m_{3D} = 0.66 = 2/3$ 
- Subsonic compressible flow
	- $m_{3D} = 0.80 = 4/5$ 
- Supersonic compressible flow
	- $m_{3D} = 1.00$      


# Index relationships

- From [Arthur et al 2016](https://ui.adsabs.harvard.edu/abs/2016MNRAS.463.2864A/abstract)

| **Description**                    | **Power-law index** | **Relationship**                 | **Kolmogorov value** | References                 |
| ---------------------------------- | ------------------- | -------------------------------- | -------------------- | -------------------------- |
| 3D emissivity fluctuations         | $n_E$               |                                  |                      |                            |
| 3D velocity fluctuations           | $n$                 | $n = -3 - m_{3D}$                | $-11/3$              | Kolmogorov (1941)          |
| 3D second-order structure function | $m_{3D}$            | $m_{3D} = -3 - n$                | $2/3$                | Kolmogorov (1941)          |
| 2D second-order structure function | $m_{2D}$            |                                  |                      |                            |
| **Projection smoothing**           |                     | $m_{2D} = m_{3D} + 1$            | $5/3$                | von Hoerner (1951)         |
| **Sheetlike emission**             |                     | $m_{2D} \sim m_{3D}$             | $2/3$                | Castañeda & O'Dell (1987)  |
| Intensity fluctuations             | $\gamma$            |                                  |                      |                            |
| Very thick velocity slice          | $\gamma_T$          | $\gamma_T \sim n_E$              |                      | Lazarian & Pogosyan (2000) |
| Thin velocity slice                | $\gamma_t$          |                                  |                      |                            |
| Shallow density $n_E > -3$         |                     | $\gamma_t = \gamma_T + m_{3D}/2$ |                      | Lazarian & Pogosyan (2000) |
| Steep density $n_E < -3$           |                     | $\gamma_t = -3 + m_{3D}/2$       | $-8/3$               | Lazarian & Pogosyan (2000) |
# Two-dimensional (projected) structure function index $m$ vs three-dimensional power spectrum index $\kappa$.

- [Original discussion](https://github.com/JavGVastro/PhD.Paper/issues/18)
- We want to determine the correct power spectrum index which is input into simulation to obtain a projected power law of $1$.
- Here we present the criteria used to determined the relation between the index of the **two-dimensonal structure function** $m_{2\text{D}}$ and the index of the **three-dimensinal power spectrum** $\kappa_{\text{3D}}$.
- The motivation for this was to perform [numerical experiments](https://github.com/JavGVastro/VIENTO/tree/main/fake_maps) using Turbustat in a "realistic" way.

## Criteria I 

For an isotropic, power-law, three-dimensional power spectrum, the spectral index does not change on going from three dimensions to two (projected) dimensions:	

$$ \kappa_{2\text{D}} = \kappa_{\text{3D}} ,$$

where $\kappa_{N\text{D}}$ is the power spectrum spectral index in $N$ dimensions. 

- This is because the line-of-sight contribution to the line-of-sight velocity has no amplitude on the $k_z = 0$ plane, where $z$ is the line-of-sight direction [Medina et al 2014](https://ui.adsabs.harvard.edu/abs/2014MNRAS.445.1797M). **Effects of projection smearing or emissivity fluctuations are not taken into consideration.**  

## Criteria II

For homogeneous turbulence the relation between the $N-\text{dimensional}$ second-order structure function index  $m_{N\text{D}}$ and the $N-\text{dimensional}$ power spectrum index $\kappa_{N\text{D}}$ is ([Medina et al 2014](https://ui.adsabs.harvard.edu/abs/2014MNRAS.445.1797M)): 

$$ \kappa_{N\text{D}} = m_{N\text{D}} + N . $$


 So, for $N=3$: 
 
 $$ \kappa_{3\text{D}} = m_{3\text{D}} + 3 \therefore  m_{3\text{D}} = \kappa_{3\text{D}}  - 3$$
 
- Effects of projection smearing or emissivity fluctuations are not taken into consideration.

## Criteria III 

Considering **projection smoothing/smearing** from $3$ to $2$ dimensions we have:

$$m_{2\text{D}} = m_{3\text{D}} + 1$$

## Criteria IV

- The **change in the index is supposed to be caused by** 
	- projection smearing term and/or (Criteria III) "$+1$"
	- emissivity/density fluctuations, $\delta \kappa$: 

The relation between the two-dimensional second order structure function index and its three-dimensional counterpart is given by 

$$ m_{2\text{D}} = m_{3\text{D}} + 1 + \delta \kappa . \tag2$$

Solving for $m_{3\text{D}}$ and substituting with eq. of criteria II: $$m_{3\text{D}} = m_{2\text{D}}  - 1 - \delta \kappa$$ $$\kappa_{3\text{D}}  - 3 = m_{2\text{D}}  - 1 - \delta \kappa .$$ Now solving for $\kappa_{3\text{D}}$ we have and considering none $\delta \kappa = 0$ and strong emissivity fluctuations $\delta \kappa = -1$: 

$$\boxed{\kappa_{3\text{D}} = m_{2\text{D}} +3-1-0 = m_{2\text{D}}  + 2 \quad \quad  \text{non-emissivity fluctuations case}}$$

$$\boxed{ \kappa_{3\text{D}} =+3-1 - (-1) = m_{2\text{D}}  + 3 \quad \quad  \text{emissivity fluctuations case}.}$$

NOTE: In simulation the intensity of the fluctuations must be accounted, e.g., sigE = 0,1,2
# On the constancy of the index

#TBD 