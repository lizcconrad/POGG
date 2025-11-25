import os
from pytest_cases import fixture

@fixture(scope="session")
def lexicon_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "lexicon/lexicon_builder")

@fixture(scope="session")
def graph_jsons_dir(lexicon_test_dir):
    return os.path.join(lexicon_test_dir, "graph_jsons")

@fixture(scope="session")
def lexicon_directories_dir(lexicon_test_dir):
    return os.path.join(lexicon_test_dir, "lexicon_directories")

@fixture(scope="session")
def lexicon_skeletons_dir(lexicon_test_dir):
    return os.path.join(lexicon_test_dir, "lexicon_skeletons")

