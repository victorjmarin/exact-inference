class EvidenceVariable:
    """
    Clase EvidenceVariable destinada a la representacion de observaciones sobre una red bayesiana.
    
    Las variables de evidencia se componen de una variable observada y un valor observado.
    """

    def __init__(self, observed_variable, observed_value = None):
        self.observed_variable = observed_variable
        self.observed_value = observed_value


    def __str__(self):
        """
        Devuelve la representacion como cadena de una variable de evidencia.

        @rtype:  str
        @return: Cadena con el formato variable_observada = valor_observado.
        """
        string = self.observed_variable.name
        if self.observed_value:
            string += ' = ' + self.observed_value
        return string