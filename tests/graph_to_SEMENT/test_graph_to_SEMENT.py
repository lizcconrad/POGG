import pytest
from pytest_cases import parametrize_with_cases

# just assume POGGSEMENTUtil works...
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_graph_to_SEMENT_cases import *


class TestPOGGGraphConverter:
    """
    Tests POGGGraphConverter class
    """
    @staticmethod
    @parametrize_with_cases("comp_fxn, parameters, gold_sement", cases=GetSement, has_tag="success")
    def test_get_sement(comp_fxn, parameters, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.get_SEMENT(comp_fxn, parameters)

        # build failure string in case assertion fails
        failure_msg = POGGSEMENTUtil.build_isomorphism_report(gold_sement, result_sement)

        assert POGGSEMENTUtil.is_sement_isomorphic(result_sement, gold_sement), failure_msg


    @staticmethod
    @parametrize_with_cases("comp_fxn, parameters", cases=GetSement, has_tag="failure")
    def test_get_sement_failure(comp_fxn, parameters, pogg_graph_converter):
        with pytest.raises(KeyError):
            pogg_graph_converter.get_SEMENT(comp_fxn, parameters)




    @staticmethod
    @parametrize_with_cases("node, evaluation, gold_sement", cases=ConvertNodeToSement, has_tag="success")
    def test_convert_node_to_sement(node, evaluation, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.convert_node_to_SEMENT(node, evaluation)

        # build failure string in case assertion fails
        failure_msg = POGGSEMENTUtil.build_isomorphism_report(gold_sement, result_sement)

        assert POGGSEMENTUtil.is_sement_isomorphic(result_sement, gold_sement), failure_msg


    @staticmethod
    @parametrize_with_cases("node, evaluation, gold_sement", cases=ConvertNodeToSement, has_tag=["success", "eval"])
    def test_convert_node_to_sement_evaluation_object(node, evaluation, gold_sement, pogg_graph_converter, mocker):
        spy = mocker.spy(evaluation, 'set_SEMENT')
        result_sement = pogg_graph_converter.convert_node_to_SEMENT(node, evaluation)

        # (1) node_covered = True
        assert evaluation.node_covered

        # (2) generation_comment is not None
        assert evaluation.generation_comment is None

        # (3) check that set_SEMENT was called
        spy.assert_called_once_with(result_sement)


    @staticmethod
    @parametrize_with_cases("node, evaluation", cases=ConvertNodeToSement, has_tag="failure")
    def test_convert_node_to_sement_bad_lexicon_key(node, evaluation, pogg_graph_converter):
        result = pogg_graph_converter.convert_node_to_SEMENT(node, evaluation)

        # failure does NOT raise an error, because conversion should continue even if a node fails
        # so instead test that the markers of failure are present

        # (1) returns None
        assert result is None

    @staticmethod
    @parametrize_with_cases("node, evaluation, gold_failure_comment", cases=ConvertNodeToSement, has_tag=["failure", "eval"])
    def test_convert_node_to_sement_bad_lexicon_key_evaluation_object(node, evaluation, gold_failure_comment, pogg_graph_converter):
        result = pogg_graph_converter.convert_node_to_SEMENT(node, evaluation)

        # failure does NOT raise an error, because conversion should continue even if a node fails
        # so instead test that the markers of failure are present

        # (1) returns None
        assert result is None

        # (2) node_covered == False
        assert evaluation.node_covered is False

        # (4) generation_comment != None
        assert evaluation.generation_comment == gold_failure_comment


    @staticmethod
    @parametrize_with_cases("edge, parent, child, evaluation, gold_sement", cases=ConvertEdgeToSement, has_tag="success")
    def test_convert_edge_to_sement(edge, parent, child, evaluation, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.convert_edge_to_SEMENT(edge, parent, child, evaluation)

        # build failure string in case assertion fails
        failure_msg = POGGSEMENTUtil.build_isomorphism_report(gold_sement, result_sement)

        assert POGGSEMENTUtil.is_sement_isomorphic(result_sement, gold_sement), failure_msg


    @staticmethod
    @parametrize_with_cases("edge, parent, child, evaluation, gold_sement", cases=ConvertEdgeToSement, has_tag=["success", "eval"])
    def test_convert_edge_to_sement_evaluation_object(edge, parent, child, evaluation, gold_sement, pogg_graph_converter, mocker):
        spy = mocker.spy(evaluation, 'set_SEMENT')
        result_sement = pogg_graph_converter.convert_edge_to_SEMENT(edge, parent, child, evaluation)

        # (1) node_covered = True
        assert evaluation.edge_covered

        # (2) generation_comment is not None
        assert evaluation.generation_comment is None

        # (3) check that set_SEMENT was called
        spy.assert_called_once_with(result_sement)


    @staticmethod
    @parametrize_with_cases("edge, parent, child, evaluation, gold_sement", cases=ConvertEdgeToSement, has_tag="failure")
    def test_convert_edge_to_sement_missing_nodes(edge, parent, child, evaluation, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.convert_edge_to_SEMENT(edge, parent, child, evaluation)

        # failure does NOT raise an error, because conversion should continue even if a node fails
        # so instead test that the markers of failure are present

        # (1) if parent is missing, result is None, otherwise result is the parent SEMENT
        # "gold_sement" argument for each test case reflects this, so confirm result matches the gold_sement
        assert result_sement == gold_sement


    @staticmethod
    @parametrize_with_cases("edge, parent, child, evaluation, gold_sement", cases=ConvertEdgeToSement,
                            has_tag=["failure", "eval"])
    def test_convert_edge_to_sement_missing_nodes_evaluation_object(edge, parent, child, evaluation, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.convert_edge_to_SEMENT(edge, parent, child, evaluation)

        # failure does NOT raise an error, because conversion should continue even if a node fails
        # so instead test that the markers of failure are present

        # (1) if parent is missing, result is None, otherwise result is the parent SEMENT
        # "gold_sement" argument for each test case reflects this, so confirm result matches the gold_sement
        assert result_sement == gold_sement

        # (2) node_covered == False
        assert evaluation.edge_covered is False

        # (4) generation_comment != None
        assert evaluation.generation_comment is not None


    @staticmethod
    @parametrize_with_cases("root, graph, evaluation, gold_sement", cases=ConvertGraphToSement, has_tag="success")
    def test_convert_graph_to_SEMENT(root, graph, evaluation, gold_sement, pogg_graph_converter):
        result_sement = pogg_graph_converter.convert_graph_to_SEMENT(graph, evaluation, root)

        # build failure string in case assertion fails
        failure_msg = POGGSEMENTUtil.build_isomorphism_report(gold_sement, result_sement)

        assert POGGSEMENTUtil.is_sement_isomorphic(result_sement, gold_sement), failure_msg


    @staticmethod
    @parametrize_with_cases("graph, evaluation, gold_gen_comment", cases=ConvertGraphToSement, has_tag="failure")
    def test_convert_graph_to_SEMENT_no_SEMENT_returned(graph, evaluation, gold_gen_comment, pogg_graph_converter):
        result = pogg_graph_converter.convert_graph_to_SEMENT(graph, evaluation)
        assert result is None
        # doing this as an if, i don't want to write another test just for the coverage idc
        if evaluation is not None:
            assert evaluation.generation_comment == gold_gen_comment
