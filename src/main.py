"""
Cálculo Numérico — UNIVASF 2026.2 — Atividade Complementar (Projeto 2)

Equipe: Tauã Oliveira, Giovanni Éber, Caio Benevides

Como executar:
    pip install -r requirements.txt
    python main.py

Fluxo do programa:
    main.py (menu)
      -> executar_topicoN()  (um por módulo, cada um com a sua entrada e saída)
           -> entrada.py      (leitura validada)
           -> método numérico (devolve um dataclass de resultado.py)
           -> relatorio.py    (mostra na tela)
      -> volta ao menu, até o usuário escolher 0 (sair)

Este arquivo só tem o menu.
"""

from ajuste import executar_topico3
from integracao import executar_topico4
from metodos_diretos import executar_topico1
from metodos_iterativos import executar_topico2

TOPICOS = [
    ("Tópico 1 — Sistemas lineares: métodos diretos (Gauss)", executar_topico1),
    ("Tópico 2 — Sistemas lineares: métodos iterativos (Gauss-Seidel)", executar_topico2),
    ("Tópico 3 — Mínimos quadrados (reta, parábola, exponencial)", executar_topico3),
    ("Tópico 4 — Integração numérica (Trapézio e Simpson)", executar_topico4),
]


def main() -> None:
    while True:
        print("=" * 60)
        print(" CÁLCULO NUMÉRICO — Atividade Complementar")
        print("=" * 60)
        for i, (nome, _) in enumerate(TOPICOS, start=1):
            print(f" {i}. {nome}")
        print(" 0. Sair")

        try:
            escolha = input("\nEscolha uma opção: ").strip()
        except EOFError:
            print()
            break

        if escolha == "0":
            print("Até mais!")
            break

        if not escolha.isdigit() or not 1 <= int(escolha) <= len(TOPICOS):
            print("Opção inválida, tente novamente.\n")
            continue

        _, executar = TOPICOS[int(escolha) - 1]
        executar()
        print()


if __name__ == "__main__":
    main()