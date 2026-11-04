"""
Integração numérica: Regras do Trapézio e de Simpson repetidas.
Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: (a definir — a divisão de tarefas será fechada em grupo)

ESQUELETO — implementação pendente (o programa já roda mostrando este aviso).

Quando preenchido, este módulo vai:
    1. ler as larguras medidas da seção do navio e o espaçamento h;
    2. aplicar a Regra do Trapézio repetida (válida para qualquer número
       de intervalos);
    3. aplicar a Regra de Simpson repetida — com um ajuste no último
       intervalo, já que a seção termina em A7 com largura zero (número
       ímpar de intervalos);
    4. montar as tabelas e o gráfico da seção, devolvendo tudo num
       Resultado.
"""

from resultado import Resultado


def resolver(caso: dict, **opcoes) -> Resultado:
    """Ponto de entrada padrão (mesma assinatura nos quatro solvers).

    Recebe o caso (dicionário de casos.py) e devolve um Resultado pronto
    para o relatorio.py. As opções extras (tol, max_iter, ...) são
    ignoradas neste módulo.
    """
    return Resultado(
        metodo="Trapézio e Simpson",
        problema=caso.get("nome", ""),
        tipo=caso.get("tipo", ""),
        sucesso=False,
        erro="método ainda não implementado (esqueleto)",
    )
