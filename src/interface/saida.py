"""Apresentação dos resultados: títulos, matrizes, sistemas e gráficos."""
import os

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")  # salva em arquivo, sem abrir janela
    import matplotlib.pyplot as plt
    TEM_MATPLOTLIB = True
except ImportError:
    plt = None
    TEM_MATPLOTLIB = False

PASTA_RESULTADOS = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results"))

LARGURA = 68


def titulo(txt):
    print("\n" + "=" * LARGURA)
    print(txt.center(LARGURA))
    print("=" * LARGURA)


def subtitulo(txt):
    print("\n" + "-" * 50)
    print(txt)
    print("-" * 50)


def imprimir_matriz(M, nome, casas=4):
    print(f"\n{nome} =")
    for linha in np.atleast_2d(M):
        print("   [" + "  ".join(f"{v:>12.{casas}f}" for v in linha) + " ]")


def imprimir_sistema(A, b, variaveis):
    print("\nSistema linear:")
    for i in range(len(b)):
        termos = []
        for j, v in enumerate(variaveis):
            coef = A[i, j]
            if coef == 0:
                continue
            sinal = "-" if coef < 0 else "+"
            termos.append(f"{sinal} {abs(coef):g}·{v}")
        expr = " ".join(termos) if termos else "0"
        expr = expr[2:] if expr.startswith("+ ") else "-" + expr[2:] if expr.startswith("- ") else expr
        print(f"   {expr} = {b[i]:g}")


def novo_grafico(**kwargs):
    """Cria uma figura, ou devolve (None, None) se o matplotlib não estiver instalado."""
    if not TEM_MATPLOTLIB:
        return None, None
    return plt.subplots(**kwargs)


def salvar_grafico(fig, nome):
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(PASTA_RESULTADOS, nome)
    fig.tight_layout()
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    print(f"\n📈 Gráfico salvo em: {caminho}")
