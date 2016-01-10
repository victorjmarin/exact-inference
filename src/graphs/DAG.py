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

from graphs.pygraph.classes.digraph import digraph
from graphs.pygraph.algorithms.cycles import find_cycle

class DAG(digraph):
    """
    Clase DAG destinada a la representacion de Grafos Aciclicos Dirigidos (Directed Acyclic Graphs).
    
    Los DAG se componen de nodos y aristas dirigidas, sin que estas formen ciclos.
    """

    def __init__(self):
        """
        Inicializacion del DAG segun la clase padre.
        """
        super().__init__()


    def add_edge(self, edge):
        """
        Anade una arista dirigida al grafo conectando dos nodos.
        
        Una arista es un par de nodos de la forma (nodo1, nodo2).

        @type  edge: tuple
        @param edge: Arista.

        @raise Exception: Si la arista a anadir produce un ciclo, no sera anadida y se lanzara una excepcion.
        """
        super().add_edge(edge)
        cycle = find_cycle(self)
        if cycle:
            raise Exception("La arista " + str(edge) + " produciria el ciclo " + str(cycle))
