# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
"""
This module groups functions directly related to the creation and the management
of the graph based on a Cadbiom model.

Here we find high-level functions to create a Networkx graph, and convert it
to JSON or GraphML formats.
"""
# Standard imports
import itertools as it
import datetime as dt
import networkx as nx

# Library imports
from cadbiom_cmd.tools.models import parse_condition

import cadbiom.commons as cm

LOGGER = cm.logger()


def build_graph(solution, steps, transitions):
    """Build a graph for the given solution.

        - Get & make all needed edges
        - Build graph

    .. note:: Legend:

        - Default nodes: grey
        - Frontier places: red
        - Transition nodes: blue
        - Inhibitors nodes: white
        - Default transition: grey
        - Inhibition edge: red
        - Activation edge: green

    :param arg1: Frontier places.
    :param arg2: List of steps (with events in each step).
    :param arg3: A dictionnary of events as keys, and transitions as values
        (see get_transitions()).
    :type arg1: <str>
    :type arg2: <list <list>>
    :type arg3: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    :return:
        - Networkx graph object.
        - Nodes corresponding to transitions with conditions.
        - All nodes in the model
        - Edges between transition node and nodes in condition
        - Normal transitions without condition
    :rtype: <networkx.classes.digraph.DiGraph>, <list>, <list>, <list>, <list>
    """

    def filter_transitions(step_event):
        """ Insert a transittion in a transition event if there is a condition.

        => Insert a node in a edge.
        => Link all nodes involved in the condition with this new node.

        :param: A list of events (transitions) (from a step in a solution).
            [('Ax', 'n1', {u'label': u'h00[]'}),]
        :type: <tuple>
        :return: Fill lists of edges:
            edges_with_cond: link to a transition node for
                transition with condition.
            transition_nodes: add new nodes corresponding to transitions with
                conditions.
            edges_in_cond: Add all edges to nodes linked to a transition
                via the condition (group of nodes involved in the path
                choosen by the solver).
            edges: transition untouched if there is no condition.
        :rtype: None
        """
        assert step_event # Todo: useful ?

        # Inactivated nodes in paths of conditions
        # This variable is set in place by parse_condition() for the current context
        inhibitors_nodes = set()

        input_places = {ori for ori, _, _ in step_event}

        # Color nodes
        # Since we explore all possible paths for each condition,
        # some edges are rewrited multiple times.
        # => included edges between origin <=> transition node
        # These edges must be grey while, edges between a node that is
        # only in a condition and a transition node must be green.
        # => notion of activator vs inhibitor vs normal input/output node
        def color_map(node):
            """Return a color used for edges, related to the role of the node"""
            # print("color for:", node)
            if node in inhibitors_nodes: # Test first (see cond below)
                return 'red'
            if node in input_places: # some/all frontier places are in this set
                return 'grey'

            return 'green'


        for trans in step_event:
            attributes = trans[2]
            ori = trans[0]
            ext = trans[1]
            event = attributes['label'].split('[')[0]

            # If there is a condition formula associated to this clock
            if attributes['condition'] != '':

                # Add the transition as node
                # PS: There may be a rewrite of an identical node here,
                # networkx will do the merge later, but the conditions
                # will not be preserved. Only the last condition is kept.
                transition_nodes.append(
                    (
                        event,
                        {
                            'name': attributes['label'], # Trick for Cytoscape
                            'color': 'blue',
                            'condition': attributes['condition'], # Partial cond (cf above)
                        }
                    )
                )

                # Origin => transition node
                edges_with_cond.append(
                    (
                        ori, event,
                        {
                            'label': ori + '-' + event,
                        }
                    )
                )

                # Transition node => ext
                edges_with_cond.append(
                    (
                        event, ext,
                        {
                            'label': event + '-' + ext,
                        }
                    )
                )

                # Add all transitions to nodes linked via the condition
                valid_paths = parse_condition(
                    attributes['condition'],
                    all_nodes,
                    inhibitors_nodes # Set in place by parse_condition
                )
                for i, path in enumerate(valid_paths):
                    for node in path:
                        edges_in_cond.append(
                            (
                                node, event,
                                {
                                    'label': '{} ({})'.format(
                                        event,
                                        i
                                    ),
                                    #'label': '{} [{}] ({})'.format(
                                    #    event,
                                    #    ', '.join(path),
                                    #    i
                                    #), #node + '-' + event,
                                    'color': color_map(node), # Set edge color
                                }
                            )
                        )
            else:
                # Normal edges
                edges.append(trans)


    # Get & make all needed edges ##############################################
    LOGGER.debug("Build graph for the solution: %s", solution)
    LOGGER.debug("Decompiled steps: ", steps)
#
#    print(transitions['_h_2755'])
#    print(transitions['_h_4716'])
#    print(transitions['_h_2206'])
#    print(transitions['_h_3426'])
#    exit()

    frontier_places  = solution.split(' ')
    edges_with_cond  = list() # Edges between ori <-> transition node <-> ext
    edges_in_cond    = list() # Edges between transition node and nodes in condition
    transition_nodes = list() # Nodes inserted because of condition in transition
    edges            = list() # Normal transitions without condition

    # Get all nodes in all transitions (origin & ext)
    try:
        all_transitions = \
            (transitions[step_event] for step_event in it.chain(*steps))
        transitions_ori_ext = \
            (tuple((ori, ext)) for ori, ext, _ in it.chain(*all_transitions))
    except KeyError:
        print("/!\One event is not in the given model file... Please check it.")
        raise
    # All nodes are: nodes involved in transitions + frontier places
    all_nodes = set(it.chain(*transitions_ori_ext)) | set(frontier_places)

    # Parse all conditions in transitions;
    # add nodes in conditions and transition nodes
    [filter_transitions(transitions[step_event])
     for step_event in it.chain(*steps)]

#    print("edges without cond", edges)
#    print("edges with cond", edges_with_cond)
#    print("transition nodes added", transition_nodes)
#    raw_input("PAUSE")

    # Make Graph ###############################################################
    G = nx.DiGraph()
    # Add all nodes (some frontier places are in this set)
    G.add_nodes_from(all_nodes, color='grey')
    # Add fontier places
    # We rewrite the color of these special nodes here.
    G.add_nodes_from(frontier_places, color='red')
    # Add all transition nodes
    G.add_nodes_from(transition_nodes, color='blue')

    # Node attribute ?
    # print(G.node['h1'])

    # Add all edges
    G.add_edges_from(edges)
    G.add_edges_from(edges_with_cond)
    G.add_edges_from(edges_in_cond)

    return G, transition_nodes, all_nodes, edges_in_cond, edges


def get_json_graph(G):
    """Translate Networkx graph into a dictionary ready to be dumped in a JSON file.

    .. note:: In classical JSON graph, ids of nodes are their names;
        also, their position in the array of nodes gives their numerical id,
        which is used as source or target in edges definitions.
        Here, for readability and debugging purpose, we use distinct attributes
        id and label for nodes.

    :param graph: Networkx graph.
    :type graph: <networkx.classes.digraph.DiGraph>
    :return: Serialized graph ready to be dumped in a JSON file.
    :rtype: <dict>
    """

    # Debug
    # Color attribute of the nodes
    # print(nx.get_node_attributes(G, 'color'))
    # Color attribute of the edges
    # print(nx.get_edge_attributes(G, 'color'))
    # Labels of edges
    # print(nx.get_edge_attributes(G, 'label'))
    # Conditions of edges
    ## Only edges without conditions here ?
    # print(nx.get_edge_attributes(G, 'condition'))

    json_data = dict()
    id_generator = it.count()
    nodes = list()
    edges = list()
    nodes_mapping = dict()
    # Build nodes
    for node_name, color in nx.get_node_attributes(G, 'color').items():
        node_id = next(id_generator)
        node = {
            'id': node_id,
            'label': node_name,
            'color': color,
        }
        nodes.append(node)
        nodes_mapping[node_name] = node_id

    #for edge, color in nx.get_edge_attributes(G, 'color').items():
    for ori, ext in G.edges_iter():
        # Update edge attributes
        edge = dict(G.get_edge_data(ori, ext))
        edge['source'] = nodes_mapping[ori] # get id of ori
        edge['target'] = nodes_mapping[ext] # get id of ext
        edges.append(edge)
        #{'label': G[ori][ext]['label'], 'color': G[ori][ext]['color']}
        #{'color': 'grey', 'source': 12838, 'target': 11741, 'label': '_h_1831 (0)'}

    json_data['nodes'] = nodes
    json_data['edges'] = edges

    return json_data


def export_graph(output_dir, solution, solution_index, G, *args):
    """Export a networkx graph to GraphML format.

    .. note:: Legend: See :meth:`~cadbiom_cmd.tools.graphs.build_graph`.

    :param output_dir: Output directory for GraphML files.
    :param solution: Solution string (mostly a set of frontier places).
    :param solution_index: Index of the solution in the Cadbiom result file
        (used to distinguish exported filenames).
    :param G: Networkx graph object.
    :type output_dir: <str>
    :type solution: <str>
    :type solution_index: <int> or <str>
    :type G: <networkx.classes.digraph.DiGraph>
    """

    creation_date = dt.datetime.now().strftime("%H-%M-%S")
    filename = "{}{}_{}_{}".format(
        output_dir, creation_date, solution_index, solution[:75]
    )

    # Save
    # PS: inhibitors will still have not the attribute 'color' = 'white'
    nx.write_graphml(G, filename + ".graphml")
