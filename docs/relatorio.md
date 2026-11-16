# Relatório — Atividade Complementar de Cálculo Numérico (LES710C, 2026.2)

**Equipe:** _[Nome 1]_, _[Nome 2]_, _[Nome 3]_
**Problema apresentado em sala:** _[ex.: Tópico 2 — Ponte de Wheatstone]_ — _[17 ou 19/11/2026]_

---

## 1. Introdução

Este relatório traz a solução dos quatro problemas sorteados, um de cada tópico da disciplina. Os métodos foram implementados em Python, sem bibliotecas prontas de álgebra linear, em um programa interativo que permite:

- usar os dados do enunciado ou digitar novos dados para problemas semelhantes;
- ver o passo a passo (sistema montado, matrizes L e U, tabela de iterações, tabela de erros);
- fazer um novo cálculo ou sair do programa.

Execução: `python src/main.py`.

## 2. Tópico 1 — Produção de componentes eletrônicos (método direto)

**Modelagem.** Sejam $x_1, x_2, x_3$ os números de transistores, resistores e chips. Cada equação diz que o consumo de um material é igual ao que está disponível:

$$4x_1 + 3x_2 + 2x_3 = 960, \quad x_1 + 3x_2 + x_3 = 510, \quad 2x_1 + x_2 + 3x_3 = 610$$

**Método.** Decomposição LU com pivoteamento parcial ($PA = LU$), seguida das substituições progressiva e retroativa.

**Resultado.** 120 transistores, 100 resistores e 90 chips (resíduo nulo).

_[Inserir print da execução e o gráfico `results/t1p1_producao.png`]_

## 3. Tópico 2 — Ponte de Wheatstone (método iterativo)

**Modelagem.** Lei dos nós de Kirchhoff em B e C, com $V_A = E$ e $V_D = 0$ (ver [metodologia.md](metodologia.md)).

**Método.** Gauss-Seidel com $x^{(0)}_i = b_i/a_{ii}$ e precisão $10^{-4}$. O critério de Sassenfeld ($\beta_1 = 0{,}125$, $\beta_2 = 0{,}042$) garante a convergência.

**Resultado** (4 iterações):

| Corrente | Valor (A) |
|---|---|
| I1 | 0,2609 |
| I2 | 0,0978 |
| I3 | 0,1522 |
| I4 | 0,2065 |
| I5 | 0,0543 |
| I6 (fonte) | 0,3587 |

_[Inserir tabela de iterações e o gráfico `results/t2p1_convergencia.png`]_

## 4. Tópico 3 — Ajuste por mínimos quadrados

| Ajuste | G(x) | Σ[F(xᵢ) − G(xᵢ)]² |
|---|---|---|
| Reta | 15,6166 − 1,3880x | 10,8424 |
| Parábola | 17,2250 − 2,4060x + 0,0884x² | **2,0850** |
| Exponencial | 20,7710·e^(−0,2357x) | 13,9593 |

A parábola é o ajuste que melhor representa os dados.

_[Inserir o gráfico `results/t3p3_ajustes.png`]_

## 5. Tópico 4 — Área da seção do navio

Foram usados 8 pontos (A até A7, com largura 0 em A7) e $h = 0{,}4$ m, ou seja, 7 subintervalos. Como esse número é ímpar, o Simpson foi composto: 1/3 nos 4 primeiros subintervalos e 3/8 nos 3 últimos.

| Regra | Área (m²) |
|---|---|
| Trapézio repetido | 5,9000 |
| Simpson repetido | 5,9283 |

A seção completa, considerando a simetria do casco, tem o dobro dessa área: ≈ 11,80 m² e 11,86 m².

_[Inserir o gráfico `results/t4p3_secao_navio.png`]_

## 6. Conclusão

_[Comentário da equipe: comparação entre os métodos, dificuldades encontradas etc.]_

## 7. Participação de cada integrante

- **_[Nome 1]_:** _[o que fez]_
- **_[Nome 2]_:** _[o que fez]_
- **_[Nome 3]_:** _[o que fez]_
