- Projection smoothing or smearing ([[Scalo 1984]]): implies that the structure function index $m_\text{3D}$ is only observed directly for separations larger than the line-of-sight depth of the emitting regions.
- For smaller separations, one potentially observes a steeper slope: $$m_\text{2D} = m_\text{3D} + 1 + \delta\kappa ,$$ where $\delta\kappa$ represents the effects of [[On the density and emissivity fluctuations|emissivity fluctuations]] along the line of sight [Brunt:2004a](https://ui.adsabs.harvard.edu/abs/2004ApJ...604..196B) , and varies from $\delta\kappa = 0$ in the incompressible limit to $\delta\kappa = -1$ in the case of strongly driven supersonic turbulence.
- In this latter case, the effects of projection smoothing and emissivity fluctuations cancel out, leading once more to $m_\text{2D} \approx m_\text{3D}$.


# Review

 \citep{od1987, 1966igd..book.....K, munch1958internal, von1951methode} han desarrollado modelos teóricos, que consideran un promedio adicional a la función de estructura, para comparar con las observaciones. 
\cite{kaplan} presentan un desarrollo de estos modelos y a continuación presentamos los resultados principales.

Considerando la Fig. \ref{fig:Kaplan}:

\begin{enumerate}

1. Se considera un sistema de masa de elementos puntuales turbulentos situados a una misma distancia $R$ del observador. Considerando las mediciones de una propiedad física $a$ se construye la función de auto correlación en función de la separación angular, $\alpha=\alpha '-\alpha''$:
  
$$  A_n (\alpha) = \overline{ \vert a (\alpha ') - a (\alpha '') \vert^{2} } = B_n (2R \sin (\alpha/2)) $$

 2.  En esta otra situación se asume que los elementos estudiados están situados a distancias diferentes a lo largo de linea de visión de extensión $R$. Se obtiene que se multiplica el argumento de la función de estructura por la distancia que separa estos elementos situados a distancias $y_{1}$ y $y_{2}$:
  

$$  A^{I}_{n}(\alpha)= \overline{ \vert a(\alpha ')-a(\alpha '') \vert^{2}}$$

  

$$   = \dfrac{1}{R^{2}}\int^{R}_{0}\int^{R}_{0} B_{n} (\sqrt{y^{2}_{1}+y^{2}_{2}+2y_{1}y_{2}cos \alpha})dy_{1}dy_{2}
$$
  
 3. En este caso se considera que estamos en posición de medir los puntos promediados a través de la línea de vision:
  

$$  A^{II}_{n}(\alpha)= \overline{ \vert \dfrac{1}{R} \int^{R}_{0} a(y_{1},\alpha ')dy_{1}-\int^{R}_{0} a(y_{2},\alpha ')dy_{2} \vert^{2}}$$

  

$$  A^{II}_{n}(\alpha)= A^{I}_{n}(\alpha) - A^{I}_{n}(0)$$

  
 4. Ahora se considera una nebulosa de dimensión $R$, donde las línea de visión se asumen paralelas y los planos separados por una distancia $x$:
  

  $$ A^{III}_{n}(x)= \dfrac{1}{R^{2}}\int^{R}_{0}\int^{R}_{0} B_{n} (\sqrt{x^{2}-(y_{1}-y_{2})^{2}})dy_{1}dy_{2}$$

  

$$  A^{IV}_{n}(x)= A^{I}_{n}(\alpha) - A^{I}_{n}(0)$$

  


%\begin{figure}
%\centering \includegraphics[width=5in]{Imagenes/TurbISM/Kaplan1}\caption{Las cuatro situaciones que analiza \cite{kaplan} para resolver el problema de las observaciones y efectos de proyección de la función de estructura al analizar las propiedades físicas entre dos puntos.}
%\label{fig:Kaplan}
%\end{figure}

Las ecuaciones \ref{eq:kap4} y \ref{eq:kap5} corresponden al modelo presentado por \cite{von1951methode}.

Los modelos presentados por \cite{od1987} tienen correspondencia con los casos presentados por \cite{kaplan}. 

Para el caso I y II la correspondencia es el llamado 'Modelo 0' de \citeauthor{od1987}, donde la nebulosa tiene el tamaño suficiente para que no haya traslape en el espectro. 
Este modelo predice una dependencia de \num{1/3} de la velocidad con la longitud y lineas solo con ensanchamiento térmico. 

El 'Modelo I' de \cite{od1987} considera una geometría plana paralela con suficiente profundidad $R$ que interfecta un conjunto de elementos turbulentos, correspondiendo al caso IV.

Lo anterior ha llevado a concluir que es posible modificar el exponente teórico en función de una situación/geometría particular ó que la diferencia de el exponente observado y el exponente teórico contiene información sobre la geometría o alguna otra propiedad del objeto.

\citet{1966igd..book.....K} menciona que a primera aproximación sería posible resolver algunas de las ecuaciones X y comparar con las observaciones astronómicas.
Como ejemplo propone usar la función


$$B(r) = \frac{\text{const}}{1+ \left( \frac{L}{r} \right) ^n }$$

donde $L$ es la escala básica de turbulencia (o longitud de correlación $r_0$ en este trabajo) y $n$ el índice de la función de estructura; este último es $m$ en la nomenclatura usada en este trabajo.
Finalmente, el problema  de la turbulencia en el medio interestelar es determinar los valores de $L$ y $n$ para un conjunto de observaciones tal como se ha realizado en este trabajo

