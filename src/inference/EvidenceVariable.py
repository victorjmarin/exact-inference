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
