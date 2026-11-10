"""
Entrada de dados: transforma o que o usuário digita em algo que os
métodos conseguem usar, sem deixar o programa quebrar com entrada inválida.

Todas as funções CONVERSAM com o usuário: perguntam, validam e perguntam
de novo até a resposta ser válida. Os métodos numéricos não chamam nada daqui.

Convenções (iguais às do projeto 1):
    - vírgula decimal é aceita ("0,5" -> 0.5);
    - notação científica é aceita ("1e-4");
    - Enter vazio usa o valor padrão, quando existe.
    - para digitar VÁRIOS números numa linha, separe com ESPAÇO ou ";"
      (a vírgula é reservada para o decimal).
"""

import math


def ler_float(mensagem: str, padrao: float | None = None) -> float:
    """Pergunta um número ao usuário até ele digitar algo válido."""
    while True:
        leitura = input(mensagem).strip()

        if leitura == "" and padrao is not None:
            return padrao

        leitura = leitura.replace(",", ".")
        try:
            valor = float(leitura)
        except ValueError:
            print("  Valor inválido. Digite um número, ex.: 0,5 ou 1e-4")
            continue

        if not math.isfinite(valor):
            print("  Digite um número finito.")
            continue

        return valor


def ler_int(mensagem: str, padrao: int | None = None, minimo: int = 1) -> int:
    """Pergunta um inteiro (>= minimo) ao usuário até ele digitar algo válido."""
    while True:
        leitura = input(mensagem).strip()

        if leitura == "" and padrao is not None:
            return padrao

        try:
            valor = int(leitura)
        except ValueError:
            print("  Valor inválido. Digite um número inteiro.")
            continue

        if valor < minimo:
            print(f"  Valor inválido. Digite um inteiro maior ou igual a {minimo}.")
            continue

        return valor


def ler_sim_nao(mensagem: str, padrao: bool | None = None) -> bool:
    """Pergunta s/n. Enter usa o padrão, se existir."""
    while True:
        leitura = input(mensagem).strip().lower()
        if leitura == "" and padrao is not None:
            return padrao
        if leitura in ("s", "sim"):
            return True
        if leitura in ("n", "nao", "não"):
            return False
        print("  Responda com s ou n.")


def ler_lista(mensagem: str, quantidade: int) -> list[float]:
    """
    Lê `quantidade` números numa única linha, separados por espaço ou ";".
    Repete a pergunta se faltar ou sobrar número, ou se algum for inválido.
    """
    while True:
        partes = input(mensagem).replace(";", " ").split()

        if len(partes) != quantidade:
            print(f"  Digite exatamente {quantidade} números (você digitou {len(partes)}).")
            continue

        try:
            valores = [float(p.replace(",", ".")) for p in partes]
        except ValueError:
            print("  Algum valor é inválido. Use números, ex.: 4 3 2,5")
            continue

        if not all(math.isfinite(v) for v in valores):
            print("  Digite apenas números finitos.")
            continue

        return valores


def ler_vetor(n: int, nome: str = "b") -> list[float]:
    """Lê um vetor de n números (uma linha)."""
    return ler_lista(f"Vetor {nome} ({n} valores): ", n)


def ler_matriz(n: int, nome: str = "A") -> list[list[float]]:
    """Lê uma matriz quadrada n x n, uma linha por vez."""
    print(f"Matriz {nome} ({n}x{n}), uma linha por vez:")
    return [ler_lista(f"  linha {i + 1}: ", n) for i in range(n)]


def ler_sistema() -> tuple[list[list[float]], list[float]]:
    """
    Lê um sistema linear completo A·x = b (usado nos Tópicos 1 e 2).
    Devolve (A, b). Mostra o sistema e pede confirmação antes de devolver.
    """
    while True:
        n = ler_int("Número de incógnitas (n): ", minimo=1)
        A = ler_matriz(n)
        b = ler_vetor(n)

        print("\nSistema lido:")
        for i in range(n):
            print("  " + "  ".join(f"{A[i][j]:>10g}" for j in range(n)) + f"  |  {b[i]:>10g}")
        if ler_sim_nao("Está correto? (s/n): "):
            return A, b


def ler_pontos(minimo: int = 2) -> tuple[list[float], list[float]]:
    """
    Lê uma tabela de pontos (x, y), um ponto por linha (Tópico 3).
    Devolve (xs, ys).
    """
    n = ler_int(f"Quantidade de pontos (mínimo {minimo}): ", minimo=minimo)
    xs: list[float] = []
    ys: list[float] = []
    for i in range(n):
        x, y = ler_lista(f"  ponto {i + 1} (x y): ", 2)
        xs.append(x)
        ys.append(y)
    return xs, ys


def ler_valores_igualmente_espacados() -> tuple[float, list[float]]:
    """
    Lê h (espaçamento) e os valores y0..yn (Tópico 4).
    Devolve (h, ys).
    """
    h = ler_float("Espaçamento h entre os pontos: ")
    while h <= 0:
        print("  h precisa ser maior que zero.")
        h = ler_float("Espaçamento h entre os pontos: ")
    n_pontos = ler_int("Quantidade de pontos (mínimo 2): ", minimo=2)
    ys = ler_lista(f"Os {n_pontos} valores de y, na ordem: ", n_pontos)
    return h, ys