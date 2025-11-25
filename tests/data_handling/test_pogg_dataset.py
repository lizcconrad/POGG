import os
import pytest
from pytest_cases import fixture, parametrize_with_cases
import yaml
from pytest_cases.plugin import parametrize

from pogg.data_handling.pogg_dataset import POGGDataset

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_pogg_dataset_cases import *

class TestPOGGDataset:
    ## TEST WORKING INITIALIZATION ##
    @staticmethod
    @parametrize_with_cases("config_filepath, gold_yaml", cases=POGGDatasetInit, has_tag="success")
    def test_POGGDataset_object(config_filepath, gold_yaml):
        pogg_dataset_object = POGGDataset(config_filepath)

        assert isinstance(pogg_dataset_object, POGGDataset)
        assert pogg_dataset_object.dataset_name == gold_yaml["dataset_name"]
        assert pogg_dataset_object.data_dir == gold_yaml["data_dir"]

        gold_data_chunk = os.path.join(gold_yaml["data_dir"], gold_yaml["data_chunk"])
        assert pogg_dataset_object.data_chunk == gold_data_chunk

        gold_graph_json_dir = os.path.join(gold_yaml["data_dir"], gold_yaml["data_chunk"], gold_yaml["graph_json_dir"])
        assert pogg_dataset_object.graph_json_dir == gold_graph_json_dir

        gold_graph_dot_dir = os.path.join(gold_yaml["data_dir"], gold_yaml["data_chunk"], gold_yaml["graph_dot_dir"])
        assert pogg_dataset_object.graph_dot_dir == gold_graph_dot_dir

        gold_lexicon_dir = os.path.join(gold_yaml["data_dir"], gold_yaml["data_chunk"], gold_yaml["lexicon_dir"])
        assert pogg_dataset_object.lexicon_dir == gold_lexicon_dir

        gold_evaluation_dir = os.path.join(gold_yaml["data_dir"], gold_yaml["data_chunk"], gold_yaml["evaluation_dir"])
        assert pogg_dataset_object.evaluation_dir == gold_evaluation_dir


    ## TEST INITIALIZATION EXCEPTIONS ##
    @staticmethod
    @parametrize_with_cases("broken_config_filepath", cases=POGGDatasetInit, has_tag="failure")
    def test_missing_dataset_name(broken_config_filepath):
        with pytest.raises(KeyError):
            POGGDataset(broken_config_filepath)


    ## TEST _store_path_value FUNCTION ##
    @staticmethod
    def test__store_path_value_dir_created(config_filepath, yaml_info):
        pogg_dataset_object = POGGDataset(config_filepath)

        prepend = os.path.join(yaml_info["data_dir"], yaml_info["data_chunk"])
        new_temp_dir = os.path.join(prepend, "dummy_dir")

        # make sure it doesn't already exist
        assert not os.path.exists(new_temp_dir)

        pogg_dataset_object._store_path_value("dummy_dir", prepend)

        # make sure it's been created
        assert os.path.isdir(new_temp_dir)

        # delete it
        os.rmdir(new_temp_dir)

    @staticmethod
    def test__store_path_value_optional_key(config_filepath):
        pogg_dataset_object = POGGDataset(config_filepath)

        # config_value should be None since this key doesn't exist in the file but is labeled as optional
        config_value = pogg_dataset_object._store_path_value("imaginary_key", None, True)
        assert config_value is None

    @staticmethod
    def test__store_path_value_return_value(config_filepath, yaml_info):
        pogg_dataset_object = POGGDataset(config_filepath)

        prepend = os.path.join(yaml_info["data_dir"], yaml_info["data_chunk"])
        # just choose one of the keys for the test
        gold_value = os.path.join(prepend, "lexicon")

        config_value = pogg_dataset_object._store_path_value("lexicon_dir", prepend)
        assert config_value == gold_value


    ## TEST _store_path_value EXCEPTIONS ##
    @staticmethod
    def test__store_path_value_missing_required_key(config_filepath, yaml_info):
        pogg_dataset_object = POGGDataset(config_filepath)

        with pytest.raises(KeyError):
            prepend = os.path.join(yaml_info["data_dir"], yaml_info["data_chunk"])
            # try to store path value for a missing key that's NOT marked as optional
            pogg_dataset_object._store_path_value("missing_key", prepend, False)










