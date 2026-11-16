"""Leitura de dados digitados pelo usuário, com validação.

Aceita vírgula ou ponto como separador decimal. Em listas, os valores são
separados por espaço ou ';'.
"""
import numpy as np

# Quando True (opção --auto), todas as perguntas recebem o valor padrão.
MODO_AUTO = False


def perguntar(msg):
    if MODO_AUTO:
        print(msg)
        return ""
    try:
        return input(msg)
    except EOFError:
        return ""


def _num(txt):
    return float(txt.strip().replace(",", "."))


def ler_float(msg, padrao=None, positivo=False):
    while True:
        sufixo = f" [Enter = {padrao:g}]" if padrao is not None else ""
        txt = perguntar(f"{msg}{sufixo}: ").strip()
        if not txt and padrao is not None:
            return float(padrao)
        try:
            v = _num(txt)
        except ValueError:
            print("  ⚠ Valor inválido. Exemplo: 3,89 ou 3.89")
            continue
        if positivo and v <= 0:
            print("  ⚠ O valor deve ser positivo.")
            continue
        return v


def ler_int(msg, padrao=None, minimo=1):
    while True:
        sufixo = f" [Enter = {padrao}]" if padrao is not None else ""
        txt = perguntar(f"{msg}{sufixo}: ").strip()
        if not txt and padrao is not None:
            return int(padrao)
        try:
            v = int(txt)
        except ValueError:
            print("  ⚠ Digite um número inteiro.")
            continue
        if v < minimo:
            print(f"  ⚠ O valor deve ser pelo menos {minimo}.")
            continue
        return v


def ler_texto(msg, padrao):
    return perguntar(f"{msg} [Enter = {padrao}]: ").strip() or padrao


def ler_vetor(msg, n=None, minimo=1):
    """Lê uma lista de números; se n for dado, exige exatamente n valores."""
    while True:
        txt = perguntar(f"{msg}: ").strip()
        partes = txt.replace(";", " ").split()
        try:
            v = np.array([_num(p) for p in partes], dtype=float)
        except ValueError:
            print("  ⚠ Use espaço ou ';' entre os números. Ex.: 3,89 0,095 0,282")
            continue
        if n is not None and len(v) != n:
            print(f"  ⚠ Esperados {n} valores, recebidos {len(v)}.")
            continue
        if len(v) < minimo:
            print(f"  ⚠ Informe pelo menos {minimo} valor(es).")
            continue
        return v


def ler_matriz(n, nome="A"):
    print(f"Digite as {n} linhas da matriz {nome} ({n} valores por linha):")
    return np.array([ler_vetor(f"  linha {i + 1}", n) for i in range(n)])


def sim_nao(msg, padrao="s"):
    txt = perguntar(f"{msg} (s/n) [Enter = {padrao}]: ").strip().lower()
    return (txt or padrao).startswith("s")


def usar_dados_enunciado():
    """True = usar os dados do enunciado; False = digitar novos dados."""
    txt = perguntar("\n  [Enter] usar dados do enunciado   [n] digitar novos dados: ")
    return txt.strip().lower() not in ("n", "nao", "não")
