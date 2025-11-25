import os
from pytest_cases import fixture, case
import networkx as nx

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs

from pogg.evaluation.evaluation import POGGNodeEvaluation, POGGEdgeEvaluation, POGGGraphEvaluation, POGGEvaluation

@fixture
def simple_graph():
    graph = nx.DiGraph()
    # update graph to have nodes and edges
    graph.add_edge("parent", "child", label="edge")
    return graph

@fixture
def all_branches_graph():
    # one graph with each of the following:
    # (1) covered / included node
    # (2) covered / NOT included node (child of uncovered)
    # (3) not covered / not included node
    # (4) covered / included edge
    # (5) covered / NOT included ege (child of uncovered)
    # (6) not covered / not included edge

    graph = nx.DiGraph()
    graph.add_nodes_from(["root", "node_cov_incl", "node_cov_noincl",
                          "node_cov_noincl2", "node_nocov_noincl"])

    # root --> node_cov_incl ... edge_cov_incl [cases 1, 4]
    graph.add_edge("root", "node_cov_incl", label="edge_cov_incl")
    # root --> node_cov_noincl ... edge_nocov_noincl [case 6]
    graph.add_edge("root", "node_cov_noincl", label="edge_nocov_noincl")
    # node_cov_incl --> node_nocov_noincl ... edge_nocov_noincl2 [case 3]
    graph.add_edge("node_cov_incl", "node_nocov_noincl", label="edge_nocov_noincl2")
    # node_cov_noincl --> node_cov_noincl2 ... edge_cov_noincl [cases 2, 5]
    graph.add_edge("node_cov_noincl", "node_cov_noincl2", label="edge_cov_noincl")

    return graph

@fixture
def all_branches_graph_eval_obj(all_branches_graph):
    # create eval object
    graph_eval = POGGGraphEvaluation(all_branches_graph, "graph")

    # set coverage for each node/edge
    graph_eval.node_evaluations["root"].node_covered = True
    graph_eval.node_evaluations["node_cov_incl"].node_covered = True
    graph_eval.node_evaluations["node_cov_noincl"].node_covered = True
    graph_eval.node_evaluations["node_cov_noincl2"].node_covered = True
    graph_eval.node_evaluations["node_nocov_noincl"].node_covered = False

    # assume get_edge_evaluation works...
    graph_eval.get_edge_evaluation("root", "node_cov_incl", {"label": "edge_cov_incl"}).edge_covered = True
    graph_eval.get_edge_evaluation("root", "node_cov_noincl", {"label": "edge_nocov_noincl"}).edge_covered = False
    graph_eval.get_edge_evaluation("node_cov_incl", "node_nocov_noincl", {"label": "edge_nocov_noincl2"}).edge_covered = False
    graph_eval.get_edge_evaluation("node_cov_noincl", "node_cov_noincl2",{"label": "edge_cov_noincl"}).edge_covered = True

    return graph_eval

@fixture
def dummy_graph_eval_1(mocker):
    graph_eval = mocker.MagicMock()
    graph_eval.configure_mock(
        **{
            "generated_SEMENT": "text",
            "generated_results": ["text"],
            "node_count": 5,
            "nodes_covered": 3,
            "nodes_included": 2,
            "edge_count": 4,
            "edges_covered": 2,
            "edges_included": 1
        }
    )
    return graph_eval

@fixture
def dummy_graph_eval_2(mocker):
    graph_eval = mocker.MagicMock()
    graph_eval.configure_mock(
        **{
            "generated_SEMENT": "text",
            "generated_results": ["text"],
            "node_count": 10,
            "nodes_covered": 7,
            "nodes_included": 5,
            "edge_count": 10,
            "edges_covered": 6,
            "edges_included": 4
        }
    )
    return graph_eval

@fixture
def dummy_graph_eval_3(mocker):
    graph_eval = mocker.MagicMock()
    graph_eval.configure_mock(
        **{
            "generated_SEMENT": None,
            "generated_results": [],
            "node_count": 5,
            "nodes_covered": 2,
            "nodes_included": 1,
            "edge_count": 4,
            "edges_covered": 2,
            "edges_included": 0
        }
    )
    return graph_eval




class SetSement:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGNodeEvaluation.set_SEMENT
        - pogg.evaluation.evaluation.POGGEdgeEvaluation.set_SEMENT
        - pogg.evaluation.evaluation.POGGGraphEvaluation.set_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Each evaluation object type has this same function so the same cases can be used each for each test
    """

    """
    SUCCESS CASES
        1. set to a legitimate SEMENT
        2. set to None 
    """

    @staticmethod
    def case_real_sement(evaluation_test_dir):
        sement_file = os.path.join(evaluation_test_dir, "cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        sement_string = sementcodecs.encode(sement, indent=True)

        return sement, sement_string

    @staticmethod
    def case_none_sement(evaluation_test_dir):
        # TODO pytest_cases throws an error if I don't put the test_dir fixture in
        return None, None


class POGGNodeEvaluationInit:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGNodeEvaluation.__init__

    GENERAL DESCRIPTION OF TEST CASES:
        Return init information along with a mock object and compare resulting object to mock object
    """

    """
    SUCCESS CASES
        1. init with some generic node information 
        2. set_SEMENT
            - set to a legitimate SEMENT
            - set to None 
    """

    @staticmethod
    def case_basic_node(mocker):
        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "node",
                "node_props": {"prop": "val"},
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "node_covered": None,
                "node_included": None,
                "generation_comment": None
            }
        )

        # attributes to compare between test and mock object
        attrs = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment"]

        return "node", {"prop": "val"}, mock_node_eval, attrs


class POGGEdgeEvaluationInit:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEdgeEvaluation.__init__

    GENERAL DESCRIPTION OF TEST CASES:
        Return init information along with a mock object and compare resulting object to mock object
    """

    """
    SUCCESS CASES
        1. init with some generic edge information 
    """

    @staticmethod
    def case_basic_edge(mocker):
        mock_edge_eval = mocker.MagicMock()
        mock_edge_eval.configure_mock(
            **{
                "edge_name": "edge",
                "edge_props": {"prop": "val"},
                "parent_node_name": "parent",
                "child_node_name": "child",
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "edge_covered": None,
                "edge_included": None,
                "generation_comment": None
            }
        )

        # attributes to compare between test and mock object
        attrs = ["edge_name", "edge_props", "parent_node_name", "child_node_name",
                 "generated_SEMENT", "generated_SEMENT_string", "edge_covered",
                 "edge_included", "generation_comment"]

        return "edge", {"prop": "val"}, "parent", "child", mock_edge_eval, attrs


class POGGGraphEvaluationInit:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.__init__

    GENERAL DESCRIPTION OF TEST CASES:
        Return init information along with a mock object and compare resulting object to mock object
    """

    """
    SUCCESS CASES
        1. init with some generic graph information 
    """

    @staticmethod
    def case_empty_graph(mocker):
        graph = nx.DiGraph()

        mock_graph_eval = mocker.MagicMock()
        mock_graph_eval.configure_mock(
            **{
                "graph": graph,
                "graph_name": "graph",
                "node_evaluations": {},
                "edge_evaluations": [],
                "node_count": None,
                "nodes_covered": None,
                "nodes_included": None,
                "node_coverage": None,
                "node_inclusion": None,
                "edge_count": None,
                "edges_covered": None,
                "edges_included": None,
                "edge_coverage": None,
                "edge_inclusion": None,
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "collapsed_SEMENT": None,
                "collapsed_SEMENT_string": None,
                "wrapped_SEMENT": None,
                "wrapped_SEMENT_string": None,
                "generated_results": []


            }
        )

        attr = ["graph", "graph_name", "node_evaluations", "edge_evaluations", "node_evaluations",
                "node_count", "nodes_covered", "nodes_included", "node_coverage", "node_inclusion",
                "edge_count", "edges_covered", "edges_included", "edge_coverage", "edge_inclusion",
                "generated_SEMENT", "generated_SEMENT_string", "collapsed_SEMENT", "collapsed_SEMENT_string",
                "wrapped_SEMENT", "wrapped_SEMENT_string", "generated_results"]

        return graph, "graph", mock_graph_eval, attr


class CreateNodeEvaluations:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.create_node_evaluations

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object and a gold example of what the graph eval object's node evaluations should look like
        Test should compare actual node evaluations after call to gold example
    """

    """
    SUCCESS CASES
        1. graph eval object with simple graph with two nodes and one edge
    """

    @staticmethod
    def case_simple_graph_node_evals(simple_graph):
        graph = nx.DiGraph()

        # init with empty graph
        # this is because the init calls create_node_evals and create_edge_evals
        # and i don't feel like patching it out so just init it empty first
        graph_eval = POGGGraphEvaluation(graph, "graph")

        # update eval object with real graph
        graph_eval.graph = simple_graph

        # expected result of create_node_evaluations
        gold_node_evaluations = {
            "parent": POGGNodeEvaluation("parent", {}),
            "child": POGGNodeEvaluation("child", {}),
        }

        attrs = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment"]


        return graph_eval, gold_node_evaluations, attrs


class CreateEdgeEvaluations:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.create_edge_evaluations

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object and a gold example of what the graph eval object's edge evaluations should look like
        Test should compare actual edge evaluations after call to gold example
    """

    """
    SUCCESS CASES
        1. graph eval object with simple graph with two nodes and one edge
    """

    @staticmethod
    def case_simple_graph_edge_evals(simple_graph):
        graph = nx.DiGraph()

        # init with empty graph
        # this is because the init calls create_node_evals and create_edge_evals
        # and i don't feel like patching it out so just init it empty first
        graph_eval = POGGGraphEvaluation(graph, "graph")

        # update eval object with real graph
        graph_eval.graph = simple_graph

        # expected result of create_node_evaluations
        gold_edge_evaluations = [POGGEdgeEvaluation("edge", {"label": "edge"}, "parent", "child")]

        attrs = ["edge_name", "edge_props", "parent_node_name", "child_node_name",
                 "generated_SEMENT", "generated_SEMENT_string", "edge_covered",
                 "edge_included", "generation_comment"]

        return graph_eval, gold_edge_evaluations, attrs


class GetNodeEvaluation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.get_node_evaluation

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object and the name of a node to retrieve the node evaluation for.
        Test should ensure the retrieved node evaluation object has the correct name when it does find a node evaluation object
    """

    """
    SUCCESS CASES
        1. existing node named "parent"
        
    FAILURE CASES:
        1. nonexistent node
    """

    @staticmethod
    @case(tags="success")
    def case_simple_graph_node_eval(simple_graph):
        graph_eval = POGGGraphEvaluation(simple_graph, "graph")
        return graph_eval, "parent"

    @staticmethod
    @case(tags="failure")
    def case_simple_graph_node_eval_failure(simple_graph):
        graph_eval = POGGGraphEvaluation(simple_graph, "graph")
        return graph_eval, "fake"


class GetEdgeEvaluation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.get_edge_evaluation

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object and the edge details to retrieve the edge evaluation for.
        Test should ensure the retrieved edge evaluation object has the correct name when it does find an edge evaluation object
    """

    """
    SUCCESS CASES
        1. existing edge between "parent" and "child" named "edge"

    FAILURE CASES:
        1. nonexistent edge
    """

    @staticmethod
    @case(tags="success")
    def case_simple_graph_edge_eval(simple_graph):
        graph_eval = POGGGraphEvaluation(simple_graph, "graph")
        return graph_eval, "parent", "child", {'label': 'edge'}

    @staticmethod
    @case(tags="failure")
    def case_simple_graph_edge_eval_failure(simple_graph):
        graph_eval = POGGGraphEvaluation(simple_graph, "graph")
        return graph_eval, "fake", "child", {'label': 'edge'}


class DetermineInclusion:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.determine_inclusion

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object with preset values for whether certain nodes/edges were covered during generation
        Additionally provide the expected result after determine_inclusion is called
        Test should compare result to expected
    """

    """
    SUCCESS CASES
        1. graph that covers all inclusion cases:
            - node, cov=True, incl=True
            - node, cov=True, incl=False
            - node, cov=False, incl=False 
            - edge, cov=True, incl=True
            - edge, cov=True, incl=False
            - edge, cov=False, incl=False 
       The following cases are meant to cover the different edge cases that arise from different values passed in for the "root" and "ancestor_incl" parameters:
       2. root=None, ancestor_incl=None
       3. root=None, ancestor_incl=False
       4. root=None, ancestor_incl=True
    """

    @staticmethod
    def case_less_simple_graph(all_branches_graph_eval_obj):
        gold_node_inclusions = {
            "root": True,
            "node_cov_incl": True,
            "node_nocov_noincl": False,
            "node_cov_noincl": False,
            "node_cov_noincl2": False,
        }

        gold_edge_inclusions = {
            "edge_cov_incl": {"parent": "root", "child": "node_cov_incl", "inclusion": True},
            "edge_nocov_noincl": {"parent": "root", "child": "node_cov_noincl", "inclusion": False},
            "edge_nocov_noincl2": {"parent": "node_cov_incl", "child": "node_nocov_noincl", "inclusion": False},
            "edge_cov_noincl":  {"parent": "node_nocov_noincl", "child": "node_nocov_noincl2", "inclusion": False}
        }

        return None, None, all_branches_graph_eval_obj, gold_node_inclusions, gold_edge_inclusions

    @staticmethod
    def case_root_only_notincluded():
        graph = nx.DiGraph()
        graph.add_node("root")

        # create eval object
        graph_eval = POGGGraphEvaluation(graph, "graph")

        gold_node_inclusions = {
            "root": False
        }

        gold_edge_inclusions = {}

        return None, None, graph_eval, gold_node_inclusions, gold_edge_inclusions


    @staticmethod
    def case_root_only_explicit_false_ancestor_incl():
        graph = nx.DiGraph()
        graph.add_node("root")

        # create eval object
        graph_eval = POGGGraphEvaluation(graph, "graph")

        gold_node_inclusions = {
            "root": False
        }

        gold_edge_inclusions = {}

        return None, False, graph_eval, gold_node_inclusions, gold_edge_inclusions

    @staticmethod
    def case_root_only_explicit_true_ancestor_incl():
        graph = nx.DiGraph()
        graph.add_node("root")

        # create eval object
        graph_eval = POGGGraphEvaluation(graph, "graph")

        gold_node_inclusions = {
            "root": False
        }

        gold_edge_inclusions = {}

        return None, True, graph_eval, gold_node_inclusions, gold_edge_inclusions

class CalculateGraphMetrics:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.calculate_metrics

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph evaluation object with preset values for whether certain nodes/edges were covered/included
        Additionally provide the expected results for the metrics after calling calculate_metrics
        Compare result of call to expected result
    """

    """
    SUCCESS CASES
        1. graph that covers all inclusion cases:
            - node, cov=True, incl=True
            - node, cov=True, incl=False
            - node, cov=False, incl=False 
            - edge, cov=True, incl=True
            - edge, cov=True, incl=False
            - edge, cov=False, incl=False 
    """

    @staticmethod
    def case_all_branches_graph(all_branches_graph_eval_obj):
        # update inclusion values explicitly
        # set coverage for each node/edge
        all_branches_graph_eval_obj.node_evaluations["root"].node_included = True
        all_branches_graph_eval_obj.node_evaluations["node_cov_incl"].node_included = True
        all_branches_graph_eval_obj.node_evaluations["node_cov_noincl"].node_included = False
        all_branches_graph_eval_obj.node_evaluations["node_cov_noincl2"].node_included = False
        all_branches_graph_eval_obj.node_evaluations["node_nocov_noincl"].node_included = False

        # assume get_edge_evaluation works...
        all_branches_graph_eval_obj.get_edge_evaluation("root", "node_cov_incl", {"label": "edge_cov_incl"}).edge_included = True
        all_branches_graph_eval_obj.get_edge_evaluation("root", "node_cov_noincl", {"label": "edge_nocov_noincl"}).edge_included = False
        all_branches_graph_eval_obj.get_edge_evaluation("node_cov_incl", "node_nocov_noincl", {"label": "edge_nocov_noincl2"}).edge_included = False
        all_branches_graph_eval_obj.get_edge_evaluation("node_cov_noincl", "node_cov_noincl2", {"label": "edge_cov_noincl"}).edge_included = False
        gold_metrics = {
            "node_count": 5,
            "edge_count": 4,
            "nodes_covered": 4,
            "nodes_included": 2,
            "node_coverage": 0.8,
            "node_inclusion": 0.4,
            "edges_covered": 2,
            "edges_included": 1,
            "edge_coverage": 0.5,
            "edge_inclusion": 0.25
        }

        return all_branches_graph_eval_obj, gold_metrics


class MarkAllUncovered:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.mark_all_uncovered

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph eval object and ensure that all nodes/edges are marked as not covered and not included after function call
    """

    """
    SUCCESS CASES
        1. graph that covers all inclusion cases:
            - node, cov=True, incl=True
            - node, cov=True, incl=False
            - node, cov=False, incl=False 
            - edge, cov=True, incl=True
            - edge, cov=True, incl=False
            - edge, cov=False, incl=False 
    """

    @staticmethod
    def case_all_branches_graph(all_branches_graph_eval_obj):
        return all_branches_graph_eval_obj


class POGGEvaluationInit:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEvaluation.__init__

    GENERAL DESCRIPTION OF TEST CASES:
        Return init information along with a mock object and compare resulting object to mock object
    """

    """
    SUCCESS CASES
        1. init with a generic dataset name
    """

    @staticmethod
    def case_eval_init(mocker):
        mock_eval = mocker.MagicMock()
        mock_eval.configure_mock(
            **{
                "dataset_name": "dataset",
                "graph_evaluations": [],
                "graph_count": None,
                "graph_SEMENT_count": None,
                "graph_SEMENT_coverage": None,
                "graphs_with_text_count": None,
                "graph_text_coverage": None,
                "full_node_count": None,
                "full_nodes_covered": None,
                "full_nodes_included": None,
                "full_node_coverage": None,
                "full_node_inclusion": None,
                "full_edge_count": None,
                "full_edges_covered": None,
                "full_edges_included": None,
                "full_edge_coverage": None,
                "full_edge_inclusion": None
            }
        )

        attr = ["dataset_name", "graph_evaluations", "graph_count", "graph_SEMENT_count", "graph_SEMENT_coverage",
                "graphs_with_text_count", "graph_text_coverage", "full_node_count",
                "full_nodes_covered", "full_nodes_included", "full_node_coverage",
                "full_node_inclusion", "full_edge_count", "full_edges_covered",
                "full_edges_included", "full_edge_coverage", "full_edge_inclusion"]

        return "dataset", mock_eval, attr


class AddGraph:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEvaluation.add_graph

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph to add and the graph's name
        Test should check that a new graph evaluation object was added with the graph's name
    """

    """
    SUCCESS CASES
        1. simple graph 
    """

    @staticmethod
    def case_simple_graph(simple_graph):
        return simple_graph, "graph"


class CalculateDatasetMetrics:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEvaluation.calculate_metrics

    GENERAL DESCRIPTION OF TEST CASES:
        Provide an evaluation object with dummy graph eval objects
        Additionally provide the expected results for the calculated metrics after calling calculate_metrics
        Compare result of call to expected result
    """

    """
    SUCCESS CASES
        1. eval object with preset values for count-based metrics 
    """

    @staticmethod
    def case_eval_obj(dummy_graph_eval_1, dummy_graph_eval_2, dummy_graph_eval_3):
        pogg_eval = POGGEvaluation("dataset")

        # add dummy graph_eval objects directly
        pogg_eval.graph_evaluations.append(dummy_graph_eval_1)
        pogg_eval.graph_evaluations.append(dummy_graph_eval_2)
        pogg_eval.graph_evaluations.append(dummy_graph_eval_3)

        gold_metrics = {
            "graph_count": 3,
            "graph_SEMENT_count": 2,
            "graphs_with_text_count": 2,
            "graph_text_coverage": 2 / 3,
            "full_node_count": 20,
            "full_nodes_covered": 12,
            "full_nodes_included": 8,
            "full_node_coverage": 12 / 20,
            "full_node_inclusion": 8 / 20,
            "full_edge_count": 18,
            "full_edges_covered": 10,
            "full_edges_included": 5,
            "full_edge_coverage": 10 / 18,
            "full_edge_inclusion": 5 / 18
        }

        return pogg_eval, gold_metrics


