# ProjetoCalculoNumerico2

> **Resoluções de Métodos Numéricos Aplicados à Problemas do Cotidiano de um Engenheiro**

Repositório da disciplina de Cálculo Numérico (Turma 2026.2 — LES710C, UNIVASF). Contém a implementação em Python dos 4 problemas sorteados para a atividade complementar, abrangendo métodos diretos e iterativos para sistemas lineares, mínimos quadrados e integração numérica.

---

## 📋 Estrutura do Projeto

```
ProjetoCalculoNumerico2/
├── data/                  ← Enunciado original (PDF)
├── src/                   ← Código-fonte modular
├── results/               ← Relatórios e gráficos gerados
└── docs/                  ← Documentação metodológica
```

## 📦 Requisitos

- Python 3.8+
- `numpy`, `scipy`, `matplotlib`

Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Execução

```bash
python src/resolver_problemas.py
```

O script gera o arquivo `results/relatorio_calculo_numerico.json` com todos os resultados e salva os gráficos na pasta `results/`.

## 📊 Problemas Resolvidos

| Tópico | Problema | Método |
|---------|----------|--------|
| T1 | Produção de componentes eletrônicos | LU decomposition |
| T2 | Ponte de Wheatstone | Gauss-Seidel (iterativo) |
| T3 | Ajuste de curvas (dados experimentais) | Mínimos quadrados (reta/parábola/exponencial) |
| T4 | Área da seção de um navio | Trapézio e Simpson |

## 📄 Referências

- Ruggiero, M. A. G., & Lopes, V. L. R. *Cálculo Numérico — Aspectos Teóricos e Computacionais*.
- Burden, R. L., & Faires, J. D. *Análise Numérica*.
- [Notas de aula da disciplina LES710C](inserido pelo professor na plataforma Amadeus).

---

> Desenvolvido com apoio do Sabiá-4 (Maritaca AI) como ferramenta de auxílio pedagógico.
