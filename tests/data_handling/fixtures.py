import os
import yaml
from pytest_cases import fixture

@fixture(scope="session")
def data_handling_test_dir(test_data_dir):
    return os.path.join(test_data_dir, "data_handling")

## pogg_dataset fixtures ##
@fixture(scope="class")
def config_filepath(test_data_dir):
    return os.path.join(test_data_dir, "data_handling/dataset_config.yml")

@fixture(scope="class")
def yaml_info(config_filepath):
    return yaml.load(open(config_filepath), Loader=yaml.FullLoader)