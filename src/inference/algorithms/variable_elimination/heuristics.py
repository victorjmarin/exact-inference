# Copyright (c) 2013 Víctor J. Marín <victorjmarin@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import itertools
import utils.utils as utils

from random import choice

def __min_degree(variables, relevant_factors):
    """
    Min. Degree: Devuelve el nodo con el menor numero de conexiones.

    @type  variables: set
    @param variables: Conjunto de variables ocultas que quedan en la red bayesiana.

    @type  relevant_factors: list
    @param relevant_factors: Lista de factores relevantes de la red bayesiana.

    @rtype:  Node
    @return: Nodo a eliminar segun la heuristica.
    """
    new_factor_length = lambda var: len(set(itertools.chain.from_iterable([f.factors for f in utils.appearing_factors(var, relevant_factors)])))
    return min(variables, key=new_factor_length)


def __min_fill(variables, relevant_factors):
    """
    Min. Fill: Devuelve el nodo que al eliminarlo introducira el menor numero de conexiones nuevas.

    @type  variables: set
    @param variables: Conjunto de variables ocultas que quedan en la red bayesiana.

    @type  relevant_factors: list
    @param relevant_factors: Lista de factores relevantes de la red bayesiana.

    @rtype:  Node
    @return: Nodo a eliminar segun la heuristica.
    """
    minimum = float("inf")
    elimination_variable = None

    for var in variables:
        new_edges_count = 0
        appearing_factors = utils.appearing_factors(var, relevant_factors)

        for f1 in appearing_factors:
            f1_position = appearing_factors.index(f1)
            appearing_factors_size = len(appearing_factors)

            for f2 in range(f1_position + 1, appearing_factors_size):
                f2_factors = appearing_factors[f2].factors
                intersection_size = len(set(f1.factors) & set(f2_factors))
                new_edges_count += (len(f1.factors) - intersection_size) * (len(f2_factors) - intersection_size)

        if new_edges_count < minimum:
            minimum = new_edges_count
            elimination_variable = var

    return elimination_variable


def __min_factor(variables, relevant_factors):
    """
    Min. Factor: Devuelve el nodo de menor peso, siendo el peso de cada nodo el producto del cardinal del dominio de sus vecinos.

    @type  variables: set
    @param variables: Conjunto de variables ocultas que quedan en la red bayesiana.

    @type  relevant_factors: list
    @param relevant_factors: Lista de factores relevantes de la red bayesiana.

    @rtype:  Node
    @return: Nodo a eliminar segun la heuristica.
    """
    minimum = float('inf')
    elimination_variable = None

    for var in variables:
        neighbors = set(list(itertools.chain.from_iterable([f.factors for f in utils.appearing_factors(var, relevant_factors)])))
        neighbors.remove(var)
        weight = 1

        for n in neighbors:
            weight *= len(n.domain)

        if weight < minimum:
            minimum = weight
            elimination_variable = var

    return elimination_variable


def __random(variables):
    """
    Random: Devuelve un nodo cualquiera.

    @type  variables: set
    @param variables: Conjunto de variables ocultas que quedan en la red bayesiana.

    @rtype:  Node
    @return: Nodo a eliminar segun la heuristica.
    """
    return choice(list(variables))


def get_elimination_variable(hidden_vars, relevant_factors, heuristic):
    """
    Llama a la funcion heuristica solicitada y devuelve su resultado.

    @type  hidden_vars: set
    @param hidden_vars: Conjunto de variables ocultas que quedan en la red bayesiana.

    @type  relevant_factors: list
    @param relevant_factors: Lista de factores relevantes de la red bayesiana.

    @type  heuristic: str
    @param heuristic: Cadena identificadora de la heuristica deseada.

    @rtype:  Node
    @return: Nodo a eliminar segun la heuristica.
    """
    heuristics = {'min-degree': __min_degree, 'min-factor': __min_factor, 'min-fill': __min_fill, 'random': __random}

    if heuristic == 'random':
        return heuristics[heuristic](hidden_vars)

    return heuristics[heuristic](hidden_vars, relevant_factors)
