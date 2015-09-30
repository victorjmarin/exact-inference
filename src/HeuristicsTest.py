import sys
import time
import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination


def calculate_queries(network):

    print('Generando consultas aleatorias...\n')

    queries = []
    for i in range(0, 100):

        q = Query.random(network, 3)
        queries.append(q)

    return queries



def run_test(algorithm, queries):

    print('Realizando ' + str(len(queries)) + ' consultas sobre la red ' + network.name + '.')

    algorithm.print_solution = False

    algorithm.heuristic = 'min-fill'

    start = time.clock()

    print('\nCalculando min-fill...')

    for q in queries:
        algorithm.query = q
        algorithm.run()

    end = time.clock()
    total2 = end - start

    print('\nTiempo min-fill: ' + str(total2))


    algorithm.heuristic = 'min-factor'

    start = time.clock()

    print('\nCalculando min-factor...')

    for q in queries:
        algorithm.query = q
        algorithm.run()

    end = time.clock()
    total2 = end - start

    print('\nTiempo min-factor: ' + str(total2))


    algorithm.heuristic = 'min-degree'

    start = time.clock()

    print('\nCalculando min-degree...')

    for q in queries:
        algorithm.query = q
        algorithm.run()

    end = time.clock()
    total2 = end - start

    print('\nTiempo min-degree: ' + str(total2))


    algorithm.heuristic = 'random'

    start = time.clock()

    print('\nCalculando random...')

    for q in queries:
        elapsed_time = time.clock() - start
        if elapsed_time < 10:
            algorithm.query = q
            algorithm.run()
        else:
            sys.exit("Tiempo de ejecucion excedido.")

    end = time.clock()
    total2 = end - start

    print('\nTiempo random: ' + str(total2) + '\n')


network = XMLBIF.load_preset_network('electrical_diagnosis')

queries = calculate_queries(network)

algorithm = VariableElimination(network)

run_test(algorithm, queries)


network = XMLBIF.load_preset_network('win95pts')

queries = calculate_queries(network)

algorithm = VariableElimination(network)

run_test(algorithm, queries)