"""Métodos numéricos implementados à mão, um módulo por tópico da disciplina.

O numpy é usado apenas para guardar vetores e matrizes.
"""
from .sistemas_diretos import decomposicao_lu, resolver_lu
from .sistemas_iterativos import criterio_sassenfeld, gauss_seidel
from .minimos_quadrados import ajuste_reta, ajuste_parabola, ajuste_exponencial
from .integracao import trapezio_repetido, simpson_repetido
