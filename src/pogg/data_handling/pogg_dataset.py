"""
The `pogg_dataset` module contains the `POGGDataset` class which stores information about a provided dataset.
Once stored as a `POGGDataset` object, the dataset can go through the POGG graph-to-text routine.

[See usage examples here.](project:/usage_nbs/pogg/data_handling/pogg_dataset_usage.ipynb)
"""

import os
import yaml
import json
import copy
from typing import List, Dict, overload
from pathlib import Path
from pogg.data_handling.graph_util import POGGGraphUtil


class POGGDataset:
    """
    A `POGGDataset` object stores information about a provided dataset such as where it's located
    and where any output from running the graph-to-text routine should be stored.
    """

    def __init__(self, dataset_name: str, graphs_info: Path | List):
        """
        Initialize the `POGGDataset` object by providing the filepath to a YAML config file.
        Each field in the config file will correspond to an instance attribute of the POGGDataset object that can be accessed.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `yaml_filepath` | `str` | filepath where the config file detailing directories relevant to the dataset |

        :::{example} YAML config example
        :collapsible:
        ```
        # top level directory
        data_dir: "/absolute/path/to/dataset/directory"

        # subdirectories
        graph_json_dir: "graph_jsons"
        graph_dot_dir: "dot"
        graph_png_dor: "png"
        evaluation_dir: "evaluation"
        gold_outputs_dir: "gold_outputs"

        # other data information
        dataset_name: "BitsyBakery"
        ```
        :::

        Provided the provided YAML config file has the appropriate fields, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Description |
        | --------- | ----------- |
        | `data_dir` | directory where the dataset is stored |
        | `graph_json_dir` | subdirectory where the graphs are stored in JSON format |
        | `graph_dot_dir` | subdirectory where the graphs are stored in DOT format |
        | `lexicon_dir` | subdirectory where the lexicon information is stored |
        | `evaluation_dir` | subdirectory where the evaluation information collected during graph to text conversion will be stored |
        | `gold_outputs_dir` | subdirectory where the gold outputs for each graph are stored |
        """

        self.dataset_name = dataset_name
        self.graphs = {}

        if not isinstance(graphs_info, List):
            self.graph_json_dirs = [graphs_info]
            self._build_graphs(graphs_info)
        else:
            for graph_info in graphs_info:
                for key, val in graph_info.items():
                    self.graphs[key] = val


    def _build_graphs(self, graph_json_dir):
        for dir_elem in os.scandir(graph_json_dir):
            if dir_elem.is_file() and dir_elem.name.endswith(".json"):
                graph_name = f"{self.dataset_name}_{dir_elem.name.split('.')[0]}"

                with open(dir_elem.path, 'r') as f:
                    graph_json = json.load(f)

                graph = POGGGraphUtil.build_graph(graph_json)
                self.graphs[graph_name] = {
                    "graph_json": graph_json,
                    "graph": graph,
                    "gold_outputs": graph_json["gold_outputs"],
                }