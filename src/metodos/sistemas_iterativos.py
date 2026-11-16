"""Tópico 2 — Sistemas lineares: métodos iterativos (Gauss-Seidel)."""
import numpy as np


def criterio_sassenfeld(A):
    """Retorna os betas de Sassenfeld; a convergência é garantida se max(beta) < 1."""
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    beta = np.zeros(n)
    for i in range(n):
        s = np.sum(np.abs(A[i, :i]) * beta[:i]) + np.sum(np.abs(A[i, i + 1:]))
        beta[i] = s / abs(A[i, i])
    return beta


def gauss_seidel(A, b, x0=None, tol=1e-4, max_iter=1000):
    """Método de Gauss-Seidel para um sistema n×n.

    Critério de parada: erro relativo max|x(k+1) - x(k)| / max|x(k+1)| < tol.
    Se x0 não for informado, usa x0_i = b_i / a_ii.
    Retorna um dicionário com a solução, as iterações e o histórico.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    n = len(b)
    if np.any(np.abs(np.diag(A)) < 1e-14):
        raise ValueError("Há zero na diagonal principal; reordene as equações.")

    x = (b / np.diag(A)) if x0 is None else np.array(x0, dtype=float)
    historico = [x.copy()]
    erro = np.inf

    for k in range(1, max_iter + 1):
        x_ant = x.copy()
        for i in range(n):
            soma = A[i, :i] @ x[:i] + A[i, i + 1:] @ x[i + 1:]
            x[i] = (b[i] - soma) / A[i, i]
        historico.append(x.copy())
        denom = np.max(np.abs(x))
        erro = np.max(np.abs(x - x_ant)) / (denom if denom > 0 else 1.0)
        if erro < tol:
            return {"x": x, "iteracoes": k, "convergiu": True,
                    "erro": erro, "historico": np.array(historico)}

    return {"x": x, "iteracoes": max_iter, "convergiu": False,
            "erro": erro, "historico": np.array(historico)}
