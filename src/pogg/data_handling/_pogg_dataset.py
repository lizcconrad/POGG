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
from pogg.data_handling._graph_util import POGGGraphUtil


class POGGDataSplit:
    def __init__(self, full_data_split_name: str, data_directories: List[Path | str], leaf:bool=False):
        self.full_data_split_name = full_data_split_name
        self.leaf = leaf
        self.graphs = {}
        self.node_keys = None
        self.edge_keys = None
        # store original names here (i.e. not lexicon keys)
        # used when checking if parent/child nodes of edges have already been added, even if the name != lexicon key
        self.original_element_names = None

        # sometimes a DataSplit is created without data_directories provided
        # specifically when creating an on-the-fly split with a set operation
        if data_directories:
            for data_dir in data_directories:
                self._build_graphs(data_dir)

        self._set_node_and_edge_keys()

    def _build_graphs(self, graph_json_dir):
        graph_counter = len(self.graphs.keys())
        for dir_elem in os.scandir(graph_json_dir):
            if dir_elem.is_file() and dir_elem.name.endswith(".json"):
                graph_name = f"{self.full_data_split_name}_{dir_elem.name.split('.')[0]}_{graph_counter}"
                graph_counter += 1

                with open(dir_elem.path, 'r') as f:
                    graph_json = json.load(f)

                graph = POGGGraphUtil.build_graph(graph_json)
                self.graphs[graph_name] = {
                    "graph_json": graph_json,
                    "graph": graph,
                    "graph_directory": dir_elem.path,
                    "gold_outputs": graph_json["gold_outputs"],
                }

    def _set_node_and_edge_keys(self):
        nodes = set()
        edges = set()
        original_element_names = set()
        for graph_name, graph in self.graphs.items():
            graph_json = graph["graph_json"]
            for node_name, node_info in graph_json["nodes"].items():
                original_element_names.add(node_name)
                if "lexicon_key" in node_info:
                    nodes.add(node_info["lexicon_key"])

                else:
                    nodes.add(node_name)

            for edge_info in graph_json["edges"]:
                edge_name = edge_info["edge_name"]
                original_element_names.add(edge_name)
                if "lexicon_key" in edge_info:
                    edges.add(edge_info["lexicon_key"])
                else:
                    edges.add(edge_name)

                if not edge_info["parent_node"] in original_element_names:
                    nodes.add(edge_info["parent_node"])
                if not edge_info["child_node"] in original_element_names:
                    nodes.add(edge_info["child_node"])

        self.node_keys = nodes
        self.edge_keys = edges
        self.original_element_names = original_element_names


class POGGDataset:
    def __init__(self, config_json):
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

        self.data_splits = {}
        # will be updated during POGGDataSplit object creation
        self.node_keys = set()
        self.edge_keys = set()
        self.original_element_names = set()
        self._create_data_split_objects(config_json["splits"], self.data_splits)



    def _create_data_split_objects(self, current_config_split, current_data_split_dict):
        for split_name, split_value in current_config_split.items():
            # "split_value" includes three sub dictionaries: experiments, split_info, and splits
            split_info = split_value["split_info"]
            split_object = POGGDataSplit(split_info["full_data_split_name"], split_info["data_directories"], split_info["leaf"])
            current_data_split_dict[split_name] = {
                "data_split_object": split_object,
                "splits": {}
            }
            # update overall nodes and edges
            self.node_keys.update(split_object.node_keys)
            self.edge_keys.update(split_object.edge_keys)
            self.original_element_names.update(split_object.original_element_names)

            if "splits" in split_value:
                self._create_data_split_objects(split_value["splits"], current_data_split_dict[split_name]["splits"])


    def get_data_split(self, *args):
        args_copy = copy.copy(list(args))
        current_dict_level = self.data_splits
        for arg in args:
            current_arg = args_copy.pop(0)

            # if it's the last argument, check for an experiment at the current level
            if len(args_copy) == 0:
                try:
                    data_split = current_dict_level[current_arg]["data_split_object"]
                except KeyError:
                    raise KeyError(f"No data split at path {".".join(args)}")

            else:
                current_dict_level = current_dict_level[current_arg]["splits"]

        return data_split
