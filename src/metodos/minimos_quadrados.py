"""Tópico 3 — Ajuste de curvas por mínimos quadrados."""
import numpy as np

from .sistemas_diretos import resolver_lu


def ajuste_polinomial(x, y, grau):
    """Monta e resolve (por LU) as equações normais de um polinômio.

    Retorna os coeficientes [c0, c1, ..., c_grau] de c0 + c1·x + c2·x² + ...
    """
    m = grau + 1
    S = np.array([[np.sum(x ** (i + j)) for j in range(m)] for i in range(m)])
    r = np.array([np.sum(y * x ** i) for i in range(m)])
    coef, *_ = resolver_lu(S, r)
    return coef


def _resultado(funcao, x, y, texto, **coef):
    g = funcao(x)
    return {**coef, "funcao": funcao, "texto": texto,
            "erro": float(np.sum((y - g) ** 2))}


def ajuste_reta(x, y):
    a, b = ajuste_polinomial(x, y, 1)
    return _resultado(lambda t: a + b * t, x, y,
                      f"g(x) = {a:.6f} + ({b:.6f})·x", a=a, b=b)


def ajuste_parabola(x, y):
    a, b, c = ajuste_polinomial(x, y, 2)
    return _resultado(lambda t: a + b * t + c * t ** 2, x, y,
                      f"g(x) = {a:.6f} + ({b:.6f})·x + ({c:.6f})·x²", a=a, b=b, c=c)


def ajuste_exponencial(x, y):
    """y = a·e^(b·x), linearizado por ln(y) = ln(a) + b·x. Exige y > 0."""
    if np.any(y <= 0):
        return None
    ln_a, b = ajuste_polinomial(x, np.log(y), 1)
    a = np.exp(ln_a)
    return _resultado(lambda t: a * np.exp(b * t), x, y,
                      f"g(x) = {a:.6f}·e^({b:.6f}·x)", a=a, b=b)
