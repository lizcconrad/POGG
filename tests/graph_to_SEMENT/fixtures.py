import os
from pytest_cases import fixture
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.base_constructions import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter

@fixture(scope="session")
def graph_to_SEMENT_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "graph_to_SEMENT")

@fixture(scope="session")
def sement_dir(graph_to_SEMENT_test_dir):
    return os.path.join(graph_to_SEMENT_test_dir, "SEMENTs")

@fixture(scope="session")
def dot_dir(graph_to_SEMENT_test_dir):
    return os.path.join(graph_to_SEMENT_test_dir, "dot")

@fixture
def pogg_graph_converter(module_pogg_config, mocker):
    # just assume SemanticComposition works...
    sem_alg = SemanticAlgebra(module_pogg_config)
    sem_comp = SemanticComposition(sem_alg)

    # mock a lexicon
    pogg_lexicon_node_entry_cake = mocker.MagicMock()
    pogg_lexicon_node_entry_cake.configure_mock(
        **{
            "composition_function_name": "noun",
            "parameters": {
                "predicate": "_cake_n_1",
                "intrinsic_variable_properties": {"NUM": "sg"}
            }
        }
    )

    pogg_lexicon_node_entry_vanilla = mocker.MagicMock()
    pogg_lexicon_node_entry_vanilla.configure_mock(
        **{
            "composition_function_name": "noun",
            "parameters": {
                "predicate": "_vanilla_n_1",
                "intrinsic_variable_properties": {}
            }
        }
    )

    pogg_lexicon_node_entry_chocolate = mocker.MagicMock()
    pogg_lexicon_node_entry_chocolate.configure_mock(
        **{
            "composition_function_name": "noun",
            "parameters": {
                "predicate": "_chooclate_n_1",
                "intrinsic_variable_properties": {}
            }
        }
    )

    # POGGLexiconEntry(key='flavor', composition_function_name='compound_noun', parameters={'head_noun_sement': 'parent', 'non_head_noun_sement': 'child'})
    pogg_lexicon_edge_entry = mocker.MagicMock()
    pogg_lexicon_edge_entry.configure_mock(
        **{
            "composition_function_name": "compound_noun",
            "parameters": {
                "head_noun_sement": "parent",
                "non_head_noun_sement": "child",
                "superfluous": "just_another_param_for_branch_coverage"
            }
        }
    )

    pogg_lexicon = mocker.MagicMock()
    pogg_lexicon.configure_mock(
        **{
            "node_entries": {
                "cake": pogg_lexicon_node_entry_cake,
                "vanilla": pogg_lexicon_node_entry_vanilla,
                "chocolate": pogg_lexicon_node_entry_chocolate
            },
            "edge_entries": {
                "flavor": pogg_lexicon_edge_entry
            }
        }
    )

    pogg_dataset = mocker.MagicMock()
    pogg_dataset.configure_mock(
        **{
            "lexicon": pogg_lexicon,
        }
    )

    return POGGGraphConverter(sem_comp, pogg_dataset)