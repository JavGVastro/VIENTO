
 
 - The aim of the next script aims to stablish a way to obtain the **power spectral density** of a 2D image. 
 - In our case we are interested in studying GEHRs radial velocity fields
 - The results are compared with the $-5/3$ **Kolmogorov law**. 
 - Different numerical methods are discussed.    


Obtaining the [[Power Spectrum#Power Spectral Density (PSD)|PSD]] 
1. From an image:
	1. FFT on the matrix (Image)
	2. Shifting Frequency (Wavenumbers) components: Nyquist freq. at the corners.
	3. Calculate the radial average of the transformed shifted image. The startig point is the center of the image and the average is made around 'rings' having a particular distance from this point.
		1. [Using the ndimage sum and avergae option](https://medium.com/tangibit-studios/2d-spectrum-characterization-e288f255cc59)
		2. Doing by "hand" the ndimage stuff
		3. [Using the codes radial_data and radialProfile](https://www.astrobetter.com/blog/2010/03/03/fourier-transforms-of-images-in-python/)
	4. Plotting these averages vs wavenumbers and perform comparison with [[Turbustat]]
2. Using the [[Fourier Transform#Wiener-Khinchin relation|Wiener-Khinchin relation]] ([[Aller 1951]])
	1. Compute the autocorrelation function.
	2. Compute the Fourier transform of the autocorrelation function.


# Notes

- Implementación numérica en Python para obtener la **densidad de energía espectral en una dimensión** del espectro, [[Power Spectrum]] (energía, potencia), de un conjunto de datos bidimensionales (imagen).
- En otras palabras, se promedia radialmente ([[#Radial average]]) la transformada de Fourier bidimensional de la imagen.

- Nutshell
	- Numerical implementation in #Python of the #radial_average in a two-dimensional #FourierTransform of an image to obtain the #1Dpsd for measuring #turbulence #turbulenceISM .
- Prereq
	 - [[Fourier Transform]]
- Biblio
	-  [2D Spectrum Characterization](https://medium.com/tangibit-studios/2d-spectrum-characterization-e288f255cc59)
	-  [Python radial profiles](https://www.astrobetter.com/wiki/python_radial_profiles)
	- [Python Image fft](https://www.astrobetter.com/wiki/tiki-index.php?page=python_image_fft)
	- Lazarian and Pogosyan 2000
	- [Turbustat](https://turbustat.readthedocs.io/en/latest/tutorials/statistics/pspec_example.html#pspec-tutorial)

