"""Tópico 4 — Integração numérica (regras do Trapézio e de Simpson repetidas)."""
import numpy as np


def trapezio_repetido(y, h):
    y = np.asarray(y, dtype=float)
    return h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


def simpson_13_repetido(y, h):
    """Simpson 1/3 repetido. Exige número PAR de subintervalos."""
    y = np.asarray(y, dtype=float)
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("Simpson 1/3 exige número par de subintervalos.")
    return h / 3 * (y[0] + 4 * np.sum(y[1:n:2]) + 2 * np.sum(y[2:n:2]) + y[n])


def simpson_38(y, h):
    """Simpson 3/8 simples (exatamente 3 subintervalos, 4 pontos)."""
    return 3 * h / 8 * (y[0] + 3 * y[1] + 3 * y[2] + y[3])


def simpson_repetido(y, h):
    """Simpson repetido para qualquer n ≥ 2.

    n par   → Simpson 1/3 em todo o intervalo.
    n ímpar → Simpson 1/3 nos n-3 primeiros subintervalos + 3/8 nos 3 últimos.
    Retorna (valor, descrição do que foi usado).
    """
    y = np.asarray(y, dtype=float)
    n = len(y) - 1
    if n < 2:
        raise ValueError("São necessários pelo menos 3 pontos.")
    if n % 2 == 0:
        return simpson_13_repetido(y, h), f"Simpson 1/3 em {n} subintervalos"
    if n == 3:
        return simpson_38(y, h), "Simpson 3/8 em 3 subintervalos"
    parte1 = simpson_13_repetido(y[: n - 2], h)
    parte2 = simpson_38(y[n - 3:], h)
    return parte1 + parte2, (f"Simpson 1/3 em {n - 3} subintervalos + "
                             f"Simpson 3/8 nos 3 últimos (n = {n} é ímpar)")
