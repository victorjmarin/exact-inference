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
