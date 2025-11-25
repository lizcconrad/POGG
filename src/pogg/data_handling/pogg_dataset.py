"""
The `pogg_dataset` module contains the `POGGDataset` class which stores information about a provided dataset.
Once stored as a `POGGDataset` object, the dataset can go through the POGG graph to text routine.
In addition, evaluation information about each graph in the dataset will be collected and stored.

[See usage examples here.](project:/usage_nbs/pogg/data_handling/pogg_dataset_usage.ipynb)
"""

import os
import yaml
from pathlib import Path
from pogg.lexicon.lexicon_builder import POGGLexiconUtil


class POGGDataset:
    """
    A `POGGDataset` object stores information about a provided dataset such as where it's located
    and where any output from running the graph to text routine should be stored.
    """
    def __init__(self, yaml_filepath):
        """
        Initialize the `POGGDataset` object by providing the filepath to a YAML config file.
        Each field in the config file will correspond to an instance attribute of the POGGDataset object that can be accessed.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `yaml_filepath` | `str` | filepath where the config file detailing directories relevant to the dataset |

        :::{info} YAML config example
        :collapsible:
        ```
        # top level directory
        data_dir: "/absolute/path/to/dataset/directory"

        # subdirectories
        data_chunk: "BitsyBakery"       # this is optional and only applies if the dataset is divided into chunks
        graph_json_dir: "graph_jsons"
        graph_dot_dir: "dot"
        lexicon_dir: "lexicon"
        evaluation_dir: "evaluation"

        # other data information
        dataset_name: "BitsyBakery"
        ```
        :::

        Provided the provided YAML config file has the appropriate fields, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `data_dir` | directory where the dataset is stored |
        | `data_chunk` | optional subdirectory where the particular data chunk is stored |
        | `graph_json_dir` | subdirectory where the graphs are stored in JSON format |
        | `graph_dot_dir` | subdirectory where the graphs are stored in DOT format |
        | `lexicon_dir` | subdirectory where the lexicon information is stored |
        | `evaluation_dir` | subdirectory where the evaluation information collected during graph to text conversion will be stored |
        """
        yaml_file = open(yaml_filepath, 'r')
        self.yaml_config = yaml.safe_load(yaml_file)
        yaml_file.close()

        # save dataset_name in the POGGDataset object
        try:
            self.dataset_name = self.yaml_config['dataset_name']
        except KeyError:
            raise KeyError("'dataset_name' is missing in the config file")


        self.data_dir = self._store_path_value("data_dir")
        self.data_chunk = self._store_path_value("data_chunk", self.data_dir, True)
        self.graph_json_dir = self._store_path_value("graph_json_dir", self.data_chunk)
        self.graph_dot_dir = self._store_path_value("graph_dot_dir", self.data_chunk)
        self.lexicon_dir = self._store_path_value("lexicon_dir", self.data_chunk)
        self.evaluation_dir = self._store_path_value("evaluation_dir", self.data_chunk)

        # initialize lexicon in case no files exist yet (skipping ones that do)
        POGGLexiconUtil.initialize_lexicon_directory(self.dataset_name, self.lexicon_dir)
        # read in existing lexicon
        self.lexicon = POGGLexiconUtil.read_lexicon_from_directory(self.dataset_name, self.lexicon_dir)


    def _store_path_value(self, key, prepend_path="", optional=False):
        """
        Helper function to create subdirectories listed in the config file if they don't exist
        as well as raise errors if certain keys are missing in the config file.

        **Parameters**
        | Parameter | Type | Description | Default |
        | --------- | ---- | ----------- | -------- |
        | `key` | `str` | key in the config file to check and store | |
        | `prepend_path` | `str` | path to prepend to directory information provided if it's a subdirectory | `""` |
        | `optional` | `bool` | whether the key is optional for the POGGDataset object | `False` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `str` | string of the absolute path to the directory |
        """

        # return the [prepend_path]/key value to be stored in the POGGDataset object
        try:
            config_value = os.path.join(prepend_path, self.yaml_config[key])
            # make directory in case it doesn't exist
            Path(config_value).mkdir(parents=True, exist_ok=True)
            return config_value
        except KeyError:
            if optional:
                return None
            else:
                raise KeyError(f"'{key}' is missing in the config file")

