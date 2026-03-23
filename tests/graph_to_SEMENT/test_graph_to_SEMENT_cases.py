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

# NOTE: for handwritten SEMENTs I have to make sure the variables don't overlap since I'm not using the VariableIterator to guarantee unique numbers
@fixture
def cake_SEMENT_no_var_props():
    # prefix all vars with 00
    SEMENT_str = """[
        TOP: h000
        INDEX: x001
        RELS: <
            [ _cake_n_1 LBL: h000 ARG0: x001 ]
        >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def cake_SEMENT_sg():
    # prefix all vars with 01
    SEMENT_str = """[
        TOP: h010
        INDEX: x011 [ NUM: sg ]
        RELS: <
            [ _cake_n_1 LBL: h010 ARG0: x011 ]
        >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def vanilla_SEMENT():
    # prefix all vars with 02
    SEMENT_str = """[
        TOP: h022
        INDEX: x023
        RELS: <
            [ _vanilla_n_1 LBL: h022 ARG0: x023 ]
        >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def vanilla_cake_SEMENT():
    # prefix all vars with 03
    SEMENT_str = """[
        TOP: h032
        INDEX: x0311
        RELS: <
            [ _vanilla_n_1 LBL: h030 ARG0: x031 ]
            [ compound LBL: h032 ARG0: e033 [ PROG: - ]  ARG1: x034 ARG2: x035 ]
            [ udef_q LBL: h036 ARG0: x037 RSTR: h038 BODY: h039 ]
            [ _cake_n_1 LBL: h0310 ARG0: x0311 ] >
        EQS: < x031 eq x037 x035 eq x031 x034 eq x0311 h032 eq h0310 >
        HCONS: < h038 qeq h030 >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def vanilla_cake_SEMENT_sg():
    # prefix all vars with 05
    SEMENT_str = """[
        TOP: h052
        INDEX: x0511 [ NUM: sg ]
        RELS: <
            [ _vanilla_n_1 LBL: h050 ARG0: x051 ]
            [ compound LBL: h052 ARG0: e053 [ PROG: - ] ARG1: x054 ARG2: x055 ]
            [ udef_q LBL: h056 ARG0: x057 RSTR: h058 BODY: h059 ]
            [ _cake_n_1 LBL: h0510 ARG0: x0511 ] >
        EQS: < x051 eq x057 x055 eq x051 x054 eq x0511 h052 eq h0510 >
        HCONS: < h058 qeq h050 >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def true_SEMENT():
    # prefix all vars with 07
    SEMENT_str = """[
        TOP: h070
        INDEX: e071
        RELS: <
            [ _true_a_of LBL: h070 ARG0: e071 ARG1: x072 ]
        >
    ]
    """
    return sementcodecs.decode(SEMENT_str)

@fixture
def blue_cake_SEMENT():
    # prefix all vars with 06
    SEMENT_str = """
        [
        TOP: h060
        INDEX: x061
        RELS: <
            [ _cake_n_1 LBL: h060 ARG0: x061 ]
            [ _blue_a_1 LBL: h060 ARG0: e063 ARG1: x061 ]
        >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def blue_SEMENT_missing_arg():
    # prefix all vars with 08
    SEMENT_str = """[
        TOP: h080
        INDEX: x081
        RELS: <
            [ _blue_a_1 LBL: h080 ARG0: i081 ]
        >
    ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def cat_who_slept():
    # prefix all vars with 09
    SEMENT_str = """[ TOP: h092
      INDEX: x091
      RELS: < [ _sleep_v_1 LBL: h092 ARG0: e093 [ e TENSE: tensed ] ARG1: x091 ]
              [ _cat_n_1 LBL: h092 ARG0: x091 ] > ]"""
    return sementcodecs.decode(SEMENT_str)


class GetSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.get_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a composition function name, parameter values as they would be found in the lexicon, and expected gold SEMENT
    """

    """
    SUCCESS CASES
        1. "noun" composition function 
        2. "compound_noun" composition function because it's nested and will test the recursion 
        3. "ARG1_relative_clause" composition function with None value for optional SEMENT parameter 
        
    FAILURE CASES
        3. Lexicon entry is missing a required parameter for the composition function 
    """
    @staticmethod
    @case(tags='success')
    def case_noun():
        comp_fxn = "noun"
        parameters = {
            "predicate": "_cake_n_1",
            "intrinsic_variable_properties": {
                "NUM": "sg"
            }
        }

        gold_SEMENT_str = """
        [
            TOP: h010
            INDEX: x011 [ x NUM: sg ]
            RELS: <
                [ _cake_n_1 LBL: h010 ARG0: x011 ]
            >
        ]
        """
        gold_SEMENT = sementcodecs.decode(gold_SEMENT_str)

        return comp_fxn, parameters, gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_compound_noun(mocker, vanilla_cake_SEMENT):
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
            "head_noun_SEMENT": mock_lexent_cake,
            "non_head_noun_SEMENT": mock_lexent_vanilla
        }

        gold_SEMENT = vanilla_cake_SEMENT

        return comp_fxn, parameters, gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_ARG1_relative_clause(mocker, cat_who_slept):
        comp_fxn = "ARG1_relative_clause"

        # create mock lexicon entries for the nested parameters
        mock_lexent_cat = mocker.MagicMock()
        mock_lexent_sleep = mocker.MagicMock()

        mock_lexent_cat.configure_mock(
            **{
                "composition_function_name": "noun",
                "parameters": {
                    "predicate": "_cat_n_1",
                    "intrinsic_variable_properties": {}
                }
            }
        )

        mock_lexent_sleep.configure_mock(
            **{
                "composition_function_name": "verb",
                "parameters": {
                    "predicate": "_sleep_v_1",
                    "intrinsic_variable_properties": {}
                }
            }
        )

        parameters = {
            "verb_SEMENT": mock_lexent_sleep,
            "ARG1_SEMENT": mock_lexent_cat,
            "ARG2_SEMENT": None
        }

        gold_SEMENT = cat_who_slept

        return comp_fxn, parameters, gold_SEMENT


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
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_node_to_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a node, a mock evaluation object, and the gold SEMENT
    """

    """
    SUCCESS CASES
        1. simple noun node (tuple of node_name and node_props)
        2. simple noun node w/o eval object 
    
    FAILURE CASES
        1. node's lexicon key is not in lexicon w/o eval obj
        2. node's lexicon key is not in lexicon w/ eval obj 
        3. predicate not found in SEMI w/o eval obj
        4. predicate not found in SEMI w/ eval obj
    """

    @staticmethod
    @case(tags=['success', 'eval'])
    def case_noun(mock_node_eval, cake_SEMENT_sg):
        # node tuple with node name and properties
        node = ("cake", {"lexicon_key": "cake"})

        gold_SEMENT = cake_SEMENT_sg

        return node, mock_node_eval, gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_noun_no_eval(cake_SEMENT_sg):
        # node tuple with node name and properties
        node = ("cake", {"lexicon_key": "cake"})

        gold_SEMENT = cake_SEMENT_sg

        return node, None, gold_SEMENT

    @staticmethod
    @case(tags='failure')
    def case_not_in_lexicon_no_eval():
        # node tuple with node name and properties
        node = ("fake", {"lexicon_key": "fake"})

        return node, None

    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_not_in_lexicon(mock_node_eval):
        # node tuple with node name and properties
        node = ("fake", {"lexicon_key": "fake"})

        gold_failure_comment = "'fake' not in lexicon's node entries"

        return node, mock_node_eval, gold_failure_comment

    @staticmethod
    @case(tags=['failure'])
    def case_not_in_SEMI_no_eval():
        # node tuple with node name and properties
        node = ("cookie", {"lexicon_key": "cookie"})

        return node, None

    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_not_in_SEMI(mock_node_eval):
        # node tuple with node name and properties
        node = ("cookie", {"lexicon_key": "cookie"})

        gold_failure_comment = "Couldn't find _coooookie_n_1 in the SEMI"

        return node, mock_node_eval, gold_failure_comment


class ConvertEdgeToSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_edge_to_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide an edge, a parent SEMENT, a child SEMENT, a mock evaluation object, and the gold SEMENT
    """

    """
    SUCCESS CASES
        1. compound_noun edge 
        2. compound_noun edge w/o eval object 
        3. boolean_property edge (i.e. edge that introduces its own SEMENT)
        
    FAILURE CASES
        1. missing parent (result is parent, aka None)
        2. missing parent w/o eval object 
        3. missing child (result is parent) 
        4. missing child w/o eval object 
        5. failure during execution w/ eval obj 
        6. failure during execution w/o eval obj
        7. lexicon_key is not in lexicon  
        8. lexicon_key is not in lexicon w/o eval obj  
    """

    @staticmethod
    @case(tags=['success', 'eval'])
    def case_compound_noun(mock_edge_eval, cake_SEMENT_no_var_props, vanilla_SEMENT, vanilla_cake_SEMENT):
        parent = cake_SEMENT_no_var_props
        child = vanilla_SEMENT
        gold_SEMENT = vanilla_cake_SEMENT

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        return edge, parent, child, mock_edge_eval, gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_compound_noun_no_eval(cake_SEMENT_no_var_props, vanilla_SEMENT, vanilla_cake_SEMENT):
        parent = cake_SEMENT_no_var_props
        child = vanilla_SEMENT
        gold_SEMENT = vanilla_cake_SEMENT

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        return edge, parent, child, None, gold_SEMENT


    @staticmethod
    @case(tags=['success', 'eval'])
    def case_boolean_property(mock_edge_eval, cake_SEMENT_no_var_props, true_SEMENT, blue_cake_SEMENT):
        parent = cake_SEMENT_no_var_props
        child = true_SEMENT
        gold_SEMENT = blue_cake_SEMENT

        edge = {'edge_type': 'property', 'label': 'boolean_color', 'lexicon_key': 'boolean_color'}
        return edge, parent, child, mock_edge_eval, gold_SEMENT


    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_missing_parent(mock_edge_eval, vanilla_SEMENT):
        child = vanilla_SEMENT

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case will be None
        return edge, None, child, mock_edge_eval, None

    @staticmethod
    @case(tags='failure')
    def case_missing_parent_no_eval(vanilla_SEMENT):
        child = vanilla_SEMENT

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case will be None
        return edge, None, child, None, None

    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_missing_child(mock_edge_eval, cake_SEMENT_no_var_props):
        parent = cake_SEMENT_no_var_props

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, None, mock_edge_eval, parent

    @staticmethod
    @case(tags='failure')
    def case_missing_child_no_eval(cake_SEMENT_no_var_props):
        parent = cake_SEMENT_no_var_props

        edge = {'edge_type': 'property', 'label': 'flavor', 'lexicon_key': 'flavor'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, None, None, parent

    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_failure_during_execution(mock_edge_eval, cake_SEMENT_no_var_props, blue_SEMENT_missing_arg):
        parent = cake_SEMENT_no_var_props
        child = blue_SEMENT_missing_arg

        edge = {'edge_type': 'property', 'label': 'color', 'lexicon_key': 'color'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, child, mock_edge_eval, parent

    @staticmethod
    @case(tags=['failure'])
    def case_failure_during_execution_no_eval(cake_SEMENT_no_var_props, blue_SEMENT_missing_arg):
        parent = cake_SEMENT_no_var_props
        child = blue_SEMENT_missing_arg

        edge = {'edge_type': 'property', 'label': 'color', 'lexicon_key': 'color'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, child, None, parent


    @staticmethod
    @case(tags=['failure', 'eval'])
    def case_bad_lexicon_key(mock_edge_eval, cake_SEMENT_no_var_props, vanilla_SEMENT):
        # include legitimate parent and child so it doesn't stop immediately
        parent = cake_SEMENT_no_var_props
        child = vanilla_SEMENT

        edge = {'edge_type': 'property', 'label': 'fake', 'lexicon_key': 'fake'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, child, mock_edge_eval, parent

    @staticmethod
    @case(tags='failure')
    def case_bad_lexicon_key_no_eval(cake_SEMENT_no_var_props, vanilla_SEMENT):
        # include legitimate parent and child so it doesn't stop immediately
        parent = cake_SEMENT_no_var_props
        child = vanilla_SEMENT

        edge = {'edge_type': 'property', 'label': 'fake', 'lexicon_key': 'fake'}
        # last return value is the "gold" SEMENT which in this case is the parent itself since no composition occurred
        return edge, parent, child, None, parent


class ConvertGraphToSement:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_to_SEMENT.POGGGraphConverter.convert_graph_to_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a graph in JSON format, convert (assume conversion works) to NetworkX graph, convert to SEMENT, and compare to gold SEMENT
    """

    """
    SUCCESS CASES
        1. simple graph with root marked ("vanilla cake")
        2. simple graph with root marked and NO eval object passed in
        3. simple graph with root unmarked ("vanilla cake")
        4. 2/3 nodes covered (i.e. one node not in lexicon)
        5. 1/2 edges covered (i.e. one edge not in lexicon)

    FAILURE CASES
        5. unable to find root, no SEMENT returned 
        6. cycle in graph, no SEMENT returned
        7. cycle in graph with NO eval object passed in
    """

    @staticmethod
    @case(tags='success')
    def case_simple_with_root_marked(dot_dir, mocker, vanilla_cake_SEMENT_sg):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "vanilla_cake.dot"))

        gold_SEMENT = vanilla_cake_SEMENT_sg

        root = ("cake", {"lexicon_key": "cake"})

        # return mock for evaluation object
        return root, graph, mocker.MagicMock(), gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_simple_with_root_marked_no_eval_obj(dot_dir, vanilla_cake_SEMENT_sg):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "vanilla_cake.dot"))

        gold_SEMENT = vanilla_cake_SEMENT_sg

        root = ("cake", {"lexicon_key": "cake"})

        # return mock for evaluation object
        return root, graph, None, gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_simple_with_root_unmarked(dot_dir, mocker, vanilla_cake_SEMENT_sg):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "vanilla_cake.dot"))

        gold_SEMENT = vanilla_cake_SEMENT_sg

        root = ("cake", {"lexicon_key": "cake"})

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_one_node_uncovered(dot_dir, mocker, vanilla_cake_SEMENT_sg):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "strawberry_vanilla_cake.dot"))

        gold_SEMENT = vanilla_cake_SEMENT_sg

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_SEMENT

    @staticmethod
    @case(tags='success')
    def case_one_edge_uncovered(dot_dir, mocker, vanilla_cake_SEMENT_sg):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "chocolate_vanilla_cake.dot"))

        gold_SEMENT = vanilla_cake_SEMENT_sg

        # return mock for evaluation object
        return None, graph, mocker.MagicMock(), gold_SEMENT


    @staticmethod
    @case(tags='failure')
    def case_no_root(dot_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "unconnected_vanilla_cake.dot"))

        mock_eval = mocker.MagicMock()

        # generation comment when root can't be found
        gold_gen_comment = "Graph is not weakly connected, can't determine root"

        # mocked graph, mocked eval object, and result SEMENT aka None
        return graph, mock_eval, gold_gen_comment

    @staticmethod
    @case(tags='failure')
    def case_cycles_in_graph(dot_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "cyclical_cake.dot"))

        mock_eval = mocker.MagicMock()

        # generation comment when root can't be found
        gold_gen_comment = "Cycle found in graph, skipping"

        # mocked graph, mocked eval object, and result SEMENT aka None
        return graph, mock_eval, gold_gen_comment

    @staticmethod
    @case(tags='failure')
    def case_cycles_in_graph_no_eval(dot_dir, mocker):
        graph = nx.drawing.nx_pydot.read_dot(os.path.join(dot_dir, "cyclical_cake.dot"))

        # mocked graph, mocked eval object, and result SEMENT aka None
        return graph, None, None



