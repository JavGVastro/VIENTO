
- Kolmogorov spectrum 
	- homogenous turbulence
	- Incompressible turbulence: changes in the pressure do not produce density variations; they push fluir around and only alter the velocity field.
- Features of turbulent flows
- Scales of turbulence
- One of the signatures on which we shall be relaying for the existence of turbulence is that there is a vorticity preset in the fluid..


# The correlation tensors and representation of the flows

From: [Shore - Astrophysical Hydrodynamics](<../Bibliography/Books/Astrophysical Hydrodynamics.md>)

- "We imagine that the flow in the fluid has a field which is a touch chaotic. This is only because the material has been assumed to be in a flow which has a fixed direction, but in which there may be eddies and waves which are not necessarily parallel to the mean velocity of the material. I.e., one of the signatures on which we shall be relying for the existence of turbulence is that there is a vorticity present in the fluid, although the mean value of the vorticity may vanish. In fact, it is the fact that the rms value of the vorticity does not vanish that gives rise to the basic signature of wat is usually called fully developed turbulent flow."
- Velocity field to have two basic components, a mean and a random component:

$$v_i (\vec{x}) = U_i(\vec{x}) + u_i(\vec{x})$$
where 

	$$ \langle v_i \rangle = Ui \quad, \langle u_i \rangle = 0 \quad, \langle u^2 \rangle \neq 0 $$

- "Here we have assumed that we have something stochastic which controls the fluctuations."
- Now take the statistical average over two component $i$ and $j$:

$$\langle v_i(\vec{x}) v_j(\vec{x'}) \rangle = Ui(\vec{x}) U_j(\vec{x'}) + R_{ij}(\vec{r})$$
- "We have used this to introduce the correlation tensor for a displacement $\vec{x'} = \vec{x} \pm \vec{r}$. This is the **two-point correlation tensor** for the velocity. It remains to show that this is related to the energy density of the turbulent velocity field and that the information contained in the two-point function in the important measure of the transport properties of a turbulent flow." 
- "We now define a quantity which is the correlation function averaged over the bulk of the fluid"

$$R_{ij}(\vec{r}) \equiv \langle u_i (\vec{x}) u_j (\vec{x} + \vec{r}) \rangle$$

- We define:

$$\Phi_{ij} (\vec{k}) = \frac{1}{2 \pi^3} \int R_{ij} (\vec{r})e^{-i \vec{k} \cdot \vec{r}} d\vec{r}$$

to be the Fourier transform of the correlation tensor.
- 'Notice that if the correlation tensor can be normalized (and this is, at this stage, by no means certain) we have a way of determining the mean value of the separation between the correlated quantities, a characteristic length scale of the turbulence."


$$ \Lambda \equiv \int R(r) dr $$
- If the medium is isotropic:

$$R_{ij} (\vec{r}) = R_{ij} (-\vec{r}) $$

- The correlation tensor for zero lag is:

$$R_{ij} (0) = \langle u_i u_j \rangle = \int \Phi_{ij} (\vec{k}) d\vec{k}$$

 - Thus, since this is  a quantity which has the dimensions of an energy, we see that the energy is giben by:

$$\int E(k)k^2dk = \int \Phi_{ii} (\vec{k}) d\vec{k}$$

- As a consequence of isotropy we have $\langle u_i u_j \rangle = 3 \langle u \rangle^2$. Here $\langle u^2 \rangle^{1/2}$ is some velocity dispersion
## Bibliography



# Kolmogorov -5/3 law (Classic theory)

- Based using the concept of cascade proposed by Richardson (1922).
- It is assumed that a driving force is present in a gaseous object with a dimension comparable to that of the largest dimension of the system. the ratio of dimensions to coefficient of viscosity, as expressed by the Reynolds number, is so large that the flow of gas is turbulent and not laminar. The energy of the mas motion at the largest scale, characterized by $\varepsilon$, the rate of energy input per unit mass, is  transferred without loss to a succession of progressively smaller mass elements. At the smallest scale one finally reaches a point where the Reynolds number becomes less than about unity and the flow stops being turbulent and the energy that has come down through the eddies of various sizes is deposited in the gas by thermal heating (viscous dissipation). 
- Kolmogorov showed that this process of loss-free-energy-cascade would lead to a relation between the root-mean-square velocity difference, $v$, of mass points of separation $r$ such that 

$$v^2 = (\varepsilon \times r)^{2/3}$$

Energy Cascade Spectrum

$$E(k, \epsilon) = C k^a \epsilon^b = C k^{-\frac{5}{3}} \varepsilon^{\frac{2}{3}}$$

$$E(k) \sim  k^{-\frac{5}{3}} \varepsilon^{\frac{2}{3}}$$ 



# Turbulence index


## Real space

- Subsonic incompressible flow (Kolmogorov theory)
	- $m_{3D} = 0.66 = 2/3$ 
- Subsonic compressible flow
	- $m_{3D} = 0.80 = 4/5$ 
- Supersonic compressible flow
	- $m_{3D} = 1.00$      

# Scales of turbulence

## Large Scales 

- Time

$$T = \frac{k}{\varepsilon}$$
- Length

$$L =T \sqrt{k} = \frac{k^{3/2}}{\varepsilon}$$


## Kolmogorov Scales (dissipative scales)

- Kolmogorov law apply to the inertial range. The Kolmogorov scales apply to the smallest scales, *dissipation subrange*, on the cascade. From [Dubin](<../Bibliography/Books/Statistical Theory and modeling for Turbulent Flows.md>) the suggestion to refer as them as the dissipative scales.

- Time

 $$\tau_k = \left( \frac{\nu}{\varepsilon} \right)^{\frac{1}{2}} \sim \dfrac{l}{u \text{Re}^{1/2}}$$
 - Length
 
 $$l_k = \left( \frac{\nu^3}{\varepsilon} \right)^{\frac{1}{4}} \sim \frac{L}{\text{Re}^{\frac{3}{4}}}$$
 - Velocity

$$u_k = \left( \nu \varepsilon \right)^{\frac{1}{4}}\sim \dfrac{u}{\text{Re}^{1/4}}$$


# On turbulence



>[!quote] [Turbulence: Kolmogorov, Nabukov, Heisenberg, Weizsäcker and Onsage](https://www.webofstories.com/play/benoit.mandelbrot/26)
>One thing I learned then, which was very important for later, was about turbulence. Kolmogorov's work- well it's a co-op between Kolmogorov, Nabukov, Heisenberg, Weizsäcker and Onsager- had done this work during the war, was now becoming known. It was totally disbelieved. Nobody thought it was right, but the quality of those men and the simplicity of the result and the strange nature of the arguments were very, very attractive, and so we had a number of lectures about turbulence which later on were essential to my life, because I both saw what had been done and I saw how difficult it was to verify, to believe it, and how beautiful it was. And let me say a few words about that. In the most extreme form of this argument, which I think is due to Onsager and not to Kolmogorov, the spectrum of turbulence, which is a great monument of human understanding, came out of pure thought; not out of the equation of flow motion, no relation whatsoever; not out of experience with flow motion, no relation whatsoever; just, if the spectrum were K-5/3 so many things would be nice and simple and convenient. It was a totally ridiculous kind of science, but at the same time extremely mystifying and also very attractive. How come that the human mind can, starting with principles so devoid of content, make predictions so full of content which one could try to verify and at that time one could not verify? So, I emphasise, it was very much a limbo, a world in which interesting things were being said but very little belief was attracted to it.
>\- Benoît Mandelbrot ^Benoit-Kolm

# Databases

- [Johns Hopkins Turbulence Databases](https://turbulence.idies.jhu.edu/home)
# Bibliography

- von Karman
- Taylor
- Dryden

## Thesis

- [On stability and turbulence of fluid flow](https://ntrs.nasa.gov/citations/19930093939)
	- [The Sad Story of Heisenberg's Doctoral Oral Exam](https://www.aps.org/archives/publications/apsnews/199801/heisenberg.cfm)

## Books

- [Batchelor - The Theory of Homogeneous Turbulence](<../Bibliography/Books/The Theory of Homogeneous Turbulence.md>)
- [Frisch - Turbulence](<../Bibliography/Books/Turbulence.md>)
- [Pope - Turbulent Flows](<../Bibliography/Books/Turbulent Flows.md>)
- [Shore - Astrophysical Hydrodynamics](<../Bibliography/Books/Astrophysical Hydrodynamics.md>)


## Divulgation YT

- [NSF Fluid Mechanics Series](https://www.youtube.com/watch?v=1_oyqLOqwnI&list=PL0EC6527BE871ABA3&index=12&ab_channel=BarryBelmont)
- [What Is Turbulence? Turbulent Fluid Dynamics are Everywhere](https://www.youtube.com/watch?v=v5IoP9Pc-Y0&ab_channel=SteveBrunton)
- [Understanding Laminar and Turbulent flow](https://www.youtube.com/watch?v=9A-uUG0WR0w&ab_channel=TheEfficientEngineer)
- [Why 5/3 is a fundamental constant for turbulence](https://www.youtube.com/watch?v=_UoTTq651dE&ab_channel=3Blue1Brown)
- [Turbulent Flow is MORE Awesome Than Laminar Flow](https://www.youtube.com/watch?v=5zI9sG3pjVU&ab_channel=Veritasium)
- [Turbulence: One of the great unsolved mysteries of physics](https://www.ted.com/talks/tomas_chor_turbulence_one_of_the_great_unsolved_mysteries_of_physics)
