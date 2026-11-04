"""
Métodos diretos: sistemas lineares resolvidos pela eliminação de Gauss,
implementada manualmente — sem bibliotecas numéricas.

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: (a definir — a divisão de tarefas será fechada em grupo)

Fluxo do módulo (T1 — produção de componentes eletrônicos):
    1. lê a matriz de coeficientes A e o vetor de disponibilidades b do caso;
    2. resolve Ax = b pela eliminação de Gauss com pivotamento parcial:
       a cada coluna k, a linha com o maior elemento em módulo em |a_kk| é
       trazida para a posição k (evita divisão por número pequeno) e os
       elementos abaixo da diagonal são zerados; as mesmas operações são
       aplicadas ao lado direito, mantendo o sistema equivalente;
    3. no fim a matriz está triangular superior: a solução sai por
       substituição retroativa (esse processo equivale à decomposição
       A = L·U, mas sem precisar montar L explicitamente);
    4. confere o resíduo ||Ax - b||;
    5. monta as tabelas (produção + balanço de materiais) e o gráfico de
       barras, devolvendo tudo num Resultado pronto para o relatorio.py.

Conferência opcional: se o SciPy estiver instalado, a solução manual é
comparada com scipy.linalg.solve(); uma divergência relevante vira AVISO,
mas o método principal continua sendo a implementação manual.
"""

import math
import time

import matplotlib.pyplot as plt

from resultado import Resultado

# Pivot menor que isso (em módulo) é tratado como zero: indica sistema
# sem solução única ou matriz mal condicionada. O problema T1 tem
# coeficientes pequenos e bem comportados, então esse limite absoluto
# simples é suficiente aqui.
_PIVO_MINIMO = 1e-14


def _montar_sistema(caso: dict) -> tuple[list[list[float]], list[float]]:
    """Extrai (A, b) do caso e valida formato/tamanho das entradas."""
    A = [[float(v) for v in linha] for linha in caso["matriz"]]
    b = [float(v) for v in caso["disponibilidade"]]

    n = len(A)
    if n == 0 or any(len(linha) != n for linha in A):
        raise ValueError("A matriz de coeficientes precisa ser quadrada.")
    if len(b) != n:
        raise ValueError(
            f"A matriz tem {n} linhas, mas o vetor de disponibilidades "
            f"tem {len(b)} valores."
        )
    return A, b


def _gauss_eliminar(A: list[list[float]], b: list[float]) -> dict:
    """
    Eliminação de Gauss com pivotamento parcial.

    Zera os elementos abaixo da diagonal aplicando as MESMAS operações
    elementares ao lado direito, deixando o sistema equivalente pronto
    para a substituição retroativa. Devolve {"U", "rhs"} (a matriz
    triangular superior e o lado direito transformado).
    """
    n = len(A)
    U = [linha[:] for linha in A]  # cópia de trabalho que vira a triangular superior
    rhs = b[:]                    # lado direito, transformado junto com as linhas

    for k in range(n):
        # --- pivotamento parcial: pega a linha com maior |elemento| na coluna k ---
        linha_pivo = max(range(k, n), key=lambda i: abs(U[i][k]))
        if abs(U[linha_pivo][k]) < _PIVO_MINIMO:
            raise ZeroDivisionError(
                "pivô nulo (ou muito pequeno): o sistema não tem solução "
                "única ou a matriz é mal condicionada"
            )
        if linha_pivo != k:
            # troca as linhas INTEIRAS (matriz + lado direito)
            U[k], U[linha_pivo] = U[linha_pivo], U[k]
            rhs[k], rhs[linha_pivo] = rhs[linha_pivo], rhs[k]

        # --- zera os elementos abaixo da diagonal ---
        for i in range(k + 1, n):
            multiplicador = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= multiplicador * U[k][j]
            rhs[i] -= multiplicador * rhs[k]

    return {"U": U, "rhs": rhs}


def _substituicao_retroativa(U: list[list[float]], rhs: list[float]) -> list[float]:
    """Resolução por substituição retroativa: U x = rhs, com U triangular superior."""
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (rhs[i] - soma) / U[i][i]
    return x


def _conferir_com_scipy(A: list[list[float]], b: list[float], x: list[float]) -> float | None:
    """Compara a solução manual com scipy.linalg.solve; devolve a maior diferença."""
    try:
        import numpy as np
        import scipy.linalg
    except ImportError:
        return None
    try:
        x_scipy = scipy.linalg.solve(
            np.array(A, dtype=float), np.array(b, dtype=float)
        )
    except Exception:
        return None
    return max(abs(a - s) for a, s in zip(x, x_scipy))


def _formatar_quantidade(valor: float) -> str:
    """Texto amigável: '120' em vez de '120.00000000000003'."""
    valor = round(valor, 6)
    if abs(valor - round(valor)) < 1e-9:
        return str(int(round(valor)))
    return f"{valor:g}"


def _criar_figura(x: list[float], nomes_componentes: list[str]):
    """Gráfico de barras da meta de produção (uma cor por componente)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    cores = plt.cm.tab10(range(len(nomes_componentes)))
    barras = ax.bar(nomes_componentes, x, color=cores)

    topo = max(x) if x else 0.0
    if topo <= 0:
        topo = 1.0
    for barra, valor in zip(barras, x):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + topo * 0.02,
            _formatar_quantidade(valor),
            ha="center", va="bottom", fontsize=10,
        )

    ax.set_title("Meta de produção semanal")
    ax.set_ylabel("Quantidade fabricada")
    ax.set_ylim(0, topo * 1.2)
    fig.tight_layout()
    return fig


def resolver(caso: dict, **opcoes) -> Resultado:
    """
    Ponto de entrada padrão do solver (mesma assinatura nos quatro módulos).

    Recebe o caso (dicionário de casos.py) e devolve um Resultado pronto
    para o relatorio.py. As opções extras (tol, max_iter, ...) são
    ignoradas neste método: sistemas diretos não usam critério de
    convergência iterativa.
    """
    inicio = time.perf_counter()
    nome = caso.get("nome", "")
    tipo = caso.get("tipo", "")
    metodo = "Eliminação de Gauss (direto)"

    try:
        A, b = _montar_sistema(caso)
        triang = _gauss_eliminar(A, b)
        x = _substituicao_retroativa(triang["U"], triang["rhs"])
    except (ValueError, ZeroDivisionError, KeyError) as erro:
        return Resultado(
            metodo=metodo,
            problema=nome,
            tipo=tipo,
            sucesso=False,
            erro=str(erro),
            tempo_ms=(time.perf_counter() - inicio) * 1000,
        )

    tempo_ms = (time.perf_counter() - inicio) * 1000

    # --- conferência 1: resíduo ||Ax - b|| ---
    residual = [
        sum(A[i][j] * x[j] for j in range(len(x))) - b[i]
        for i in range(len(b))
    ]
    norma_residual = math.sqrt(sum(r * r for r in residual))

    # --- conferência 2 (opcional): comparação com o SciPy ---
    aviso = None
    diferenca = _conferir_com_scipy(A, b, x)
    if diferenca is not None and diferenca > 1e-6:
        aviso = (
            f"a solução manual divergiu da conferência com SciPy "
            f"(maior diferença = {diferenca:.2e})"
        )

    nomes_componentes = caso.get("nomes_componentes") or [
        f"x{i+1}" for i in range(len(x))
    ]
    nomes_materiais = caso.get("nomes_materiais") or [
        f"Material {i+1}" for i in range(len(b))
    ]

    # --- tabela 1: meta de produção ---
    tabela_producao = {
        "titulo": "Meta de produção semanal",
        "cabecalho": ["Componente", "Quantidade fabricada"],
        "linhas": [
            [nome_c, _formatar_quantidade(v)]
            for nome_c, v in zip(nomes_componentes, x)
        ],
    }

    # --- tabela 2: conferência do balanço de materiais ---
    tabela_conferencia = {
        "titulo": "Conferência do balanço de materiais (A·x = b?)",
        "cabecalho": ["Material", "Disponível", "Consumido", "Diferença"],
        "linhas": [
            [
                nome_m,
                _formatar_quantidade(b[i]),
                _formatar_quantidade(sum(A[i][j] * x[j] for j in range(len(x)))),
                "0" if residual[i] == 0 else f"{abs(residual[i]):.2e}",
            ]
            for i, nome_m in enumerate(nomes_materiais)
        ],
    }

    # --- gráfico ---
    figura = _criar_figura(x, nomes_componentes)

    observacoes = [
        f"resíduo ||Ax − b|| = {norma_residual:.2e} "
        f"(solução exata dentro do arredondamento)."
    ]
    if diferenca is not None:
        observacoes.append(
            f"conferência contra scipy.linalg.solve: maior diferença = {diferenca:.2e}."
        )

    return Resultado(
        metodo=metodo,
        problema=nome,
        tipo=tipo,
        sucesso=True,
        tempo_ms=tempo_ms,
        tabelas=[tabela_producao, tabela_conferencia],
        figuras=[figura],
        observacoes=observacoes,
        aviso=aviso,
    )
