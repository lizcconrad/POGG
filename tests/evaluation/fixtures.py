import os
from pytest_cases import fixture

@fixture(scope="session")
def evaluation_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "evaluation")
