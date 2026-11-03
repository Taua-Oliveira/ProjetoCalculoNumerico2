"""
Saída dos resultados: tabelas no terminal e janelas com os gráficos.

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: Giovanni Éber, Tauã Oliveira

Só depende do formato Resultado (resultado.py): não sabe nada de como cada
método calcula, apenas lê os campos prontos para exibição:

    resultado.tabelas      -> [{"titulo": ..., "cabecalho": [...], "linhas": [[...]]}]
    resultado.figuras      -> figuras Matplotlib já montadas pelo solver
    resultado.observacoes  -> notas de rodapé (avisos, observações)

Fluxo de exibição (um caso por vez):
    exibir_resultado -> imprimir_resultado  (tabelas alinhadas no terminal)
                    -> mostrar_figuras     (uma janela por figura, bloqueante)

Os solvers criam as próprias figuras porque só eles sabem o que faz sentido
plotar; este módulo cuida da parte comum: formatação de tabelas e abertura
das janelas.
"""

import matplotlib.pyplot as plt

from resultado import Resultado


def _formatar_linha(linha) -> list[str]:
    """Converte uma linha de tabela para texto; None vira '—'."""
    return ["—" if valor is None else str(valor) for valor in linha]


def _larguras_por_coluna(cabecalho: list[str], linhas: list[list[str]]) -> list[int]:
    """Largura de cada coluna = maior comprimento entre cabeçalho e linhas."""
    todas_as_linhas = [cabecalho] + linhas
    return [max(len(str(valor)) for valor in coluna) for coluna in zip(*todas_as_linhas)]


def imprimir_resultado(resultado: Resultado) -> None:
    """Imprime no terminal o cabeçalho do problema e as tabelas do resultado."""
    print()
    print("=" * 60)
    print(f" {resultado.problema}")
    print(f" Método: {resultado.metodo}")
    print("=" * 60)

    if resultado.falhou:
        print(f"\n  O método falhou: {resultado.erro}\n")
        return

    for tabela in resultado.tabelas:
        cabecalho = [str(c) for c in tabela["cabecalho"]]
        linhas = [_formatar_linha(l) for l in tabela["linhas"]]
        larguras = _larguras_por_coluna(cabecalho, linhas)

        print(f"\n  {tabela['titulo']}")
        print("  " + " | ".join(c.ljust(l) for c, l in zip(cabecalho, larguras)))
        print("  " + "-+-".join("-" * l for l in larguras))
        for linha in linhas:
            print("  " + " | ".join(c.ljust(l) for c, l in zip(linha, larguras)))

    if resultado.observacoes:
        print()
        for nota in resultado.observacoes:
            print(f"  * {nota}")

    print()


def mostrar_figuras(resultado: Resultado) -> None:
    """
    Abre uma janela por figura, na ordem, aguardando o fechamento de cada
    uma antes de seguir (é isso que garante a leitura "um gráfico por vez").
    """
    if not resultado.figuras:
        print("  (nenhum gráfico para este resultado)\n")
        return

    total = len(resultado.figuras)
    print(f"  Abrindo {total} janela(s) de gráfico; feche cada uma para continuar.\n")

    for i, fig in enumerate(resultado.figuras, start=1):
        titulo = f"{resultado.problema} — figura {i} de {total}"
        try:
            fig.canvas.manager.set_window_title(titulo)
        except AttributeError:
            pass  # backend sem gerenciador de janela (ex.: ambientes remotos)
        plt.show()
        plt.close(fig)


def exibir_resultado(resultado: Resultado) -> None:
    """Exibe o resultado completo: tabelas no terminal + gráficos nas janelas."""
    imprimir_resultado(resultado)
    mostrar_figuras(resultado)


if __name__ == "__main__":
    # Autoteste de demonstração: roda SEM depender de nenhum solver.
    # Serve para conferir tabelas e janelas durante o desenvolvimento.
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(0, 2.5, 200)
    ax.plot(x, np.exp(-x) * np.cos(2 * x))
    ax.set_title("Exemplo de gráfico do relatório")
    ax.grid(alpha=0.3)

    exemplo = Resultado(
        metodo="(demo)",
        problema="Autoteste do relatorio.py",
        tipo="demo",
        tabelas=[{
            "titulo": "Tabela de exemplo",
            "cabecalho": ["Parâmetro", "Valor"],
            "linhas": [["Amplitude inicial", "1,00"], ["Decaimento", "0,40"]],
        }],
        figuras=[fig],
        observacoes=["Este é apenas um teste visual do módulo relatorio.py."],
    )
    exibir_resultado(exemplo)