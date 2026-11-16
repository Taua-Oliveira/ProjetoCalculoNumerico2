"""T3.P3 — Ajuste por mínimos quadrados (reta, parábola e exponencial)."""
import numpy as np

from interface import entrada as ent
from interface import saida as out
from metodos import ajuste_reta, ajuste_parabola, ajuste_exponencial

NOME = "Tópico 3 — Mínimos quadrados (reta, parábola, exponencial)"

# Dados do enunciado
X = np.array([0, 1.5, 2.6, 4.2, 6, 8.2, 10, 11.4])
Y = np.array([18, 13, 11, 9, 6, 4, 2, 1], dtype=float)


def _ler_dados():
    if ent.usar_dados_enunciado():
        return X, Y
    x = ent.ler_vetor("Valores de x", minimo=3)
    y = ent.ler_vetor(f"Valores de F(x) ({len(x)} valores)", len(x))
    return x, y


def _mostrar_ajuste(nome, aj, x, y):
    print(f"\n▸ {nome}")
    if aj is None:
        print("   Não aplicável: a exponencial exige F(x) > 0 em todos os pontos.")
        return
    print(f"   {aj['texto']}")
    g = aj["funcao"](x)
    print(f"   {'x':>7} {'F(x)':>9} {'G(x)':>10} {'[F-G]²':>10}")
    for xi, yi, gi in zip(x, y, g):
        print(f"   {xi:>7g} {yi:>9g} {gi:>10.4f} {(yi - gi) ** 2:>10.4f}")
    print(f"   Erro quadrático Σ[F(xi) - G(xi)]² = {aj['erro']:.6f}")
    if nome == "Exponencial":
        print("   (ajuste feito na forma linearizada ln F = ln a + b·x)")


def resolver():
    out.titulo("T3.P3 — AJUSTE POR MÍNIMOS QUADRADOS")
    x, y = _ler_dados()

    print("\n   x    : " + "  ".join(f"{v:>7g}" for v in x))
    print("   F(x) : " + "  ".join(f"{v:>7g}" for v in y))

    ajustes = {"Reta": ajuste_reta(x, y),
               "Parábola": ajuste_parabola(x, y),
               "Exponencial": ajuste_exponencial(x, y)}
    for nome, aj in ajustes.items():
        _mostrar_ajuste(nome, aj, x, y)

    validos = {k: v for k, v in ajustes.items() if v is not None}
    melhor = min(validos, key=lambda k: validos[k]["erro"])
    print(f"\n🏆 Menor erro quadrático: {melhor} ({validos[melhor]['erro']:.6f})")

    _grafico(x, y, validos)


def _grafico(x, y, ajustes):
    fig, ax = out.novo_grafico(figsize=(8, 5))
    if fig is None:
        return
    xs = np.linspace(x.min(), x.max(), 200)
    ax.scatter(x, y, color="black", zorder=5, label="Dados")
    for (nome, aj), estilo in zip(ajustes.items(), ("--", "-", ":")):
        ax.plot(xs, aj["funcao"](xs), estilo, label=f"{nome} (erro² = {aj['erro']:.3f})")
    ax.set_title("Ajustes por mínimos quadrados")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.grid(alpha=0.3)
    ax.legend()
    out.salvar_grafico(fig, "t3p3_ajustes.png")
