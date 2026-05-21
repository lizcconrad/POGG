"""
The evaluation module contains the `POGGNodeEvaluation`, `POGGEdgeEvaluation`, `POGGGraphEvaluation`, and `POGGEvaluation` classes
that each store evaluation information about the respective elements of a dataset that has been run through the data-to-text algorithm.

[See usage examples here.](project:/usage_nbs/pogg/evaluation/evaluation_usage.ipynb)
"""
import os
from pathlib import Path
import json
import networkx as nx
from pogg.my_delphin import sementcodecs
from pogg.data_handling import POGGGraphUtil

# data class ?
class POGGNodeEvaluation:
    """
    A `POGGNodeEvaluation` object stores evaluation information about a particular node in a graph.
    """
    def __init__(self, node_name, node_props):
        """
        Initialize the `POGGNodeEvaluation` object by providing the node's name and its properties.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `node_name` | `str` | name of the node in the graph | `"cake1"` |
        | `node_props` | `dict` of `str:str` | dictionary of node properties | `{"lexicon_key": "cake"}` |


        Once the object is created, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `node_name` | name of the node |
        | `node_props` | dictionary of node properties |
        | `generated_SEMENT` | `SEMENT` object generated for this node during graph-to-SEMENT conversion |
        | `generated_SEMENT_string` | string encoding of the `SEMENT` object generated for this node |
        | `node_covered` | boolean indicating whether the node was covered during conversion (i.e. generated a `SEMENT` object) |
        | `node_included` | boolean indicating whether the node was including in the final SEMENT during conversion |
        | `generation_comment` | comment describing reason for failing to generate a SEMENT if applicable |
        | `inclusion_comment` | comment describing reason for failing to include the generated SEMENT in the final result if applicable |
        """

        # node information
        self.node_name = node_name
        self.node_props = node_props

        # functions called during generation
        self.sem_alg_fxns_used = {}
        self.sem_comp_fxns_used = {}

        # associated SEMENT
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None

        # evaluation information
        # was there a SEMENT generated from this node?
        self.node_covered = None
        # was this node included in the final SEMENT?
        self.node_included = None
        # explanation in the event of failure to generate (i.e. not covered)
        self.generation_comment = None
        # explanation in the event of not being included in the final result
        self.inclusion_comment = None

    def set_SEMENT(self, sement):
        """
        Set the SEMENT properties (`generated_SEMENT` and `generated_SEMENT_string`) for the evaluation object.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | `SEMENT` object to associate with this node |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def get_dict_representation(self):
        return {
            'node_name': self.node_name,
            'node_props': self.node_props,

            'generated_SEMENT_string': self.generated_SEMENT_string,

            'sem_alg_fxns_used': dict(sorted(self.sem_alg_fxns_used.items())),
            'sem_comp_fxns_used': dict(sorted(self.sem_comp_fxns_used.items())),
            'node_covered': self.node_covered,

            'node_included': self.node_included,
            'generation_comment': self.generation_comment,
            'inclusion_comment': self.inclusion_comment
        }

    @classmethod
    def create_from_json(cls, node_json):
        node_eval = POGGNodeEvaluation(node_json["node_name"], node_json["node_props"])
        for key, val in node_json.items():
            if key != "node_name" and key != "node_props":
                setattr(node_eval, key, val)

        # set SEMENT object
        if node_eval.generated_SEMENT_string is not None:
            node_eval.set_SEMENT(sementcodecs.decode(node_eval.generated_SEMENT_string))

        return node_eval


class POGGEdgeEvaluation:
    """
    A `POGGEdgeEvaluation` object stores evaluation information about a particular edge in a graph.
    """
    def __init__(self, edge_name, edge_props, parent_name, child_name):
        """
        Initialize the `POGGEdgeEvaluation` object by providing the edge's name, its properties, its parent node name, and its child node name.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `edge_name` | `str` | name of the edge in the graph | `"flavor"` |
        | `edge_props` | `dict` of `str:str` | dictionary of edge properties | `{"lexicon_key": "flavor"}` |
        | `parent_name` | `str` | name of the parent node | `"cake1"` |
        | `child_name` | `str` | name of the child node | `"vanilla1"` |


        Once the object is created, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `edge_name` | name of the edge |
        | `edge_props` | dictionary of edge properties |
        | `parent_node_name` | name of the parent node |
        | `child_node_name` | name of the child node |
        | `generated_SEMENT` | `SEMENT` object generated for this edge during graph-to-SEMENT conversion |
        | `generated_SEMENT_string` | string encoding of the `SEMENT` object generated for this edge |
        | `edge_covered` | boolean indicating whether the edge was covered during conversion (i.e. generated a `SEMENT` object) |
        | `edge_included` | boolean indicating whether the edge was including in the final SEMENT during conversion |
        | `generation_comment` | comment describing reason for failing to generate a SEMENT if applicable |
        | `inclusion_comment` | comment describing reason for failing to include the generated SEMENT in the final result |
        """
        # edge information
        self.edge_name = edge_name
        self.edge_props = edge_props
        self.parent_node_name = parent_name
        self.child_node_name = child_name

        # associated SEMENT
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None

        # functions called during generation
        self.sem_alg_fxns_used = {}
        self.sem_comp_fxns_used = {}

        # evaluation information
        # was there a SEMENT generated from this node?
        self.edge_covered = None
        # was this node included in the final SEMENT?
        self.edge_included = None
        # explanation in the event of failure to generate (i.e. not covered)
        self.generation_comment = None
        # explanation in the event of not being included in the final result
        self.inclusion_comment = None

    def set_SEMENT(self, sement):
        """
        Set the SEMENT properties (`generated_SEMENT` and `generated_SEMENT_string`) for the evaluation object.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | `SEMENT` object to associate with this edge |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def get_dict_representation(self):
        return {
            'edge_name': self.edge_name,
            'edge_props': self.edge_props,
            'parent_node_name': self.parent_node_name,
            'child_node_name': self.child_node_name,

            'generated_SEMENT_string': self.generated_SEMENT_string,

            'sem_alg_fxns_used': dict(sorted(self.sem_alg_fxns_used.items())),
            'sem_comp_fxns_used': dict(sorted(self.sem_comp_fxns_used.items())),

            'edge_covered': self.edge_covered,
            'edge_included': self.edge_included,
            'generation_comment': self.generation_comment,
            'inclusion_comment': self.inclusion_comment,
        }

    @classmethod
    def create_from_json(cls, edge_json):
        edge_name = edge_json["edge_name"]
        edge_props = edge_json["edge_props"]
        parent_node_name = edge_json["parent_node_name"]
        child_node_name = edge_json["child_node_name"]
        edge_eval = POGGEdgeEvaluation(edge_name, edge_props, parent_node_name, child_node_name)

        for key, val in edge_json.items():
            if key != "edge_name" and key != "edge_props" and key != "parent_node_name" and key != "child_node_name":
                setattr(edge_eval, key, val)

        if edge_eval.generated_SEMENT_string is not None:
            edge_eval.set_SEMENT(sementcodecs.decode(edge_eval.generated_SEMENT_string))

        return edge_eval


class POGGGraphEvaluation:
    """
    A `POGGGraphEvaluation` object stores evaluation information about a graph.
    """
    def __init__(self, graph_name, graph_info):
        """
        Initialize the `POGGGraphEvaluation` object by providing the graph and its name.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `graph` | NetworkX `digraph` | graph object | |
        | `graph_name` | `str` | name of the graph | `vanilla_cake` |


        Once the object is created, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `graph` | graph associated with the evaluation object |
        | `graph_name` | name of the graph |
        | `node_evaluations` | `dict` of `POGGNodeEvaluation` objects for each node in the graph |
        | `edge_evaluations` | `dict` of `POGGEdgeEvaluation` objects for each edge in the graph |
        | `node_count` | number of nodes in the graph |
        | `nodes_covered` | number of nodes that generated a `SEMENT` object |
        | `nodes_included` | number of nodes whose generated SEMENT information was included in the final SEMENT for the graph |
        | `node_coverage` | percentage of nodes covered |
        | `node_inclusion` | percentage of nodes included |
        | `edge_count` | number of edges in the graph |
        | `edges_covered` | number of edges that generated a `SEMENT` object |
        | `edges_included` | number of edges whose generated SEMENT information was included in the final SEMENT for the graph |
        | `edge_coverage` | percentage of edges covered |
        | `edge_inclusion` | percentage of edges included |
        | `generation_comment` | comment explaining why generation failed at the root if it did |
        | `generated_SEMENT` | `SEMENT` object generated for this graph during graph-to-SEMENT conversion |
        | `generated_SEMENT_string` | string encoding of the `SEMENT` object generated for this graph |
        | `collapsed_SEMENT` | `SEMENT` object generated for this graph with equalities collapsed into one representative variable |
        | `collapsed_SEMENT_string` | string encoding of the collapsed `SEMENT` object generated for this graph |
        | `prepped_SEMENT` | `SEMENT` object generated for this graph that has been prepared for generation |
        | `prepped_SEMENT_string` | string encoding of the prepped `SEMENT` object generated for this graph |
        | `generated_results` | list of text results generated from the `SEMENT` for this graph |
        """

        self.graph_name = graph_name
        self.graph = graph_info["graph"]
        self.graph_json = graph_info["graph_json"]
        self.gold_outputs = graph_info["gold_outputs"]

        # initialize self.node_evaluations (list of node evaluation objects)
        self.node_evaluations = {}
        self.create_node_evaluations()
        # initialize self.edge_evaluations (list of edge evaluation objects)
        self.edge_evaluations = []
        self.create_edge_evaluations()

        # calculations made over the graph
        self.node_count = None
        self.nodes_covered = None
        self.nodes_included = None
        self.node_coverage = None
        self.node_inclusion = None
        self.edge_count = None
        self.edges_covered = None
        self.edges_included = None
        self.edge_coverage = None
        self.edge_inclusion = None

        # functions called during generation
        self.sem_alg_fxns_used = {}
        self.sem_comp_fxns_used = {}

        # gold output information
        self.generated_gold_outputs = set()
        # no. of gold outputs generated / no. of gold outputs in list
        self.gold_output_generation_coverage = None

        # generated results
        self.generation_comment = None
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None
        self.collapsed_SEMENT = None
        self.collapsed_SEMENT_string = None
        self.prepped_SEMENT = None
        self.prepped_SEMENT_string = None
        self.generated_results = set()

    @classmethod
    def read_from_directory(cls, graph_evaluation_directory):
        # read in graph_json
        for item in os.listdir(graph_evaluation_directory):
            if item.endswith("_outputs.json"):
                with open(Path(graph_evaluation_directory, item), "r") as f:
                    outputs_json = json.load(f)
            elif item.endswith("_metrics.json"):
                with open(Path(graph_evaluation_directory, item), "r") as f:
                    metrics_json = json.load(f)
            elif item.endswith(".json"):
                with open(Path(graph_evaluation_directory, item), "r") as f:
                    graph_json = json.load(f)
            else:
                pass

        graph_name = metrics_json["graph_name"]
        graph_dict = {
            "graph_json": graph_json,
            "graph": POGGGraphUtil.build_graph(graph_json),
            "gold_outputs": set(outputs_json["gold_outputs"]),
        }
        eval_obj = POGGGraphEvaluation(graph_name, graph_dict)

        # set outputs attributes
        eval_obj.generated_gold_outputs = set(outputs_json["generated_gold_outputs"])
        eval_obj.generated_results = set(outputs_json["generated_results"])

        # set metrics attributes
        for key, val in metrics_json.items():
            if key == "nodes":
                eval_obj._create_node_evaluations_from_json(val)
            elif key == "edges":
                eval_obj._create_edge_evaluations_from_json(val)
            else:
                setattr(eval_obj, key, val)

        if eval_obj.generated_SEMENT_string is not None:
            eval_obj.set_SEMENT(sementcodecs.decode(eval_obj.generated_SEMENT_string))
        if eval_obj.collapsed_SEMENT_string is not None:
            eval_obj.set_collapsed_SEMENT(sementcodecs.decode(eval_obj.collapsed_SEMENT_string))
        if eval_obj.prepped_SEMENT_string is not None:
            eval_obj.set_prepped_SEMENT(sementcodecs.decode(eval_obj.prepped_SEMENT_string))

        # TODO: once that's done... make diffs
        # TODO: then reports ...
        # TODO: then remove semcomp from this repo
        # TODO: then FINALLY WebNLG.............

        return eval_obj


    def _create_node_evaluations_from_json(self, nodes_json):
        for key, val in nodes_json.items():
            node_eval = POGGNodeEvaluation.create_from_json(val)
            self.node_evaluations[key] = node_eval

    def _create_edge_evaluations_from_json(self, edges_json):
        # clear out edge_evaluations list
        # because this is a list and not a dict appending will create duplicates
        self.edge_evaluations = []
        for edge_json in edges_json:
            self.edge_evaluations.append(POGGEdgeEvaluation.create_from_json(edge_json))


    def create_node_evaluations(self):
        """
        Create `POGGNodeEvaluation` objects for each node in the graph.
        Store them in the `node_evaluations` instance attribute dictionary.

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        if self.graph is not None:
            for node in self.graph.nodes(data=True):
                node_name = node[0]
                node_props = node[1]
                self.node_evaluations[node_name] = POGGNodeEvaluation(node_name, node_props)

    def create_edge_evaluations(self):
        """
        Create `POGGEdgeEvaluation` objects for each edge in the graph.
        Store them in the `edge_evaluations` instance attribute dictionary.

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        if self.graph is not None:
            for edge in self.graph.edges(data=True):
                parent = edge[0]
                child = edge[1]
                edge_name = edge[2]['label']
                props = edge[2]
                self.edge_evaluations.append(POGGEdgeEvaluation(edge_name, props, parent, child))

    def set_SEMENT(self, sement):
        """
        Set the SEMENT properties (`generated_SEMENT` and `generated_SEMENT_string`) for the evaluation object.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | `SEMENT` object to associate with this graph |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def set_collapsed_SEMENT(self, sement):
        """
        Set the collapsed SEMENT properties (`collapsed_SEMENT` and `collapsed_SEMENT_string`) for the evaluation object.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | collapsed `SEMENT` object to associate with this graph |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.collapsed_SEMENT = sement
        if self.collapsed_SEMENT is not None:
            self.collapsed_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def set_prepped_SEMENT(self, sement):
        """
        Set the prepped SEMENT properties (`prepped_SEMENT` and `prepped_SEMENT_string`) for the evaluation object.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | `SEMENT` object that has been prepared for generation to associate with this graph |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.prepped_SEMENT = sement
        if self.prepped_SEMENT is not None:
            self.prepped_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def get_node_evaluation(self, node_name):
        """
        Get the `POGGNodeEvaluation` object for a node given its name.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `node_name` | `str` | name of the node to get the evaluation object for |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGNodeEvaluation` | evaluation object associated with the given node name |
        """
        try:
            return self.node_evaluations[node_name]
        except KeyError:
            raise KeyError("{} not a node in graph".format(node_name))

    def get_edge_evaluation(self, parent_name, child_name, edge_data):
        """
        Get the `POGGEdgeEvaluation` object for an edge given the parent name, child name, and edge data.

         **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `parent_name` | `str` | name of the parent node associated with the edge to get the evaluation object for | `"cake"` |
        | `child_name` | `str` | name of the child node associated with the edge to get the evaluation object for | `"vanilla"` |
        | `edge_data` | `str` | edge data associated with the edge to get the evaluation object for | `{'label': 'flavor'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGEdgeEvaluation` | evaluation object associated with the given edge information |
        """
        edge_name = edge_data['label']
        for edge_eval in self.edge_evaluations:
            if edge_name == edge_eval.edge_name and parent_name == edge_eval.parent_node_name and child_name == edge_eval.child_node_name:
                return edge_eval
        raise KeyError("{} with parent {} and child {} not an edge in graph".format(edge_name, parent_name, child_name))

    def determine_inclusion(self, root, ancestor_inclusion):
        """
        Recursively determine the inclusion of each element in the graph in the final generated SEMENT.

        Once all nodes and edges are marked for coverage, inclusion must be marked on every node and edge.
        This is done *after* all nodes and edges are marked for coverage because inclusion is impacted by the coverage of related elements in the graph.
        For example, if there's a graph with two nodes that each generated a SEMENT but are linked by an edge that did not get covered,
        the child node will need to be marked as `False` for inclusion as a result of the connecting edge not being covered.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `root` | `str` | root of the (sub)graph to traverse and determine inclusion for each element |
        | `ancestor_inclusion` | `boolean` | whether the direct ancestor has been included |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """

        # check if the graph has cycles, if it does just return
        try:
            nx.find_cycle(self.graph)
            return
        except nx.exception.NetworkXNoCycle:
            pass

        if root is None:
            # returns it as a tuple so get the first element which is just the name
            try:
                root = POGGGraphUtil.find_root(self.graph)[0]
            # if we get here then the graph has no distinct root (which is already stored in the generation comment) so just return
            except ValueError:
                return

        root_eval = self.get_node_evaluation(root)

        # comment should reflect the first point of failure
        # that is, if the node is not covered, use that as the comment
        # but if it is covered, and it's a successor of a failed element, use that
        if root_eval.node_covered:
            # None case for first call of function
            if ancestor_inclusion or ancestor_inclusion is None:
                ancestor_inclusion = True
                root_eval.node_included = True
            else:
                ancestor_inclusion = False
                root_eval.node_included = False
                root_eval.inclusion_comment = "Successor of failed element"
        else:
            ancestor_inclusion = False
            root_eval.node_included = False
            root_eval.inclusion_comment = "No SEMENT generated for this node"

        for child in self.graph.successors(root):
            # determine if edge is included
            edge_data = self.graph.get_edge_data(root, child)
            edge_eval = self.get_edge_evaluation(root, child, edge_data)

            # comment should reflect the first point of failure
            # that is, if the node is not covered, use that as the comment
            # but if it is covered, and it's a successor of a failed element, use that
            if edge_eval.edge_covered:
                if ancestor_inclusion:
                    # descendants of this child may be included
                    descendant_inclusion = True
                    edge_eval.edge_included = True
                else:
                    # descendants of this child will not be included
                    descendant_inclusion = False
                    edge_eval.edge_included = False
                    edge_eval.inclusion_comment = "Successor of failed element"
            else:
                # descendants of this child will not be included
                descendant_inclusion = False
                edge_eval.edge_included = False
                edge_eval.inclusion_comment = "No SEMENT generated for this edge"


            # recurse down to child
            self.determine_inclusion(child, descendant_inclusion)

    def calculate_metrics(self):
        """
        Calculate the evaluation metrics (node coverage, node inclusion, edge coverage, edge inclusion) for the graph.

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        # !!! NOTE: all lines with division are written as: "y and x / y"
        # if y is 0, then x/y throws a ZeroDivisionError
        # per https://docs.python.org/3.10/reference/expressions.html#boolean-operations,
        # "Note that neither and nor or restrict the value and type they return to False and True, but rather return the last evaluated argument."
        # so if y is 0, then x/y will not evaluate and 'and' will return the last evaluated argument, i.e. just 'y'
        # basically a shorter way to catch all possible ZeroDivisionErrors

        # determine inclusion
        self.determine_inclusion(None, None)

        self.node_count = len(self.graph.nodes())
        self.edge_count = len(self.graph.edges())

        self.nodes_covered = 0
        self.nodes_included = 0
        for node in self.node_evaluations.keys():
            node_eval = self.node_evaluations[node]

            # add the functions used to the set for the whole graph
            self.sem_alg_fxns_used = {
                k: self.sem_alg_fxns_used.get(k, 0) + node_eval.sem_alg_fxns_used.get(k, 0)
                for k in self.sem_alg_fxns_used.keys() | node_eval.sem_alg_fxns_used.keys()}

            self.sem_comp_fxns_used = {
                k: self.sem_comp_fxns_used.get(k, 0) + node_eval.sem_comp_fxns_used.get(k, 0)
                for k in self.sem_comp_fxns_used.keys() | node_eval.sem_comp_fxns_used.keys()}

            # compute coverage / inclusion
            if node_eval.node_covered:
                self.nodes_covered += 1
            if node_eval.node_included:
                self.nodes_included += 1
        self.node_coverage = self.node_count and self.nodes_covered / self.node_count
        self.node_inclusion = self.node_count and self.nodes_included / self.node_count

        self.edges_covered = 0
        self.edges_included = 0
        for edge_eval in self.edge_evaluations:
            # add the functions used to the set for the whole graph
            self.sem_alg_fxns_used = {
                k: self.sem_alg_fxns_used.get(k, 0) + edge_eval.sem_alg_fxns_used.get(k, 0)
                for k in self.sem_alg_fxns_used.keys() | edge_eval.sem_alg_fxns_used.keys()}

            self.sem_comp_fxns_used = {
                k: self.sem_comp_fxns_used.get(k, 0) + edge_eval.sem_comp_fxns_used.get(k, 0)
                for k in self.sem_comp_fxns_used.keys() | edge_eval.sem_comp_fxns_used.keys()}

            # compute coverage / inclusion
            if edge_eval.edge_covered:
                self.edges_covered += 1
            if edge_eval.edge_included:
                self.edges_included += 1

        # it's possible for there to be no edges
        self.edge_coverage = self.edge_count and self.edges_covered / self.edge_count
        self.edge_inclusion = self.edge_count and self.edges_included / self.edge_count


        # gold outputs metrics
        lowercase_results = [result.lower() for result in sorted(list(self.generated_results))]
        # results = [result for result in sorted(list(self.generated_results))]
        for gold_output in self.gold_outputs:
            if gold_output.lower() in lowercase_results:
            # if gold_output in results:
                self.generated_gold_outputs.add(gold_output)

        self.gold_output_generation_coverage = len(self.gold_outputs) and len(self.generated_gold_outputs) / len(self.gold_outputs)

    def mark_all_uncovered(self):
        """
        Mark all nodes and edges as uncovered.

        This might be necessary when some error (e.g. unable to find the root) occurs during conversion so no element of the graph generates a SEMENT.

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        for node_key in self.node_evaluations.keys():
            self.node_evaluations[node_key].node_covered = False
            self.node_evaluations[node_key].node_included = False
        for edge in self.edge_evaluations:
            edge.edge_covered = False
            edge.edge_included = False

    def get_POGG_metrics_dict(self):
        return {
            'graph_name': self.graph_name,

            'sem_alg_fxns_used': dict(sorted(self.sem_alg_fxns_used.items())),
            'sem_comp_fxns_used': dict(sorted(self.sem_comp_fxns_used.items())),

            'node_count': self.node_count,
            'nodes_covered': self.nodes_covered,
            'nodes_included': self.nodes_included,

            'edge_count': self.edge_count,
            'edges_covered': self.edges_covered,
            'edges_included': self.edges_included,

            'generation_comment': self.generation_comment,
            'generated_SEMENT_string': self.generated_SEMENT_string,
            'collapsed_SEMENT_string': self.collapsed_SEMENT_string,
            'prepped_SEMENT_string': self.prepped_SEMENT_string,

            'nodes': {key: val.get_dict_representation() for key, val in self.node_evaluations.items()},
            'edges': [edge.get_dict_representation() for edge in self.edge_evaluations],
        }

    def get_text_outputs_dict(self):
        return {
            'gold_outputs': sorted(list(self.gold_outputs)),
            'generated_gold_outputs': sorted(list(self.generated_gold_outputs)),
            'generated_results': sorted(list(self.generated_results))
        }


    def create_evaluation_object_from_directory(self, evaluation_directory):
        # find the dot file
        for item in os.listdir(evaluation_directory):
            if item.endswith(".dot"):
                self.graph = POGGGraphUtil.read_graph_from_dot(Path(evaluation_directory, item))
            elif item.endswith(".json"):
                if item.endswith("evaluation.json"):
                    with open(Path(evaluation_directory, item)) as json_file:
                        graph_evaluation_json = json.load(json_file)
                # else:
                #     with open(Path(evaluation_directory, item)) as json_file:
                #         graph = json.load(json_file)

        self.graph_name = graph_evaluation_json['graph_name']

        self.generated_SEMENT_string = graph_evaluation_json['generated_SEMENT_string']
        if self.generated_SEMENT_string is not None:
            self.generated_SEMENT = sementcodecs.decode(self.generated_SEMENT_string)

        self.collapsed_SEMENT_string = graph_evaluation_json['collapsed_SEMENT_string']
        if self.collapsed_SEMENT_string is not None:
            self.collapsed_SEMENT = sementcodecs.decode(self.collapsed_SEMENT_string)

        self.prepped_SEMENT_string = graph_evaluation_json['prepped_SEMENT_string']
        if self.prepped_SEMENT_string is not None:
            self.prepped_SEMENT = sementcodecs.decode(self.prepped_SEMENT_string)

        self.generation_comment = graph_evaluation_json['generation_comment']

        self.gold_outputs = graph_evaluation_json['gold_outputs']
        self.generated_gold_outputs = graph_evaluation_json['generated_gold_outputs']
        self.gold_output_generation_coverage = graph_evaluation_json['gold_output_generation_coverage']

        self.generated_results = graph_evaluation_json['generated_results']
        self.sem_comp_fxns_used = graph_evaluation_json['sem_comp_fxns_used']
        self.sem_alg_fxns_used = graph_evaluation_json['sem_alg_fxns_used']

        self.node_count = graph_evaluation_json['node_count']
        self.nodes_covered = graph_evaluation_json['nodes_covered']
        self.nodes_included = graph_evaluation_json['nodes_included']
        self.node_coverage = graph_evaluation_json['node_coverage']
        self.node_inclusion = graph_evaluation_json['node_inclusion']
        self.edge_count = graph_evaluation_json['edge_count']
        self.edges_covered = graph_evaluation_json['edges_covered']
        self.edges_included = graph_evaluation_json['edges_included']
        self.edge_coverage = graph_evaluation_json['edge_coverage']
        self.edge_inclusion = graph_evaluation_json['edge_inclusion']

        # make node evaluations
        self.node_evaluations = {}
        for item in os.listdir(Path(evaluation_directory, "nodes")):
            node_eval = POGGNodeEvaluation(None, None, Path(evaluation_directory, "nodes", item))
            self.node_evaluations[node_eval.node_name] = node_eval
        # make edge evaluations
        self.edge_evaluations = []
        for item in os.listdir(Path(evaluation_directory, "edges")):
            self.edge_evaluations.append(POGGEdgeEvaluation(None, None, None, None, Path(evaluation_directory, "edges", item)))


class POGGEvaluation:
    """
    A `POGGEvaluation` object stores evaluation information about dataset.
    """
    def __init__(self, experiment_name):
        """
        Initialize the `POGGEvaluation` object by providing the name of the dataset.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `dataset_name` | `str` | graph object | `dataset_example` |

        Once the object is created, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `dataset_name` | name of the dataset |
        | `graph_evaluations` | dictionary of graph evaluation objects for each graph in the dataset |
        | `graph_count` | number of graphs |
        | `graph_SEMENT_count` | number of graphs that generated a SEMENT |
        | `graph_SEMENT_coverage` | percentage of graphs that generated a SEMENT |
        | `graphs_with_text_count` | number of graphs that generated text from their SEMENT |
        | `graphs_with_text_coverage` | percentage of graphs that generated text from their SEMENT |
        | `full_node_count` | total number of nodes across all graphs in the dataset |
        | `full_nodes_covered` | total number of nodes that generated a SEMENT across all graphs in the dataset |
        | `full_nodes_included` | total number of nodes included in all final graph SEMENTs in the dataset |
        | `full_node_coverage` | percentage of nodes that generated a SEMENT across all graphs in the dataset  |
        | `full_nodes_inclusion` | percentage of nodes included in all final graph SEMENTs in the dataset |
        | `full_edge_count` | total number of edges across all graphs in the dataset |
        | `full_edges_covered` | total number of edges that generated a SEMENT across all graphs in the dataset |
        | `full_edges_included` | total number of edges included in all final graph SEMENTs in the dataset |
        | `full_edge_coverage` | percentage of edges that generated a SEMENT across all graphs in the dataset  |
        | `full_edges_inclusion` | percentage of edges included in all final graph SEMENTs in the dataset |
        | `run_id` | ID for the run, used to distinguish runs from each other for comparative analysis |
        """

        self.experiment_name = experiment_name
        self.graph_evaluations = {}

        self.dataset_location = None
        self.lexicon = None

        # calculations made over all graphs
        self.graph_count = None
        self.graph_SEMENT_count = None
        self.graph_SEMENT_coverage = None

        # NOT number of results, but number that generated text
        self.graphs_with_text_count = None
        self.graphs_with_text_coverage = None
        self.graphs_with_gold_text_count = None
        self.graphs_with_complete_gold_text_count = None

        self.graphs_with_gold_text_coverage = None
        self.graphs_with_complete_gold_text_coverage = None

        self.full_node_count = None
        self.full_nodes_covered = None
        self.full_nodes_included = None
        self.full_node_coverage = None
        self.full_node_inclusion = None
        self.full_edge_count = None
        self.full_edges_covered = None
        self.full_edges_included = None
        self.full_edge_coverage = None
        self.full_edge_inclusion = None

        self.sem_alg_fxns_available = set(),
        self.sem_comp_fxns_available = set(),

        self.sem_alg_fxns_used = {}
        self.sem_alg_fxns_used_coverage = None

        self.sem_comp_fxns_used = {}
        self.sem_comp_fxns_used_coverage = None

        # metadata about the run itself for reporting/comparing evaluations between runs
        self.run_id = None

    @classmethod
    def read_from_directory(cls, evaluation_directory):
        # read eval_metadata.json file
        try:
            with open(Path(evaluation_directory, "run_metadata.json"), 'r') as metadata_file:
                metadata = json.load(metadata_file)
                eval_obj = POGGEvaluation(metadata["experiment_name"])

                for key, val in metadata.items():
                    setattr(eval_obj, key, val)
        except FileNotFoundError as e:
            raise e

        # read dataset_eval.json file
        try:
            with open(Path(evaluation_directory, "dataset_metrics.json"), 'r') as dataset_eval_file:
                dataset_eval = json.load(dataset_eval_file)

                for key, val in dataset_eval.items():
                    setattr(eval_obj, key, val)
        except FileNotFoundError as e:
            raise e

        eval_obj.graph_evaluations = {}

        graph_dir = Path(evaluation_directory, "graphs")
        for item in os.listdir(graph_dir):
            eval_obj.graph_evaluations[item] = POGGGraphEvaluation.read_from_directory(Path(graph_dir, item))

        return eval_obj


    def add_graph(self, graph_name, graph_info):
        """
        Create a graph evaluation object given a graph and add it to the dictionary of graph evaluation objects.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph` | NetworkX `digraph` | graph to add an evaluation object for |
        | `graph_name` | `str` | name of the graph |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """

        # create graph evaluation object
        if isinstance(graph_info, POGGGraphEvaluation):
            self.graph_evaluations[graph_name] = graph_info
        else:
            self.graph_evaluations[graph_name] = POGGGraphEvaluation(graph_name, graph_info)

    def get_graph_evaluation(self, graph_name):
        """
        Get the `POGGGraphEvaluation` object for a graph given its name.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_name` | `str` | name of the graph to get the evaluation object for |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGGraphEvaluation` | evaluation object associated with the given graph name |
        """
        try:
            return self.graph_evaluations[graph_name]
        except KeyError:
            raise KeyError("No evaluation object for a graph named '{}'".format(graph_name))

    def calculate_metrics(self):
        """
        Calculate the evaluation metrics (node coverage over all graphs, node inclusion over all graphs,
        edge coverage over all graphs, edge inclusion over all graphs) for the graph.

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """
        self.graph_count = len(self.graph_evaluations)

        self.graph_SEMENT_count = 0
        self.graphs_with_text_count = 0
        self.graphs_with_gold_text_count = 0
        self.graphs_with_complete_gold_text_count = 0
        self.full_node_count = 0
        self.full_nodes_covered = 0
        self.full_nodes_included = 0
        self.full_edge_count = 0
        self.full_edges_covered = 0
        self.full_edges_included = 0

        self.sem_alg_fxns_used_coverage = 0
        self.sem_comp_fxns_used_coverage = 0

        for graph_name in self.graph_evaluations.keys():
            graph_eval = self.graph_evaluations[graph_name]

            self.sem_alg_fxns_used = {
                k: self.sem_alg_fxns_used.get(k, 0) + graph_eval.sem_alg_fxns_used.get(k, 0)
                for k in self.sem_alg_fxns_used.keys() | graph_eval.sem_alg_fxns_used.keys()}

            self.sem_comp_fxns_used = {
                k: self.sem_comp_fxns_used.get(k, 0) + graph_eval.sem_comp_fxns_used.get(k, 0)
                for k in self.sem_comp_fxns_used.keys() | graph_eval.sem_comp_fxns_used.keys()}

            if graph_eval.generated_SEMENT is not None:
                self.graph_SEMENT_count += 1
            if len(graph_eval.generated_results) > 0:
                self.graphs_with_text_count += 1
            if len(graph_eval.generated_gold_outputs) > 0:
                self.graphs_with_gold_text_count += 1
            if graph_eval.gold_output_generation_coverage == 1:
                self.graphs_with_complete_gold_text_count += 1

            self.full_node_count += graph_eval.node_count
            self.full_nodes_covered += graph_eval.nodes_covered
            self.full_nodes_included += graph_eval.nodes_included
            self.full_edge_count += graph_eval.edge_count
            self.full_edges_covered += graph_eval.edges_covered
            self.full_edges_included += graph_eval.edges_included

        self.graph_SEMENT_coverage = self.graph_count and self.graph_SEMENT_count / self.graph_count
        self.graphs_with_text_coverage = self.graph_count and self.graphs_with_text_count / self.graph_count
        self.graphs_with_gold_text_coverage = self.graph_count and self.graphs_with_gold_text_count / self.graph_count
        self.graphs_with_complete_gold_text_coverage = self.graph_count and self.graphs_with_complete_gold_text_count / self.graph_count

        self.full_node_coverage = self.full_node_count and self.full_nodes_covered / self.full_node_count
        self.full_node_inclusion = self.full_node_count and self.full_nodes_included / self.full_node_count
        self.full_edge_coverage = self.full_edge_count and self.full_edges_covered / self.full_edge_count
        self.full_edge_inclusion = self.full_edge_count and self.full_edges_included / self.full_edge_count

        self.sem_alg_fxns_used_coverage = len([x for x in self.sem_alg_fxns_used if self.sem_alg_fxns_used[x] > 0]) / len(self.sem_alg_fxns_available)
        self.sem_comp_fxns_used_coverage = len([x for x in self.sem_comp_fxns_used if self.sem_comp_fxns_used[x] > 0]) / len(self.sem_comp_fxns_available)

    def get_POGG_metrics_dict(self):
        return {
            'graph_count': self.graph_count,
            'graph_SEMENT_count': self.graph_SEMENT_count,
            'graphs_with_text_count': self.graphs_with_text_count,
            'graphs_with_gold_text_count': self.graphs_with_gold_text_count,
            'graphs_with_complete_gold_text_count': self.graphs_with_complete_gold_text_count,

            'sem_alg_fxns_available': sorted(list(self.sem_alg_fxns_available)),
            'sem_comp_fxns_available': sorted(list(self.sem_comp_fxns_available)),

            'sem_alg_fxns_used': dict(sorted(self.sem_alg_fxns_used.items())),
            'sem_comp_fxns_used': dict(sorted(self.sem_comp_fxns_used.items())),

            'full_node_count': self.full_node_count,
            'full_nodes_covered': self.full_nodes_covered,
            'full_nodes_included': self.full_nodes_included,

            'full_edge_count': self.full_edge_count,
            'full_edges_covered': self.full_edges_covered,
            'full_edges_included': self.full_edges_included,
        }
