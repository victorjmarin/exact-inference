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

from random import choice
from inference.EvidenceVariable import EvidenceVariable

class Query:
    """
    Clase Query destinada a la representacion de consultas sobre una red bayesiana.

    Las consultas se componen de una variable de consulta y, generalmente, de una o mas variables de evidencia.
    """

    def __init__(self, query_variable, evidence_variables = []):
        """
        Inicializacion de la consulta estableciendo la variable de consulta y las variables de evidencia.
        """
        self.query_variable = query_variable
        self.evidence_variables = evidence_variables


    def query_nodes(self):
        """
        Devuelve todas las variables involucradas en la consulta, tanto de evidencia como de consulta.

        @rtype:  list
        @return: Lista de variables de la consulta.
        """
        query_nodes = [ev.observed_variable for ev in self.evidence_variables]
        query_nodes.append(self.query_variable)
        return query_nodes


    def __str__(self):
        """
        Devuelve la representacion como cadena de una consulta.

        @rtype:  str
        @return: Cadena con el formato P(variable de consulta | variables de evidencia separadas por comas).
        """
        evidence_variables = ""

        if self.evidence_variables:
            num_evidence_vars = len(self.evidence_variables)
            evidence_variables = ' | '

            for i in range(num_evidence_vars):
                evidence_variables += str(self.evidence_variables[i])

                if i != num_evidence_vars - 1:
                    evidence_variables += ', '

        return 'P(' + self.query_variable.name + evidence_variables + ')'


    @staticmethod
    def random(network, num_observations = None):
        """
        Devuelve una consulta al azar realizable sobre una red bayesiana. Si no se especifica un numero de observaciones, se elige aleatoriamente.

        @type  network: BayesNet
        @param network: Red bayesiana.

        @type  num_observations: int
        @param num_observations: Numero de observaciones [0, cardinal del dominio].

        @raise Exception: Si el numero de observaciones solicitado no es valido, no se creara la consulta.

        @rtype:  Query
        @return: Consulta aleatoria a una red bayesiana.
        """

        network_nodes = network.nodes()

        max_observations = len(network_nodes) - 1

        query_variable = choice(network_nodes)
        network_nodes.remove(query_variable)

        evidence_variables = []

        if num_observations == None:
            num_observations = choice(range(0, max_observations + 1))

        if num_observations >= 0 and num_observations <= max_observations:
            for i in range(0, num_observations):
                observed_variable = choice(network_nodes)
                network_nodes.remove(observed_variable)

                observed_value = choice(observed_variable.domain)

                new_observation = EvidenceVariable(observed_variable, observed_value)
                evidence_variables.append(new_observation)
        else:
            raise Exception('El numero de observaciones no es valido.')

        return Query(query_variable, evidence_variables)

