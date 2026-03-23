"""
The `graph_to_SEMENT` module contains the `POGGGraphConverter` class used to convert directed graphs into SEMENTs.

[See usage examples here.](project:/usage_nbs/pogg/graph_to_SEMENT/POGGGraphConverter_usage.ipynb)
"""

import copy
import inspect
import networkx as nx

import pogg.lexicon.lexicon_builder
from pogg.my_delphin.my_delphin import SEMENT
from pogg.data_handling.graph_util import POGGGraphUtil
from pogg.lexicon.lexicon_builder import POGGLexicon
from pogg.semantic_composition.semantic_composition import SemanticComposition

class POGGGraphConverter:
    """
    A `POGGGraphConverter` object has `SemanticComposition` and `POGGDataset` objects as instance attributes and
    has instance methods for converting graphs in the dataset to SEMENTs.
    """
    def __init__(self, semantic_composition, dataset):
        """
        Initialize the `POGGGraphConverter` object.

        Each parameter may also be accessed as an instance attribute.

        **Parameters / Instance Attributes**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `semantic_composition` | `SemanticComposition` | `SemanticComposition` object that has functions for creating and composing SEMENTs |
        """
        self.sem_comp = semantic_composition
        self.lexicon = dataset.lexicon

    def get_SEMENT(self, comp_fxn_name, given_parameters):
        """
        Get a SEMENT object by providing the composition function name and parameters for the function call.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `comp_fxn_name` | `str` | name of the composition function to call | `compound_noun` |
        | `given_parameters` | `dict` | dictionary of parameters and their values to be passed in for the function call | `{'head_noun_sement': noun1, 'non_head_noun_sement': noun2}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT produced by calling the composition function |
        """

        comp_fxn_obj = getattr(self.sem_comp, comp_fxn_name)

        # get parameters for the comp_fxn
        defined_parameter_keys = inspect.signature(comp_fxn_obj).parameters

        parameters_to_pass = {}
        for key in defined_parameter_keys:
            if key in given_parameters:
                # if the parameter calls for type SEMENT
                if defined_parameter_keys[key].annotation.__name__ == "SEMENT":
                    optional_param = defined_parameter_keys[key].default is not inspect.Parameter.empty
                    param_val = given_parameters[key]

                    # if it's NOT optional or optional and HAS a value
                    if not optional_param or (optional_param and param_val):
                        # if the value is not already a SEMENT, recurse
                        if not isinstance(given_parameters[key], SEMENT):
                            nested_comp_fxn = given_parameters[key].composition_function_name
                            nested_params = copy.deepcopy(given_parameters[key].parameters)
                            parameters_to_pass[key] = self.get_SEMENT(nested_comp_fxn, nested_params)
                            continue

                    # only gets here if...
                    # (1) non-optional with SEMENT value
                    # (2) optional with None value
                    parameters_to_pass[key] = given_parameters[key]
                # not type SEMENT
                else:
                    parameters_to_pass[key] = given_parameters[key]
            else:
                # if the parameter isn't in the lexicon entry but the function has a default value, just use that
                if defined_parameter_keys[key].default is not inspect.Parameter.empty:
                    parameters_to_pass[key] = defined_parameter_keys[key].default
                else:
                    raise KeyError(f"The parameter '{key}' is not defined in the lexicon entry; {given_parameters}")

        sement = comp_fxn_obj(**parameters_to_pass)

        return sement

    def convert_node_to_SEMENT(self, node, node_evaluation=None):
        """
        Convert a node from a directed graph to a SEMENT

        **Parameters**
        | Parameter | Type | Description | Default | Example |
        | --------- | ---- | ----------- | ------- | ------- |
        | `node` | tuple of `str` and `dict` | node to convert  | -- | `('cake1', {'lexicon_key': 'cake'})` |
        | `node_evaluation` | `POGGNodeEvaluation` | evaluation object associated with the node | `None` | |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT produced with the given node information |
        """

        # comes in as a tuple from the NetworkX NodeView
        node_name, node_props = node[0], node[1]

        # try to get the comp_fxn
        try:
            # get the comp_fxn
            comp_fxn_name = self.lexicon.node_entries[node_props['lexicon_key']].composition_function_name
            param_vals = copy.deepcopy(self.lexicon.node_entries[node_props['lexicon_key']].parameters)
        except KeyError:
            comment = f"'{node_props['lexicon_key']}' not in lexicon's node entries"
            if node_evaluation:
                node_evaluation.node_covered = False
                node_evaluation.generation_comment = comment
            return None


        # try to do the conversion
        try:
            sement = self.get_SEMENT(comp_fxn_name, param_vals)

            if node_evaluation:
                node_evaluation.node_covered = True
                node_evaluation.set_SEMENT(sement)
                # add fxn to list of fxns used
                node_evaluation.sem_comp_fxns_used.add(comp_fxn_name)

            return sement
        except Exception as err:
            # if some unforeseen error occurs just leave it in the comment
            comment = err.args[0]

            if node_evaluation:
                node_evaluation.node_covered = False
                node_evaluation.generation_comment = comment
            return None



    def convert_edge_to_SEMENT(self, edge, parent, child, edge_evaluation=None):
        """
        Convert an edge from a directed graph to a SEMENT

        **Parameters**
        | Parameter | Type | Description | Default | Example |
        | --------- | ---- | ----------- | ------- | ------- |
        | `edge` | `dict` | `dict` of edge properties | -- | `{'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}` |
        | `parent` | `SEMENT` | SEMENT object produced for parent node | -- | |
        | `child` | `SEMENT` | SEMENT object produced for child node | -- |
        | `edge_evaluation` | `POGGEdgeEvaluation` | evaluation object associated with the edge | `None` | |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT produced with the given edge information |
        """

        # check if one of the SEMENTs to compose is None
        if parent is None:
            if edge_evaluation:
                edge_evaluation.edge_covered = False
                edge_evaluation.generation_comment = f"parent of '{edge['lexicon_key']}' has no SEMENT"
            return parent
        if child is None:
            if edge_evaluation:
                edge_evaluation.edge_covered = False
                edge_evaluation.generation_comment = f"child of '{edge['lexicon_key']}' has no SEMENT"
            return parent

        try:
            # get comp_fxn
            comp_fxn_name = self.lexicon.edge_entries[edge['lexicon_key']].composition_function_name
            param_vals = copy.deepcopy(self.lexicon.edge_entries[edge['lexicon_key']].parameters)
        except KeyError:
            if edge_evaluation:
                edge_evaluation.edge_covered = False
                edge_evaluation.generation_comment = f"'{edge['lexicon_key']}' not in lexicon's edge entries"
            # return the parent SEMENT (if the edge fails then anything contributed from child etc doesn't matter)
            return parent

        # swap out 'parent' and 'child' in param_vals for the SEMENTs themselves
        for key in param_vals.keys():
            if param_vals[key] == 'parent':
                param_vals[key] = parent
            elif param_vals[key] == 'child':
                param_vals[key] = child
            # if there's a parameter that introduces its own SEMENT, build it and insert it as the value
            elif isinstance(param_vals[key], pogg.lexicon.lexicon_builder.POGGLexiconEntry):
                param_vals[key] = self.get_SEMENT(param_vals[key].composition_function_name, param_vals[key].parameters)
            else:
                # I don't think I should raise an error?
                # If there's some other edge parameter, just leave it alone
                pass

        # if some other unforeseen error occurs, leave it in the comment and proceed
        try:
            sement = self.get_SEMENT(comp_fxn_name, param_vals)
        except Exception as err:
            if edge_evaluation:
                edge_evaluation.generation_comment = f"Error during execution ({err})"
                edge_evaluation.edge_covered = False
            # just return the parent, i.e. the SEMENT before attempting to compose
            return parent

        if edge_evaluation:
            # add fxn to list of fxns used
            edge_evaluation.sem_comp_fxns_used.add(comp_fxn_name)
            edge_evaluation.edge_covered = True
            edge_evaluation.set_SEMENT(sement)

        return sement


    def convert_graph_to_SEMENT(self, graph, graph_evaluation=None, root=None):
        """
        Convert a directed graph to a SEMENT.

        **Parameters**
        | Parameter | Type | Description | Default | Example |
        | --------- | ---- | ----------- | ------- | ------- |
        | `graph` | `DiGraph` | NetworkX directed graph | -- | |
        | `graph_evaluation` | `SEMENT` | SEMENT object produced for child node | None | |
        | `root` | tuple of `str` and `dict` | root of the (sub)graph | None | `('cake1', {'lexicon_key': 'cake'})` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT produced for the given graph |
        """

        # first check for cycles, skip the graph if there are any
        try:
            nx.find_cycle(graph)
            if graph_evaluation is not None:
                # mark all nodes and edges as not covered
                graph_evaluation.mark_all_uncovered()
                graph_evaluation.generation_comment = "Cycle found in graph, skipping"
            return None
        except nx.exception.NetworkXNoCycle:
            pass


        # try to find the root if it's not passed in
        if root is None:
            try:
                root = POGGGraphUtil.find_root(graph)
            except ValueError as err:
                graph_evaluation.generation_comment = err.args[0]
                root = None
        # if it's STILL none...
        if root is None:
            # mark all nodes and edges as not covered
            graph_evaluation.mark_all_uncovered()
            return None

        # root comes in as a tuple with name first and properties second: ('cake', {'lexicon_key: 'cake'})
        root_name = root[0]

        # get SEMENT for root
        if graph_evaluation is not None:
            node_evaluation = graph_evaluation.get_node_evaluation(root_name)
        else:
            node_evaluation = None

        # attempt to convert node to SEMENT
        latest_sement = self.convert_node_to_SEMENT(root, node_evaluation)

        # recurse on each child
        for child in graph.successors(root_name):
            # get node properties for child
            child_properties = graph.nodes[child]
            # convert to tuple
            child_with_props = (child, child_properties)
            # get SEMENT for child by recursing on it as a subgraph
            child_sement = self.convert_graph_to_SEMENT(graph, graph_evaluation, child_with_props)
            # get edge information between current root (parent) and child
            edge_data = graph.get_edge_data(root_name, child)

            # perform composition between parent and child
            if graph_evaluation is not None:
                edge_evaluation = graph_evaluation.get_edge_evaluation(root_name, child, edge_data)
            else:
                edge_evaluation = None

            latest_sement = self.convert_edge_to_SEMENT(edge_data, latest_sement, child_sement, edge_evaluation)


        return latest_sement