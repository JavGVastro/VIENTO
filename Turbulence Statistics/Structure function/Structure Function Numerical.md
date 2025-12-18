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


# Loading data

The input data are: $x$, $y$, and $f$, in which the first two are coordinates and a physical property or value $f$, which is the value to correlate with itself. In the context of [[Turbulence]]  $f$ would be velocity or density. 

Input data as a list: 

$$
\{x,y,f\}  =
\begin{bmatrix} 
x_0 & y_0  & f_0 \\ 
x_1 & y_1  & f_1 \\ 
x_2 & y_2  & f_2 \\ 
\vdots & \vdots & \vdots \\
x_n & y_n & f_n  
\end{bmatrix} 
$$
 
Input data as matrix: 

$$
\{x,y,f\}  = 
\begin{bmatrix}
f_{11} & f_{12}  & \dots \\  
f_{21} & f_{22}  & \dots \\  
f_{31} & f_{32}  & \dots \\ 
\vdots & \vdots & \ddots \\ 
f_{n1} & f_{n2} & f_{nn}  
\end{bmatrix}
$$

where the columns would be the $x$ coordinate and the rows the $y$ coordinate in relation to expression $1$.

# Correlations computations

## Toy model

- They "toy model" is the numerical approach where each correlation value is computed independently, making it good as a didactic tool but impractical for research purposes. For an efficient case the algorithm use the Pythonic option to  vectorize an operation to an entire array.
- This algorithm uses for loops and list comprehension methods.

Computations of the **squared velocity difference** for the  Second-order structure function: 

$$b_{ij}=(f_i-f_j)^2 \quad \forall  \quad i>j \tag3$$


$$
B  = 
\begin{bmatrix} 
(f_{0}-f_{0})^2 & 0 & 0 & 0 & 0 \\ 
(f_{1}-f_{0})^2 & (f_{1}-f_{1})^2 & 0 & 0 & 0 \\ 
(f_{2}-f_{0})^2 & (f_{2}-f_{1})^2 & (f_{2}-f_{2})^2 & 0 & 0 \\ 
\vdots &  \vdots &  \vdots & \ddots & \vdots \\ 
(f_{n}-f_{0})^2 & (f_{n}-f_{1})^2 & (f_{n}-f_{2})^2 & \cdots & (f_{n}-f_{n})^2 
\end{bmatrix}$$

or computations of the **products** for the Autocorrelation Function: 


$$c_{ij}=f_i \cdot f_j \quad \forall  \quad i>j \tag4$$


$$
C  = 
\begin{bmatrix} 
(f_{0}f_{0}) & 0 & 0 & 0 & 0 \\ 
(f_{1}f_{0}) & (f_{1}f_{1}) & 0 & 0 & 0 \\ 
(f_{2}f_{0}) & (f_{2}f_{1}) & (f_{2}f_{2}) & 0 & 0 \\ 
\vdots &  \vdots &  \vdots & \ddots & \vdots \\
(f_{n}f_{0}) & (f_{n}f_{1}) & (f_{n}f_{2}) & \cdots & (f_{n}f_{n}) 
\end{bmatrix}
$$



- Matrices $B$ and $C$  are the covariance of value $f$. The condition $i>j$ guarantees to the matrix is of the [triangular form](https://en.wikipedia.org/wiki/Triangular_matrix). 
- The previous conditions guarantees that there are **zeros values in the main diagonal**. Therefore matrix $A$ is lower triangular matrix or **left triangular matrix**, $L$.  
- Note that the diagonals are the **lags**. Therefore, main diagonal correspond to $\text{lag} \ 0$, the diagonal below correspond to $\text{lag} \ 1$, an so on. 


Computation of the **lags**: 

$$l_{ij}=\sqrt{ (x_i-x_j)^2+(y_i-y_j)^2 } = \sqrt{\Delta x_{ij}^2 - \Delta y_{ij}^2} \quad \forall  \quad i>j \tag2$$


where matrix $L$ is the matrix having al the lags values: 

$$
A  =
\begin{bmatrix} 
\sqrt{\Delta x_{00}^2 - \Delta y_{00}^2} & 0 & 0 & 0 & 0 \\ 
\sqrt{\Delta x_{10}^2 - \Delta y_{10}^2} & \sqrt{\Delta x_{11}^2 - \Delta y_{11}^2} & 0 & 0 & 0 \\ 
\sqrt{\Delta x_{20}^2 - \Delta y_{20}^2} & \sqrt{\Delta x_{21}^2 - \Delta y_{21}^2} & \sqrt{\Delta x_{22}^2 - \Delta y_{22}^2} & 0 & 0 \\ 
\vdots &  \vdots &  \vdots & \ddots & \vdots \\ 
\sqrt{\Delta x_{n0}^2 - \Delta y_{n0}^2} & \sqrt{\Delta x_{n1}^2 - \Delta y_{n1}^2} & \sqrt{\Delta x_{n2}^2 - \Delta y_{n2}^2}  & \cdots & \sqrt{\Delta x_{nn}^2 - \Delta y_{nn}^2} 
\end{bmatrix}
$$


## Production model (Vectorization)

**Correlations:**

Having the  vector $\vec{f}$:

$$\vec{f} = [f_0, f_1, f_2, \dots, f_n ] ,$$

the following vectorized operation is performed:

$$[\vec{f}]-\vec{f}$$

which implies the operations 

$$[f_0]-[f_0, f_1, f_2, \dots, f_n ] ,$$

$$[f_1]-[f_0, f_1, f_2, \dots, f_n ],$$

$$\dots ,$$

$$[f_n]-[f_0, f_1, f_2, \dots, f_n ]$$

are performed at the same time. The results is:

$$
[\vec{f}]-\vec{f}  = 
\begin{bmatrix}  
[f_0-f_0,f_0-f_1,f_0-f_2, \dots,f_0-f_n] \\ 
[f_1-f_0,f_1-f_1,f_1-f_2, \dots,f_1-f_n] \\ 
[f_2-f_0,f_2-f_1,f_2-f_2, \dots,f_2-f_n]  \\ 
[f_3-f_0,f_3-f_1,f_3-f_2, \dots,f_3-f_n]  \\ 
\vdots \\  
[f_n-f_0,f_n-f_1,f_n-f_2, \dots,f_n-f_n]  
\end{bmatrix}$$

Applying the lower triangular matrix and squaring each velocity difference we have the matrix:

$$
([\vec{f}]-\vec{f})^2  =  
\begin{bmatrix} 
(f_0-f_0)^2 & 0 & 0 & 0  \\
(f_1-f_0)^2 & (f_1-f_1)^2 & \dots  \\
(f_2-f_0)^2 & (f_2-f_1)^2 & (f_2-f_2)^2 & \vdots \\ 
\vdots   \\
(f_n-f_0)^2 & (f_n-f_1)^2& \dots & (f_n-f_n)^2
\end{bmatrix}$$

which is the same result as matrix $B$.

**Lags:**

Having the  vector $\vec{x}$:

$$\vec{x} = [x_0, x_1, x_2, \dots, x_n ] ,$$


the following vectorized operation is performed:

$$[\vec{x}]-\vec{x}$$

which implies the operations 

$$[x_0]-[x_0, x_1, x_2, \dots, x_n ] ,$$

$$[x_1]-[x_0, x_1, x_2, \dots, x_n ],$$ 

$$\dots ,$$ 

$$[x_n]-[x_0, x_1, x_2, \dots, x_n ]$$

# Grouping, binning and descriptive statistics of the correlations and lags

Creation and arrange of matrix $C$ that contains the results form matrix $A$, $(\Delta V^2)$, and matrix $B$, $r$, applying the condition $\text{Mat } A, \text{ Mat } B > 0$.  Also, logarithmic values are added: 

$$
C =
\{\Delta V^2, r, \log \Delta V^2, \log r\}  =
\begin{bmatrix} a_{00} & b_{00} & \log a_{00} & \log b_{00}  \\ 
a_{10} & b_{10} &  \log a_{10} & \log b_{10}  \\  
b_{20} & b_{20} &  \log a_{20} & \log b_{20}  \\ 
a_{21} & b_{21} &  \log a_{21} & \log b_{21}   \\ 
\vdots & \vdots & \vdots & \vdots  \\ 
a_{nn} & b_{nn} & \log a_{nn} & \log b_{nn} 
\end{bmatrix}$$


## Logarithmic binning

- Defining a Dex of: $\text{dlogs} = 0.1 = 10^{0.1}$
- The number of bins is obtained as: 

$$ \text{number bins} (i) = \text{int} \left( \frac{b_\text{max} - b_\text{min}}{\text{dlogs}} + \frac{1}{2 \cdot \text{dlogs}} \right)$$


- Therefore, the range of each bin is obtained as 

$$0 + i \cdot \text{dlogs} \quad , \quad i \cdot \text{dlogs} +i \cdot \text{dlogs} $$

- The outcome is a like dictionary where each entry are the lags and velocity differences (indexes along their logarithmic values) between the specified values (keys).

# Structure Function Numba (Dr. Will Henney script)

- [ ] Add Dr. Will's original Jupyter notebook

`structfunc_numba_parallel()`
Naive Python algorithm with Numba for parallel processing

**Function Signature and Docstring**

```python
def strucfunc_numba_parallel(vmap, dlogr=0.15, wmap=None, wmin_factor=1e-3): """Calculate structure function via naive python algorithm"""
```

- `vmap`: matrix numpy array
- `dlogr`: bin size of the logarithmic "radius" `r`
- `wmap`: a 2D array (weight map) that assigns weights to each element in  in `vmap`
- `wmin_factor`: A factor to determine the minimum weight threshold

**Initialization and Parameters**

```python
    ny, nx = vmap.shape
    if wmap is None:
        wmap = np.ones((ny, nx))
    wmin = wmin_factor * np.nanmax(wmap)
    maxr = np.hypot(nx, ny)
    nr = int(np.log10(maxr) / dlogr)
    logr = np.arange(nr) * dlogr
    sf = np.zeros((nr,))
    nsf = np.zeros((nr,), dtype=np.int64)
    wsf = np.zeros((nr,))
    weight = np.zeros((nr,))

```

- `ny, nx`: Dimensions of the velocity map.
- `wmap`: Initializes the weight map to ones if `None`.
- `wmin`: Minimum weight threshold, calculated as a fraction of the maximum weight in `wmap`.
- `maxr`: The maximum radius, which is the hypotenuse of the map dimensions.
- `nr`: Number of bins for the logarithm of the radius.
- `logr`: Array of logarithmic radius bin edges.
- `sf`, `nsf`, `wsf`, `weight`: Arrays to store the structure function, number of pairs, weighted structure function, and sum of weights, respectively.

**Call to the Helper Function**

The helper function `_strucfunc_numba_parallel` is called to perform the parallel computation.
```python
sf, weight, wsf, nsf = _strucfunc_numba_parallel( ny, nx, nr, vmap, wmap, wmin, dlogr, maxr, sf, weight, wsf, nsf )
```

**Return Dictionary**

``` python
    return {'log10 r': logr,
            'Sum dv^2': sf,
            'Sum weights': weight,
            'Sum w * dv^2': wsf,
            'N pairs': nsf,
            'Unweighted B(r)': sf/nsf,
            'Weighted B(r)': wsf/weight}

```

The function returns a dictionary with the computed results:

- `log10 r`: Logarithm of the radius bins.
- `Sum dv^2`: Sum of squared differences of velocities.
- `Sum weights`: Sum of weights.
- `Sum w * dv^2`: Weighted sum of squared differences.
- `N pairs`: Number of pairs for each radius bin.
- `Unweighted B(r)`: Unweighted structure function.
- `Weighted B(r)`: Weighted structure function.


**Function Signature**

```python
@numba.jit(nopython=True, parallel=True) def _strucfunc_numba_parallel( ny, nx, nr, vmap, wmap, wmin, dlogr, maxr, sf, weight, wsf, nsf ):
```

The function parameters:

- `ny, nx, nr`: Dimensions of the velocity map and number of radius bins.
- `vmap, wmap`: Velocity map and weight map.
- `wmin, dlogr, maxr`: Minimum weight, logarithm of the radius bin size, and maximum radius.
- `sf, weight, wsf, nsf`: Arrays to accumulate the results.

**Initialization of Temporary Arrays**

```python
    _sf = np.zeros((ny, nr))
    _weight = np.zeros((ny, nr))
    _wsf = np.zeros((ny, nr))
    _nsf = np.zeros((ny, nr), dtype=np.int64)
```


**Outer Parallel Loop**

```python
    for j in numba.prange(ny):
        for i in range(nx):
            for jj in range(ny):
                for ii in range(i+1, nx):
                    r = np.hypot(ii - i, jj - j)
                    ir = int(np.log10(r) / dlogr)
                    if 0 <= ir < nr:
                        dvsq = (vmap[jj, ii] - vmap[j, i])**2
                        if (wmap[j, i] > wmin) and (wmap[jj, ii] > wmin):
                            _sf[j, ir] += dvsq
                            _nsf[j, ir] += 1
                        w = wmap[j, i] * wmap[jj, ii]
                        _wsf[j, ir] += w * dvsq
                        _weight[j, ir] += w

```

- The outer loop `for j in numba.prange(ny)` runs in parallel.
- For each pixel `(i, j)` in the velocity map, it calculates the distance `r` to all other pixels `(ii, jj)`.
- It bins the distances into logarithmic bins.
- It computes the squared velocity differences `dvsq`.
- If both pixels have weights above the minimum threshold, it updates the temporary arrays with the calculated values.

**Summing Partial Results**
```python
sf = np.sum(_sf, axis=0) 
weight = np.sum(_weight, axis=0) 
wsf = np.sum(_wsf, axis=0) 
nsf = np.sum(_nsf, axis=0) 
return sf, weight, wsf, nsf
```

The partial results are summed across all rows to get the final arrays `sf`, `weight`, `wsf`, and `nsf`.
