import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination

network = XMLBIF.load_preset_network('simple_diagnosis')

"""
# Consulta predefinida

evidence_variable_1 = EvidenceVariable(network.get_node_by_name('Influenza'), 'T')
evidence_variable_2 = EvidenceVariable(network.get_node_by_name('Fever'), 'F')
evidence_variable_3 = EvidenceVariable(network.get_node_by_name('Wheezing'), 'T')

query = Query(network.get_node_by_name('Smokes'), [evidence_variable_1, evidence_variable_2, evidence_variable_3])
"""

# Consulta aleatoria
query = Query.random(network, 3)

ve = VariableElimination(network)
ve.heuristic = 'min-factor'
ve.mode = 'verbose'
ve.query = query
ve.run()

