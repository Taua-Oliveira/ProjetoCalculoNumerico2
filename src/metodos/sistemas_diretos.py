"""Tópico 1 — Sistemas lineares: métodos diretos (Decomposição LU)."""
import numpy as np

TOLERANCIA_PIVO = 1e-14


def decomposicao_lu(A):
    """Decomposição LU com pivoteamento parcial: P·A = L·U.

    Retorna (P, L, U): P é a matriz de permutação, L é triangular inferior
    com 1 na diagonal e U é triangular superior.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("A matriz de coeficientes precisa ser quadrada.")

    U = A.copy()
    L = np.zeros((n, n))
    perm = list(range(n))

    for k in range(n - 1):
        # Pivoteamento parcial: escolhe a linha com maior |pivô| na coluna k
        p = k + int(np.argmax(np.abs(U[k:, k])))
        if abs(U[p, k]) < TOLERANCIA_PIVO:
            raise ValueError("Matriz singular: o sistema não tem solução única.")
        if p != k:
            U[[k, p]] = U[[p, k]]
            L[[k, p], :k] = L[[p, k], :k]
            perm[k], perm[p] = perm[p], perm[k]

        for i in range(k + 1, n):
            m = U[i, k] / U[k, k]  # multiplicador
            L[i, k] = m
            U[i, k:] -= m * U[k, k:]

    if abs(U[n - 1, n - 1]) < TOLERANCIA_PIVO:
        raise ValueError("Matriz singular: o sistema não tem solução única.")

    np.fill_diagonal(L, 1.0)
    P = np.eye(n)[perm]
    return P, L, U


def substituicao_progressiva(L, b):
    """Resolve L·y = b (L triangular inferior)."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y


def substituicao_retroativa(U, y):
    """Resolve U·x = y (U triangular superior)."""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


def resolver_lu(A, b):
    """Resolve A·x = b por decomposição LU. Retorna (x, P, L, U)."""
    b = np.asarray(b, dtype=float)
    P, L, U = decomposicao_lu(A)
    y = substituicao_progressiva(L, P @ b)
    x = substituicao_retroativa(U, y)
    return x, P, L, U
