import utils.XMLBIF as XMLBIF

from inference.Query import Query
from inference.EvidenceVariable import EvidenceVariable
from inference.algorithms.variable_elimination.VariableElimination import VariableElimination

network = XMLBIF.load_preset_network('win95pts')

ve = VariableElimination(network)
ve.heuristic = 'min-fill'
ve.mode = 'brief'

# Consultas predefinidas

# Queremos ver la probabilidad de que sea la velocidad de la red la que este haciendo
# que las impresiones sean demasiado lentas sabiendo que la red esta correctamente configurada.

evidence_variable_1 = EvidenceVariable(network.get_node_by_name('Too Slow'), 'Too Long')
evidence_variable_2 = EvidenceVariable(network.get_node_by_name('Network Configuration'), 'Correct')

query = Query(network.get_node_by_name('Net Speed'), [evidence_variable_1, evidence_variable_2])

ve.query = query
ve.run()

print('\n===========================================\n')

# Queremos conocer la probabilidad de que los drivers esten bien configurados sabiendo que 
# las impresiones muestran graficos distorsionados o incompletos y los graficos son PostScript.

evidence_variable_1 = EvidenceVariable(network.get_node_by_name('Graphics Distorted or Incomplete'), 'Yes')
evidence_variable_2 = EvidenceVariable(network.get_node_by_name('PS Graphic'), 'Yes')

query = Query(network.get_node_by_name('Driver Config - Graphics'), [evidence_variable_1, evidence_variable_2])

ve.query = query
ve.run()

"""
# Consulta aleatoria
query = Query.random(network, 3)

ve.query = query
ve.run()
"""