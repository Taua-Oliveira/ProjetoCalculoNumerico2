# Metodologia — Métodos Numéricos Aplicados

## 1. Sistemas Lineares — Métodos Diretos (Tópico 1)

### Método utilizado: Decomposição LU

A decomposição LU fatora a matriz de coeficientes **A** em dois fatores:

$$A = LU$$

onde **L** é triangular inferior com 1s na diagonal e **U** é triangular superior. A solução do sistema **Ax = b** se reduz a resolver dois sistemas triangulares:

$$
egin{cases}
Ly = Pb \ 
Ux = y
\end{cases}
$$

O pivoteamento parcial (**P**) garante estabilidade numérica evitando divisão por zero ou por valores muito pequenos.

**Aplicação no problema T1.P1:** O sistema modela o balanço de materiais (cobre, zinco, vidro) para produzir transistores, resistores e chips. A matriz é bem condicionada e a solução é exata (residual ≈ 0).

---

## 2. Sistemas Lineares — Métodos Iterativos (Tópico 2)

### Método utilizado: Gauss-Seidel com critério de Sassenfeld

O método de Gauss-Seidel atualiza iterativamente cada componente da solução usando os valores mais recentes já calculados na mesma iteração:

$$x_i^{(k+1)} = \dfrac{1}{a_{ii}}\left(b_i - \sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)}ight)$$

O **critério de Sassenfeld** garante convergência:

$$eta_i = \dfrac{1}{|a_{ii}|}\left(\sum_{j=1}^{i-1}|a_{ij}|eta_j + \sum_{j=i+1}^{n}|a_{ij}|ight) < 1, \quad orall i$$

**Aplicação no problema T2.P1:** A ponte de Wheatstone gera um sistema 2×2 para os potenciais nos nós B e C. O critério de Sassenfeld é satisfeito e o método converge em 5 iterações.

---

## 3. Ajuste de Curvas — Mínimos Quadrados (Tópico 3)

### Modelos ajustados

| Modelo | Transformação | Sistema |
|--------|--------------|---------|
| **Reta** | $y = a + bx$ | $egin{bmatrix}n & \Sigma x\ \Sigma x & \Sigma x^2\end{bmatrix}egin{bmatrix}a\b\end{bmatrix}=egin{bmatrix}\Sigma y\\Sigma xy\end{bmatrix}$ |
| **Parábola** | $y = a + bx + cx^2$ | Sistema 3×3 com $\Sigma x^3$, $\Sigma x^4$ |
| **Exponencial** | $y = ae^{bx} 	o \ln y = \ln a + bx$ | Linearização via logaritmo |

O **erro quadrático** $\sum (y_i - \hat{y}_i)^2$ seleciona o melhor modelo (parábola, neste caso).

---

## 4. Integração Numérica (Tópico 4)

### Regras compostas

| Método | Fórmula |
|--------|----------|
| **Trapézio** | $\int_a^b f(x)dx pprox \dfrac{h}{2}\left[y_0 + 2\sum_{i=1}^{n-1} y_i + y_night]$ |
| **Simpson** | $\int_a^b f(x)dx pprox \dfrac{h}{3}\left[y_0 + 4\sum_{	ext{ímpares}} y_i + 2\sum_{	ext{pares}} y_i + y_night]$ (n par) |

Simpson é mais preciso para funções suaves e foi aplicável (n = 6 intervalos, par).

---

> **Referências:** Ruggiero & Lopes (2016); Burden & Faires (2016); notas de aula LES710C.
