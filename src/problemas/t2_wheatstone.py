"""T2.P1 — Ponte de Wheatstone (Gauss-Seidel).

Topologia: fonte E entre A (+) e D (-); R1: A-B, R2: A-C, R4: B-D, R3: C-D,
R5: B-C (ponte). Lei dos nós de Kirchhoff com V_A = E e V_D = 0:
   nó B: (E - VB)/R1 = VB/R4 + (VB - VC)/R5
   nó C: (E - VC)/R2 + (VB - VC)/R5 = VC/R3
"""
import numpy as np

from interface import entrada as ent
from interface import saida as out
from metodos import criterio_sassenfeld, gauss_seidel

NOME = "Tópico 2 — Ponte de Wheatstone (Gauss-Seidel)"

# Dados do enunciado
E_PADRAO = 30.0
R_PADRAO = (20.0, 120.0, 120.0, 120.0, 120.0)  # R1..R5
TOL_PADRAO = 1e-4


def montar_sistema(E, R1, R2, R3, R4, R5):
    """Sistema nodal A·[VB, VC] = b."""
    A = np.array([[1 / R1 + 1 / R4 + 1 / R5, -1 / R5],
                  [-1 / R5, 1 / R2 + 1 / R3 + 1 / R5]])
    b = np.array([E / R1, E / R2])
    return A, b


def correntes(E, R, VB, VC):
    R1, R2, R3, R4, R5 = R
    I1 = (E - VB) / R1
    I2 = (E - VC) / R2
    I3 = VC / R3
    I4 = VB / R4
    I5 = (VB - VC) / R5
    return {"I1": I1, "I2": I2, "I3": I3, "I4": I4, "I5": I5, "I6": I1 + I2}


def executar_gauss_seidel(A, b, variaveis, tol):
    """Roda o Gauss-Seidel mostrando Sassenfeld e a tabela de iterações."""
    beta = criterio_sassenfeld(A)
    print("\nCritério de Sassenfeld: " +
          ", ".join(f"β{i + 1} = {v:.4f}" for i, v in enumerate(beta)))
    if np.max(beta) < 1:
        print("   max β < 1 → convergência garantida.")
    else:
        print("   ⚠ max β ≥ 1 → convergência NÃO garantida (pode ainda convergir).")

    r = gauss_seidel(A, b, tol=tol)
    print("\nx(0) = b_i/a_ii")
    print(f"\n{'k':>4} | " + " | ".join(f"{v:>12}" for v in variaveis))
    print("-" * (7 + 15 * len(variaveis)))
    for k, linha in enumerate(r["historico"]):
        print(f"{k:>4} | " + " | ".join(f"{v:>12.6f}" for v in linha))

    if r["convergiu"]:
        print(f"\n✅ Convergiu em {r['iteracoes']} iterações "
              f"(erro relativo = {r['erro']:.2e} < {tol:g})")
    else:
        print(f"\n❌ Não convergiu em {r['iteracoes']} iterações.")
    return r


def _sistema_generico():
    n = ent.ler_int("Ordem do sistema", 3)
    A = ent.ler_matriz(n)
    b = ent.ler_vetor("Termos independentes b", n)
    tol = ent.ler_float("Precisão", TOL_PADRAO, positivo=True)
    variaveis = [f"x{i + 1}" for i in range(n)]
    out.imprimir_sistema(A, b, variaveis)
    try:
        executar_gauss_seidel(A, b, variaveis, tol)
    except ValueError as e:
        print(f"\n❌ {e}")


def resolver():
    out.titulo("T2.P1 — PONTE DE WHEATSTONE (GAUSS-SEIDEL)")
    print("  [1] Ponte de Wheatstone (digitar E e resistências)")
    print("  [2] Sistema linear qualquer por Gauss-Seidel")
    if ent.perguntar("Opção [Enter = 1]: ").strip() == "2":
        _sistema_generico()
        return

    print("\nTopologia: fonte E entre A (+) e D (-); R1: A-B, R2: A-C,\n"
          "R4: B-D, R3: C-D, R5: B-C (ponte).")
    if ent.usar_dados_enunciado():
        E, R, tol = E_PADRAO, R_PADRAO, TOL_PADRAO
    else:
        E = ent.ler_float("E (V)", E_PADRAO)
        R = tuple(ent.ler_float(f"R{i + 1} (Ω)", p, positivo=True)
                  for i, p in enumerate(R_PADRAO))
        tol = ent.ler_float("Precisão", TOL_PADRAO, positivo=True)

    A, b = montar_sistema(E, *R)
    print("\nLei dos nós de Kirchhoff (V_A = E, V_D = 0):")
    print("   nó B:  (1/R1 + 1/R4 + 1/R5)·VB - (1/R5)·VC = E/R1")
    print("   nó C: -(1/R5)·VB + (1/R2 + 1/R3 + 1/R5)·VC = E/R2")
    out.imprimir_sistema(np.round(A, 6), np.round(b, 6), ["VB", "VC"])

    r = executar_gauss_seidel(A, b, ["VB", "VC"], tol)
    VB, VC = r["x"]
    I = correntes(E, R, VB, VC)

    out.subtitulo("RESULTADO")
    print(f"   VB = {VB:.6f} V    VC = {VC:.6f} V")
    descricoes = {"I1": "A→B por R1", "I2": "A→C por R2", "I3": "C→D por R3",
                  "I4": "B→D por R4", "I5": "B→C por R5", "I6": "fonte, D→A"}
    for nome, valor in I.items():
        print(f"   {nome} = {valor:>10.6f} A   ({descricoes[nome]})")
    print("\nVerificação (lei dos nós):")
    print(f"   nó B: I1 - I4 - I5 = {I['I1'] - I['I4'] - I['I5']:.2e}")
    print(f"   nó C: I2 + I5 - I3 = {I['I2'] + I['I5'] - I['I3']:.2e}")
    print(f"   nó D: I3 + I4 - I6 = {I['I3'] + I['I4'] - I['I6']:.2e}")

    _grafico(r["historico"])


def _grafico(h):
    fig, ax = out.novo_grafico(figsize=(7, 4))
    if fig is None:
        return
    ax.plot(h[:, 0], "o-", label="VB")
    ax.plot(h[:, 1], "s-", label="VC")
    ax.set_title("Convergência do Gauss-Seidel")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Potencial (V)")
    ax.grid(alpha=0.3)
    ax.legend()
    out.salvar_grafico(fig, "t2p1_convergencia.png")
