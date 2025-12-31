


**TL;DR:** In this folder we develop the relevant topics related to the ISM, particularly H II regions, which come from the hypothesis the ionized gas is [turbulent](<Turbulence.md>) .

# Turbulence in the interstellar medium
## Continuous-medium hypothesis

The idea of treating the interstellar medium—and, in our particular case, ionized regions—from the standpoint of fluid mechanics comes from considering this medium under the **continuous-medium hypothesis**. This hypothesis is validated using the **Knudsen number** \citep{Knudsen1935}, defined as:

$$
\text {Kn} = \dfrac{\lambda_{\text{mfp}}}{l} 
$$

where $\lambda_\text{mfp}$ is the mean free path of the medium (*mean free path*) and $l$ is a characteristic length scale of the phenomenon under study.

Taking into account:
- $\lambda_{\text{HII}} = 2.7e-7 \ \text{pc}$ \citep{1941ApJ....93..369S}
- and $l_{\text{HII}} = 1 \ \text{pc}$ for ionized regions

one obtains:

$$\text {Kn}_{\text{HII}} = \frac{l_{\text{HII}}}{\lambda_{\text{HII}}} \approx 10^{-7}.$$

In general, the continuous-medium hypothesis is valid for $\text{Kn} \ll 1$ \citep{astflo}.


## Reynolds number

In astrophysics, it is possible to approximate the **Reynolds number** \citep{1883Reynolds} by defining:

- the kinematic viscosity as $\nu \sim c_{s}\lambda$ \citep{ryden09},
- the Mach number as $\textbf{\textit{M}} = v / c_{s}$ \citep{white},
- and the mean free path as $\lambda_\text{mfp}= 1 / \langle n \rangle \sigma_{cs}$ \citep{Leqism}.  

In the expressions above, the term $c_s$ is the sound speed in the medium, $\langle n \rangle$ is the mean density of the medium, and $\sigma_{cs}$ is the collision cross section of the particles in the medium. Substituting the expressions above into the definition of $\text{Re}$ (equation~\ref{eq:Re}) yields:

$$
\text{Re} \approx \dfrac{v l}{c_s \lambda_\text{mfp}} \approx \dfrac{\textbf{\textit{M}} \ l}{\lambda_\text{mfp}} \sim \textbf{\textit{M}} \ l \ \langle n \rangle \ \sigma_{cs}
$$

With this analysis, it is possible to show that, for typical interstellar-medium conditions such as:

- a Mach number between $0.5$ and $3$,
- characteristic length scales $10 <  l  <  10^{3} \ \text{pc}$,
- typical densities $1 <\langle n \rangle <   10^{4}  \ \text{cm}^{-3}$,
- $\lambda_{\text{hii}} = 2.7 \times  10^{-7} \text{pc}$ and $\sigma_H \sim  10^{-15} \  \text{cm}^2$,

the conditions for a turbulent regime will be satisfied, with a range:

$$
 10^{2}< \text{Re}_{\text{HII}} < 10^{9}\ .
$$

## Taylor hypothesis

It is assumed that fluctuations in physical properties are stochastic in nature. Such processes assume an average taken over a volume, a time interval, or a distance. By considering that the data samples span sufficiently large distances (length scales) or times, this mean value accurately describes the phenomenon being measured \citep{Shore}. As an example, in equation~\ref{eq:aleatorio} the term $\overline{u(x)}$ denotes this mean value of the velocity.

In practice, this is done by computing the spatial average over a volume \(V\):

$$
\overline{\mathbf{u}} = \frac{1}{V} \int_V \mathbf{u} d^3x   
$$

or over a time interval $\tau$:

$$
\overline{\mathbf{u}} = \frac{1}{\tau} \int_t ^{t+\tau} \mathbf{u} dt
$$

The **Taylor hypothesis** \citep{taylor1938} treats the two expressions above as equivalent. Thus, in a situation where turbulence is fully developed, both the spatial and temporal descriptions are valid \citep{ryden09}. Therefore, the description presented in Appendix~\ref{sec:turbulencia_stats}, which is related to temporal variations, also holds for spatial variations. As mentioned previously, this is important because astronomical observations are a “snapshot,” and the hypothesis above allows turbulent theory to be applied to H II regions.
