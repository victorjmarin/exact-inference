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