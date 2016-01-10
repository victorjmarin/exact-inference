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

def get_irrelevant_factors(network, query, relevant_factors):

    # Calcular diferencia entre nodos de la red y nodos de la consulta.
    query_nodes = query.query_nodes()
    network_nodes = network.nodes()
    difference = list(set(network_nodes) - set(query_nodes))

    # Obtener los nodos que no son antecesor de ninguna de las variables de la consulta.
    f_is_predecessor = network.is_predecessor
    not_predecessors = __get_not_predecessors(difference, query_nodes, f_is_predecessor)

    # Obtener los factores que contienen a los nodos que no son antecesores.
    irrelevant_factors = {rf for np in not_predecessors for rf in relevant_factors if rf.contains_variable(np)}

    return list(irrelevant_factors)


def __get_not_predecessors(difference, query_nodes, f_is_predecessor):
    not_predecessors = []

    for node_x in difference:
        is_predecessor = False

        for node_y in query_nodes:
            is_predecessor = is_predecessor or f_is_predecessor(node_x, node_y)

            if is_predecessor:
                break

        if not is_predecessor:
            not_predecessors.append(node_x)

    return not_predecessors
