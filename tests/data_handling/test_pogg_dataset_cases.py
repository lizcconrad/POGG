import os
import yaml
from pytest_cases import case, fixture

class POGGDatasetInit:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.pogg_dataset.POGGDataset.__init__

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a path to a config file and the gold YAML info and ensure that the initialization occurred correctly
    """

    """
    SUCCESS CASES
        1. legitimate config file 

    FAILURE CASES
        2. broken config file
    """

    @staticmethod
    @case(tags="success")
    def case_legitimate_config(data_handling_test_dir):
        config_filepath = os.path.join(data_handling_test_dir, "dataset_config.yml")
        gold_yaml = yaml.load(open(config_filepath), Loader=yaml.FullLoader)


        return config_filepath, gold_yaml

    @staticmethod
    @case(tags="failure")
    def case_broken_config(data_handling_test_dir):
        config_filepath = os.path.join(data_handling_test_dir, "dataset_config_missing_dataset_name.yml")
        return config_filepath

