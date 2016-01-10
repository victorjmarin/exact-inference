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

import math
import utils.utils as utils
import inference.algorithms.variable_elimination.heuristics as heuristics
import inference.algorithms.variable_elimination.elimination as elimination
import inference.algorithms.variable_elimination.observation as observation
import inference.algorithms.variable_elimination.sumout as sumout

from inference.Factor import Factor


class VariableElimination:
    """
    Clase VariableElimination destinada a controlar el flujo del algoritmo de Eliminacion de Variables.
    """

    # Numero de decimales de la probabilidad inferida.
    OUTPUT_DECIMALS = 5

    def __init__(self, bayes_net, heuristic = 'min-degree', mode = 'brief'):
        self.bayes_net = bayes_net
        self.query = None
        self.heuristic = heuristic
        self.mode = mode
        self.initial_factors = []
        self.relevant_factors = []
        self.eliminated_factors = []
        self.print_solution = True

    def run(self):

        # Como los factores iniciales son siempre los mismos dada una red bayesiana, 
        # los almacenamos como un atributo para no tener que recomputarlos con cada consulta.

        # 1. Calcular factores iniciales
        if self.is_first_query():
            self.__get_initial_factors()
        else:
            # Reiniciar indices y factores eliminados de la consulta anterior.
            Factor.CURRENT_ID = len(self.initial_factors)
            self.eliminated_factors = []

        # Establecer los factores relevantes igual a los factores iniciales e imprimir estado.
        self.relevant_factors = list(self.initial_factors)
        self.__execution_status(0)

        # 2. Eliminar variables irrelevantes e imprimir estado.
        self.__prune_irrelevant_variables()
        self.__execution_status(1)

        # 3. Proyectar observaciones si las hay e imprimir estado.
        if self.query.evidence_variables:
            self.__project_observations()
            self.__execution_status(2)

        # 4. Eliminar variables ocultas e imprimir estado.
        self.__execution_status(3)
        self.__sum_out_hidden_variables()

        # 5. Multiplicar factores finales.
        self.__execution_status(4)
        self.__multiply_final_factors()

        # 6. Normalizar factor final e imprimir estado.
        self.__normalize()
        self.__execution_status(5)


    # 1. GET INITIAL FACTORS

    def __get_initial_factors(self):

        for node in self.bayes_net.nodes():

            factor_nodes = [parent_node for parent_node in self.bayes_net.graph.incidents(node)]
            factor_nodes.append(node)

            initial_factor = Factor(factor_nodes, node.cpt)
            self.initial_factors.append(initial_factor)


    # 2. PRUNE IRRELEVANT VARIABLES

    def __prune_irrelevant_variables(self):

        # Obtener factores irrelevantes.
        self.eliminated_factors = elimination.get_irrelevant_factors(self.bayes_net, self.query, self.relevant_factors)

        # Si se ha eliminado algun factor, quitarlo de los factores relevantes.
        if self.eliminated_factors:
            self.relevant_factors = list(set(self.relevant_factors) - set(self.eliminated_factors))


    # 3. PROJECT OBSERVATIONS

    def __project_observations(self):

        for evidence_var in self.query.evidence_variables:
            appearing_factors = utils.appearing_factors(evidence_var.observed_variable, self.relevant_factors)

            while(appearing_factors):
                observation.project_observation(appearing_factors, evidence_var, self.relevant_factors, self.eliminated_factors, self.initial_factors, self.query.evidence_variables)


    # 4. SUM OUT HIDDEN VARIABLES

    def __sum_out_hidden_variables(self):

        # Obtener las variables ocultas.
        hidden_vars = sumout.get_hidden_variables(self.relevant_factors, self.query.query_variable)

        if hidden_vars:

            # Repetir el proceso mientras queden variables por eliminar.
            while(hidden_vars):

                # Obtener la siguiente variable a eliminar segun la heuristica.
                elimination_variable = heuristics.get_elimination_variable(hidden_vars, self.relevant_factors, self.heuristic)

                # Eliminar la variable.
                sumout.sum_out(elimination_variable, self.relevant_factors, self.mode, self.eliminated_factors, self.query.query_variable)

                # Quitar la variable de las variables ocultas una vez eliminada.
                hidden_vars.remove(elimination_variable)

        elif self.mode == "verbose":
            print('No hay variables ocultas.\n')


    # 5. MULTIPLY FINAL FACTORS

    def __multiply_final_factors(self):

        if len(self.relevant_factors) > 1:
            elimination_variable = self.relevant_factors[0].query_variable()
            sumout.sum_out(elimination_variable, self.relevant_factors, self.mode, self.eliminated_factors, self.query.query_variable)

        elif self.mode == "verbose":
            print('No es necesario multiplicar.\n')


    # 6. NORMALIZE

    def __normalize(self):

        final_factor = self.relevant_factors[0]

        total = math.fsum(final_factor.cpt.values())

        if total != 0:
            for key in final_factor.cpt.keys():
                final_factor.cpt[key] = round(final_factor.cpt[key] / total, VariableElimination.OUTPUT_DECIMALS)


    def is_first_query(self):
        return not self.initial_factors


    def __execution_status(self, step, current_factors = None, eliminated_factors = None):

        if self.mode == 'verbose':

            status = ['CALCULAR FACTORES INICIALES', 'ELIMINAR VARIABLES IRRELEVANTES', 'PROYECTAR OBSERVACIONES', 
            'ELIMINAR VARIABLES OCULTAS', 'MULTIPLICAR FACTORES FINALES', 'NORMALIZAR FACTOR FINAL']

            print(status[step] + '\n')
            if step in [0, 1, 2]:
                print('Factores actuales: ' + str([str(factor) for factor in self.relevant_factors]))
                print('Factores eliminados: ' + str([str(factor) for factor in self.eliminated_factors]) + '\n')

        if step == 5 and self.print_solution:
            print(str(self.query) + ' = ' + str(self.relevant_factors[0].cpt))
