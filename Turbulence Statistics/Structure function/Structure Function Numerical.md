- Comments and main ideas regarding the numerical implementation in Python for the second order structure function used in Garcia Vazquez et al 2023, where the structure function is used to study the fluctuations in the velocity field of in H II regions. 
- Once Dr. Will joined the project (phd epoch), his algorithm was adopted due to its greater efficiency, as it leverages the [[Numba]] package, which brings the speed of languages like C++ to Python.


# Numerical recipe

1. Load or create [[#1 Data|Data]]. Rearrange as columns.
	1. scattered data: This is used in this version since its input is a table/list with three columns.
	2. matrix form data
2. Determine the [[#2 Correlations|Correlations]] of the data.
3. Determine the [[#3 Lags|Lags]] of the data.
4. Determine [[#4 Bins and Grouping|Bins and grouping]]. Linear or logarithmic clustering.
5. [[#5 Plots|Plots]].
