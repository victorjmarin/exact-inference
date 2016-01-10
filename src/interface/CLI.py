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

import os
import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.Factor import Factor
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination

class CLI:

    algorithm = None

    def start():
        options = {'1': CLI.preset_network, '2': CLI.specify_network_route}
        menu_options = ['Elegir red predefinida', 'Especificar ruta del archivo XMLBIF']
        index = CLI.build_menu(menu_options, back = False)
        CLI.call_function(options[index])


    def preset_network():
        print('\nRedes predefinidas disponibles:')
        options = {'1': CLI.load_network, '2': CLI.load_network, '3': CLI.load_network, '4': CLI.load_network, '5': CLI.start}
        file_name = {'1': 'fire_alarm', '2': 'simple_diagnosis', '3': 'electrical_diagnosis', '4': 'win95pts'}
        menu_options = ['Fire Alarm', 'Simple Diagnosis', 'Electrical Diagnosis Problem', 'Windows 95 Printer Troubleshooter']
        index = CLI.build_menu(menu_options)
        if(index != '5'):
            CLI.call_function(options[index], file_name[index])
        else:
            CLI.call_function(options[index])


    def specify_network_route():
        network_file = input('\nIntroduzca la ruta del archivo XMLBIF: ')
        CLI.call_function(CLI.load_network, network_file, True)


    def load_network(network_file, external = False):
        print('\nCargando red...')
        if external:
            network = XMLBIF.read(network_file)
        else:
            network = XMLBIF.load_preset_network(network_file)
        CLI.algorithm = None
        print('Red bayesiana \"' + network.name + '\"' + ' cargada.')
        CLI.network_operations(network)


    def network_operations(network):
        print('\n' + network.name)
        options = {'1': CLI.query_type, '2': CLI.network_nodes, '3': CLI.preset_network}
        menu_options = ['Inferencia', 'Nodos de la red']
        index = CLI.build_menu(menu_options)
        if(index != '3'):
            CLI.call_function(options[index], network)
        else:
            CLI.call_function(options[index])


    def query_type(network):
        print('\nSeleccione el tipo de consulta:')
        options = {'1': CLI.custom_query, '2': CLI.random_query, '3': CLI.network_operations}
        menu_options = ['Consulta personalizada', 'Consulta aleatoria']
        index = CLI.build_menu(menu_options)
        CLI.call_function(options[index], network)


    def custom_query(network):
        query_variable = input('\nIntroduzca la variable de consulta: ')
        node = network.get_node_by_name(query_variable)
        if node not in network.graph.nodes():
            print('\nEl nodo \"' + query_variable + '\" no existe en la red.')
            CLI.custom_query(network)

        query = Query(node)
        query.evidence_variables = []
        CLI.current_query(network, query)


    def random_query(network):
        max_observations = len(network.nodes()) - 1
        observations = input('\nIntroduzca el numero de observaciones [0, ' + str(max_observations) + ']: ')
        query = Query.random(network, int(observations))
        CLI.current_query(network, query)


    def network_nodes(network):
        print('\n' + str([node.name for node in network.nodes()]))
        options = {'1': CLI.node_info, '2': CLI.network_operations}
        menu_options = ['Ver informacion de nodo']
        index = CLI.build_menu(menu_options)
        CLI.call_function(options[index], network)


    def node_info(network):
        node_name = input('\nIntroduzca el nombre del nodo del cual quiere ver su informacion: ')
        node = network.get_node_by_name(node_name)
        if not node:
            print('\nEl nodo \"' + node_name + '\" no existe en la red.')
            CLI.node_info(network)
        print('\nNombre: ' + node.name)
        print('Dominio: ' + str(node.domain))
        print('Nodos incidentes: ' + str([node.name for node in network.graph.incidents(node)]))
        print('Tabla de probabilidad: ' + str(node.cpt))
        options = {'1': CLI.node_info, '2': CLI.network_operations}
        menu_options = ['Consultar otro nodo']
        index = CLI.build_menu(menu_options)
        CLI.call_function(options[index], network)


    def current_query(network, query):
        print('\nConsulta actual: ' + str(query))
        options = {'1': CLI.make_observation, '2': CLI.variable_elimination, '3': CLI.query_type,'4': CLI.network_operations}
        menu_options = ['Hacer observacion', 'Realizar inferencia', 'Cambiar consulta']
        index = CLI.build_menu(menu_options)
        if(index != '3' and index != '4'):
            CLI.call_function(options[index], network, query)
        else:
            CLI.call_function(options[index], network)


    def make_observation(network, query):
        evidence_variable = input('\nIntroduzca la variable observada: ')
        evidence_node = network.get_node_by_name(evidence_variable)
        if not evidence_node:
            print('\nLa variable \"' + evidence_variable + '\" no existe.')
            CLI.make_observation(network, query)
        print('Los posibles valores observados son: ' + str(evidence_node.domain))
        observed_value = input('Introduzca el valor observado: ')
        if observed_value not in evidence_node.domain:
            print('\nEl valor \"' + observed_value + '\" no existe.')
            CLI.make_observation(network, query)
        evidence = EvidenceVariable(evidence_node, observed_value)
        query.evidence_variables.append(evidence)
        CLI.current_query(network, query)


    def variable_elimination(network, query):
        if not CLI.algorithm:
            CLI.algorithm = VariableElimination(network)
        CLI.algorithm.query = query
        print('\nSeleccione una heuristica:')
        options = {'1': CLI.execution_mode, '2': CLI.execution_mode, '3': CLI.execution_mode, '4': CLI.execution_mode, '5': CLI.current_query}
        heuristics = {'1': 'min-degree', '2': 'min-fill', '3': 'min-factor', '4': 'random'}
        menu_options = ['Min. Degree', 'Min. Fill', 'Min. Factor', 'Random']
        index = CLI.build_menu(menu_options)
        if(index != '5'):
            CLI.call_function(options[index], heuristics[index])
        else:
            CLI.call_function(options[index], network, query)


    def execution_mode(heuristic):
        print('\nSeleccione un modo de ejecucion:')
        options = {'1': CLI.brief, '2': CLI.verbose, '3': CLI.variable_elimination}
        menu_options = ['Modo rapido', 'Modo traza']
        index = CLI.build_menu(menu_options)
        if(index != '3'):
            CLI.call_function(options[index], heuristic)
        else:
            CLI.call_function(options[index], CLI.algorithm.bayes_net, CLI.algorithm.query)


    def brief(heuristic):
        CLI.algorithm.mode = 'brief'
        CLI.algorithm.heuristic = heuristic
        print('\nEjecutando ' + heuristic + ' en modo rapido...\n')
        CLI.algorithm.run()
        CLI.new_query_or_exit(heuristic)


    def verbose(heuristic):
        CLI.algorithm.mode = 'verbose'
        CLI.algorithm.heuristic = heuristic
        print('\nEjecutando ' + heuristic + ' en modo traza...\n')
        CLI.algorithm.run()
        CLI.new_query_or_exit(heuristic)


    def new_query_or_exit(heuristic):
        Factor.CURRENT_ID = 0
        options = {'1': CLI.query_type, '2': CLI.exit, '3': CLI.execution_mode}
        menu_options = ['Realizar otra consulta', 'Salir']
        index = CLI.build_menu(menu_options)
        if index == '1':
            CLI.call_function(options[index], CLI.algorithm.bayes_net)
        elif index == '2':
            CLI.call_function(options[index])
        else:
            CLI.call_function(options[index], heuristic)


    def exit():
        return 0


    def call_function(function, *args):
        try:
            function(*args)
        except KeyError:
            print('Instruccion no reconocida.')


    def build_menu(menu_options, back = True):
        count = 1
        menu = ''
        double_new_line = '\n\n'
        for option in menu_options:
            menu += '\n' + str(count) + '. ' + option
            count += 1
            if (menu_options.index(option) == len(menu_options) - 1) and not back:
                menu += double_new_line
        if back:
            menu += '\n' + str(count) + '. ' + 'Atras' + double_new_line
        return input(menu)
