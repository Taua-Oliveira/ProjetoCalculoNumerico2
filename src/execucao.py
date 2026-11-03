"""
Execução: liga o caso escolhido ao seu método e devolve o Resultado.

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: (a definir — a divisão de tarefas será fechada em grupo)

Os módulos de método não são conhecidos diretamente: cada um é procurado
pelo campo "tipo" do caso, na tabela SOLVERS. Assim, o núcleo do programa
fica independente dos métodos — para acrescentar um problema novo basta
criar o módulo com uma função `resolver(caso, **opcoes)` e registrá-la aqui.

Fluxo:
    executar_caso      -> procura o solver do tipo, roda e devolve o
                          Resultado (se o módulo ainda não existir, devolve
                          um Resultado marcando "método não implementado")
    executar_e_mostrar -> executar_caso + relatorio.exibir_resultado
"""

import importlib

from resultado import Resultado
import relatorio

# tipo do caso -> (nome do módulo, nome da função)
SOLVERS = {
    "producao":   ("metodos_diretos", "resolver"),
    "wheatstone": ("metodos_iterativos", "resolver"),
    "ajustes":    ("ajustes", "resolver"),
    "navio":      ("integracao", "resolver"),
}


def executar_caso(caso: dict, **opcoes) -> Resultado:
    """Roda o solver correspondente ao caso e devolve o Resultado.

    As opções extras (tol, max_iter, ...) são repassadas ao solver; cada
    módulo usa o que fizer sentido para o seu problema.
    """
    tipo = caso.get("tipo", "")

    if tipo not in SOLVERS:
        return Resultado(
            metodo="(sem solver cadastrado)",
            problema=caso.get("nome", tipo),
            tipo=tipo,
            sucesso=False,
            erro=f"não existe método cadastrado para o tipo '{tipo}'",
        )

    nome_modulo, nome_funcao = SOLVERS[tipo]
    try:
        modulo = importlib.import_module(nome_modulo)
        solver = getattr(modulo, nome_funcao)
        return solver(caso, **opcoes)
    except ImportError:
        return Resultado(
            metodo="(em implementação)",
            problema=caso.get("nome", tipo),
            tipo=tipo,
            sucesso=False,
            erro=f"o módulo '{nome_modulo}' ainda não existe — método em desenvolvimento",
        )
    except Exception as erro:  # nunca deixar o programa morrer numa conta
        return Resultado(
            metodo="(erro interno)",
            problema=caso.get("nome", tipo),
            tipo=tipo,
            sucesso=False,
            erro=f"ocorreu um erro inesperado: {erro}",
        )


def executar_e_mostrar(caso: dict, **opcoes) -> Resultado:
    """Executa o caso e exibe o resultado (tabelas no terminal + gráficos)."""
    resultado = executar_caso(caso, **opcoes)
    relatorio.exibir_resultado(resultado)
    return resultado
