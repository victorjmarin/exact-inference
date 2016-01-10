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
