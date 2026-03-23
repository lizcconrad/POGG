import os
from pytest_cases import fixture
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.lexicon.lexicon_builder import POGGLexiconEntry

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

    pogg_lexicon_node_entry_cookie = mocker.MagicMock()
    pogg_lexicon_node_entry_cookie.configure_mock(
        **{
            "composition_function_name": "noun",
            "parameters": {
                "predicate": "_coooookie_n_1",
                "intrinsic_variable_properties": {}
            }
        }
    )

    pogg_lexicon_node_entry_vanilla = mocker.MagicMock()
    pogg_lexicon_node_entry_vanilla.configure_mock(
        **{
            "composition_function_name": "noun",
            "parameters": {
                "predicate": "_vanilla_n_1"
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

    pogg_lexicon_node_entry_true = mocker.MagicMock()
    pogg_lexicon_node_entry_true.configure_mock(
        **{
            "composition_function_name": "boolean_value",
            "parameters": {
                "value": True,
                "intrinsic_variable_properties": {}
            }
        }
    )

    # POGGLexiconEntry(key='flavor', composition_function_name='compound_noun', parameters={'head_noun_SEMENT': 'parent', 'non_head_noun_SEMENT': 'child'})
    pogg_lexicon_edge_entry_flavor = mocker.MagicMock()
    pogg_lexicon_edge_entry_flavor.configure_mock(
        **{
            "composition_function_name": "compound_noun",
            "parameters": {
                "head_noun_SEMENT": "parent",
                "non_head_noun_SEMENT": "child",
                "superfluous": "just_another_param_for_branch_coverage"
            }
        }
    )


    pogg_lexicon_edge_entry_color = mocker.MagicMock()
    pogg_lexicon_edge_entry_color.configure_mock(
        **{
            "composition_function_name": "prenominal_adjective",
            "parameters": {
                "adjective_SEMENT": "child",
                "nominal_SEMENT": "parent"
            }
        }
    )


    # just making a ridiculous boolean edge for coverage purposes
    # make this a proper POGGLexiconEntry object because this gets checked for nested entries
    pogg_lexicon_edge_entry_boolean_color = POGGLexiconEntry(
        key='flavor',
        composition_function_name='boolean_property',
        parameters={
            'boolean_node_SEMENT': 'child',
            'modified_SEMENT': 'parent',
            "true_SEMENT": POGGLexiconEntry(
                key="adjective",
                composition_function_name="adjective",
                parameters={
                    "predicate": "_blue_a_1",
                    "intrinsic_variable_properties": {}
                }
            ),
            "false_SEMENT": POGGLexiconEntry(
                key="adjective",
                composition_function_name="adjective",
                parameters={
                    "predicate": "_red_a_1",
                    "intrinsic_variable_properties": {}
                }
            ),
        })

    pogg_lexicon = mocker.MagicMock()
    pogg_lexicon.configure_mock(
        **{
            "node_entries": {
                "cake": pogg_lexicon_node_entry_cake,
                "cookie": pogg_lexicon_node_entry_cookie,
                "vanilla": pogg_lexicon_node_entry_vanilla,
                "chocolate": pogg_lexicon_node_entry_chocolate,
                "true": pogg_lexicon_node_entry_true,
            },
            "edge_entries": {
                "flavor": pogg_lexicon_edge_entry_flavor,
                "color": pogg_lexicon_edge_entry_color,
                "boolean_color": pogg_lexicon_edge_entry_boolean_color,
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