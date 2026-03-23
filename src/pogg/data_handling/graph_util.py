"""
The `graph_util` module contains the `POGGGraphUtil` class that builds NetworkX graphs, enables selecting subgraphs, and
prints graphs to various filetypes (`.dot`, `.png`, and `.svg`)

[See usage examples here.](project:/usage_nbs/pogg/data_handling/graph_util_usage.ipynb)
"""
import json

import networkx as nx

class POGGGraphUtil:
    """Provides static functions for building and writing graphs to files."""
    @staticmethod
    def build_graph(graph_json):
        """
        Build a NetworkX graph from a JSON object containing the graph data.

        See the [Converting graphs to JSON format]() page for more details on the specific format this function requires.

        ````{example} Input data shape example
        :collapsible:

        ```
        {
            "nodes": {
                "idCar1": {
                    "lexicon_key": "idCar",
                    "node_properties": {
                        "node_type": "entity",
                        "root": "root"
                    }
                },
                "red": {
                    "node_properties": {
                        "node_type": "property"
                    }
                }
            },
            "edges": [
                {
                    "edge_name": "idColor",
                    "parent_node": "idCar1",
                    "child_node": "red",
                    "lexicon_key": "idColor",
                    "edge_properties": {
                        "edge_type": "property"
                    }
                }
            ]
        }
        ```
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_json` | `JSON` | JSON object containing the graph data |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | NetworkX `DiGraph` | directed graph of the data from the JSON object |
        """
        # create the graph
        graph = nx.DiGraph()

        # add nodes
        for node in graph_json['nodes'].keys():
            # dictionary of properties pulled from json to be added as actual node properties in the networkx graph
            if 'node_properties' in graph_json['nodes'][node]:
                node_properties = graph_json['nodes'][node]['node_properties']
            else:
                node_properties = {}

            # get lexicon_key and add it to node_properties dict
            if 'lexicon_key' in graph_json['nodes'][node]:
                node_properties['lexicon_key'] = graph_json['nodes'][node]['lexicon_key']
            else:
                # if lexicon_key isn't set, just use the node name
                node_properties['lexicon_key'] = node

            graph.add_node(node, **node_properties)

        # add edges
        for edge in graph_json['edges']:
            parent_node = edge['parent_node']
            child_node = edge['child_node']

            # check if parent_node and child_node are in nodes
            # if not, add them with default lexicon_key
            if parent_node not in graph.nodes:
                graph.add_node(parent_node, lexicon_key=parent_node)
            if child_node not in graph.nodes:
                graph.add_node(child_node, lexicon_key=child_node)

            # dictionary of properties pulled from json to be added as actual edge properties in the networkx graph
            if 'edge_properties' in edge:
                edge_properties = edge['edge_properties']
            else:
                edge_properties = {}

            if 'lexicon_key' in edge:
                edge_properties['lexicon_key'] = edge['lexicon_key']
            else:
                # if lexicon_key isn't set, just use the edge name
                edge_properties['lexicon_key'] = edge['edge_name']

            graph.add_edge(parent_node, child_node, label=edge['edge_name'], **edge_properties)

        return graph

    @staticmethod
    def find_root(graph):
        """
        Find the root of a given graph.

        1. First check for the "root" attribute.
        2. If no node has the "root" attribute, try doing a [topological sort](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html) and treat the first node as the root.
        3. If topological sort fails because the graph has cycles, find the node with no inward edges.


        If there are multiple node candidates at any stage of the search, the root can't be guessed.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `DiGraph` | Graph to find root for |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | NetworkX `N` | root of graph |
        """
        root_candidate = None

        # attempt to use 'root' attribute
        root_node_list = [node for node, attrs in graph.nodes(data=True)
                          if 'root' in attrs.keys() and attrs['root'] == 'root']
        if len(root_node_list) > 1:
            raise ValueError("More than one node in the graph is marked as the root")
        elif len(root_node_list) == 1:
            root_candidate = root_node_list[0]

        # ensure graph is weakly connected (i.e. when edge direction is ignored, there is a possible path between any two nodes)
        if root_candidate is None and not nx.is_weakly_connected(graph):
            raise ValueError("Graph is not weakly connected, can't determine root")

        # try topological sort (only works if there are no cycles)
        if root_candidate is None:
            try:
                root_node_list = list(nx.topological_sort(graph))

                # sometimes there seemed to be a random "newline" node
                # but now that only weakly connected graphs are accepted this check isn't necessary
                # if root_node_list[0] == "\\n":
                #     root_candidate = root_node_list[1]
                # else:

                root_candidate = root_node_list[0]
            except nx.NetworkXUnfeasible:
                pass

        if root_candidate is None:
            # try finding node with no in-degree=0
            root_node_list = [node for node, indegree in graph.in_degree() if indegree == 0]

            # now that only weakly connected graphs are accepted, this check isn't necessary
            # if len(root_node_list) > 1:
            #     raise ValueError("No node is marked as root and more than one node in the graph has no in-edges; cannot determine root")

            if len(root_node_list) == 1:
                root_candidate = root_node_list[0]
            else:
                # no candidate found
                pass

        # get root with its data
        for node in graph.nodes(data=True):
            # if first element in node info tuple (aka the name) matches the candidate, return the node
            if node[0] == root_candidate:
                return node

        # if we make it here, we didn't find a root
        return None

    @staticmethod
    def read_graph_from_dot(filepath):
        """
        Read a graph from a `.dot` file.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `filepath` | `str` | path to the `dot` file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | NetowrkX `DiGraph` | `DiGraph` object based on the information in the `dot` file |
        """
        return nx.nx_pydot.read_dot(filepath)

    @staticmethod
    def write_graph_to_dot(graph, filepath):
        """
        Write the graph to a `.dot` file.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `DiGraph` | graph to be written to file |
        | `filepath` | `str` | path to the output file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        nx.nx_pydot.write_dot(graph, filepath)

    @staticmethod
    def write_graph_to_png(graph, filepath):
        """
        Write the graph to a `.png` file.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `DiGraph` | graph to be written to file |
        | `filepath` | `str` | path to the output file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        png_graph = nx.drawing.nx_pydot.to_pydot(graph)
        png_graph.write_png(filepath)

    @staticmethod
    def write_graph_to_svg(graph, filepath):
        """
        Write the graph to an `.svg` file.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `DiGraph` | graph to be written to file |
        | `filepath` | `str` | path to the output file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        png_graph = nx.drawing.nx_pydot.to_pydot(graph)
        png_graph.write_svg(filepath)

    @staticmethod
    def write_graph_to_json(graph, filepath):
        """
        Write the graph to a `.json` file in the POGG format.

        ````{example} POGG format for graphs in JSON
        :collapsible:

        ```
        {
            "nodes": {
                "idCar1": {
                    "lexicon_key": "idCar",
                    "node_properties": {
                        "node_type": "entity",
                        "root": "root"
                    }
                },
                "red": {
                    "node_properties": {
                        "node_type": "property"
                    }
                }
            },
            "edges": [
                {
                    "edge_name": "idColor",
                    "parent_node": "idCar1",
                    "child_node": "red",
                    "lexicon_key": "idColor",
                    "edge_properties": {
                        "edge_type": "property"
                    }
                }
            ]
        }
        ```
        ````


        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `DiGraph` | graph to be written to file |
        | `filepath` | `str` | path to the output file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """

        graph_json = {
            "nodes": {},
            "edges": []
        }
        for node in graph.nodes(data=True):
            node_name = node[0]
            node_props = node[1]

            graph_json["nodes"][node_name] = {
                "lexicon_key": node_props["lexicon_key"],
            }
            del node_props["lexicon_key"]
            graph_json["nodes"][node_name]["node_properties"] = node_props

        for edge in graph.edges(data=True):
            parent = edge[0]
            child = edge[1]
            edge_props = edge[2]

            edge_dict = {
                "edge_name": edge_props["label"],
                "parent_node": parent,
                "child_node": child,
                "lexicon_key": edge_props["lexicon_key"]
            }
            del edge_props["label"]
            del edge_props["lexicon_key"]
            edge_dict["edge_properties"] = edge_props

            graph_json["edges"].append(edge_dict)

        with open(filepath, "w") as f:
            json.dump(graph_json, f, indent=4)