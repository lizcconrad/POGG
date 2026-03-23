import os
from pytest_cases import fixture
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition

@fixture(scope="session")
def semantic_composition_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "semantic_composition")

@fixture(scope="session")
def sement_util_test_dir(semantic_composition_test_dir):
    return os.path.join(semantic_composition_test_dir, "sement_util")

@fixture(scope="session")
def semantic_algebra_test_dir(semantic_composition_test_dir):
    return os.path.join(semantic_composition_test_dir, "semantic_algebra")

@fixture(scope="session")
def base_constructions_test_dir(semantic_composition_test_dir):
    return os.path.join(semantic_composition_test_dir, "base_constructions")

@fixture(scope="class")
def sem_alg_obj(module_pogg_config):
    # set variterator to start at 100 to avoid collision with gold SEMENTs
    module_pogg_config.var_labeler.varIt.set(1000)
    return SemanticAlgebra(module_pogg_config)

@fixture(scope="class")
def sem_comp_obj(sem_alg_obj):
    return SemanticComposition(sem_alg_obj)