# Metodologia — Métodos Numéricos Aplicados

Todos os métodos estão implementados à mão em [`src/metodos/`](../src/metodos/), um arquivo por tópico. O `numpy` só guarda os vetores e as matrizes.

---

## 1. Sistemas lineares — métodos diretos (Tópico 1, Problema 1)

### Modelagem

Incógnitas: $x_1$ = transistores, $x_2$ = resistores, $x_3$ = chips. Cada equação diz que o consumo total de um material é igual à quantidade disponível:

$$
\begin{cases}
4x_1 + 3x_2 + 2x_3 = 960 & \text{(cobre)}\\
1x_1 + 3x_2 + 1x_3 = 510 & \text{(zinco)}\\
2x_1 + 1x_2 + 3x_3 = 610 & \text{(vidro)}
\end{cases}
$$

### Decomposição LU com pivoteamento parcial

A matriz é fatorada como $PA = LU$, onde $L$ é triangular inferior com diagonal unitária (guarda os multiplicadores $m_{ik} = u_{ik}/u_{kk}$) e $U$ é triangular superior. Em cada etapa $k$, a linha com maior $|a_{ik}|$ é trazida para a posição de pivô. Depois resolvem-se dois sistemas triangulares:

$$
Ly = Pb \quad \text{(substituição progressiva)}, \qquad Ux = y \quad \text{(substituição retroativa)}
$$

**Resultado:** $x = (120,\ 100,\ 90)$, com resíduo $\|Ax-b\|_\infty = 0$.

---

## 2. Sistemas lineares — métodos iterativos (Tópico 2, Problema 1)

### Modelagem da Ponte de Wheatstone

A fonte $E$ fica entre os nós A (potencial $E$) e D (potencial 0). Aplicando a lei dos nós de Kirchhoff em B e C:

$$
\begin{cases}
\left(\dfrac{1}{R_1}+\dfrac{1}{R_4}+\dfrac{1}{R_5}\right)V_B - \dfrac{1}{R_5}V_C = \dfrac{E}{R_1}\\[2mm]
-\dfrac{1}{R_5}V_B + \left(\dfrac{1}{R_2}+\dfrac{1}{R_3}+\dfrac{1}{R_5}\right)V_C = \dfrac{E}{R_2}
\end{cases}
$$

As correntes saem da lei de Ohm: $I_1 = (E-V_B)/R_1$, $I_2 = (E-V_C)/R_2$, $I_3 = V_C/R_3$, $I_4 = V_B/R_4$, $I_5 = (V_B-V_C)/R_5$ e $I_6 = I_1 + I_2$.

### Método de Gauss-Seidel

$$
x_i^{(k+1)} = \frac{1}{a_{ii}}\left(b_i - \sum_{j<i} a_{ij}x_j^{(k+1)} - \sum_{j>i} a_{ij}x_j^{(k)}\right)
$$

- **Aproximação inicial:** $x_i^{(0)} = b_i / a_{ii}$.
- **Critério de parada:** $\dfrac{\max_i |x_i^{(k+1)} - x_i^{(k)}|}{\max_i |x_i^{(k+1)}|} < \varepsilon$, com $\varepsilon = 10^{-4}$.
- **Convergência (critério de Sassenfeld):** $\beta_i = \dfrac{1}{|a_{ii}|}\left(\sum_{j<i}|a_{ij}|\beta_j + \sum_{j>i}|a_{ij}|\right)$. Se $\max\beta_i < 1$, a convergência é garantida.

**Resultado** ($E = 30$ V, $R_1 = 20\ \Omega$, demais $= 120\ \Omega$): $\beta = (0{,}125;\ 0{,}042)$, convergência em 4 iterações, $V_B \approx 24{,}7825$ V, $V_C \approx 18{,}2608$ V, $I_1 \approx 0{,}2609$ A, $I_2 \approx 0{,}0978$ A, $I_3 \approx 0{,}1522$ A, $I_4 \approx 0{,}2065$ A, $I_5 \approx 0{,}0543$ A e $I_6 \approx 0{,}3587$ A.

---

## 3. Ajuste de curvas — mínimos quadrados (Tópico 3, Problema 3)

Minimiza-se $\sum [F(x_i) - G(x_i)]^2$ resolvendo as **equações normais** (por LU):

| Modelo | Forma | Equações normais |
|---|---|---|
| Reta | $G(x) = a + bx$ | $\begin{bmatrix} n & \sum x \\ \sum x & \sum x^2 \end{bmatrix}\begin{bmatrix} a\\ b\end{bmatrix} = \begin{bmatrix}\sum y\\ \sum xy\end{bmatrix}$ |
| Parábola | $G(x) = a + bx + cx^2$ | sistema 3×3 com $\sum x^k$ ($k \le 4$) e $\sum x^k y$ ($k \le 2$) |
| Exponencial | $G(x) = a\,e^{bx}$ | linearização: $\ln y = \ln a + bx$ (reta nos pontos $(x_i, \ln y_i)$) |

**Resultados:**

| Ajuste | Função | Erro quadrático |
|---|---|---|
| Reta | $15{,}6166 - 1{,}3880x$ | 10,8424 |
| Parábola | $17{,}2250 - 2{,}4060x + 0{,}0884x^2$ | **2,0850** |
| Exponencial | $20{,}7710\,e^{-0{,}2357x}$ | 13,9593 |

A parábola tem o menor erro. Na exponencial, o ajuste minimiza o erro em $\ln y$; o erro da tabela foi calculado em $y$ para permitir a comparação.

---

## 4. Integração numérica (Tópico 4, Problema 3)

A seção vai de A até A7 em 7 subintervalos de $h = 0{,}4$ m, ou seja, **8 pontos**. Em A7 o casco encontra a linha de referência, então $y_7 = 0$:

$$y = (3{,}00;\ 2{,}92;\ 2{,}75;\ 2{,}52;\ 2{,}30;\ 1{,}84;\ 0{,}92;\ 0)$$

| Regra | Fórmula |
|---|---|
| Trapézio repetido | $\dfrac{h}{2}\left[y_0 + 2\sum_{i=1}^{n-1} y_i + y_n\right]$ |
| Simpson 1/3 repetido ($n$ par) | $\dfrac{h}{3}\left[y_0 + 4\sum_{i\ \text{ímpar}} y_i + 2\sum_{i\ \text{par}} y_i + y_n\right]$ |
| Simpson 3/8 (3 subintervalos) | $\dfrac{3h}{8}\left[y_0 + 3y_1 + 3y_2 + y_3\right]$ |

Como $n = 7$ é ímpar, o Simpson 1/3 não cobre o intervalo inteiro. Por isso aplicamos o **1/3 nos 4 primeiros subintervalos e o 3/8 nos 3 últimos**.

**Resultado:** Trapézio = **5,9000 m²** · Simpson = **5,9283 m²**. Esses valores são a área desenhada na figura (meia seção). A seção completa, por simetria, é o dobro: ≈ 11,80 m² e 11,86 m².

---

> **Referências:** Ruggiero & Lopes, *Cálculo Numérico — Aspectos Teóricos e Computacionais*; Burden & Faires, *Análise Numérica*; notas de aula LES710C.
