"""T4.P3 — Área da seção de um navio (Trapézio e Simpson repetidos)."""
import numpy as np

from interface import entrada as ent
from interface import saida as out
from metodos import trapezio_repetido, simpson_repetido

NOME = "Tópico 4 — Área da seção do navio (Trapézio e Simpson)"

# Dados do enunciado: larguras de A-B até A7 (em A7 o casco toca a linha → 0)
LARGURAS = np.array([3.00, 2.92, 2.75, 2.52, 2.30, 1.84, 0.92, 0.0])
H = 0.4


def _ler_dados():
    if ent.usar_dados_enunciado():
        return LARGURAS, H
    larguras = ent.ler_vetor("Larguras (m), da primeira à última medição", minimo=3)
    h = ent.ler_float("Espaçamento entre as medições h (m)", H, positivo=True)
    return larguras, h


def resolver():
    out.titulo("T4.P3 — ÁREA DA SEÇÃO DO NAVIO (TRAPÉZIO E SIMPSON)")
    print("Larguras medidas de A-B até A7, igualmente espaçadas. Em A7 o casco\n"
          "encontra a linha de referência, então a largura ali é 0.")
    larguras, h = _ler_dados()

    n = len(larguras) - 1
    print(f"\n   {n + 1} pontos, {n} subintervalos, h = {h:g} m, intervalo [0, {n * h:g}] m")
    print("   " + "  ".join(f"y{i}={v:g}" for i, v in enumerate(larguras)))

    trap = trapezio_repetido(larguras, h)
    simp, desc = simpson_repetido(larguras, h)

    out.subtitulo("RESULTADO (área da seção representada na figura)")
    print(f"   Trapézio repetido : {trap:.6f} m²")
    print(f"   Simpson repetido  : {simp:.6f} m²   [{desc}]")
    print(f"   Diferença         : {abs(trap - simp):.6f} m²")
    print("\n   Obs.: a figura mostra meia seção (do eixo A-A7 até o casco).")
    print(f"   Seção completa (simétrica) = 2 × área: Trapézio {2 * trap:.4f} m², "
          f"Simpson {2 * simp:.4f} m²")

    _grafico(larguras, h, simp)


def _grafico(larguras, h, area):
    fig, ax = out.novo_grafico(figsize=(5, 6))
    if fig is None:
        return
    prof = np.arange(len(larguras)) * h
    ax.plot(larguras, prof, "o-", color="navy", label="Casco (pontos medidos)")
    ax.fill_betweenx(prof, 0, larguras, color="skyblue", alpha=0.5,
                     label=f"Área ≈ {area:.3f} m² (Simpson)")
    ax.invert_yaxis()
    ax.set_xlabel("Largura (m)")
    ax.set_ylabel("Profundidade a partir de A (m)")
    ax.set_title("Seção do navio")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left")
    out.salvar_grafico(fig, "t4p3_secao_navio.png")
