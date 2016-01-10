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

import os
import itertools
import xml.dom.minidom as minidom

import utils.utils as utils
from inference.RandomVariable import RandomVariable
from networks.BayesNet import BayesNet


def read(file_route):
    xmlbif = minidom.parse(file_route)
    return __generate_BayesNet(xmlbif)


def __generate_BayesNet(xmlbif):
    bif_tags = xmlbif.getElementsByTagName("BIF")
    if len(bif_tags) != 1:
        raise Exception("No se soportan ficheros con mas de una etiqueta <BIF>.")

    network_tags = bif_tags[0].getElementsByTagName("NETWORK")
    if len(network_tags) != 1:
        raise Exception("No se soportan ficheros con mas de una red bayesiana.")

    network_name = network_tags[0].getElementsByTagName("NAME")[0].childNodes[0].data
    bayes_net = BayesNet(network_name)

    variable_tags = network_tags[0].getElementsByTagName("VARIABLE")
    definition_tags = network_tags[0].getElementsByTagName("DEFINITION")

    __build_nodes(bayes_net, variable_tags)
    __build_edges(bayes_net, definition_tags)

    return bayes_net


def __build_nodes(bayes_net, variable_tags):

    for variable in variable_tags:

        if variable.attributes["TYPE"].value == "nature":

            node_name = variable.getElementsByTagName("NAME")[0].childNodes[0].data
            node_domain = [domain.childNodes[0].data for domain in variable.getElementsByTagName("OUTCOME")]
            node = RandomVariable(node_name, node_domain)
            bayes_net.add_node(node)

        else:
            raise Exception("Los nodos del grafo han de ser del tipo \"nature\".")


def __build_edges(bayes_net, definition_tags):

    for definition in definition_tags:

        for_tag = definition.getElementsByTagName("FOR")[0]

        child_node_name = for_tag.childNodes[0].data
        child_node = __get_node(bayes_net, child_node_name)

        for given_tag in definition.getElementsByTagName("GIVEN"):
            parent_node_name = given_tag.childNodes[0].data
            parent_node = __get_node(bayes_net, parent_node_name)

            if parent_node != None:
                bayes_net.add_edge((parent_node, child_node))

        # Establecer tabla de probabilidad
        raw_cpt = definition.getElementsByTagName("TABLE")[0].childNodes[0].data
        __set_cpt(child_node, bayes_net.graph.incidents(child_node), raw_cpt)


def __get_node(bayes_net, node_name):

    node = bayes_net.get_node_by_name(node_name)

    if node == None:
        raise Exception("La V.A. (" + node_name + ") aparece en una tabla de probabilidad pero no se encuentra definida como nodo.")

    return node


def __set_cpt(node, parent_nodes, raw_cpt):
    splitted_cpt = raw_cpt.split()
    nodes = []
    if parent_nodes:
        nodes = [n for n in parent_nodes]
    nodes.append(node)

    domains = [n.domain for n in nodes]
    cpt = {}
    index = 0
    for k in itertools.product(*domains):
        key = utils.proper_key(k)
        cpt[key] = float(splitted_cpt[index])
        index += 1

    node.cpt = cpt


def load_preset_network(network_name):
    networks_files = {'fire_alarm': 'basicfirealarm.xml', 'simple_diagnosis': 'influenzasmokes.xml', 'electrical_diagnosis': 'electricaldiagnosis.xml', 'win95pts': 'win95pts.xml'}
    return read(os.getcwd() + '\\xml\\' + networks_files[network_name])
