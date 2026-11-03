"""
Casos: os problemas sorteados para a equipe, com os dados oficiais do
enunciado (Atividade Complementar LES710C — UNIVASF 2026.2).

Cálculo Numérico — UNIVASF 2026.2 — Projeto Unidade 2
Responsável: Giovanni Éber, Tauã Oliveira

Cada caso é um dicionário com os dados do problema e um campo "tipo"
que diz aos módulos de método qual cálculo executar:

    tipo "producao"   -> T1: produção de componentes eletrônicos
                          (sistema linear, métodos diretos)
    tipo "wheatstone" -> T2: ponte de Wheatstone
                          (sistema linear, métodos iterativos)
    tipo "ajustes"    -> T3: ajuste de curvas por mínimos quadrados
                          (reta, parábola e exponencial)
    tipo "navio"      -> T4: área da seção do navio
                          (integração numérica: trapézio e Simpson)

Os números foram transcritos diretamente do PDF da atividade e conferidos
com o texto extraído.
"""

CASOS = [
    {
        # ------------------------------------------------------------------
        # TÓPICO 1 — Problema 1 (métodos diretos)
        # Sistema Ax = b: cada linha é um material (cobre, zinco, vidro) e
        # cada coluna é um componente (transistor, resistor, chip).
        # ------------------------------------------------------------------
        "nome": "T1 — Produção de componentes eletrônicos",
        "topico": "Tópico 1 — Sistemas de equações lineares: métodos diretos",
        "tipo": "producao",
        "matriz": [
            [4, 3, 2],   # cobre por componente
            [1, 3, 1],   # zinco por componente
            [2, 1, 3],   # vidro por componente
        ],
        "disponibilidade": [960, 510, 610],  # unidades disponíveis na semana
        "nomes_componentes": ["Transistor", "Resistor", "Chip"],
        "nomes_materiais": ["Cobre", "Zinco", "Vidro"],
    },
    {
        # ------------------------------------------------------------------
        # TÓPICO 2 — Problema 1 (métodos iterativos)
        # Ponte de Wheatstone: fonte E entre os nós A e D; R1 (A-B), R2 (A-C),
        # R3 (C-D), R4 (B-D) e R5 (transversal B-C). Incógnitas: potenciais Vb e Vc.
        # ------------------------------------------------------------------
        "nome": "T2 — Ponte de Wheatstone",
        "topico": "Tópico 2 — Sistemas de equações lineares: métodos iterativos",
        "tipo": "wheatstone",
        "E": 30.0,      # volts
        "R1": 20.0,     # ohms
        "R2": 120.0,    # ohms
        "R3": 120.0,    # ohms
        "R4": 120.0,    # ohms
        "R5": 120.0,    # ohms
        "tol_padrao": 1e-4,
        "max_iter_padrao": 1000,
    },
    {
        # ------------------------------------------------------------------
        # TÓPICO 3 — Problema 3 (mínimos quadrados)
        # Ajustar reta, parábola e exponencial aos dados; apresentar também o
        # erro quadrático cometido = soma (F(xi) - G(xi))^2 de cada ajuste.
        # ------------------------------------------------------------------
        "nome": "T3 — Ajuste de curvas por mínimos quadrados",
        "topico": "Tópico 3 — Interpolação polinomial / mínimos quadrados",
        "tipo": "ajustes",
        "x": [0, 1.5, 2.6, 4.2, 6.0, 8.2, 10.0, 11.4],
        "F": [18, 13, 11, 9, 6, 4, 2, 1],
    },
    {
        # ------------------------------------------------------------------
        # TÓPICO 4 — Problema 3 (integração numérica)
        # Larguras medidas da seção do navio (estações A até A6), igualmente
        # espaçadas de h = 0,4 m.
        # Obs. da figura: aparecem 8 estações (A...A7) e 7 espaçamentos de
        # 0,4 m; a última estação (A7) NÃO tem largura mediana marcada -- ela
        # serve apenas para fechar o desenho. A integração usa as 7 larguras
        # medidas (6 intervalos), cenário em que a Regra de Simpson Repetida
        # é aplicável sem ajustes (número par de intervalos). Se depois o
        # professor indicar outra leitura da figura, basta editar esta lista.
        # ------------------------------------------------------------------
        "nome": "T4 — Área da seção do navio",
        "topico": "Tópico 4 — Integração numérica",
        "tipo": "navio",
        "larguras": [3.00, 2.92, 2.75, 2.52, 2.30, 1.84, 0.92],  # metros
        "h": 0.4,  # espaçamento entre estações, em metros
    },
]


def buscar_caso(tipo: str) -> dict:
    """Devolve o primeiro caso com o tipo informado (ex.: 'producao')."""
    for caso in CASOS:
        if caso["tipo"] == tipo:
            return caso
    raise ValueError(f"Não existe caso do tipo '{tipo}'.")