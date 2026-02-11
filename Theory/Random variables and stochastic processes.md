# Random signals and distributions

From: [Poularikas - Adaptive Filtering Primer with MATLAB](<../Bibliography/Books/Adaptive Filtering Primer with MATLAB.md>)

- Most signals in practice are not deterministic and can not be described by precise mathematical analysis, and therefore we must characterize them in probabilistic terms using the tools of statistical analysis.
- A **discrete random signal** $\{ X{n} \}$ is a sequence of indexed *random variables* (rv's) assuming the values:

$$\{ x(0), x(1), x(2), \dots \} .$$

- The random sequence with values $\{ x(n) \}$ is discrete with respect to sampling index $n$. Here we will assume that the random variable at any time $n$ is a continuous function, and therefore, it is a continuous rv at any time $n$. this type of sequence is also know as *time series*.
- A particular rv, $X(n)$, is characterized by its *probability density function* (pdf), $f(x(n)) :$

$$ f(x(n)) = \dfrac{\partial F (x(n))}{ \partial x(n)} $$
and its *cumulative density function* (cfd), $F(x(n)) :$

$$F(x(n)) =p(X(n) \leq x(n)) = \int^{x(n)}_{- \infty} f(y(n))dy(n) .$$

- $p(X(n) \leq x(n))$ is the probability that the rv $X(n)$ will take values less than or equal to $x(n)$ at time $n$. As the value of $x(n)$ goes to infinity, $F(x(n))$ approaches unity.
- Multivariate distributions of rv: #TBD 
- To obtain a formal definition of a discrete-time stochastic process, we consider an experiment with a finite or infinite number of unpredictable outcomes from a sample space, $S(z_1, z_2, ...)$, each one occurring with a probability $p(z_i) .$
- Next, by some rule we assign a deterministic sequence $x(n,z_i), -\infty < n < \infty ,$ to each element $z_i$ of the sample space.
- The sample space, the probabilities of each outcome, and the sequences constitute a **discrete-time stochastic process** or **random sequence**.
- From this definition we obtain the following four interpretations:
	- $x(n,z)$ is an rv if $n$ is fixed and $z$ is variable.
	- $x(n,z)$ is a sample sequence called realization if $z$ is fixed and $n$ is variable.
	- $x(n,z)$ is a number if both $n$ and $z$ are fixed.
	- $x(n,z)$ is a stochastic process if both $n$ and $z$ are variables.
- Each time we run an experiment under identical conditions, we create a sequence of rv's $\{ X(n) \} ,$ which is known as a realization and constitutes an event. 
- A realization is one member of a set called the ensemble of all possible results from the repetition of an experiment.

## Stationary and ergodic processes

# Averages

## Mean value

## Correlation

## Covariance

## Stationary processes

- Wide-sense stationary process...

# Special random signals and probability density functions

## White noise

# Wiener-Khintchin relations

# Autoregressive moving average process (ARMA)

## Autoregressive process (AR)