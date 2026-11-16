"""Atividade Complementar — Cálculo Numérico (LES710C, UNIVASF 2026.2)

Uso:
  python src/main.py          → menu interativo
  python src/main.py --auto   → resolve os 4 problemas com os dados do
                                enunciado e sai
"""
import sys

from interface import entrada as ent
from interface.saida import titulo
from problemas import TODOS


def menu():
    while True:
        titulo("CÁLCULO NUMÉRICO — ATIVIDADE COMPLEMENTAR (LES710C)")
        for i, problema in enumerate(TODOS, start=1):
            print(f"  [{i}] {problema.NOME}")
        print("  [0] Sair")

        op = ent.perguntar("\nEscolha uma opção: ").strip()
        if op == "0":
            print("\nAté mais!")
            return
        if not op.isdigit() or not 1 <= int(op) <= len(TODOS):
            print("  ⚠ Opção inválida.")
            continue

        problema = TODOS[int(op) - 1]
        while True:
            try:
                problema.resolver()
            except KeyboardInterrupt:
                print("\n  (cálculo cancelado)")
            if not ent.sim_nao("\nFazer um novo cálculo deste problema?", "n"):
                break


def main():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")  # acentos e símbolos no terminal do Windows
        except (AttributeError, ValueError):
            pass

    if "--auto" in sys.argv:
        ent.MODO_AUTO = True
        for problema in TODOS:
            problema.resolver()
        return

    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nAté mais!")


if __name__ == "__main__":
    main()
