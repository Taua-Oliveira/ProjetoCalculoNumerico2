"""T1.P1 — Produção de transistores, resistores e chips (Decomposição LU)."""
import numpy as np

from interface import entrada as ent
from interface import saida as out
from metodos import resolver_lu

NOME = "Tópico 1 — Produção de componentes (LU)"

# Dados do enunciado
PRODUTOS = ["Transistor", "Resistor", "Chip"]
MATERIAIS = ["Cobre", "Zinco", "Vidro"]
# CONSUMO[i][j] = unidades do material j usadas em uma unidade do produto i
CONSUMO = np.array([[4, 1, 2], [3, 3, 1], [2, 1, 3]], dtype=float)
DISPONIVEL = np.array([960, 510, 610], dtype=float)


def _ler_dados():
    if ent.usar_dados_enunciado():
        disponivel = DISPONIVEL
        if not ent.sim_nao("Usar a disponibilidade da semana do enunciado (960, 510, 610)?"):
            disponivel = ent.ler_vetor("Disponível de " + " ".join(MATERIAIS), 3)
        return PRODUTOS, MATERIAIS, CONSUMO, disponivel

    n = ent.ler_int("Número de produtos (= número de materiais)", 3)
    produtos = [ent.ler_texto(f"  Nome do produto {i + 1}", f"P{i + 1}") for i in range(n)]
    materiais = [ent.ler_texto(f"  Nome do material {j + 1}", f"M{j + 1}") for j in range(n)]
    consumo = np.array([
        ent.ler_vetor(f"Consumo de {' '.join(materiais)} por unidade de {p}", n)
        for p in produtos])
    disponivel = ent.ler_vetor(f"Quantidade disponível de {' '.join(materiais)}", n)
    return produtos, materiais, consumo, disponivel


def resolver():
    out.titulo("T1.P1 — PRODUÇÃO DE COMPONENTES (DECOMPOSIÇÃO LU)")
    print("Cada componente consome materiais; dada a quantidade disponível de\n"
          "cada material, calcula-se quantas unidades de cada componente produzir.")

    produtos, materiais, consumo, disponivel = _ler_dados()

    # Cada EQUAÇÃO é um material; cada INCÓGNITA é um produto → A = consumoᵀ
    A = consumo.T
    variaveis = [f"x{i + 1}" for i in range(len(produtos))]
    print("\nIncógnitas: " + ", ".join(f"{v} = nº de {p}" for v, p in zip(variaveis, produtos)))
    print("Cada equação: consumo total de um material = quantidade disponível")
    out.imprimir_sistema(A, disponivel, variaveis)

    try:
        x, P, L, U = resolver_lu(A, disponivel)
    except ValueError as e:
        print(f"\n❌ {e}")
        return

    out.imprimir_matriz(P, "P (permutação)", 0)
    out.imprimir_matriz(L, "L")
    out.imprimir_matriz(U, "U")

    out.subtitulo("RESULTADO")
    for p, v in zip(produtos, x):
        print(f"   {p:<20} {v:>12.4f}")
    residuo = np.max(np.abs(A @ x - disponivel))
    print(f"\n   Resíduo máx |A·x - b| = {residuo:.2e}")
    if np.any(x < -1e-9):
        print("   ⚠ Há valores negativos: com esses materiais a produção não é viável.")
    elif np.any(np.abs(x - np.round(x)) > 1e-6):
        print("   ℹ A solução não é inteira; na prática arredonda-se para baixo.")

    _grafico(produtos, x)


def _grafico(produtos, x):
    fig, ax = out.novo_grafico(figsize=(7, 4))
    if fig is None:
        return
    barras = ax.bar(produtos, x, color=[f"C{i}" for i in range(len(x))])
    ax.bar_label(barras, fmt="%.1f")
    ax.set_title("Meta de produção")
    ax.set_ylabel("Quantidade")
    out.salvar_grafico(fig, "t1p1_producao.png")
