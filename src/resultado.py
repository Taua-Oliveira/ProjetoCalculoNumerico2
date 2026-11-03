"""
Resultado: o formato que os solvers devolvem e o relatorio consome.

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: Giovanni Éber, Tauã Oliveira

Fluxo: cada módulo de método (metodos_diretos.py, metodos_iterativos.py,
ajustes.py, integracao.py) preenche um Resultado; o relatorio.py só lê
estes campos para montar as tabelas e mostrar os gráficos, sem saber como
cada método calcula.

erro x aviso:
    erro  -> o método falhou e o resultado não vale (ex.: sistema impossível);
    aviso -> o resultado vale, mas algo merece registro
             (ex.: convergência lenta, muitos arredondamentos).
"""

from dataclasses import dataclass, field


@dataclass
class Resultado:
    """Envelope padrão de saída de qualquer método numérico do projeto."""

    metodo: str            # Ex.: "Decomposição LU", "Gauss-Seidel", "Simpson"
    problema: str          # Ex.: "T1 — Produção de componentes eletrônicos"
    tipo: str              # "producao", "wheatstone", "ajustes" ou "navio";
                           # é o que diz ao relatorio qual gráfico montar

    sucesso: bool = True
    erro: str | None = None       # mensagem de falha (None se deu tudo certo)
    aviso: str | None = None      # observação que não invalida o resultado
    tempo_ms: float = 0.0         # tempo de execução do método, em milissegundos
    iteracoes: int | None = None  # número de iterações (None se não se aplica)

    # Tabelas prontas para exibição. Cada item é um dicionário no formato:
    # {"titulo": str, "cabecalho": [str, ...], "linhas": [[..., ...], ...]}
    tabelas: list[dict] = field(default_factory=list)

    # Figuras Matplotlib já montadas pelo módulo que resolveu o problema
    figuras: list = field(default_factory=list)

    # Notas de rodapé (avisos, observações sobre arredondamento etc.)
    observacoes: list[str] = field(default_factory=list)

    @property
    def falhou(self) -> bool:
        """True se o método registrou falha (flag ou mensagem de erro)."""
        return not self.sucesso or self.erro is not None