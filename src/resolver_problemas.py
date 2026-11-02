import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt
import json
import os
from typing import Dict, Any


def to_serializable(obj):
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_serializable(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return [to_serializable(v) for v in obj.tolist()]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, complex):
        return {"real": float(obj.real), "imag": float(obj.imag)}
    elif isinstance(obj, (bool, int, float, str, type(None))):
        return obj
    else:
        return str(obj)


def resolver_producao_eletronica(A=None, b=None, nomes_componentes=None, nomes_materiais=None):
    if A is None:
        A = np.array([[4, 3, 2], [1, 3, 1], [2, 1, 3]], dtype=float)
    if b is None:
        b = np.array([960, 510, 610], dtype=float)
    if nomes_componentes is None:
        nomes_componentes = ["Transistor", "Resistor", "Chip"]
    if nomes_materiais is None:
        nomes_materiais = ["Cobre", "Zinco", "Vidro"]

    try:
        P, L, U = scipy.linalg.lu(A)
        Pb = P @ b
        y = scipy.linalg.solve_triangular(L, Pb, lower=True)
        x = scipy.linalg.solve_triangular(U, y, lower=False)
        x = np.round(x, 6)
        residual = A @ x - b
        residual_norm = np.linalg.norm(residual)

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(nomes_componentes, x, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
        ax.set_title("Meta de produção semanal")
        ax.set_ylabel("Quantidade fabricada")
        ax.set_ylim(0, max(x)*1.2)
        for bar, val in zip(bars, x):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    f"{int(val)}", ha='center', va='bottom', fontsize=10)
        plt.tight_layout()
        plt.savefig("results/t1p1_producao.png")
        plt.close(fig)

        return {
            "metodo": "LU decomposition (SciPy)",
            "A": A.tolist(),
            "b": b.tolist(),
            "solucao": {n: float(v) for n, v in zip(nomes_componentes, x)},
            "residual_norm": float(residual_norm),
            "grafico": "results/t1p1_producao.png"
        }
    except Exception as e:
        return {"erro": str(e)}


def resolver_ponte_wheatstone(E=30.0, R1=20.0, R2=120.0, R3=120.0, R4=120.0, R5=120.0, tol=1e-4, max_iter=1000):
    G1, G2, G3, G4, G5 = 1/R1, 1/R2, 1/R3, 1/R4, 1/R5
    a11 = G1 + G4 + G5
    a12 = -G5
    a21 = -G5
    a22 = G2 + G3 + G5
    B_vec = np.array([G1 * E, G2 * E], dtype=float)
    A = np.array([[a11, a12], [a21, a22]])

    beta1 = abs(a12) / abs(a11)
    beta2 = abs(a21) * beta1 / abs(a22)
    convergencia = (beta1 < 1 and beta2 < 1)

    x0 = np.array([B_vec[0]/A[0,0], B_vec[1]/A[1,1]])
    x = x0.copy()
    historico = [x0.copy()]

    for k in range(max_iter):
        x_old = x.copy()
        x[0] = (B_vec[0] - A[0,1] * x[1]) / A[0,0]
        x[1] = (B_vec[1] - A[1,0] * x[0]) / A[1,1]
        historico.append(x.copy())
        if np.linalg.norm(x - x_old) < tol:
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
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(hist_arr[:,0], label="Vb (nó B)", marker='o')
    ax.plot(hist_arr[:,1], label="Vc (nó C)", marker='s')
    ax.set_title(f"Convergência Gauss-Seidel — tolerância {tol}")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Potencial (V)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/t2p1_convergencia.png")
    plt.close(fig)

    return {
        "metodo": "Gauss-Seidel",
        "iteracoes": int(k + 1),
        "convergiu": bool(np.linalg.norm(x - x_old) < tol),
        "criterio_sassenfeld": {"beta1": float(beta1), "beta2": float(beta2),
                                 "satisfaz": bool(convergencia)},
        "potenciais": {"Va": float(Va), "Vb": float(Vb), "Vc": float(Vc), "Vd": float(Vd)},
        "correntes": {"I1": float(I1), "I2": float(I2), "I3": float(I3),
                       "I4": float(I4), "I5": float(I5), "I_total_fonte": float(I_total)},
        "grafico_convergencia": "results/t2p1_convergencia.png",
        "tol_utilizada": float(tol)
    }


def ajuste_minimos_quadrados(x=None, y=None):
    if x is None:
        x = np.array([0, 1.5, 2.6, 4.2, 6.0, 8.2, 10.0, 11.4], dtype=float)
    if y is None:
        y = np.array([18, 13, 11, 9, 6, 4, 2, 1], dtype=float)

    n = len(x)
    sx, sy = np.sum(x), np.sum(y)
    sx2, sxy = np.sum(x**2), np.sum(x*y)

    A_reta = np.array([[n, sx], [sx, sx2]])
    b_reta = np.array([sy, sxy])
    a_reta, b_reta = np.linalg.solve(A_reta, b_reta)
    y_reta = a_reta + b_reta * x
    erro_reta = np.sum((y - y_reta)**2)

    sx3, sx4 = np.sum(x**3), np.sum(x**4)
    sxy2 = np.sum(x**2 * y)
    A_parab = np.array([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]])
    b_parab = np.array([sy, sxy, sxy2])
    a_parab, b_parab, c_parab = np.linalg.solve(A_parab, b_parab)
    y_parab = a_parab + b_parab * x + c_parab * x**2
    erro_parab = np.sum((y - y_parab)**2)

    if np.all(y > 0):
        ln_y = np.log(y)
        sy_ln = np.sum(ln_y)
        sxy_ln = np.sum(x * ln_y)
        A_exp = np.array([[n, sx], [sx, sx2]])
        b_exp = np.array([sy_ln, sxy_ln])
        ln_a_exp, b_exp_coef = np.linalg.solve(A_exp, b_exp)
        a_exp = np.exp(ln_a_exp)
        y_exp = a_exp * np.exp(b_exp_coef * x)
        erro_exp = np.sum((y - y_exp)**2)
        exp_valida = True
    else:
        a_exp, b_exp_coef, y_exp, erro_exp = None, None, None, None
        exp_valida = False

    x_dense = np.linspace(min(x), max(x), 200)
    y_dense_reta = a_reta + b_reta * x_dense
    y_dense_parab = a_parab + b_parab * x_dense + c_parab * x_dense**2

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(x, y, color='red', s=60, label='Dados originais', zorder=5)
    ax.plot(x_dense, y_dense_reta, 'b--', label=f"Reta (erro²={erro_reta:.3f})")
    ax.plot(x_dense, y_dense_parab, 'g-.', label=f"Parábola (erro²={erro_parab:.3f})")
    if exp_valida:
        y_dense_exp = a_exp * np.exp(b_exp_coef * x_dense)
        ax.plot(x_dense, y_dense_exp, 'r:', label=f"Exponencial (erro²={erro_exp:.3f})")
    ax.set_title("Ajustes por Mínimos Quadrados")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/t3p3_ajustes.png")
    plt.close(fig)

    result = {
        "ajuste_reta": {"a": float(a_reta), "b": float(b_reta), "erro_quadratico": float(erro_reta)},
        "ajuste_parabola": {"a": float(a_parab), "b": float(b_parab), "c": float(c_parab), "erro_quadratico": float(erro_parab)},
        "exp_valida": bool(exp_valida)
    }
    if exp_valida:
        result["ajuste_exponencial"] = {"a": float(a_exp), "b": float(b_exp_coef), "erro_quadratico": float(erro_exp)}
    return result


def area_secao_navio(larguras=None, h=0.4):
    if larguras is None:
        larguras = np.array([3.00, 2.92, 2.75, 2.52, 2.30, 1.84, 0.92], dtype=float)
    n = len(larguras) - 1
    simpson_possivel = (n % 2 == 0)

    area_trapezio = (h/2) * (larguras[0] + 2*np.sum(larguras[1:n]) + larguras[n])

    if simpson_possivel:
        soma_par = np.sum(larguras[2:n:2])
        soma_impar = np.sum(larguras[1:n:2])
        area_simpson = (h/3) * (larguras[0] + 4*soma_impar + 2*soma_par + larguras[n])
    else:
        area_simpson = None

    x_pts = np.arange(0, (n+1)*h, h)[:len(larguras)]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_pts, larguras, 'bo-', label="Larguras medidas")
    ax.fill_between(x_pts, larguras, 0, color='skyblue', alpha=0.4, label="Área estimada")
    ax.set_title("Seção transversal do navio")
    ax.set_xlabel("Posição (m)")
    ax.set_ylabel("Largura (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig("results/t4p3_secao_navio.png")
    plt.close(fig)

    return {
        "metodo_trapezio": {"area": float(area_trapezio)},
        "metodo_simpson": {"area": float(area_simpson) if simpson_possivel else None},
        "dados": {"larguras_m": larguras.tolist(), "espacamento_m": float(h)},
        "grafico": "results/t4p3_secao_navio.png"
    }


def main():
    os.makedirs("results", exist_ok=True)

    print("="*60)
    print("RESOLUÇÃO — Atividade Complementar LES710C")
    print("="*60 + "
")

    res1 = resolver_producao_eletronica()
    print(f"[1/4] T1.P1 — Solução: {res1['solucao']}, residual={res1['residual_norm']:.2e}
")

    res2 = resolver_ponte_wheatstone()
    print(f"[2/4] T2.P1 — Vb={res2['potenciais']['Vb']:.4f} V, Vc={res2['potenciais']['Vc']:.4f} V")
    print(f"           Correntes: { {k: f'{v:.4f} A' for k,v in res2['correntes'].items()} }
")

    res3 = ajuste_minimos_quadrados()
    print(f"[3/4] T3.P3 — Erro reta²={res3['ajuste_reta']['erro_quadratico']:.3f}, parábola²={res3['ajuste_parabola']['erro_quadratico']:.3f}")
    if res3.get('exp_valida', False):
        print(f"              Erro exponencial²={res3['ajuste_exponencial']['erro_quadratico']:.3f}
")

    res4 = area_secao_navio()
    print(f"[4/4] T4.P3 — Área (Trapézio): {res4['metodo_trapezio']['area']:.4f} m²")
    print(f"              Área (Simpson): {res4['metodo_simpson']['area']:.4f} m²
")

    relatorio = {
        "T1_P1_producao": res1,
        "T2_P1_wheatstone": res2,
        "T3_P3_minimos_quadrados": res3,
        "T4_P3_area_navio": res4
    }

    relatorio_serial = to_serializable(relatorio)
    with open("results/relatorio_calculo_numerico.json", "w", encoding="utf-8") as f:
        json.dump(relatorio_serial, f, indent=2, ensure_ascii=False)

    print("✅ Relatório salvo em results/relatorio_calculo_numerico.json")

if __name__ == "__main__":
    main()
