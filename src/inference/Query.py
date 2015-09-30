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

