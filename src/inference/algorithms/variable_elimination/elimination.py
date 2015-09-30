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