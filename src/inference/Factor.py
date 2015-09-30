class Factor:
    """
    Clase Factor destinada a la representacion de factores en la inferencia sobre una red bayesiana.
    
    Los factores se componen de un identificador entero, un conjunto de variables (factors) y una tabla de probabilidad (cpt).
    """

    CURRENT_ID = 0

    def __init__(self, factors, cpt, auto_increment = True):
        self.id = Factor.CURRENT_ID
        self.factors = factors
        self.cpt = cpt
        if auto_increment:
            Factor.CURRENT_ID += 1


    def query_variable(self):
        """
        Devuelve la variable de consulta asociada al factor.

        @rtype:  RandomVariable
        @return: Variable de consulta asociada al factor.
        """
        return self.factors[-1]


    def evidence_variables(self):
        """
        Devuelve las variables de evidencia asociadas al factor.

        @rtype:  list
        @return: Lista de variables de evidencia asociadas al factor.
        """
        number_of_factors = len(self.factors)
        evidence_var = None
        if number_of_factors > 1:
            evidence_var = self.factors[0:number_of_factors - 1]
        return evidence_var


    def contains_variable(self, variable):
        """
        Comprueba si una variable se encuentra presente en el factor.

        @type  variable: RandomVariable
        @param variable: Variable a comprobar si pertenece al factor.

        @rtype:  boolean
        @return: Valor booleano indicando la presencia o no de la variable en el factor.
        """
        return variable in self.factors


    def __str__(self):
        """
        Devuelve la representacion como cadena de un factor.

        @rtype:  str
        @return: Cadena con el formato fID(variables de la consulta que representa separadas por comas).
        """
        factors = [str(f) for f in self.factors]
        return 'f' + str(self.id) + '(' + str(factors) + ')'