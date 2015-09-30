import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination

network = XMLBIF.load_preset_network('electrical_diagnosis')

"""
# Consulta predefinida

evidence_variable_1 = EvidenceVariable(network.get_node_by_name('w2'), 'live')
evidence_variable_2 = EvidenceVariable(network.get_node_by_name('p1'), 'T')

query = Query(network.get_node_by_name('w0'), [evidence_variable_1, evidence_variable_2])
"""

# Consulta aleatoria
query = Query.random(network, 2)

ve = VariableElimination(network)
ve.heuristic = 'min-degree'
ve.mode = 'verbose'
ve.query = query
ve.run()

