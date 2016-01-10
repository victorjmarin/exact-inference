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

