import os
import json
import networkx as nx
from pytest_cases import case, fixture

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs


# TODO: i don't know why i can't put this fixture IN the class that i'm using it in...
# like when i put it in the ConvertNodeToSement class it isn't able to find it
@fixture
def mock_node_eval(mocker):
    mock_eval = mocker.MagicMock()
    mock_eval.configure_mock(
        **{
            "node_covered": None,
            "generated_SEMENT": None,
            "generation_comment": None
        }
    )
    return mock_eval

@fixture
def mock_edge_eval(mocker):
    mock_eval = mocker.MagicMock()
    mock_eval.configure_mock(
        **{
            "edge_covered": None,
            "generated_SEMENT": None,
            "generation_comment": None
        }
    )
    return mock_eval



class GetSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.get_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a composition function name, parameter values as they would be found in the lexicon, and expected gold SEMENT
    """

    """
    SUCCESS CASES
        1. "noun" composition function 
        2. "compound_noun" composition function because it's nested and will test the recursion 
        
    FAILURE CASES
        3. Lexicon entry is missing a required parameter for the composition function 
    """
    @staticmethod
    @case(tags='success')
    def case_noun(sement_dir):
        comp_fxn = "noun"
        parameters = {
            "predicate": "_cake_n_1",
            "intrinsic_variable_properties": {
                "NUM": "sg"
            }
        }

        with open(os.path.join(sement_dir, "cake_sg_01.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        return comp_fxn, parameters, gold_sement

    @staticmethod
    @case(tags='success')
    def case_compound_noun(sement_dir, mocker):
        comp_fxn = "compound_noun"

        # create mock lexicon entries for the nested parameters
        mock_lexent_vanilla = mocker.MagicMock()
        mock_lexent_cake = mocker.MagicMock()

        mock_lexent_vanilla.configure_mock(
            **{
                "composition_function_name": "noun",
                "parameters": {
                    "predicate": "_vanilla_n_1",
                    "intrinsic_variable_properties": {}
                }
            }
        )

        mock_lexent_cake.configure_mock(
            **{
                "composition_function_name": "noun",
                "parameters": {
                    "predicate": "_cake_n_1",
                    "intrinsic_variable_properties": {}
                }
            }
        )

        parameters = {
            "head_noun_sement": mock_lexent_cake,
            "non_head_noun_sement": mock_lexent_vanilla
        }

        with open(os.path.join(sement_dir, "vanilla_cake_03.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        return comp_fxn, parameters, gold_sement


    @staticmethod
    @case(tags='failure')
    def case_missing_parameter():
        comp_fxn = "noun"
        # missing "predicate"
        parameters = {
            "intrinsic_variable_properties": {
                "NUM": "sg"
            }
        }

        return comp_fxn, parameters


class ConvertNodeToSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_node_to_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a node, a mock evaluation object, and the gold SEMENT
    """

    """
    SUCCESS CASES
        1. simple noun node (tuple of node_name and node_props)
    
    FAILURE CASES
        2. node's lexicon key is not in lexicon 
    """

    @staticmethod
    @case(tags='success')
    def case_noun(sement_dir, mock_node_eval):
        # node tuple with node name and properties
        node = ("cake", {"lexicon_key": "cake"})

        with open(os.path.join(sement_dir, "cake_sg_01.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        return node, mock_node_eval, gold_sement


    @staticmethod
    @case(tags='failure')
    def case_not_in_lexicon(mock_node_eval):
        # node tuple with node name and properties
        node = ("fake", {"lexicon_key": "fake"})

        return node, mock_node_eval


class ConvertEdgeToSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_edge_to_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide an edge, a parent SEMENT, a child SEMENT, a mock evaluation object, and the gold SEMENT
    """

    """
    SUCCESS CASES
        1. compound_noun edge 
        
    FAILURE CASES
        2. missing parent (result is parent, aka None)
        3. missing child (result is parent) 
        4. lexicon_key is not in lexicon 
    """

    @staticmethod
    @case(tags='success')
    def case_compound_noun(sement_dir, mock_edge_eval):

        with open(os.path.join(sement_dir, "cake_00.txt"), "r") as f:
            parent = sementcodecs.decode(f.read())

        with open(os.path.join(sement_dir, "vanilla_02.txt"), "r") as f:
            child = sementcodecs.decode(f.read())

        with open(os.path.join(sement_dir, "vanilla_cake_03.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())


        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        return edge, parent, child, mock_edge_eval, gold_sement


    @staticmethod
    @case(tags='failure')
    def case_missing_parent(sement_dir, mock_edge_eval):

        with open(os.path.join(sement_dir, "vanilla_02.txt"), "r") as f:
            child = sementcodecs.decode(f.read())

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case will be None
        return edge, None, child, mock_edge_eval, None


    @staticmethod
    @case(tags='failure')
    def case_missing_child(sement_dir, mock_edge_eval):
        with open(os.path.join(sement_dir, "cake_00.txt"), "r") as f:
            parent = sementcodecs.decode(f.read())

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, None, mock_edge_eval, parent


    @staticmethod
    @case(tags='failure')
    def case_bad_lexicon_key(sement_dir, mock_edge_eval):
        # include legitimate parent and child so it doesn't stop immediately
        with open(os.path.join(sement_dir, "cake_00.txt"), "r") as f:
            parent = sementcodecs.decode(f.read())

        with open(os.path.join(sement_dir, "vanilla_02.txt"), "r") as f:
            child = sementcodecs.decode(f.read())

        edge = {'edge_type': 'property', 'label': 'fake', 'lexicon_key': 'fake'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, child, mock_edge_eval, parent


class ConvertGraphToSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_graph_to_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph in JSON format, convert (assume conversion works) to NetworkX graph, convert to SEMENT, and compare to gold SEMENT
    """

    """
    SUCCESS CASES
        1. simple graph with root marked ("vanilla cake")
        2. simple graph with root unmarked ("vanilla cake")
        3. 2/3 nodes covered (i.e. one node not in lexicon)
        4. 1/2 edges covered (i.e. one edge not in lexicon)

    FAILURE CASES
        5. unable to find root, no SEMENT returned 
    """

    @staticmethod
    @case(tags='success')
    def case_simple_with_root_marked(dot_dir, sement_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "vanilla_cake.dot"))

        with open(os.path.join(sement_dir, "vanilla_cake_sg_05.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        root = ("cake", {"lexicon_key": "cake"})

        # return mock for evaluation object
        return root, graph, mocker.MagicMock(), gold_sement

    @staticmethod
    @case(tags='success')
    def case_simple_with_root_unmarked(dot_dir, sement_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "vanilla_cake.dot"))

        with open(os.path.join(sement_dir, "vanilla_cake_sg_05.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        root = ("cake", {"lexicon_key": "cake"})

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_sement

    @staticmethod
    @case(tags='success')
    def case_one_node_uncovered(dot_dir, sement_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "strawberry_vanilla_cake.dot"))

        with open(os.path.join(sement_dir, "vanilla_cake_sg_05.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_sement

    @staticmethod
    @case(tags='success')
    def case_one_edge_uncovered(dot_dir, sement_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "chocolate_vanilla_cake.dot"))

        with open(os.path.join(sement_dir, "vanilla_cake_sg_05.txt"), "r") as f:
            gold_sement = sementcodecs.decode(f.read())

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_sement


    @staticmethod
    @case(tags='failure')
    def case_no_root(mocker):
        mock_graph = mocker.MagicMock()
        mock_eval = mocker.MagicMock()

        # mocked graph, mocked eval object, and result SEMENT aka None
        return mock_graph, mock_eval, None



