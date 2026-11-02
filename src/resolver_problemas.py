import json
import os

import matplotlib
matplotlib.use("Agg")  # funciona sem interface gráfica
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg

RESULTS_DIR = "results"


def _garantir_pasta(pasta=RESULTS_DIR):
    os.makedirs(pasta, exist_ok=True)
    return pasta


def to_serializable(obj):
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_serializable(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return [to_serializable(v) for v in obj.tolist()]
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, (complex, np.complexfloating)):
        return {"real": float(obj.real), "imag": float(obj.imag)}
    elif isinstance(obj, (bool, int, float, str, type(None))):
        return obj
    else:
        return str(obj)


def resolver_producao_eletronica(A=None, b=None, nomes_componentes=None,
                                 nomes_materiais=None, pasta=RESULTS_DIR):
    if A is None:
        A = np.array([[4, 3, 2], [1, 3, 1], [2, 1, 3]], dtype=float)
    if b is None:
        b = np.array([960, 510, 610], dtype=float)
    if nomes_componentes is None:
        nomes_componentes = ["Transistor", "Resistor", "Chip"]
    if nomes_materiais is None:
        nomes_materiais = ["Cobre", "Zinco", "Vidro"]

    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    _garantir_pasta(pasta)

    # scipy.linalg.lu devolve A = P @ L @ U, logo P.T @ b é o lado direito permutado
    P, L, U = scipy.linalg.lu(A)
    Pb = P.T @ b
    y = scipy.linalg.solve_triangular(L, Pb, lower=True)
    x = scipy.linalg.solve_triangular(U, y, lower=False)

    residual = A @ x - b
    residual_norm = np.linalg.norm(residual)
    x = np.round(x, 6)

    cores = plt.cm.tab10(np.arange(len(nomes_componentes)) % 10)
    caminho = os.path.join(pasta, "t1p1_producao.png")
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(nomes_componentes, x, color=cores)
    ax.set_title("Meta de produção semanal")
    ax.set_ylabel("Quantidade fabricada")
    ax.set_ylim(0, max(x) * 1.2)
    for bar, val in zip(bars, x):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01 * max(x),
                f"{round(val)}", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)

    return {
        "metodo": "Decomposição LU (SciPy)",
        "A": A.tolist(),
        "b": b.tolist(),
        "solucao": {n: float(v) for n, v in zip(nomes_componentes, x)},
        "residual_norm": float(residual_norm),
        "grafico": caminho,
    }


def resolver_ponte_wheatstone(E=30.0, R1=20.0, R2=120.0, R3=120.0, R4=120.0,
                              R5=120.0, tol=1e-4, max_iter=1000, pasta=RESULTS_DIR):
    _garantir_pasta(pasta)
    G1, G2, G3, G4, G5 = 1 / R1, 1 / R2, 1 / R3, 1 / R4, 1 / R5
    a11 = G1 + G4 + G5
    a12 = -G5
    a21 = -G5
    a22 = G2 + G3 + G5
    B_vec = np.array([G1 * E, G2 * E], dtype=float)
    A = np.array([[a11, a12], [a21, a22]])

    # Critério de Sassenfeld
    beta1 = abs(a12) / abs(a11)
    beta2 = abs(a21) * beta1 / abs(a22)
    convergencia = beta1 < 1 and beta2 < 1

    x0 = np.array([B_vec[0] / A[0, 0], B_vec[1] / A[1, 1]])
    x = x0.copy()
    historico = [x0.copy()]
    convergiu = False
    iteracoes = 0

    for k in range(max_iter):
        x_old = x.copy()
        x[0] = (B_vec[0] - A[0, 1] * x[1]) / A[0, 0]
        x[1] = (B_vec[1] - A[1, 0] * x[0]) / A[1, 1]
        historico.append(x.copy())
        iteracoes = k + 1
        if np.linalg.norm(x - x_old) < tol:
            convergiu = True
            break

    Va, Vd = E, 0.0
    Vb, Vc = x
    I1 = (Va - Vb) / R1
    I2 = (Va - Vc) / R2
    I4 = (Vb - Vd) / R4
    I3 = (Vc - Vd) / R3
    I5 = (Vb - Vc) / R5
    I_total = I1 + I2

    hist_arr = np.array(historico)
    caminho = os.path.join(pasta, "t2p1_convergencia.png")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(hist_arr[:, 0], label="Vb (nó B)", marker="o")
    ax.plot(hist_arr[:, 1], label="Vc (nó C)", marker="s")
    ax.set_title(f"Convergência Gauss-Seidel — tolerância {tol}")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Potencial (V)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)

    return {
        "metodo": "Gauss-Seidel",
        "iteracoes": int(iteracoes),
        "convergiu": bool(convergiu),
        "criterio_sassenfeld": {"beta1": float(beta1), "beta2": float(beta2),
                                "satisfaz": bool(convergencia)},
        "potenciais": {"Va": float(Va), "Vb": float(Vb), "Vc": float(Vc), "Vd": float(Vd)},
        "correntes": {"I1": float(I1), "I2": float(I2), "I3": float(I3),
                      "I4": float(I4), "I5": float(I5), "I_total_fonte": float(I_total)},
        "grafico_convergencia": caminho,
        "tol_utilizada": float(tol),
    }


def ajuste_minimos_quadrados(x=None, y=None, pasta=RESULTS_DIR):
    if x is None:
        x = np.array([0, 1.5, 2.6, 4.2, 6.0, 8.2, 10.0, 11.4], dtype=float)
    if y is None:
        y = np.array([18, 13, 11, 9, 6, 4, 2, 1], dtype=float)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    _garantir_pasta(pasta)

    n = len(x)
    sx, sy = np.sum(x), np.sum(y)
    sx2, sxy = np.sum(x**2), np.sum(x * y)

    # Reta: y = a + b x
    A_reta = np.array([[n, sx], [sx, sx2]])
    rhs_reta = np.array([sy, sxy])
    a_reta, b_reta = np.linalg.solve(A_reta, rhs_reta)
    y_reta = a_reta + b_reta * x
    erro_reta = np.sum((y - y_reta) ** 2)

    # Parábola: y = a + b x + c x²
    sx3, sx4 = np.sum(x**3), np.sum(x**4)
    sx2y = np.sum(x**2 * y)
    A_parab = np.array([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]])
    rhs_parab = np.array([sy, sxy, sx2y])
    a_parab, b_parab, c_parab = np.linalg.solve(A_parab, rhs_parab)
    y_parab = a_parab + b_parab * x + c_parab * x**2
    erro_parab = np.sum((y - y_parab) ** 2)

    # Exponencial: y = a e^(b x), linearizada com ln(y).
    # Obs.: o ajuste minimiza o erro em ln(y), não em y; o erro² abaixo é
    # calculado em y apenas para comparação com os demais ajustes.
    if np.all(y > 0):
        ln_y = np.log(y)
        A_exp = np.array([[n, sx], [sx, sx2]])
        rhs_exp = np.array([np.sum(ln_y), np.sum(x * ln_y)])
        ln_a_exp, b_exp_coef = np.linalg.solve(A_exp, rhs_exp)
        a_exp = np.exp(ln_a_exp)
        y_exp = a_exp * np.exp(b_exp_coef * x)
        erro_exp = np.sum((y - y_exp) ** 2)
        exp_valida = True
    else:
        a_exp = b_exp_coef = erro_exp = None
        exp_valida = False

    x_dense = np.linspace(x.min(), x.max(), 200)
    caminho = os.path.join(pasta, "t3p3_ajustes.png")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(x, y, color="black", s=60, label="Dados originais", zorder=5)
    ax.plot(x_dense, a_reta + b_reta * x_dense, "b--", label=f"Reta (erro²={erro_reta:.3f})")
    ax.plot(x_dense, a_parab + b_parab * x_dense + c_parab * x_dense**2, "g-.",
            label=f"Parábola (erro²={erro_parab:.3f})")
    if exp_valida:
        ax.plot(x_dense, a_exp * np.exp(b_exp_coef * x_dense), "r:",
                label=f"Exponencial (erro²={erro_exp:.3f})")
    ax.set_title("Ajustes por Mínimos Quadrados")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)

    result = {
        "ajuste_reta": {"a": float(a_reta), "b": float(b_reta),
                        "erro_quadratico": float(erro_reta)},
        "ajuste_parabola": {"a": float(a_parab), "b": float(b_parab), "c": float(c_parab),
                            "erro_quadratico": float(erro_parab)},
        "exp_valida": bool(exp_valida),
        "grafico": caminho,
    }
    if exp_valida:
        result["ajuste_exponencial"] = {
            "a": float(a_exp), "b": float(b_exp_coef),
            "erro_quadratico": float(erro_exp),
            "observacao": "Ajuste feito em ln(y); erro² calculado em y apenas para comparação.",
        }
    return result


def area_secao_navio(larguras=None, h=0.4, pasta=RESULTS_DIR):
    if larguras is None:
        larguras = np.array([3.00, 2.92, 2.75, 2.52, 2.30, 1.84, 0.92], dtype=float)
    larguras = np.asarray(larguras, dtype=float)
    _garantir_pasta(pasta)

    n = len(larguras) - 1  # número de intervalos
    simpson_possivel = (n % 2 == 0)

    area_trapezio = (h / 2) * (larguras[0] + 2 * np.sum(larguras[1:n]) + larguras[n])

    if simpson_possivel:
        soma_impar = np.sum(larguras[1:n:2])
        soma_par = np.sum(larguras[2:n:2])
        area_simpson = (h / 3) * (larguras[0] + 4 * soma_impar + 2 * soma_par + larguras[n])
    else:
        area_simpson = None

    x_pts = np.arange(len(larguras)) * h
    caminho = os.path.join(pasta, "t4p3_secao_navio.png")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_pts, larguras, "bo-", label="Larguras medidas")
    ax.fill_between(x_pts, larguras, 0, color="skyblue", alpha=0.4, label="Área estimada")
    ax.set_title("Seção transversal do navio")
    ax.set_xlabel("Posição (m)")
    ax.set_ylabel("Largura (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)

    return {
        "metodo_trapezio": {"area": float(area_trapezio)},
        "metodo_simpson": {"area": float(area_simpson) if simpson_possivel else None},
        "dados": {"larguras_m": larguras.tolist(), "espacamento_m": float(h)},
        "grafico": caminho,
    }


def main():
    _garantir_pasta()

    print("=" * 60)
    print("RESOLUÇÃO — Atividade Complementar LES710C")
    print("=" * 60 + "\n")

    res1 = resolver_producao_eletronica()
    print(f"[1/4] T1.P1 — Solução: {res1['solucao']}, residual={res1['residual_norm']:.2e}\n")

    res2 = resolver_ponte_wheatstone()
    print(f"[2/4] T2.P1 — Vb={res2['potenciais']['Vb']:.4f} V, "
          f"Vc={res2['potenciais']['Vc']:.4f} V")
    correntes = {k: f"{v:.4f} A" for k, v in res2["correntes"].items()}
    print(f"           Correntes: {correntes}\n")

    res3 = ajuste_minimos_quadrados()
    print(f"[3/4] T3.P3 — Erro reta²={res3['ajuste_reta']['erro_quadratico']:.3f}, "
          f"parábola²={res3['ajuste_parabola']['erro_quadratico']:.3f}")
    if res3.get("exp_valida", False):
        print(f"              Erro exponencial²={res3['ajuste_exponencial']['erro_quadratico']:.3f}")
    print()

    res4 = area_secao_navio()
    print(f"[4/4] T4.P3 — Área (Trapézio): {res4['metodo_trapezio']['area']:.4f} m²")
    area_s = res4["metodo_simpson"]["area"]
    if area_s is not None:
        print(f"              Área (Simpson): {area_s:.4f} m²\n")
    else:
        print("              Área (Simpson): não aplicável (número ímpar de intervalos)\n")

    relatorio = {
        "T1_P1_producao": res1,
        "T2_P1_wheatstone": res2,
        "T3_P3_minimos_quadrados": res3,
        "T4_P3_area_navio": res4,
    }

    caminho_json = os.path.join(RESULTS_DIR, "relatorio_calculo_numerico.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(to_serializable(relatorio), f, indent=2, ensure_ascii=False)

    print(f"✅ Relatório salvo em {caminho_json}")


if __name__ == "__main__":
    main()