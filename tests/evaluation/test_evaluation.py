import re
import networkx as nx
import pytest
from pytest_cases import parametrize_with_cases

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_evaluation_cases import *


class TestPOGGNodeEvaluation:
    """
    Tests the POGGNodeEvaluation class
    """

    @staticmethod
    @parametrize_with_cases("node_name, node_props, gold_node_eval, attributes", cases=POGGNodeEvaluationInit)
    def test_init(node_name, node_props, gold_node_eval, attributes):
        test_node_eval = POGGNodeEvaluation(node_name, node_props)
        for attr in attributes:
            assert getattr(test_node_eval, attr) == getattr(gold_node_eval, attr)

    @staticmethod
    @parametrize_with_cases("sement, sement_string", cases=SetSement)
    def test_set_SEMENT(sement, sement_string):
        test_node_eval = POGGNodeEvaluation("name", {})
        test_node_eval.set_SEMENT(sement)

        assert test_node_eval.generated_SEMENT == sement
        assert test_node_eval.generated_SEMENT_string == sement_string


class TestPOGGEdgeEvaluation:
    """
    Tests the POGGEdgeEvaluation class
    """

    @staticmethod
    @parametrize_with_cases("edge_name, edge_props, parent_name, child_name, gold_edge_eval, attributes", cases=POGGEdgeEvaluationInit)
    def test_init(edge_name, edge_props, parent_name, child_name, gold_edge_eval, attributes):
        test_edge_eval = POGGEdgeEvaluation(edge_name, edge_props, parent_name, child_name)
        for attr in attributes:
            assert getattr(test_edge_eval, attr) == getattr(gold_edge_eval, attr)

    @staticmethod
    @parametrize_with_cases("sement, sement_string", cases=SetSement)
    def test_set_SEMENT(sement, sement_string):
        test_node_eval = POGGEdgeEvaluation("name", {}, "parent", "child")
        test_node_eval.set_SEMENT(sement)

        assert test_node_eval.generated_SEMENT == sement
        assert test_node_eval.generated_SEMENT_string == sement_string


class TestPOGGGraphEvaluation:
    """
    Tests the POGGGraphEvaluation class
    """

    @staticmethod
    @parametrize_with_cases("graph, graph_name, gold_graph_eval, attributes", cases=POGGGraphEvaluationInit)
    def test_init(graph, graph_name, gold_graph_eval, attributes):
        test_graph_eval = POGGGraphEvaluation(graph, graph_name)
        for attr in attributes:
            assert getattr(test_graph_eval, attr) == getattr(gold_graph_eval, attr)

    @staticmethod
    @parametrize_with_cases("graph_eval, gold_node_evaluations, attrs", cases=CreateNodeEvaluations)
    def test_create_node_evaluations(graph_eval, gold_node_evaluations, attrs):
        graph_eval.create_node_evaluations()

        # assert length of node_evaluations is the same as gold
        assert len(graph_eval.node_evaluations.keys()) == len(gold_node_evaluations.keys())

        # assert for each node_eval object that the attributes match
        for key in graph_eval.node_evaluations.keys():
            for attr in attrs:
                assert getattr(graph_eval.node_evaluations[key], attr) == getattr(gold_node_evaluations[key], attr)

    @staticmethod
    @parametrize_with_cases("graph_eval, gold_edge_evaluations, attrs", cases=CreateEdgeEvaluations)
    def test_create_edge_evaluations(graph_eval, gold_edge_evaluations, attrs):
        graph_eval.create_edge_evaluations()

        # assert length of node_evaluations is the same as gold
        assert len(graph_eval.edge_evaluations) == len(gold_edge_evaluations)

        # assert for each node_eval object that the attributes match
        for i in range(len(graph_eval.edge_evaluations)):
            for attr in attrs:
                assert getattr(graph_eval.edge_evaluations[i], attr) == getattr(gold_edge_evaluations[i], attr)

    @staticmethod
    @parametrize_with_cases("sement, sement_string", cases=SetSement)
    def test_set_SEMENT(sement, sement_string):
        test_graph_eval = POGGGraphEvaluation(nx.DiGraph(), "name")
        test_graph_eval.set_SEMENT(sement)

        assert test_graph_eval.generated_SEMENT == sement
        assert test_graph_eval.generated_SEMENT_string == sement_string

    @staticmethod
    @parametrize_with_cases("sement, sement_string", cases=SetSement)
    def test_set_wrapped_SEMENT(sement, sement_string):
        test_graph_eval = POGGGraphEvaluation(nx.DiGraph(), "name")
        test_graph_eval.set_wrapped_SEMENT(sement)

        assert test_graph_eval.wrapped_SEMENT == sement
        assert test_graph_eval.wrapped_SEMENT_string == sement_string

    @staticmethod
    @parametrize_with_cases("sement, sement_string", cases=SetSement)
    def test_set_collapsed_SEMENT(sement, sement_string):
        test_graph_eval = POGGGraphEvaluation(nx.DiGraph(), "name")
        test_graph_eval.set_collapsed_SEMENT(sement)

        assert test_graph_eval.collapsed_SEMENT == sement
        assert test_graph_eval.collapsed_SEMENT_string == sement_string

    @staticmethod
    @parametrize_with_cases("graph_eval, node_name", cases=GetNodeEvaluation, has_tag="success")
    def test_get_node_evaluation(graph_eval, node_name):
        node_eval = graph_eval.get_node_evaluation(node_name)
        assert node_eval.node_name == node_name

    @staticmethod
    @parametrize_with_cases("graph_eval, node_name", cases=GetNodeEvaluation, has_tag="failure")
    def test_get_node_evaluation_failure(graph_eval, node_name):
        with pytest.raises(KeyError):
            graph_eval.get_node_evaluation(node_name)

    @staticmethod
    @parametrize_with_cases("graph_eval, edge_parent, edge_child, edge_data", cases=GetEdgeEvaluation, has_tag="success")
    def test_get_edge_evaluation(graph_eval, edge_parent, edge_child, edge_data):
        edge_eval = graph_eval.get_edge_evaluation(edge_parent, edge_child, edge_data)
        assert edge_eval.parent_node_name == edge_parent
        assert edge_eval.child_node_name == edge_child
        assert edge_eval.edge_name == edge_data['label']

    @staticmethod
    @parametrize_with_cases("graph_eval, edge_parent, edge_child, edge_data", cases=GetEdgeEvaluation, has_tag="failure")
    def test_get_edge_evaluation_failure(graph_eval, edge_parent, edge_child, edge_data):
        with pytest.raises(KeyError):
            graph_eval.get_edge_evaluation(edge_parent, edge_child, edge_data)

    @staticmethod
    @parametrize_with_cases("root, initial_ancestor_inclusion, graph_eval, gold_node_inclusions, gold_edge_inclusions", cases=DetermineInclusion)
    def test_determine_inclusion(root, initial_ancestor_inclusion, graph_eval, gold_node_inclusions, gold_edge_inclusions):
        # make sure all inclusions are False before calling function
        for node_eval_key in graph_eval.node_evaluations.keys():
            assert not graph_eval.node_evaluations[node_eval_key].node_included
        for edge_eval in graph_eval.edge_evaluations:
            assert not edge_eval.edge_included

        # run determine_inclusion
        graph_eval.determine_inclusion(root, initial_ancestor_inclusion)

        # make sure updated node_inclusions match gold_node_inclusions
        for node_eval_key in graph_eval.node_evaluations.keys():
            assert graph_eval.node_evaluations[node_eval_key].node_included == gold_node_inclusions[node_eval_key]

        # make sure updated edge_inclusions match gold_edge_inclusions
        for edge_eval in graph_eval.edge_evaluations:
            gold_edge_inclusion = gold_edge_inclusions[edge_eval.edge_name]
            assert edge_eval.edge_included == gold_edge_inclusion["inclusion"]

    @staticmethod
    @parametrize_with_cases("graph_eval, gold_metrics", cases=CalculateGraphMetrics)
    def test_calculate_metrics(graph_eval, gold_metrics):
        # make sure all metrics are None before calling
        for key in gold_metrics.keys():
            assert getattr(graph_eval, key) is None

        graph_eval.calculate_metrics()

        for key in gold_metrics.keys():
            assert getattr(graph_eval, key) == gold_metrics[key]

    @staticmethod
    @parametrize_with_cases("graph_eval", cases=MarkAllUncovered)
    def test_mark_all_uncovered(graph_eval):
        graph_eval.mark_all_uncovered()

        for node_eval_key in graph_eval.node_evaluations.keys():
            assert not graph_eval.node_evaluations[node_eval_key].node_covered
            assert not graph_eval.node_evaluations[node_eval_key].node_included

        for edge_eval in graph_eval.edge_evaluations:
            assert not edge_eval.edge_covered
            assert not edge_eval.edge_included


class TestPOGGEvaluation:
    @staticmethod
    @parametrize_with_cases("dataset_name, gold_pogg_eval, attributes", cases=POGGEvaluationInit)
    def test_init(dataset_name, gold_pogg_eval, attributes):
        test_pogg_eval = POGGEvaluation(dataset_name)
        for attr in attributes:
            assert getattr(test_pogg_eval, attr) == getattr(gold_pogg_eval, attr)


    @staticmethod
    @parametrize_with_cases("graph, graph_name", cases=AddGraph)
    def test_add_graph(graph, graph_name):
        test_pogg_eval = POGGEvaluation("dataset")
        test_pogg_eval.add_graph(graph, graph_name)

        assert len(test_pogg_eval.graph_evaluations) == 1
        assert test_pogg_eval.graph_evaluations[0].graph == graph
        assert test_pogg_eval.graph_evaluations[0].graph_name == graph_name


    @staticmethod
    @parametrize_with_cases("pogg_eval, gold_metrics", cases=CalculateDatasetMetrics)
    def test_calculate_metrics(pogg_eval, gold_metrics):
        # make sure all metrics are None before calling
        for key in gold_metrics.keys():
            assert getattr(pogg_eval, key) is None

        pogg_eval.calculate_metrics()

        for key in gold_metrics.keys():
            assert getattr(pogg_eval, key) == gold_metrics[key]