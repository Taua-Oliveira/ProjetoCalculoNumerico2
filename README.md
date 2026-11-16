# ProjetoCalculoNumerico2

> **Métodos numéricos aplicados a problemas do dia a dia de um engenheiro**

Atividade complementar de Cálculo Numérico (2026.2, LES710C, UNIVASF). Programa interativo em Python que resolve os 4 problemas sorteados e aceita novos dados para problemas do mesmo tipo.

## Estrutura

```
ProjetoCalculoNumerico2/
├── data/                     ← enunciado original (PDF)
├── src/
│   ├── main.py                       ← ponto de entrada: menu principal
│   ├── metodos/                      ← métodos numéricos (implementados à mão)
│   │   ├── sistemas_diretos.py       ←   T1: decomposição LU
│   │   ├── sistemas_iterativos.py    ←   T2: Gauss-Seidel + Sassenfeld
│   │   ├── minimos_quadrados.py      ←   T3: reta, parábola, exponencial
│   │   └── integracao.py             ←   T4: Trapézio e Simpson repetidos
│   ├── problemas/                    ← um arquivo por problema sorteado
│   │   ├── t1_producao.py
│   │   ├── t2_wheatstone.py
│   │   ├── t3_minimos_quadrados.py
│   │   └── t4_area_navio.py
│   └── interface/                    ← interação com o usuário
│       ├── entrada.py                ←   leitura e validação de dados
│       └── saida.py                  ←   impressão formatada e gráficos
├── docs/
│   ├── metodologia.md        ← modelagem e fórmulas de cada problema
│   └── relatorio.md          ← relatório da entrega
└── results/                  ← gráficos gerados ao executar (não versionado)
```

## Instalação

Requer Python 3.8 ou mais recente.

```bash
pip install -r requirements.txt
```

O `matplotlib` é opcional: sem ele, o programa funciona normalmente e apenas não salva os gráficos.

## Execução

```bash
python src/main.py
```

O menu principal oferece os 4 problemas e a opção **0 para sair**. Em cada problema dá para:
- apertar **Enter** para usar os dados do enunciado, ou **n** para digitar novos dados;
- ao final, escolher se quer **fazer um novo cálculo** ou voltar ao menu.

Os números podem ser digitados com vírgula ou ponto decimal (`3,89` ou `3.89`). Em listas, separe os valores com espaço ou `;`.

Para resolver os 4 problemas de uma vez com os dados do enunciado:

```bash
python src/main.py --auto
```

## Problemas resolvidos

| Tópico | Problema | Método | Resultado |
|---|---|---|---|
| T1.P1 | Produção de transistores, resistores e chips | Decomposição LU com pivoteamento | 120, 100 e 90 unidades |
| T2.P1 | Ponte de Wheatstone | Gauss-Seidel (critério de Sassenfeld) | I1 ≈ 0,2609 A … I6 ≈ 0,3587 A |
| T3.P3 | Ajuste de curvas | Mínimos quadrados: reta, parábola e exponencial | Parábola com menor erro (2,085) |
| T4.P3 | Área da seção de um navio | Trapézio e Simpson repetidos (1/3 + 3/8) | 5,900 m² e 5,928 m² |

Os detalhes de cada problema estão em [docs/metodologia.md](docs/metodologia.md).

## Referências

- Ruggiero, M. A. G., & Lopes, V. L. R. *Cálculo Numérico — Aspectos Teóricos e Computacionais*.
- Burden, R. L., & Faires, J. D. *Análise Numérica*.
- Notas de aula da disciplina LES710C.
