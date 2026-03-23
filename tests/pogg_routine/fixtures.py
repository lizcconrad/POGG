import os
from pytest_cases import fixture

@fixture(scope="session")
def pogg_routine_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "pogg_routine")

@fixture(scope="module")
def dataset_config_file(pogg_routine_test_dir):
    return os.path.join(pogg_routine_test_dir, "dataset_config.yml")
