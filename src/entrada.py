"""
Entrada de dados: transforma o que o usuário digita em algo que os
métodos conseguem usar, sem deixar o programa quebrar com entrada inválida.

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: Giovanni Éber, Tauã Oliveira

Contém dois tipos de função:
    ler_float, ler_int  -> CONVERSAM com o usuário: perguntam, validam e
                           perguntam de novo até a resposta ser válida
                           (vindas do Projeto 1, sem mudanças).
    ler_vetor,          -> CONVERTEM texto em sequências de números:
    ler_matriz             vetores (ex.: larguras do navio) e matrizes
                           (ex.: coeficientes dos sistemas lineares).

Não foram trazidas do Projeto 1: ler_funcao e montar_caso_personalizado
(este projeto não usa funções simbólicas; o caso personalizado pode ser
revisitado depois, junto do casos.py).
"""

import math


def ler_float(mensagem: str, padrao: float | None = None) -> float:
    """
    Pergunta um número ao usuário até ele digitar algo válido.

    - Aceitar vírgula como separador decimal ("0,5" -> 0.5).
    - Aceitar notação científica ("1e-6").
    - Se padrao não for None e o usuário só apertar Enter, usar o padrão.
    """
    while True:  # repete até o usuário digitar algo válido
        leitura = input(mensagem).strip()  # lê o texto e tira espaços das pontas

        # Enter sem digitar nada: usa o valor padrão, se existir
        if leitura == "" and padrao is not None:
            return padrao

        leitura = leitura.replace(",", ".")  # aceita "0,5" como 0.5

        try:
            valor = float(leitura)  # tenta converter o texto em número
        except ValueError:
            print("  Valor inválido. Digite um número, ex.: 0,5 ou 1e-6")
            continue  # volta para o início do while e pergunta de novo

        # float() aceita "inf" e "nan", que não servem para os métodos
        if not math.isfinite(valor):
            print("  Digite um número finito.")
            continue

        return valor


def ler_int(mensagem: str, padrao: int | None = None) -> int:
    """Igual ao ler_float, mas para inteiros positivos (ex.: max_iter)."""
    while True:  # repete até o usuário digitar algo válido
        leitura = input(mensagem).strip()  # lê o texto e tira espaços das pontas

        # Enter sem digitar nada: usa o valor padrão, se existir
        if leitura == "" and padrao is not None:
            return padrao

        try:
            valor = int(leitura)  # tenta converter o texto em número inteiro
        except ValueError:
            print("  Valor inválido. Digite um número inteiro.")
            continue  # volta para o início do while e pergunta de novo

        # Não faz sentido rodar 0 ou um número negativo de iterações
        if valor <= 0:
            print("  Valor inválido. Digite um número inteiro maior que 0.")
            continue

        return valor


def _texto_para_float(leitura: str) -> float:
    """Converte UM texto ('2,5' ou '1e-6') em float; lança ValueError se não der."""
    valor = float(leitura.replace(",", "."))  # aceita vírgula decimal
    if not math.isfinite(valor):
        raise ValueError("inf/nan não são aceitos")
    return valor


def ler_vetor(mensagem: str, tamanho: int | None = None) -> list[float]:
    """
    Pergunta uma sequência de números e devolve uma lista de floats.

    Como digitar: valores separados por ESPAÇO, tudo em uma linha
    (a vírgula é tratada como separador decimal, não como separador).
        Exemplo:  3 2,92 2,75 2,52

    tamanho: se informado, exige exatamente essa quantidade de valores;
    sem informar, aceita qualquer quantidade a partir de 1.
    Repete a pergunta até a resposta ser válida.
    """
    while True:
        leitura = input(mensagem).strip()

        if leitura == "":
            print("  Digite pelo menos um número. Exemplo: 3 2,92 2,75")
            continue

        partes = leitura.split()  # separa pelos espaços
        try:
            valores = [_texto_para_float(parte) for parte in partes]
        except ValueError:
            print("  Valor inválido na sequência. Exemplo: 3 2,92 2,75")
            continue

        if tamanho is not None and len(valores) != tamanho:
            print(f"  Preciso de exatamente {tamanho} valores, você digitou {len(valores)}.")
            continue

        return valores


def ler_matriz(mensagem: str, formato: tuple[int, int] | None = None) -> list[list[float]]:
    """
    Pergunta uma matriz e devolve como lista de listas de floats
    (a multiplicação por np.asarray fica a cargo de quem for usar).

    Como digitar: linhas separadas por ';' e valores separados por ESPAÇO,
    tudo em uma linha (a vírgula é tratada como separador decimal):
        Exemplo:  4 3 2; 1 3 1; 2 1 3

    formato: se informado como (linhas, colunas), exige essa dimensão.
    Repete a pergunta até a resposta ser válida.
    """
    while True:
        leitura = input(mensagem).strip()

        if leitura == "":
            print("  Digite a matriz. Exemplo: 4 3 2; 1 3 1; 2 1 3")
            continue

        # Cada linha da matriz é um trecho entre ';'
        linhas_texto = [linha.strip() for linha in leitura.split(";") if linha.strip() != ""]

        try:
            matriz = [[_texto_para_float(valor) for valor in linha.split()]
                      for linha in linhas_texto]
        except ValueError:
            print("  Valor inválido na matriz. Use ';' entre linhas e espaço entre números.")
            continue

        if len(matriz) == 0:
            print("  A matriz precisa ter pelo menos uma linha.")
            continue

        quantos_por_linha = {len(linha) for linha in matriz}
        if len(quantos_por_linha) != 1:
            print("  Todas as linhas precisam ter a mesma quantidade de números.")
            continue

        n_linhas, n_colunas = len(matriz), len(matriz[0])
        if formato is not None and (n_linhas, n_colunas) != formato:
            print(f"  Esperava uma matriz {formato[0]}x{formato[1]}, recebi {n_linhas}x{n_colunas}.")
            continue

        return matriz