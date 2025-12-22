- [The Spectral Correlation Function](https://lweb.cfa.harvard.edu/~agoodman/scf/SCF/scfmain.html)
- [The velocity structure of the Interstellar medium](https://lweb.cfa.harvard.edu/~agoodman/scf/velocity_methods.html)

The **Spatial Correlation Function (SCF)** is a measure of spectral similarity as a function of spatial separation. It quantifies how rapidly the structure of spectra decorrelates with distance.

For two spectra $S_1(v)$ and $S_2(v)$ at spatial positions separated by a distance $r$, the SCF is defined as:
$$\text{SCF}(r) = 1 - \left\langle \frac{ \sum_v | S_1(v) - S_2(v) |^2 }{ \sum_v \left( |S_1(v)|^2 + |S_2(v)|^2 \right) } \right\rangle_{|r_1 - r_2| = r}$$This function typically decays with increasing spatial separation, and a power-law decay indicates self-similar or fractal structure in the turbulence.
# The Spectral Correlation Function (SCF) Method

This method provides a new diagnostic of spectral-line maps, aimed at identifying physically meaningful velocity structure in the ISM. A large grid of spectra (data cube) is analyzed in order to determine how similar neighboring spectra are to one another. The method differs from more traditional [[Autocorrelation Function]] (ACF) or [[Structure Function]] (SF) analyses ([[Scalo 1984]]), in that it preserves spatial information. Both methods can produce information on how spectral properties vary with the separation of spectra in a map. The new "SCF" method dives this information, along with information on where in a map spectral changes occur. These changes can be quantitively correlated with changes in other mapped parameters, such as mean velocity, line width, integrated intensity, antenna temperature.

## Gradient filtering

Building n the velocity gradient-fitting methods, we are working on a new technique for measuring the variations in velocity gradient within a large region of the ISM. The program under development goes through a large data cube and fits a gradient localized region around each observed position. The resolution of the gradient filter can be adjusted so that maps of the "gradient field" which should relate to the velocity field, relevant to a range of spectral scales can be produced.
