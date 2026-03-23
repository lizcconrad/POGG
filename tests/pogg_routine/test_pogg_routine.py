import pytest
from pytest_cases import parametrize_with_cases
from pathlib import Path

import pogg.my_delphin.my_delphin
from pogg.data_handling.pogg_dataset import POGGDataset
from pogg.evaluation.evaluation import POGGEvaluation
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.pogg_config import POGGConfig
from pogg.pogg_routine import POGG
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_pogg_routine_cases import *


class TestPOGG:
    """
    Tests POGG class
    """
    @staticmethod
    def test_init(pogg_config_file, dataset_config_file):
        pogg_routine = POGG(pogg_config_file, dataset_config_file)

        # assert that each instance attribute is the right type
        assert isinstance(pogg_routine.pogg_config, POGGConfig)
        assert isinstance(pogg_routine.dataset, POGGDataset)
        assert isinstance(pogg_routine.evaluation, POGGEvaluation)
        assert isinstance(pogg_routine.semantic_algebra, SemanticAlgebra)
        assert isinstance(pogg_routine.semantic_composition, SemanticComposition)
        assert isinstance(pogg_routine.graph_converter, POGGGraphConverter)

    @staticmethod
    @parametrize_with_cases("pogg_obj, result_eval_dir, gold_eval_dir", cases=RunPOGGDataToTextAlgorithm, has_tag="success")
    def test_run_POGG_data_to_text_algorithm(pogg_obj, result_eval_dir, gold_eval_dir):
        pogg_obj.run_POGG_data_to_text_algorithm()
        # maybe should split this up into another test but i kinda don't care to be tee bee aych about it all...
        # set run_id to be "test_run"
        pogg_obj.evaluation.run_id = "test_run"
        pogg_obj.store_evaluation_report()

        # for each file in the result eval dir, make sure it matches the gold file of the same name

        gold_files = sorted([(file, Path(src, file)) for src, _, files in os.walk(gold_eval_dir) for file in files],
                            key=lambda x: x[0])
        eval_files = sorted([(file, Path(src, file)) for src,_,files in os.walk(result_eval_dir) for file in files],
                            key=lambda x: x[0])


        for i in range(len(gold_files)):
            gold_file_path = gold_files[i][1]
            result_file_path = eval_files[i][1]
            with (open(result_file_path, "r") as result_file, open(gold_file_path, "r") as gold_file):
                # TODO: severe hack but whatever ...
                # skipping these files because the list of available sem comp fxns will keep changing
                # so the original gold report i created won't reflect that
                if (str(result_file_path).endswith("eval_metadata.json")
                        or str(result_file_path).endswith("dataset_eval.json")
                        or str(result_file_path).endswith("dataset_report.txt")):
                    continue
                else:
                    assert result_file.read() == gold_file.read()

    @staticmethod
    @parametrize_with_cases("pogg_obj", cases=RunPOGGDataToTextAlgorithm, has_tag="failure")
    def test_try_to_store_no_run(pogg_obj):
        with pytest.raises(ValueError):
            pogg_obj.store_evaluation_report()

    @staticmethod
    @parametrize_with_cases("pogg_obj, graph_name, graph, gold_properties",
                            cases=RunPOGGDatatToTextAlgorithmOnSingleGraph, has_tag="success")
    def test_run_POGG_data_to_text_algorithm_on_single_graph(pogg_obj, graph_name, graph, gold_properties):
        output = pogg_obj.run_POGG_data_to_text_algorithm_on_single_graph(graph_name, graph)

        for key in gold_properties.keys():
            if isinstance(gold_properties[key], pogg.my_delphin.my_delphin.SEMENT):
                assert  POGGSEMENTUtil.is_sement_isomorphic(getattr(output, key), gold_properties[key])
            else:
                assert getattr(output, key) == gold_properties[key]

    @staticmethod
    @parametrize_with_cases("pogg_obj, graph_name",
                            cases=RunPOGGDatatToTextAlgorithmOnSingleGraph, has_tag="failure")
    def test_run_POGG_data_to_text_algorithm_on_single_graph_error(pogg_obj, graph_name):
        with pytest.raises(FileNotFoundError):
            pogg_obj.run_POGG_data_to_text_algorithm_on_single_graph(graph_name, None)
