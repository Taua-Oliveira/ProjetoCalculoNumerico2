"""
Métodos iterativos: sistemas lineares resolvidos por Gauss-Seidel.
Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: (a definir — a divisão de tarefas será fechada em grupo)

ESQUELETO — implementação pendente (o programa já roda mostrando este aviso).

Quando preenchido, este módulo vai:
    1. montar o sistema 2x2 dos potenciais da ponte de Wheatstone;
    2. resolver por Gauss-Seidel, parando quando ||x(k+1) - x(k)|| < tol
       OU ao atingir max_iter (com guarda para NaN/divergência);
    3. guardar o histórico de iterações (para o gráfico de convergência);
    4. calcular as correntes e devolver tudo num Resultado.
"""

from resultado import Resultado


def resolver(caso: dict, **opcoes) -> Resultado:
    """Ponto de entrada padrão (mesma assinatura nos quatro solvers).

    Recebe o caso (dicionário de casos.py) e devolve um Resultado pronto
    para o relatorio.py. As opções extras (tol, max_iter, ...) serão
    usadas quando o método for implementado.
    """
    return Resultado(
        metodo="Gauss-Seidel",
        problema=caso.get("nome", ""),
        tipo=caso.get("tipo", ""),
        sucesso=False,
        erro="método ainda não implementado (esqueleto)",
    )
