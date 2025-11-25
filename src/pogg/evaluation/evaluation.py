import pandas
from great_tables import GT
from pogg.my_delphin import sementcodecs
from pogg.data_handling.graph_util import POGGGraphUtil

# data class ?
class POGGNodeEvaluation:
    def __init__(self, node_name, node_props):
        # node information
        self.node_name = node_name
        self.node_props = node_props

        # associated SEMENT
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None

        # evaluation information
        # was there a SEMENT generated from this node?
        self.node_covered = None
        # was this node included in the final SEMENT?
        self.node_included = None
        # explanation in the event of failure
        self.generation_comment = None

    def set_SEMENT(self, sement):
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass


class POGGEdgeEvaluation:
    def __init__(self, edge_name, edge_props, parent, child):
        # edge information
        self.edge_name = edge_name
        self.edge_props = edge_props
        self.parent_node_name = parent
        self.child_node_name = child

        # associated SEMENT
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None

        # evaluation information
        # was there a SEMENT generated from this node?
        self.edge_covered = None
        # was this node included in the final SEMENT?
        self.edge_included = None
        # explanation in the event of failure
        self.generation_comment = None

    def set_SEMENT(self, sement):
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass




class POGGGraphEvaluation:
    def __init__(self, graph, graph_name):
        self.graph = graph
        self.graph_name = graph_name
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

        # generated results
        self.generated_SEMENT = None
        self.generated_SEMENT_string = None
        self.collapsed_SEMENT = None
        self.collapsed_SEMENT_string = None
        self.wrapped_SEMENT = None
        self.wrapped_SEMENT_string = None
        self.generated_results = []

    def create_node_evaluations(self):
        for node in self.graph.nodes(data=True):
            node_name = node[0]
            node_props = node[1]
            self.node_evaluations[node_name] = POGGNodeEvaluation(node_name, node_props)


    def create_edge_evaluations(self):
        for edge in self.graph.edges(data=True):
            parent = edge[0]
            child = edge[1]
            edge_name = edge[2]['label']
            props = edge[2]
            self.edge_evaluations.append(POGGEdgeEvaluation(edge_name, props, parent, child))

    def set_SEMENT(self, sement):
        self.generated_SEMENT = sement
        if self.generated_SEMENT is not None:
            self.generated_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def set_wrapped_SEMENT(self, sement):
        self.wrapped_SEMENT = sement
        if self.wrapped_SEMENT is not None:
            self.wrapped_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def set_collapsed_SEMENT(self, sement):
        self.collapsed_SEMENT = sement
        if self.collapsed_SEMENT is not None:
            self.collapsed_SEMENT_string = sementcodecs.encode(sement, indent=True)
        else:
            pass

    def get_node_evaluation(self, node_name):
        try:
            return self.node_evaluations[node_name]
        except KeyError:
            raise KeyError("{} not a node in graph".format(node_name))

    def get_edge_evaluation(self, parent, child, edge_data):
        edge_name = edge_data['label']
        for edge_eval in self.edge_evaluations:
            if edge_name == edge_eval.edge_name and parent == edge_eval.parent_node_name and child == edge_eval.child_node_name:
                return edge_eval
        raise KeyError("{} with parent {} and child {} not an edge in graph".format(edge_name, parent, child))

    def determine_inclusion(self, root, ancestor_inclusion):
        """
        once all nodes/edges are marked for coverage, inclusion must be marked on every node/edge
        this is done AFTER all nodes/edges are marked for coverage because
        inclusion is impacted by the coverage of related elements in the graph
        e.g. a graph with two nodes that generated a SEMENT but that are linked by an edge that did not get covered
        the child node will need to be marked as False for inclusion as a result of the connecting edge not being covered
        """
        if root is None:
            # returns it as a tuple so get the first element which is just the name
            root = POGGGraphUtil.find_root(self.graph)[0]

        root_eval = self.get_node_evaluation(root)
        if ancestor_inclusion:
            if root_eval.node_covered:
                root_eval.node_included = True
            else:
                root_eval.node_included = False
                # update ancestor_inclusion to false for remaining graph elements
                ancestor_inclusion = False
        # for first call of function
        elif ancestor_inclusion is None:
            if root_eval.node_covered:
                root_eval.node_included = True
                # set ancestor_inclusion to true now that we have one node included
                ancestor_inclusion = True
            else:
                root_eval.node_included = False
                # update ancestor_inclusion to false for remaining graph elements
                ancestor_inclusion = False
        else:
            root_eval.node_included = False
            # only gets here if ancestor is not included
            root_eval.generation_comment = "Successor of failed element"


        for child in self.graph.successors(root):
            # determine if edge is included
            edge_data = self.graph.get_edge_data(root, child)
            edge_eval = self.get_edge_evaluation(root, child, edge_data)

            if ancestor_inclusion:
                if edge_eval.edge_covered:
                    edge_eval.edge_included = True
                else:
                    edge_eval.edge_included = False
                    ancestor_inclusion = False
            else:
                edge_eval.edge_included = False

            # recurse down to child
            self.determine_inclusion(child, ancestor_inclusion)


    def calculate_metrics(self):
        # determine inclusion
        self.determine_inclusion(None, None)

        self.node_count = len(self.graph.nodes())
        self.edge_count = len(self.graph.edges())

        self.nodes_covered = 0
        self.nodes_included = 0
        for node in self.node_evaluations.keys():
            node_eval = self.node_evaluations[node]
            if node_eval.node_covered:
                self.nodes_covered += 1
            if node_eval.node_included:
                self.nodes_included += 1
        self.node_coverage = self.nodes_covered / self.node_count
        self.node_inclusion = self.nodes_included / self.node_count

        self.edges_covered = 0
        self.edges_included = 0
        for edge_eval in self.edge_evaluations:
            if edge_eval.edge_covered:
                self.edges_covered += 1
            if edge_eval.edge_included:
                self.edges_included += 1
        self.edge_coverage = self.edges_covered / self.edge_count
        self.edge_inclusion = self.edges_included / self.edge_count


    def mark_all_uncovered(self):
        for node_key in self.node_evaluations.keys():
            self.node_evaluations[node_key].node_covered = False
            self.node_evaluations[node_key].node_included = False
        for edge in self.edge_evaluations:
            edge.edge_covered = False
            edge.edge_included = False


class POGGEvaluation:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.graph_evaluations = []

        # calculations made over all graphs
        self.graph_count = None
        self.graph_SEMENT_count = None
        self.graph_SEMENT_coverage = None
        # NOT number of results, but number that generated text
        self.graphs_with_text_count = None
        self.graph_text_coverage = None
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

    def add_graph(self, graph, graph_name):
        # create graph evaluation object
        self.graph_evaluations.append(POGGGraphEvaluation(graph, graph_name))

    def calculate_metrics(self):
        self.graph_count = len(self.graph_evaluations)

        self.graph_SEMENT_count = 0
        self.graphs_with_text_count = 0
        self.full_node_count = 0
        self.full_nodes_covered = 0
        self.full_nodes_included = 0
        self.full_edge_count = 0
        self.full_edges_covered = 0
        self.full_edges_included = 0
        for graph_eval in self.graph_evaluations:
            if graph_eval.generated_SEMENT is not None:
                self.graph_SEMENT_count += 1
            if len(graph_eval.generated_results) > 0:
                self.graphs_with_text_count += 1

            self.full_node_count += graph_eval.node_count
            self.full_nodes_covered += graph_eval.nodes_covered
            self.full_nodes_included += graph_eval.nodes_included
            self.full_edge_count += graph_eval.edge_count
            self.full_edges_covered += graph_eval.edges_covered
            self.full_edges_included += graph_eval.edges_included

        self.graph_SEMENT_coverage = self.graph_SEMENT_count / self.graph_count
        self.graph_text_coverage = self.graphs_with_text_count / self.graph_count
        self.full_node_coverage = self.full_nodes_covered / self.full_node_count
        self.full_node_inclusion = self.full_nodes_included / self.full_node_count
        self.full_edge_coverage = self.full_edges_covered / self.full_edge_count
        self.full_edge_inclusion = self.full_edges_included / self.full_edge_count

