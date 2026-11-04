"""
Ajustes por mínimos quadrados: reta, parábola e exponencial.
Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: (a definir — a divisão de tarefas será fechada em grupo)

ESQUELETO — implementação pendente (o programa já roda mostrando este aviso).

Quando preenchido, este módulo vai:
    1. ler os pontos (x, F(x)) do caso;
    2. ajustar por mínimos quadrados uma reta, uma parábola e uma
       exponencial (esta última linearizada por ln);
    3. calcular o erro quadrático de cada ajuste: soma de (F(xi) - G(xi))²;
    4. montar a tabela comparativa e o gráfico das três curvas sobre os
       dados, devolvendo tudo num Resultado.
"""

from resultado import Resultado


def resolver(caso: dict, **opcoes) -> Resultado:
    """Ponto de entrada padrão (mesma assinatura nos quatro solvers).

    Recebe o caso (dicionário de casos.py) e devolve um Resultado pronto
    para o relatorio.py. As opções extras (tol, max_iter, ...) são
    ignoradas neste módulo.
    """
    return Resultado(
        metodo="Mínimos quadrados",
        problema=caso.get("nome", ""),
        tipo=caso.get("tipo", ""),
        sucesso=False,
        erro="método ainda não implementado (esqueleto)",
    )
