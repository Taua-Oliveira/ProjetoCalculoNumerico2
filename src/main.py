"""
Simulador de Métodos Numéricos Aplicados à Problemas do Cotidiano do Engenheiro.
Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2 (Atividade Complementar)

Equipe: Giovanni Éber, Caio Benevides, Tauã Oliveira

Como executar:
    pip install -r requirements.txt
    python main.py

Fluxo do programa:
    main.py (menu)
      -> casos.py                    (os 4 problemas sorteados)
      -> entrada.py                  (ler_float / ler_int — só quando o caso usa)
      -> execucao.py                 (despacha pelo campo "tipo" do caso)
           -> metodos_diretos.py     (T1 — produção de componentes eletrônicos)
           -> metodos_iterativos.py  (T2 — ponte de Wheatstone)
           -> ajustes.py             (T3 — mínimos quadrados)
           -> integracao.py          (T4 — área da seção do navio)
      -> relatorio.py                (tabelas no terminal e janelas com gráficos)
      -> volta ao menu, até o usuário escolher 0 (sair)

Este arquivo só tem o menu; o trabalho de verdade está nos outros.
"""

import casos
import execucao
from entrada import ler_float, ler_int


def main() -> None:
    while True:
        print("=" * 60)
        print(" MÉTODOS NUMÉRICOS APLICADOS — Problemas de Engenharia")
        print("=" * 60)
        for i, caso in enumerate(casos.CASOS, start=1):
            print(f" {i}. {caso['nome']}")
        print(" 0. Sair")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            print("Até mais!")
            break

        if not escolha.isdigit() or not 1 <= int(escolha) <= len(casos.CASOS):
            print("Opção inválida, tente novamente.\n")
            continue

        caso = casos.CASOS[int(escolha) - 1]

        # Parâmetros adicionais: só são pedidos quando o caso prevê
        # (no momento, apenas o T2 — iterativo — usa tolerância e max_iter).
        opcoes = {}
        if "tol_padrao" in caso:
            opcoes["tol"] = ler_float(
                f"Precisão tol (Enter = {caso['tol_padrao']}): ",
                padrao=caso["tol_padrao"],
            )
        if "max_iter_padrao" in caso:
            opcoes["max_iter"] = ler_int(
                f"Máximo de iterações (Enter = {caso['max_iter_padrao']}): ",
                padrao=caso["max_iter_padrao"],
            )

        execucao.executar_e_mostrar(caso, **opcoes)


if __name__ == "__main__":
    main()
