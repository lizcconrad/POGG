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

    # add some gold outputs
    graph_eval.gold_outputs = ["ME when i'm an output", "me when i'm also an output"]
    graph_eval.generated_results = ["me when i'm an OUTPUT", "me when i'm a FAKE output"]

    return graph_eval

@fixture
def rootless_graph():
    graph = nx.DiGraph()
    graph.add_node("node1")
    graph.add_node("node2")
    return graph

@fixture
def rootless_graph_eval_obj(rootless_graph):
    graph_eval = POGGGraphEvaluation(rootless_graph, "graph")
    graph_eval.node_evaluations["node1"].node_covered = False
    graph_eval.node_evaluations["node1"].node_included= False
    graph_eval.node_evaluations["node2"].node_covered = False
    graph_eval.node_evaluations["node2"].node_included = False
    return graph_eval

@fixture
def it_is_just_one_little_nodie():
    graph = nx.DiGraph()
    graph.add_node("node")
    return graph

@fixture
def it_is_just_one_little_nodie_eval_obj(it_is_just_one_little_nodie):
    graph_eval = POGGGraphEvaluation(it_is_just_one_little_nodie, "graph")
    # set coverage and inclusion for the node/edge
    graph_eval.node_evaluations["node"].node_covered = False
    graph_eval.node_evaluations["node"].node_included = False
    return graph_eval

@fixture
def cyclical_graph():
    graph = nx.DiGraph()
    graph.add_edge("root", "root", label="edge")
    return graph

@fixture
def cyclical_graph_eval_obj(cyclical_graph):
    graph_eval = POGGGraphEvaluation(cyclical_graph, "graph")
    # set coverage and inclusion for the node/edge
    graph_eval.node_evaluations["root"].node_covered = False
    graph_eval.node_evaluations["root"].node_included = False
    graph_eval.get_edge_evaluation("root", "root", {"label": "edge"}).edge_covered = False
    graph_eval.get_edge_evaluation("root", "root", {"label": "edge"}).edge_included = False
    return graph_eval

@fixture
def dummy_graph_eval_1(mocker):
    graph_eval = mocker.MagicMock()
    graph_eval.configure_mock(
        **{
            "generated_SEMENT": "text",
            "generated_results": ["text"],
            "gold_outputs": ["text"],
            "generated_gold_outputs": ["text"],
            "gold_output_generation_coverage": 1,
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

@fixture
def dummy_graph_eval_no_edges(mocker):
    graph_eval = mocker.MagicMock()
    graph_eval.configure_mock(
        **{
            "generated_SEMENT": "text",
            "generated_results": ["text"],
            "node_count": 1,
            "nodes_covered": 1,
            "nodes_included": 1,
            "edge_count": 0,
            "edges_covered": 0,
            "edges_included": 0
        }
    )
    return graph_eval

@fixture
def cookie_SEMENT():
    SEMENT_str = """[  
        TOP: h2
        INDEX: x1
        RELS: < [ _cookie_n_1 LBL: h2 ARG0: x1 ] > 
    ]
    """
    return sementcodecs.decode(SEMENT_str)


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
    def case_real_sement(cookie_SEMENT):
        sement = cookie_SEMENT
        sement_string = sementcodecs.encode(sement, indent=True)

        return sement, sement_string

    @staticmethod
    def case_none_sement():
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
        2. init from a file with a SEMENT in it
        3. init from a file without a SEMENT in it
    """

    @staticmethod
    # TODO pytest_cases throws an error if I don't put the test_dir fixture in every case in the class
    def case_basic_node(evaluation_test_dir, mocker):
        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "node",
                "node_props": {"prop": "val"},
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "node_covered": None,
                "node_included": None,
                "generation_comment": None,
                "inclusion_comment": None
            }
        )

        # attributes to compare between test and mock object
        attrs = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment", "inclusion_comment"]

        return "node", {"prop": "val"}, None, mock_node_eval, attrs

    @staticmethod
    def case_file_w_sement(evaluation_test_dir, mocker):
        eval_file = os.path.join(evaluation_test_dir, "node_eval_file.json")

        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "cake",
                "node_props": {"lexicon_key": "cake"},
                "generated_SEMENT": sementcodecs.decode("[ TOP: h1\n  INDEX: x2\n  RELS: < [ _bear_n_1 LBL: h1 ARG0: x2 ] > ]"),
                "generated_SEMENT_string": "[ TOP: h1\n  INDEX: x2\n  RELS: < [ _bear_n_1 LBL: h1 ARG0: x2 ] > ]",
                "node_covered": True,
                "node_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["noun"]
            }
        )

        # attributes to compare between test and mock object
        attrs = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment", "sem_comp_fxns_used"]

        return "node", {"prop": "val"}, eval_file, mock_node_eval, attrs

    @staticmethod
    def case_file_w_no_sement(evaluation_test_dir, mocker):
        eval_file = os.path.join(evaluation_test_dir, "node_eval_file_no_sement.json")

        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "cake",
                "node_props": {"lexicon_key": "cake"},
                "generated_SEMENT_string": None,
                "generated_SEMENT": None,
                "node_covered": True,
                "node_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["noun"]
            }
        )

        # attributes to compare between test and mock object
        attrs = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment", "sem_comp_fxns_used"]

        return "node", {"prop": "val"}, eval_file, mock_node_eval, attrs

class POGGNodeEvaluationGetDictRepresentation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGNodeEvaluation.get_dict_representation

    GENERAL DESCRIPTION OF TEST CASES:
        Return POGGNodeEvaluation object and gold dict representation
    """

    """
    SUCCESS CASES
        1. generic POGGNodeEvaluation object 
    """

    @staticmethod
    def case_basic_node():
        node_eval_obj = POGGNodeEvaluation("node", {"prop": "val"})
        # set some values
        node_eval_obj.generated_SEMENT_string = "fake SEMENT string"
        node_eval_obj.node_covered = True
        node_eval_obj.node_included = False
        node_eval_obj.generation_comment = "fake comment"
        node_eval_obj.inclusion_comment = "fake comment 2.0"

        gold_dict = {
            'node_name': "node",
            'node_props': {"prop": "val"},
            'generated_SEMENT_string': "fake SEMENT string",
            'sem_comp_fxns_used': {},
            'sem_alg_fxns_used': {},
            'node_covered': True,
            'node_included': False,
            'generation_comment': "fake comment",
            'inclusion_comment': "fake comment 2.0"
        }

        return node_eval_obj, gold_dict



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
        2. init from a file with a SEMENT in it
        3. init from a file without a SEMENT in it
    """

    # TODO pytest_cases throws an error if I don't put the test_dir fixture in every case in the class
    @staticmethod
    def case_basic_edge(evaluation_test_dir, mocker):
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
                "generation_comment": None,
                "inclusion_comment": None,
            }
        )

        # attributes to compare between test and mock object
        attrs = ["edge_name", "edge_props", "parent_node_name", "child_node_name",
                 "generated_SEMENT", "generated_SEMENT_string", "edge_covered",
                 "edge_included", "generation_comment", "inclusion_comment"]

        return "edge", {"prop": "val"}, "parent", "child", None, mock_edge_eval, attrs

    @staticmethod
    def case_file_w_sement(evaluation_test_dir, mocker):
        eval_file = os.path.join(evaluation_test_dir, "edge_eval_file.json")

        mock_edge_eval = mocker.MagicMock()
        mock_edge_eval.configure_mock(
            **{
                "edge_name": "edge",
                "edge_props": {"prop": "val"},
                "parent_node_name": "parent",
                "child_node_name": "child",
                "generated_SEMENT": sementcodecs.decode("[ TOP: h1372\n  INDEX: x1371\n  RELS: < [ _black_a_1 LBL: h1375 ARG0: i1373 ARG1: i1374 ]\n          [ _bear_n_1 LBL: h1372 ARG0: x1371 ] >\n  EQS: < h1375 eq h1372 i1374 eq x1371 > ]"),
                "generated_SEMENT_string": "[ TOP: h1372\n  INDEX: x1371\n  RELS: < [ _black_a_1 LBL: h1375 ARG0: i1373 ARG1: i1374 ]\n          [ _bear_n_1 LBL: h1372 ARG0: x1371 ] >\n  EQS: < h1375 eq h1372 i1374 eq x1371 > ]",
                "edge_covered": True,
                "edge_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["prenominal_adjective"],
            }
        )

        # attributes to compare between test and mock object
        attrs = ["edge_name", "edge_props", "generated_SEMENT", "generated_SEMENT_string",
                 "edge_covered", "edge_included", "generation_comment", "inclusion_comment", "sem_comp_fxns_used"]

        return "edge", {"prop": "val"}, "parent", "child", eval_file, mock_edge_eval, attrs

    @staticmethod
    def case_file_w_no_sement(evaluation_test_dir, mocker):
        eval_file = os.path.join(evaluation_test_dir, "edge_eval_file_no_sement.json")

        mock_edge_eval = mocker.MagicMock()
        mock_edge_eval.configure_mock(
            **{
                "edge_name": "edge",
                "edge_props": {"prop": "val"},
                "parent_node_name": "parent",
                "child_node_name": "child",
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "edge_covered": True,
                "edge_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["prenominal_adjective"],
            }
        )

        # attributes to compare between test and mock object
        attrs = ["edge_name", "edge_props", "generated_SEMENT", "generated_SEMENT_string",
                 "edge_covered", "edge_included", "generation_comment", "inclusion_comment", "sem_comp_fxns_used"]

        return "edge", {"prop": "val"}, "parent", "child", eval_file, mock_edge_eval, attrs

class POGGEdgeEvaluationGetDictRepresentation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEdgeEvaluation.get_dict_representation

    GENERAL DESCRIPTION OF TEST CASES:
        Return POGGEdgeEvaluation object and gold dict representation
    """

    """
    SUCCESS CASES
        1. generic POGGNodeEvaluation object 
    """

    @staticmethod
    def case_basic_edge():
        edge_eval_obj = POGGEdgeEvaluation("edge", {"prop": "val"}, "parent", "child")
        # set some values
        edge_eval_obj.generated_SEMENT_string = "fake SEMENT string"
        edge_eval_obj.edge_covered = True
        edge_eval_obj.edge_included = False
        edge_eval_obj.generation_comment = "fake comment"
        edge_eval_obj.inclusion_comment = "fake comment 2.0"

        gold_dict = {
            'edge_name': "edge",
            'child_node_name': "child",
            'parent_node_name': "parent",
            'edge_props': {"prop": "val"},
            'generated_SEMENT_string': "fake SEMENT string",
            'sem_comp_fxns_used': {},
            'sem_alg_fxns_used': {},
            'edge_covered': True,
            'edge_included': False,
            'generation_comment': "fake comment",
            'inclusion_comment': "fake comment 2.0"
        }

        return edge_eval_obj, gold_dict



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
        2. init with a file with SEMENT strings in it
        3. init with a file without SEMENT strings in it
    """

    # TODO pytest_cases throws an error if I don't put the test_dir fixture in every case in the class
    @staticmethod
    def case_empty_graph(evaluation_test_dir, mocker):
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
                "prepped_SEMENT": None,
                "prepped_SEMENT_string": None,
                "generated_results": []
            }
        )

        g_attr = ["graph", "graph_name", "node_evaluations", "edge_evaluations", "node_evaluations",
                "node_count", "nodes_covered", "nodes_included", "node_coverage", "node_inclusion",
                "edge_count", "edges_covered", "edges_included", "edge_coverage", "edge_inclusion",
                "generated_SEMENT", "generated_SEMENT_string", "collapsed_SEMENT", "collapsed_SEMENT_string",
                "prepped_SEMENT", "prepped_SEMENT_string", "generated_results"]

        n_attr = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                 "node_covered", "node_included", "generation_comment", "sem_comp_fxns_used"]

        e_attr = ["edge_name", "edge_props", "generated_SEMENT", "generated_SEMENT_string",
                 "edge_covered", "edge_included", "generation_comment", "inclusion_comment", "sem_comp_fxns_used"]

        return graph, "graph", None, mock_graph_eval, g_attr, n_attr, e_attr

    @staticmethod
    def case_eval_file_w_sements(evaluation_test_dir, mocker):
        evaluation_directory_sample_dir = os.path.join(evaluation_test_dir, "eval_dir/complete_graphs/graph")
        graph = nx.nx_pydot.read_dot(os.path.join(evaluation_directory_sample_dir, "graph.dot"))

        # mock node eval
        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "node",
                "node_props": {"lexicon_key": "node"},
                "generated_SEMENT": sementcodecs.decode(
                    "[ TOP: h1\n  INDEX: x2\n  RELS: < [ _bear_n_1 LBL: h1 ARG0: x2 ] > ]"),
                "generated_SEMENT_string": "[ TOP: h1\n  INDEX: x2\n  RELS: < [ _bear_n_1 LBL: h1 ARG0: x2 ] > ]",
                "node_covered": True,
                "node_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["noun"],
                "sem_alg_fxns_used": ["create_base_SEMENT"]
            }
        )

        # mock edge eval
        mock_edge_eval = mocker.MagicMock()
        mock_edge_eval.configure_mock(
            **{
                "edge_name": "edge",
                "edge_props": {"prop": "val"},
                "parent_node_name": "parent",
                "child_node_name": "child",
                "generated_SEMENT": sementcodecs.decode(
                    "[ TOP: h1372\n  INDEX: x1371\n  RELS: < [ _black_a_1 LBL: h1375 ARG0: i1373 ARG1: i1374 ]\n          [ _bear_n_1 LBL: h1372 ARG0: x1371 ] >\n  EQS: < h1375 eq h1372 i1374 eq x1371 > ]"),
                "generated_SEMENT_string": "[ TOP: h1372\n  INDEX: x1371\n  RELS: < [ _black_a_1 LBL: h1375 ARG0: i1373 ARG1: i1374 ]\n          [ _bear_n_1 LBL: h1372 ARG0: x1371 ] >\n  EQS: < h1375 eq h1372 i1374 eq x1371 > ]",
                "edge_covered": True,
                "edge_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": ["prenominal_adjective"],
                "sem_alg_fxns_used": ["create_base_SEMENT", "op_non_scopal_argument_hook"]
            }
        )

        mock_graph_eval = mocker.MagicMock()
        mock_graph_eval.configure_mock(
            **{
                "graph": graph,
                "graph_name": "graph",
                "node_evaluations": {"node": mock_node_eval},
                "edge_evaluations": [mock_edge_eval],
                "node_count": 2,
                "nodes_covered": 2,
                "nodes_included": 2,
                "node_coverage": 1.0,
                "node_inclusion": 1.0,
                "edge_count": 1,
                "edges_covered": 1,
                "edges_included": 1,
                "edge_coverage": 1.0,
                "edge_inclusion": 1.0,
                "generated_SEMENT": sementcodecs.decode("[ TOP: h718\n  INDEX: x717\n  RELS: < [ _silver_a_1 LBL: h721 ARG0: i719 ARG1: i720 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] >\n  EQS: < h721 eq h718 i720 eq x717 > ]"),
                "generated_SEMENT_string": "[ TOP: h718\n  INDEX: x717\n  RELS: < [ _silver_a_1 LBL: h721 ARG0: i719 ARG1: i720 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] >\n  EQS: < h721 eq h718 i720 eq x717 > ]",
                "collapsed_SEMENT": sementcodecs.decode("[ TOP: h718\n  INDEX: x717\n  RELS: < [ _silver_a_1 LBL: h718 ARG0: i719 ARG1: x717 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] > ]"),
                "collapsed_SEMENT_string": "[ TOP: h718\n  INDEX: x717\n  RELS: < [ _silver_a_1 LBL: h718 ARG0: i719 ARG1: x717 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] > ]",
                "prepped_SEMENT": sementcodecs.decode("[ TOP: h730\n  INDEX: e727\n  RELS: < [ unknown LBL: h726 ARG: x717 ARG0: e727 ]\n          [ def_udef_a_q LBL: h725 ARG0: x717 RSTR: h723 BODY: h724 ]\n          [ _silver_a_1 LBL: h718 ARG0: i719 ARG1: x717 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] >\n  HCONS: < h723 qeq h718 h730 qeq h726 > ]"),
                "prepped_SEMENT_string": "[ TOP: h730\n  INDEX: e727\n  RELS: < [ unknown LBL: h726 ARG: x717 ARG0: e727 ]\n          [ def_udef_a_q LBL: h725 ARG0: x717 RSTR: h723 BODY: h724 ]\n          [ _silver_a_1 LBL: h718 ARG0: i719 ARG1: x717 ]\n          [ _horse_n_1 LBL: h718 ARG0: x717 ] >\n  HCONS: < h723 qeq h718 h730 qeq h726 > ]",
                "generated_results": [
                    "A silver horse",
                    "A silver horse.",
                    "Silver horse",
                    "Silver horse.",
                    "Silver horses",
                    "Silver horses.",
                    "The silver horse",
                    "The silver horse.",
                    "The silver horses",
                    "The silver horses."
                ]
            }
        )

        g_attr = ["graph", "graph_name", "node_evaluations", "edge_evaluations", "node_evaluations",
                "node_count", "nodes_covered", "nodes_included", "node_coverage", "node_inclusion",
                "edge_count", "edges_covered", "edges_included", "edge_coverage", "edge_inclusion",
                "generated_SEMENT", "generated_SEMENT_string", "collapsed_SEMENT", "collapsed_SEMENT_string",
                "prepped_SEMENT", "prepped_SEMENT_string", "generated_results"]

        n_attr = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                  "node_covered", "node_included", "generation_comment", "sem_comp_fxns_used"]

        e_attr = ["edge_name", "edge_props", "generated_SEMENT", "generated_SEMENT_string",
                  "edge_covered", "edge_included", "generation_comment", "inclusion_comment", "sem_comp_fxns_used"]

        return graph, "graph", evaluation_directory_sample_dir, mock_graph_eval, g_attr, n_attr, e_attr

    @staticmethod
    def case_eval_file_w_no_sements(evaluation_test_dir, mocker):
        evaluation_directory_sample_dir = os.path.join(evaluation_test_dir, "eval_dir_no_sements")
        graph = nx.nx_pydot.read_dot(os.path.join(evaluation_directory_sample_dir, "graph.dot"))

        # mock node eval
        mock_node_eval = mocker.MagicMock()
        mock_node_eval.configure_mock(
            **{
                "node_name": "node",
                "node_props": {"lexicon_key": "node"},
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "node_covered": True,
                "node_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": {"noun": 1},
                "sem_alg_fxns_used": {"create_base_SEMENT": 1}
            }
        )

        # mock edge eval
        mock_edge_eval = mocker.MagicMock()
        mock_edge_eval.configure_mock(
            **{
                "edge_name": "edge",
                "edge_props": {"prop": "val"},
                "parent_node_name": "parent",
                "child_node_name": "child",
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "edge_covered": True,
                "edge_included": True,
                "generation_comment": "me when i'm a comment",
                "inclusion_comment": "me when i'm also a comment",
                "sem_comp_fxns_used": {"prenominal_adjective": 1},
                "sem_alg_fxns_used": {"create_base_SEMENT": 2, "op_non_scopal_argument_hook": 1}
            }
        )

        mock_graph_eval = mocker.MagicMock()
        mock_graph_eval.configure_mock(
            **{
                "graph": graph,
                "graph_name": "graph",
                "node_evaluations": {"node": mock_node_eval},
                "edge_evaluations": [mock_edge_eval],
                "node_count": 2,
                "nodes_covered": 2,
                "nodes_included": 2,
                "node_coverage": 1.0,
                "node_inclusion": 1.0,
                "edge_count": 1,
                "edges_covered": 1,
                "edges_included": 1,
                "edge_coverage": 1.0,
                "edge_inclusion": 1.0,
                "generated_SEMENT": None,
                "generated_SEMENT_string": None,
                "collapsed_SEMENT": None,
                "collapsed_SEMENT_string": None,
                "prepped_SEMENT": None,
                "prepped_SEMENT_string": None,
                "generated_results": [
                    "A silver horse",
                    "A silver horse.",
                    "Silver horse",
                    "Silver horse.",
                    "Silver horses",
                    "Silver horses.",
                    "The silver horse",
                    "The silver horse.",
                    "The silver horses",
                    "The silver horses."
                ]
            }
        )

        g_attr = ["graph", "graph_name", "node_evaluations", "edge_evaluations", "node_evaluations",
                  "node_count", "nodes_covered", "nodes_included", "node_coverage", "node_inclusion",
                  "edge_count", "edges_covered", "edges_included", "edge_coverage", "edge_inclusion",
                  "generated_SEMENT", "generated_SEMENT_string", "collapsed_SEMENT", "collapsed_SEMENT_string",
                  "prepped_SEMENT", "prepped_SEMENT_string", "generated_results"]

        n_attr = ["node_name", "node_props", "generated_SEMENT", "generated_SEMENT_string",
                  "node_covered", "node_included", "generation_comment", "sem_alg_fxns_used", "sem_comp_fxns_used"]

        e_attr = ["edge_name", "edge_props", "generated_SEMENT", "generated_SEMENT_string",
                  "edge_covered", "edge_included", "generation_comment", "inclusion_comment", "sem_alg_fxns_used", "sem_comp_fxns_used"]

        return graph, "graph", evaluation_directory_sample_dir, mock_graph_eval, g_attr, n_attr, e_attr

class POGGGraphEvaluationGetDictRepresentation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGGraphEvaluation.get_top_level_dict_representation

    GENERAL DESCRIPTION OF TEST CASES:
        Return POGGGraphEvaluation object and gold dict representation
    """

    """
    SUCCESS CASES
        1. generic POGGNodeEvaluation object 
    """

    @staticmethod
    def case_basic_graph():
        graph = nx.DiGraph()

        graph_eval_obj = POGGGraphEvaluation(graph, "graph")
        # set some values
        graph_eval_obj.generated_SEMENT_string = "fake SEMENT string"
        graph_eval_obj.collapsed_SEMENT_string = "fake SEMENT string"
        graph_eval_obj.prepped_SEMENT_string = "fake SEMENT string"
        graph_eval_obj.node_count = 5
        graph_eval_obj.nodes_covered = 4
        graph_eval_obj.nodes_included = 3
        graph_eval_obj.node_coverage = 0.8
        graph_eval_obj.node_inclusion = 0.6
        graph_eval_obj.edge_count = 4
        graph_eval_obj.edges_covered = 4
        graph_eval_obj.edges_included = 3
        graph_eval_obj.edge_coverage = 1.0
        graph_eval_obj.edge_inclusion = 0.75
        graph_eval_obj.gold_outputs = ["me", "when"]
        graph_eval_obj.generated_results = ["me", "myself", "i"]
        graph_eval_obj.generated_gold_outputs = ["me"]
        graph_eval_obj.gold_output_generation_coverage = 0.5
        graph_eval_obj.sem_alg_fxns_used = {"fxn": 1}
        graph_eval_obj.sem_comp_fxns_used = {"fxn": 1}

        gold_dict = {
            'graph_name': "graph",
            'sem_alg_fxns_used': {"fxn": 1},
            'sem_comp_fxns_used': {"fxn": 1},
            'node_count': 5,
            'nodes_covered': 4,
            'nodes_included': 3,
            'node_coverage': 0.8,
            'node_inclusion': 0.6,
            'edge_count': 4,
            'edges_covered': 4,
            'edges_included': 3,
            'edge_coverage': 1.0,
            'edge_inclusion': 0.75,
            'gold_outputs': ["me", "when"],
            'generated_gold_outputs': ["me"],
            'gold_output_generation_coverage': 0.5,
            'generation_comment': None,
            'generated_SEMENT_string': "fake SEMENT string",
            'collapsed_SEMENT_string': "fake SEMENT string",
            'prepped_SEMENT_string': "fake SEMENT string",
            'generated_results': ["i", "me", "myself"]
        }

        return graph_eval_obj, gold_dict

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

        Each case returns:
        - root
        - initial_ancestor_inclusion
        - graph_eval
        - gold_node_inclusions
        - gold_edge_inclusions
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
        2. rootless graph, cov/incl should all be false bu we have to test that it works
        3. cyclical graph, cov/incl should all be false but we have to test that it works 
       The following cases are meant to cover the different edge cases that arise from different values passed in for the "root" and "ancestor_incl" parameters:
       4. root=None, ancestor_incl=None
       5. root=None, ancestor_incl=False
       6. root=None, ancestor_incl=True
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
    def case_rootless_graph(rootless_graph_eval_obj):
        gold_node_inclusions = {
            "node1": False,
            "node2": False
        }
        gold_edge_inclusions = {}
        return None, None, rootless_graph_eval_obj, gold_node_inclusions, gold_edge_inclusions

    @staticmethod
    def case_cyclical_graph(cyclical_graph_eval_obj):
        gold_node_inclusions = {
            "root": False
        }

        gold_edge_inclusions = {
            "edge": {"parent": "root", "child": "root", "inclusion": False}
        }
        return None, None, cyclical_graph_eval_obj, gold_node_inclusions, gold_edge_inclusions

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
        2. graph with no edges (to catch ZeroDivisionError)
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
            "edge_inclusion": 0.25,
            "gold_output_generation_coverage": 0.5
        }

        return all_branches_graph_eval_obj, gold_metrics

    @staticmethod
    def case_no_edges(it_is_just_one_little_nodie_eval_obj):
        gold_metrics = {
            "node_count": 1,
            "edge_count": 0,
            "nodes_covered": 0,
            "nodes_included": 0,
            "node_coverage": 0,
            "node_inclusion": 0,
            "edges_covered": 0,
            "edges_included": 0,
            "edge_coverage": 0,
            "edge_inclusion": 0
        }
        return it_is_just_one_little_nodie_eval_obj, gold_metrics

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
        2. read from a directory
        
    FAILURE CASES
        1. no dataset name given 
        2. eval_metadata.json file not found
        3. dataset_eval.json file not found
    """

    @staticmethod
    @case(tags="success")
    def case_eval_init(evaluation_test_dir, mocker):
        mock_eval = mocker.MagicMock()
        mock_eval.configure_mock(
            **{
                "dataset_name": "dataset",
                "graph_count": None,
                "graph_SEMENT_count": None,
                "graph_SEMENT_coverage": None,
                "graphs_with_text_count": None,
                "graphs_with_text_coverage": None,
                "graphs_with_gold_text_count": None,
                "graphs_with_gold_text_coverage": None,
                "graphs_with_complete_gold_text_count": None,
                "graphs_with_complete_gold_text_coverage": None,
                "full_node_count": None,
                "full_nodes_covered": None,
                "full_nodes_included": None,
                "full_node_coverage": None,
                "full_node_inclusion": None,
                "full_edge_count": None,
                "full_edges_covered": None,
                "full_edges_included": None,
                "full_edge_coverage": None,
                "full_edge_inclusion": None,
                "sem_alg_fxns_available": set(),
                "sem_comp_fxns_available": set(),
                "sem_alg_fxns_used": {},
                "sem_comp_fxns_used": {},
                "sem_comp_fxns_used_count": None,
                "sem_comp_fxns_used_coverage": None,
                "sem_alg_fxns_used_count": None,
                "sem_alg_fxns_used_coverage": None,

            }
        )

        attr = ["dataset_name", "graph_count", "graph_SEMENT_count", "graph_SEMENT_coverage",
                "graphs_with_text_count", "graphs_with_text_coverage", "full_node_count",
                "full_nodes_covered", "full_nodes_included", "full_node_coverage",
                "full_node_inclusion", "full_edge_count", "full_edges_covered",
                "full_edges_included", "full_edge_coverage", "full_edge_inclusion",
                "graphs_with_gold_text_count", "graphs_with_gold_text_coverage",
                "graphs_with_complete_gold_text_count", "graphs_with_complete_gold_text_coverage",
                "sem_comp_fxns_used_count", "sem_comp_fxns_used_coverage",
                "sem_alg_fxns_available", "sem_comp_fxns_available", "sem_comp_fxns_used",
                "sem_alg_fxns_used", "sem_alg_fxns_used_count", "sem_alg_fxns_used_coverage"]

        return "dataset", None, mock_eval, attr

    @staticmethod
    @case(tags="success")
    def case_eval_from_directory(evaluation_test_dir, mocker):
        eval_sample_directory = os.path.join(evaluation_test_dir, "eval_dir")

        mock_eval = mocker.MagicMock()
        mock_eval.configure_mock(
            **{
                "dataset_name": "dataset",
                "run_id": "00000",
                "run_complete": True,
                "sem_alg_fxns_available": {"fxn0"},
                "sem_comp_fxns_available": {"fxn1", "fxn2"},
                "sem_comp_fxns_used": {"fxn1": 1},
                "sem_alg_fxns_used": {"fxn0": 1},
                "graph_count": 10,
                "graph_SEMENT_count": 10,
                "graph_SEMENT_coverage": 1.0,
                "graphs_with_text_count": 8,
                "graphs_with_text_coverage": 0.8,
                "graphs_with_gold_text_count": 7,
                "graphs_with_gold_text_coverage": 0.7,
                "graphs_with_complete_gold_text_count": 6,
                "graphs_with_complete_gold_text_coverage": 0.6,
                "full_node_count": 100,
                "full_nodes_covered": 90,
                "full_nodes_included": 80,
                "full_node_coverage": 0.9,
                "full_node_inclusion": 0.8,
                "full_edge_count": 100,
                "full_edges_covered": 90,
                "full_edges_included": 80,
                "full_edge_coverage": 0.9,
                "full_edge_inclusion": 0.8,
                "sem_comp_fxns_used_count": 1,
                "sem_comp_fxns_used_coverage": 0.5,
                "sem_alg_fxns_used_count": 1,
                "sem_alg_fxns_used_coverage": 1.0,
            }
        )

        attr = ["dataset_name", "graph_count", "graph_SEMENT_count", "graph_SEMENT_coverage",
                "graphs_with_text_count", "graphs_with_text_coverage", "full_node_count",
                "full_nodes_covered", "full_nodes_included", "full_node_coverage",
                "full_node_inclusion", "full_edge_count", "full_edges_covered",
                "full_edges_included", "full_edge_coverage", "full_edge_inclusion",
                "graphs_with_gold_text_count", "graphs_with_gold_text_coverage",
                "graphs_with_complete_gold_text_count", "graphs_with_complete_gold_text_coverage",
                "sem_comp_fxns_used_count", "sem_comp_fxns_used_coverage",
                "sem_alg_fxns_available", "sem_comp_fxns_available", "sem_comp_fxns_used",
                "sem_alg_fxns_used", "sem_alg_fxns_used_count", "sem_alg_fxns_used_coverage"]

        return "dataset", eval_sample_directory, mock_eval, attr

    @staticmethod
    @case(tags="failure")
    def case_no_name_given(evaluation_test_dir):
        return None, None

    @staticmethod
    @case(tags="no_files")
    def case_no_metadata_file(evaluation_test_dir):
        return "dataset", evaluation_test_dir

    @staticmethod
    @case(tags="no_files")
    def case_no_dataset_file(evaluation_test_dir):
        return "dataset", os.path.join(evaluation_test_dir, "metadata_file_only")

class POGGEvaluationGetDictRepresentation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEvaluation.get_top_level_dict_representation

    GENERAL DESCRIPTION OF TEST CASES:
        Return POGGEvaluation object and gold dict representation
    """

    """
    SUCCESS CASES
        1. generic POGGNodeEvaluation object 
    """

    @staticmethod
    def case_basic_graph():
        graph = nx.DiGraph()

        eval_obj = POGGEvaluation("dataset")
        # set some values
        eval_obj.graph_count = 10
        eval_obj.graph_SEMENT_count = 10
        eval_obj.graph_SEMENT_coverage = 1.0
        eval_obj.graphs_with_text_count = 9
        eval_obj.graphs_with_text_coverage = 0.9
        eval_obj.graphs_with_gold_text_count = 8
        eval_obj.graphs_with_gold_text_coverage = 0.8
        eval_obj.graphs_with_complete_gold_text_count = 7
        eval_obj.graphs_with_complete_gold_text_coverage = 0.7
        eval_obj.sem_alg_fxns_available = {"fxn0"}
        eval_obj.sem_alg_fxns_used = {"fxn0": 1}
        eval_obj.sem_comp_fxns_available = {"fxn1", "fxn2"}
        eval_obj.sem_comp_fxns_used = {"fxn1": 1}
        eval_obj.sem_comp_fxns_used_count = 1
        eval_obj.sem_comp_fxns_used_coverage = 0.5
        eval_obj.sem_alg_fxns_used_coverage = 1.0
        eval_obj.full_node_count = 100
        eval_obj.full_nodes_covered = 90
        eval_obj.full_nodes_included = 80
        eval_obj.full_node_coverage = 0.9
        eval_obj.full_node_inclusion = 0.8
        eval_obj.full_edge_count = 100
        eval_obj.full_edges_covered = 90
        eval_obj.full_edges_included = 80
        eval_obj.full_edge_coverage = 0.9
        eval_obj.full_edge_inclusion = 0.8

        gold_dict = {
            'graph_count': 10,
            'graph_SEMENT_count': 10,
            'graph_SEMENT_coverage': 1.0,
            'graphs_with_text_count': 9,
            'graphs_with_text_coverage': 0.9,
            'graphs_with_gold_text_count': 8,
            'graphs_with_gold_text_coverage': 0.8,
            'graphs_with_complete_gold_text_count': 7,
            'graphs_with_complete_gold_text_coverage': 0.7,
            'sem_alg_fxns_available': ["fxn0"],
            'sem_alg_fxns_used': {"fxn0": 1},
            'sem_comp_fxns_available': ["fxn1", "fxn2"],
            'sem_comp_fxns_used': {"fxn1": 1},
            'sem_comp_fxns_used_count': 1,
            'sem_comp_fxns_used_coverage': 0.5,
            'sem_alg_fxns_used_count': 1,
            'sem_alg_fxns_used_coverage': 1.0,
            'full_node_count': 100,
            'full_nodes_covered': 90,
            'full_nodes_included': 80,
            'full_node_coverage': 0.9,
            'full_node_inclusion': 0.8,
            'full_edge_count': 100,
            'full_edges_covered': 90,
            'full_edges_included': 80,
            'full_edge_coverage': 0.9,
            'full_edge_inclusion': 0.8
        }

        return eval_obj, gold_dict

class GetGraphEvaluation:
    """
    FUNCTIONS BEING TESTED:
        - pogg.evaluation.evaluation.POGGEvaluation.get_graph_evaluation

    GENERAL DESCRIPTION OF TEST CASES:
        Provide an evaluation object and the name of a graph to retrieve the graph evaluation for.
        Test should ensure the retrieved object matches the "gold" (which is just a random string for testing).
    """

    """
    SUCCESS CASES
        1. existing graph named "graph"

    FAILURE CASES:
        1. nonexistent graph
    """

    @staticmethod
    @case(tags="success")
    def case_graph():
        eval_obj = POGGEvaluation("dataset")
        eval_obj.graph_evaluations['graph'] = "test"
        return eval_obj, "graph", "test"

    @staticmethod
    @case(tags="failure")
    def case_fake_graph():
        eval_obj = POGGEvaluation("dataset")
        return eval_obj, "fake_graph"

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
        2. eval object with preset values for count-based metrics, with edge count at 0 to catch ZeroDivisionError
    """

    @staticmethod
    def case_eval_obj(dummy_graph_eval_1, dummy_graph_eval_2, dummy_graph_eval_3):
        pogg_eval = POGGEvaluation("dataset")

        # add dummy graph_eval objects directly
        pogg_eval.graph_evaluations['dummy_graph_eval_1'] = dummy_graph_eval_1
        pogg_eval.graph_evaluations['dummy_graph_eval_2'] = dummy_graph_eval_2
        pogg_eval.graph_evaluations['dummy_graph_eval_3'] = dummy_graph_eval_3

        gold_metrics = {
            "graph_count": 3,
            "graph_SEMENT_count": 2,
            "graphs_with_text_count": 2,
            "graphs_with_text_coverage": 2 / 3,
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

    @staticmethod
    def case_no_edges(dummy_graph_eval_no_edges):
        pogg_eval = POGGEvaluation("dataset")

        # add dummy graph_eval objects directly
        pogg_eval.graph_evaluations['dummy_graph_eval_no_edges'] = dummy_graph_eval_no_edges

        gold_metrics = {
            "graph_count": 1,
            "graph_SEMENT_count": 1,
            "graphs_with_text_count": 1,
            "graphs_with_text_coverage": 1,
            "full_node_count": 1,
            "full_nodes_covered": 1,
            "full_nodes_included": 1,
            "full_node_coverage": 1,
            "full_node_inclusion": 1,
            "full_edge_count": 0,
            "full_edges_covered": 0,
            "full_edges_included": 0,
            "full_edge_coverage": 0,
            "full_edge_inclusion": 0
        }

        return pogg_eval, gold_metrics
