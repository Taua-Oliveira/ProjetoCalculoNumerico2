# ProjetoCalculoNumerico2

> **Resoluções de Métodos Numéricos Aplicados à Problemas do Cotidiano de um Engenheiro**

Projeto da disciplina de **Cálculo Numérico — UNIVASF (Turma 2026.2, LES710C)**, referente à Atividade Complementar. Reúne os 4 problemas sorteados pela equipe, resolvidos em Python com arquitetura modular: cada problema é um solver independente, plugado a um núcleo comum (menu → execução → relatório).

**Equipe:** Giovanni Éber, Caio Benevides e Tauã Oliveira.

---

## 🧩 Estrutura do projeto

Todos os módulos ficam na raiz do repositório (sem pastas de código aninhadas):

\```
ProjetoCalculoNumerico2/
├── main.py                 ← menu principal (loop; sai com 0)
├── casos.py                ← os 4 problemas sorteados (dados oficiais do enunciado)
├── entrada.py              ← ler_float / ler_int / ler_vetor / ler_matriz (entrada validada)
├── resultado.py            ← contrato Resultado: formato único de saída dos solvers
├── execucao.py             ← liga o caso escolhido ao seu solver (despacho pelo "tipo")
├── relatorio.py            ← tabelas no terminal + janelas com gráficos
│
├── metodos_diretos.py      ← T1: sistemas lineares (métodos diretos / LU)
├── metodos_iterativos.py   ← T2: ponte de Wheatstone (Gauss-Seidel)
├── ajustes.py              ← T3: mínimos quadrados (reta, parábola e exponencial)
├── integracao.py           ← T4: trapézio e Simpson repetidos (seção do navio)
│
├── data/                   ← enunciado original (PDF)
├── docs/                   ← documentação metodológica
└── LICENSE                 ← licença MIT
\```

## ▶️ Como executar

\```bash
pip install -r requirements.txt
python main.py
\```

O programa abre um menu com os 4 problemas. Escolha um número e pressione Enter: o caso roda isoladamente, mostrando as tabelas no terminal e abrindo **uma janela por gráfico** (basta fechar para voltar ao menu). Para sair, escolha `0`.

## 🔄 Fluxo interno

\```
main.py (menu)
  ├── casos.py       → dicionário do caso escolhido
  ├── entrada.py     → tol / max_iter (só quando o caso precisa)
  ├── execucao.py    → despacha pelo campo "tipo" do caso
  │     ├── metodos_diretos.py     (T1)
  │     ├── metodos_iterativos.py  (T2)
  │     ├── ajustes.py             (T3)
  │     └── integracao.py          (T4)
  └── relatorio.py   → tabelas + gráficos
  └── volta ao menu (até o usuário escolher 0)
\```

Cada solver devolve sempre um **`Resultado`** (definido em `resultado.py`): método, sucesso/erro, aviso, iterações, tabelas e figuras. Com isso, os módulos não conhecem uns aos outros — para acrescentar um problema novo, basta criar o módulo com uma função `resolver(caso)` e registrá-lo em `SOLVERS` (em `execucao.py`).