class RandomVariable:
    """
    Clase RandomVariable destinada a la representacion de variables aleatorias.
    
    Las variables aleatorias se componen de un nombre, un dominio y una tabla de probabilidad condicional.
    """

    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.cpt = None


    def __str__(self):
        """
        Devuelve la representacion como cadena de una variable aleatoria.

        @rtype:  str
        @return: Nombre de la variable aleatoria.
        """
        return self.name