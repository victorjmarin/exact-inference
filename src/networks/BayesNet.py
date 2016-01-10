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

from graphs.DAG import DAG
from graphs.pygraph.algorithms.traversal import traversal

class BayesNet:
    """
    Clase BayesNet destinada a la representacion de redes bayesianas.
    
    Las redes bayesianas se componen de un nombre y un DAG (Directed Acyclic Graph).
    """
    
    def __init__(self, name):
        self.name = name
        self.graph = DAG()


    def nodes(self):
        """
        Devuelve los nodos de la red.

        @rtype:  list
        @return: Lista de variables aleatorias que se encuentran en la red.
        """
        return self.graph.nodes()


    def get_node_by_name(self, name):
        """
        Recupera un nodo de la red por su nombre.

        @type  name: str
        @param name: Nombre de la variable aleatoria.

        @rtype:  RandomVariable
        @return: Variable aleatoria cuyo nombre coincide.
        """
        return next((node for node in self.nodes() if node.name == name), None)


    def edges(self):
        """
        Devuelve las aristas de la red.

        @rtype:  list
        @return: Lista de aristas de la red.
        """
        return self.graph.edges()


    def add_node(self, node):
        """
        Pone una variable aleatoria en la red.

        @type  node: RandomVariable
        @param node: Variable aleatoria que poner en la red.
        """
        self.graph.add_node(node)


    def add_edge(self, edge):
        """
        Pone una arista en la red.

        @type  edge: tuple
        @param edge: Arista que poner en la red.
        """
        self.graph.add_edge(edge)


    def is_predecessor(self, node_x, node_y):
        """
        Comprueba si node_x es antecesor de node_y segun Dietz’s numbering scheme.

        @type  node_x: RandomVariable
        @param node_x: Nodo antecesor.

        @type  node_y: RandomVariable
        @param node_y: Nodo descendiente.

        @rtype:  boolean
        @return: Valor de verdad acerca de si x es antecesor de y.
        """
        pre_iterator = traversal(self.graph, node_x, 'pre')
        post_iterator = traversal(self.graph, node_x, 'post')

        pre_tree = [node for node in pre_iterator]
        post_tree = [node for node in post_iterator]

        is_predecessor = False

        if(node_y in pre_tree):
            is_predecessor = (pre_tree.index(node_x) < pre_tree.index(node_y)) and (post_tree.index(node_x) > post_tree.index(node_y))

        return is_predecessor
