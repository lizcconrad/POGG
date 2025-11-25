import copy
from inspect import signature
from pogg.my_delphin.my_delphin import SEMENT
from pogg.data_handling.graph_util import POGGGraphUtil
from pogg.lexicon.lexicon_builder import POGGLexicon
from pogg.semantic_composition.base_constructions import SemanticComposition

class POGGGraphConverter:
    def __init__(self, semantic_composition, dataset):
        self.sem_comp = semantic_composition
        self.lexicon = dataset.lexicon

    def get_sement(self, comp_fxn_name, parameter_values):
        comp_fxn_obj = getattr(self.sem_comp, comp_fxn_name)

        # get parameters for the comp_fxn
        parameter_keys = signature(comp_fxn_obj).parameters

        parameters = {}
        for key in parameter_keys:
            if key in parameter_values:
                # if the parameter calls for type SEMENT *AND* the value isn't already a SEMENT object, we need to recurse to build one
                if parameter_keys[key].annotation.__name__ == "SEMENT" and not isinstance(parameter_values[key], SEMENT):
                    nested_comp_fxn = parameter_values[key].composition_function_name
                    nested_params = copy.deepcopy(parameter_values[key].parameters)
                    parameters[key] = self.get_sement(nested_comp_fxn, nested_params)
                else:
                    parameters[key] = parameter_values[key]
            else:
                raise KeyError("The parameter '{}' is not defined in the lexicon entry; {}".format(key, parameter_values))

        return comp_fxn_obj(**parameters)

    def convert_node_to_sement(self, node, node_evaluation):
        # comes in as a tuple from the NetworkX NodeView
        node_name, node_props = node[0], node[1]

        try:
            # get the comp_fxn
            comp_fxn_name = self.lexicon.node_entries[node_props['lexicon_key']].composition_function_name
            param_vals = copy.deepcopy(self.lexicon.node_entries[node_props['lexicon_key']].parameters)
            sement = self.get_sement(comp_fxn_name, param_vals)
            node_evaluation.node_covered = True
            node_evaluation.set_SEMENT(sement)
            return sement
        except KeyError:
            node_evaluation.node_covered = False
            node_evaluation.generation_comment = f"'{node_props['lexicon_key']}' not in lexicon's node entries"
            return None



    def convert_edge_to_sement(self, edge, parent, child, edge_evaluation):
        # check if one of the SEMENTs to compose is None
        if parent is None:
            edge_evaluation.edge_covered = False
            edge_evaluation.generation_comment = f"parent of '{edge['lexicon_key']}' has no SEMENT"
            return parent
        if child is None:
            edge_evaluation.edge_covered = False
            edge_evaluation.generation_comment = f"child of '{edge['lexicon_key']}' has no SEMENT"
            return parent

        try:
            # get comp_fxn
            comp_fxn_name = self.lexicon.edge_entries[edge['lexicon_key']].composition_function_name
            param_vals = copy.deepcopy(self.lexicon.edge_entries[edge['lexicon_key']].parameters)
        except KeyError:
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
            else:
                # I don't think I should raise an error?
                # If there's some other edge parameter, just leave it alone
                pass

        sement = self.get_sement(comp_fxn_name, param_vals)
        edge_evaluation.edge_covered = True
        edge_evaluation.set_SEMENT(sement)
        return sement





    def convert_graph_to_sement(self, root, graph, graph_eval_obj):
        # try to find the root if it's not passed in
        if root is None:
            root = POGGGraphUtil.find_root(graph)
        # if it's STILL none...
        if root is None:
            # mark all nodes and edges as not covered
            graph_eval_obj.mark_all_uncovered()
            return None

        # root comes in as a tuple with name first and properties second: ('cake', {'lexicon_key: 'cake'})
        root_name = root[0]

        # get SEMENT for root
        node_evaluation = graph_eval_obj.get_node_evaluation(root_name)
        latest_sement = self.convert_node_to_sement(root, node_evaluation)

        # recurse on each child
        for child in graph.successors(root_name):
            # get node properties for child
            child_properties = graph.nodes[child]
            # convert to tuple
            child_with_props = (child, child_properties)
            # get SEMENT for child by recursing on it as a subgraph
            child_sement = self.convert_graph_to_sement(child_with_props, graph, graph_eval_obj)
            # get edge information between current root (parent) and child
            edge_data = graph.get_edge_data(root_name, child)

            # perform composition between parent and child
            edge_evaluation = graph_eval_obj.get_edge_evaluation(root_name, child, edge_data)
            latest_sement = self.convert_edge_to_sement(edge_data, latest_sement, child_sement, edge_evaluation)


        return latest_sement