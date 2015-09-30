import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination

network = XMLBIF.load_preset_network('fire_alarm')

"""
# Consulta predefinida

evidence_variable_1 = EvidenceVariable(network.get_node_by_name('report'), 'T')
evidence_variable_2 = EvidenceVariable(network.get_node_by_name('tampering'), 'T')

query = Query(network.get_node_by_name('fire'), [evidence_variable_1, evidence_variable_2])
"""

# Consulta aleatoria
query = Query.random(network, 2)

ve = VariableElimination(network)
ve.heuristic = 'random'
ve.mode = 'verbose'
ve.query = query
ve.run()

