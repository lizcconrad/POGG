"""
This module contains the POGG class, which has key objects as instance attributes (e.g. `POGGDataset` and `POGGGraphConverter`).
It also has instance methods for running the POGG data-to-text algorithm .

[See usage examples here.](project:/usage_nbs/pogg/pogg_routine_usage.ipynb)
"""

import os
import datetime
from pathlib import Path
import json
import re
from delphin import ace

from pogg.lexicon.lexicon_builder import POGGLexiconUtil
from pogg.pogg_config import POGGConfig
from pogg.data_handling.pogg_dataset import POGGDataset
from pogg.evaluation.evaluation import POGGEvaluation, POGGGraphEvaluation
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.data_handling.graph_util import POGGGraphUtil
from pogg.semantic_composition.sement_util import POGGSEMENTUtil
from pogg.evaluation.reporting import POGGGraphReporting, POGGDatasetReporting


class POGG:
    """
    Holds all key objects necessary to run the data-to-text algorithm.
    """
    def __init__(self, config_file, dataset_file):
        """
         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ------------ |
        | `config_file` | `str` | path to the YAML file which contains the configuration information |
        | `dataset_file` | `str` | filepath where the config file detailing directories relevant to the dataset |

        :::{example} POGGConfig YAML file example
        :collapsible:
        ```
        # top level directory
        data_dir: "/absolute/path/to/dataset/directory"

        # subdirectories
        # Grammar information
        grammar_location: ./ERG/ERG_2023/erg-2023.dat
        SEMI: ./ERG/ERG_2023/trunk/etc/erg.smi
        ```
        :::

        :::{example} POGGDataset YAML example
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

        Provided the provided YAML config files have the appropriate fields, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Type | Description |
        | --------- | ---- | ------------ |
        | `pogg_config` | `POGGConfig` | stores grammar information for text generation |
        | `dataset` | `POGGDataset` | stores each data point in the given dataset |
        | `evaluation` | `POGGEvaluation` | stores evaluation metrics for each data point as well as the dataset as a whole |
        | `semantic_algebra` | `SemanticAlgebra` | contains methods for low-level SEMENT composition |
        | `semantic_composition` | `SemanticComposition` |  contains methods for composing SEMENTs using named constructions (e.g. `prenominal_adjective`) |
        | `graph_converter` | `SemanticComposition` |  contains methods for converting graph objects to SEMENTs and then to English text |
        """
        self.pogg_config = POGGConfig(config_file)
        self.dataset = POGGDataset(dataset_file)
        self.evaluation = POGGEvaluation(self.dataset.dataset_name)
        self.semantic_algebra = SemanticAlgebra(self.pogg_config)
        self.semantic_composition = SemanticComposition(self.semantic_algebra)
        self.graph_converter = POGGGraphConverter(self.semantic_composition, self.dataset)


    def run_POGG_data_to_text_algorithm_on_single_graph(self, given_graph_name, graph_object=None):
        """
        Run the POGG data-to-text algorithm on a single graph.
        If no object is given, the function searches for a file with the given graph name in the data directory.
        Otherwise, it uses the provided object.

        **Parameters**
        | Parameter | Type | Description | Default |
        | --------- | ---- | ----------- | ------- |
        | `given_graph_name` | `str` | name of the graph | -- |
        | `graph_object` | `dict` or `DiGraph` | either a NetworkX graph or a graph in the POGG JSON format | `None` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGGraphEvaluation` | evaluation object with results of running the data-to-text algorithm on the given graph |
        """

        graph = None

        if graph_object is not None:
            if isinstance(graph_object, dict):
                graph = POGGGraphUtil.build_graph(graph_object)
            else:
                graph = graph_object
        else:
            for graph_name in os.listdir(self.dataset.graph_json_dir):
                graph_name_stem = graph_name.split('.')[0]
                graph_path = os.path.join(self.dataset.graph_json_dir, graph_name)

                # if the path does not point to a JSON file, skip it
                if not os.path.isfile(graph_path) or not graph_path.endswith('.json'):
                    continue

                if graph_name_stem == given_graph_name:
                    print(f"Converting {graph_path}...")
                    graph_json = json.load(open(graph_path))
                    graph = POGGGraphUtil.build_graph(graph_json)
                    break

            if graph is None:
                raise FileNotFoundError(f"Graph {given_graph_name} not found")

        graph_evaluation = POGGGraphEvaluation(graph, given_graph_name)


        # store the gold outputs in the evaluation object
        try:
            with open(Path(self.dataset.gold_outputs_dir, given_graph_name + ".txt"), "r") as gold_outputs_file:
                graph_evaluation.gold_outputs = gold_outputs_file.read().splitlines()
        except FileNotFoundError:
            # no gold outputs
            graph_evaluation.gold_outputs = []

        # 3. Perform graph -> SEMENT conversion and save result to evaluation object
        sement = self.graph_converter.convert_graph_to_SEMENT(graph, graph_evaluation, None)
        graph_evaluation.set_SEMENT(sement)

        # 4. If SEMENT is created, perform English text generation
        if sement is not None:
            # collapse EQs for easier reading
            collapsed_sement = POGGSEMENTUtil.overwrite_eqs(sement)
            graph_evaluation.set_collapsed_SEMENT(collapsed_sement)

            final_sement = self.semantic_algebra.prepare_for_generation(sement)
            graph_evaluation.set_prepped_SEMENT(final_sement)

            with ace.ACEGenerator(self.pogg_config.grammar_location, ['-r', 'root_frag']) as generator:
                response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                results = response.results()

            # 5. Store results in evaluation object
            for r in results:
                graph_evaluation.generated_results.append(r['surface'])

        # 6. Calculate evaluation metrics
        graph_evaluation.calculate_metrics()

        return graph_evaluation


    def run_POGG_data_to_text_algorithm(self, skip_list=None, focus_list=None):
        """
        Run the POGG data-to-text algorithm on a dataset.

        **Parameters**
        | Parameter | Type | Description | Default |
        | --------- | ---- | ----------- | ------- |
        | `skip_list` | `list` of `str` | list of names of graph files to skip | `None` |
        | `focus_list` | `list` of `str`| list of names of graph files to focus on; if this is included all other graphs are skipped | `None` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGEvaluation` | evaluation object with results of running the data-to-text algorithm on the dataset |
        """

        # 0. store run metadata
        now = datetime.datetime.now()
        self.evaluation.run_id = now.strftime("%m%d%Y_%H%M%S")

        # TODO: a little hacky but oh well...
        self.evaluation.sem_alg_fxns_available = set([method_name for method_name in dir(self.semantic_algebra)
                                                       if callable(
                getattr(self.semantic_algebra, method_name)) and not re.match("__.*__", method_name)])
        self.evaluation.sem_alg_fxns_available.remove('_get_slots')
        self.evaluation.sem_alg_fxns_available.remove('prepare_for_generation')


        self.evaluation.sem_comp_fxns_available = set([method_name for method_name in dir(self.semantic_composition)
                         if callable(getattr(self.semantic_composition, method_name)) and not re.match("__.*__", method_name)])


        # 1. loop through graphs
        for graph_name in os.listdir(self.dataset.graph_json_dir):
            graph_name_stem = graph_name.split('.')[0]
            graph_path = os.path.join(self.dataset.graph_json_dir, graph_name)

            # if the path does not point to a JSON file, skip it
            if not os.path.isfile(graph_path) or not graph_path.endswith('.json'):
                continue


            # if there's a focus list, only do graphs in that list
            if focus_list and graph_name_stem not in focus_list:
                print(f"Focus list active. Skipping {graph_path}...")
                continue
            elif skip_list and graph_name_stem in skip_list:
                print(f"{graph_path} in skip list. Skipping...")
                continue

            print(f"Converting {graph_path}...")

            graph_json = json.load(open(graph_path))

            # 2. build NetworkX graph from JSON data; create associated evaluation object
            graph = POGGGraphUtil.build_graph(graph_json)

            self.evaluation.add_graph(graph, graph_name_stem)
            # get the POGGGraphEvaluation object that was just added
            graph_evaluation = self.evaluation.graph_evaluations[graph_name_stem]

            # store the gold outputs in the evaluation object
            try:
                with open(Path(self.dataset.gold_outputs_dir, graph_name_stem + ".txt"), "r") as gold_outputs_file:
                    graph_evaluation.gold_outputs = gold_outputs_file.read().splitlines()
            except FileNotFoundError:
                # no gold outputs
                graph_evaluation.gold_outputs = []

            # 3. Perform graph -> SEMENT conversion and save result to evaluation object
            sement = self.graph_converter.convert_graph_to_SEMENT(graph, graph_evaluation, None)
            graph_evaluation.set_SEMENT(sement)

            # 4. If SEMENT is created, perform English text generation
            if sement is not None:
                # collapse EQs for easier reading
                collapsed_sement = POGGSEMENTUtil.overwrite_eqs(sement)
                graph_evaluation.set_collapsed_SEMENT(collapsed_sement)

                final_sement = self.semantic_algebra.prepare_for_generation(sement)
                graph_evaluation.set_prepped_SEMENT(final_sement)

                with ace.ACEGenerator(self.pogg_config.grammar_location, ['-r', 'root_frag']) as generator:
                    response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                    results = response.results()

                # 5. Store results in evaluation object
                for r in results:
                    graph_evaluation.generated_results.append(r['surface'])

            # 6. Calculate evaluation metrics
            graph_evaluation.calculate_metrics()


        # 8. Calculate metrics for full dataset
        self.evaluation.calculate_metrics()

        # mark run as complete
        self.evaluation.run_complete = True


    def store_evaluation_report(self):
        """
        Store an evaluation report after running the data-to-text algorithm on the dataset.

        See the dropdown for the structure of the report's directory.
        Note that most JSON files are just meant to enable reading in the evaluation report later for comparing metrics between runs.
        The `txt` files, on the other hand are meant to be human-readable for analyzing the results yourself.

        :::{info} Directory structure of the report
        :collapsible:
        ```txt
        - evaluation/                   <-- evaluation output from POGG algorithm will be stored here
            - single_runs/              <-- evaluation reports from this function are stored here
                - 20260702_123456/      <-- each run's top level directory is named after the time that the run started
                    - 20260702_123456_graph_notes.json      <-- take notes here about the results of each graph if desired
                    - eval_metadata.json
                    - dataset_eval.json
                    - lexicon.json
                    - dataset_report.txt    <-- readable report of the dataset-level metrics
                    - complete_graphs/      <-- graphs with full element coverage, inclusion, and gold results generated
                        - graph_name/
                            - nodes/            <-- contains JSON files of node evaluation information
                            - edges/            <-- contains JSON files of edge evaluation information
                            - graph_name_evaluation.json
                            - graph_name_evaluation.txt     <-- readable report of the graph-level metrics
                            - graph_name.dot
                            - graph_name.json
                    - incomplete_graphs/
                        - full_inclusion/
                            - full_inclusion_no_results/    <-- all elements included in final MRS, but no text results generated
                            - full_inclusion_w_results/     <-- all elements included in final MRS, but *gold* text results not generated
                        - gold_covered/                     <-- not all elements included in final MRS, but all gold text results generated
                        - true_incomplete/                  <-- none of the above
        ```
        :::

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """

       # TODO: add metadata to txt report then move metadata into the dataset_eval json

        # check if run_complete flag is True
        if not self.evaluation.run_complete:
            raise ValueError("The evaluation object's `run_complete` flag is False. "
                             "A run has not been completed to report evaluation information from.")


        # 0. create the directory for this run's evaluation
        run_eval_dir = Path(self.dataset.evaluation_dir, "single_runs", self.evaluation.run_id)
        Path(run_eval_dir).mkdir(parents=True, exist_ok=True)

        # create a file for notes about each graph
        graph_notes = {}

        # 1. store the metadata for the eval
        eval_metadata = {
            "run_id": self.evaluation.run_id,
            "dataset_name": self.dataset.dataset_name,
            "dataset_location": str(Path(self.dataset.data_dir).resolve()),
            "semantic_algebra_functions_available": [method_name for method_name in dir(self.semantic_algebra)
                        if callable(getattr(self.semantic_algebra, method_name)) and not re.match("__.*__", method_name)],
            "semantic_composition_functions_available": [method_name for method_name in dir(self.semantic_composition)
                         if callable(getattr(self.semantic_composition, method_name)) and not re.match("__.*__", method_name)]
        }

        # 2. dump the lexicon
        POGGLexiconUtil.dump_complete_lexicon_object_to_json(Path(run_eval_dir, "lexicon.json"), self.dataset.lexicon)

        with open(Path(run_eval_dir, 'eval_metadata.json'), 'w') as f:
            f.write(json.dumps(eval_metadata, indent=4))

        # 3. store eval files for whole dataset
        with open(Path(run_eval_dir, 'dataset_eval.json'), 'w') as f:
            f.write(json.dumps(self.evaluation.get_top_level_dict_representation(), indent=4))

        with open(Path(run_eval_dir, 'dataset_report.txt'), 'w') as f:
            f.write(POGGDatasetReporting.build_ASCII_dataset_report(self.evaluation))



        # 4. store eval files for graphs
        complete_graphs_dir = Path(run_eval_dir, "complete_graphs")
        incomplete_graphs_dir = Path(run_eval_dir, "incomplete_graphs")

        full_inclusion_dir = Path(incomplete_graphs_dir, "full_inclusion")
        full_inclusion_w_results = Path(full_inclusion_dir, "full_inclusion_w_results")
        full_inclusion_no_results = Path(full_inclusion_dir, "full_inclusion_no_results")

        gold_covered_but_incomplete = Path(incomplete_graphs_dir, "gold_covered")

        true_incomplete = Path(incomplete_graphs_dir, "true_incomplete")


        Path.mkdir(complete_graphs_dir, parents=True, exist_ok=True)
        Path.mkdir(incomplete_graphs_dir, parents=True, exist_ok=True)
        Path.mkdir(full_inclusion_dir, parents=True, exist_ok=True)
        Path.mkdir(full_inclusion_w_results, parents=True, exist_ok=True)
        Path.mkdir(full_inclusion_no_results, parents=True, exist_ok=True)
        Path.mkdir(gold_covered_but_incomplete, parents=True, exist_ok=True)
        Path.mkdir(true_incomplete, parents=True, exist_ok=True)

        for graph_name in self.evaluation.graph_evaluations:
            graph_notes[graph_name] = {
                "tags": {
                }
            }

            graph_evaluation = self.evaluation.graph_evaluations[graph_name]

            # add some tags
            if graph_evaluation.node_coverage == 1.0:
                graph_notes[graph_name]["tags"]["full_node_coverage"] = ""
            if graph_evaluation.edge_coverage == 1.0:
                graph_notes[graph_name]["tags"]["full_edge_coverage"] = ""
            if graph_evaluation.node_inclusion == 1.0:
                graph_notes[graph_name]["tags"]["full_node_inclusion"] = ""
            if graph_evaluation.edge_inclusion == 1.0:
                graph_notes[graph_name]["tags"]["full_edge_inclusion"] = ""

            if graph_evaluation.generated_SEMENT is None:
                graph_notes[graph_name]["tags"]["no_SEMENT"] = ""
            else:
                graph_notes[graph_name]["tags"]["generated_SEMENT"] = ""

            if len(graph_evaluation.generated_results) == 0:
                graph_notes[graph_name]["tags"]["no_text_results"] = ""
            else:
                graph_notes[graph_name]["tags"]["generated_text_results"] = ""

            if graph_evaluation.gold_output_generation_coverage == 1.0:
                graph_notes[graph_name]["tags"]["full_gold_generation_coverage"] = ""
            if graph_evaluation.generation_comment and "cycle" in graph_evaluation.generation_comment.lower():
                graph_notes[graph_name]["tags"]["cycle"] = ""

            graph_report = POGGGraphReporting.build_ASCII_graph_report_detail(graph_evaluation)

            # determine which subdirectory the graph's eval folder goes in
            full_gold_coverage = graph_evaluation.gold_output_generation_coverage == 1.0
            full_node_cov_and_incl = graph_evaluation.node_coverage == 1.0 and graph_evaluation.node_inclusion == 1.0
            full_edge_cov_and_incl = (graph_evaluation.edge_coverage == 1.0 and graph_evaluation.edge_inclusion == 1.0) or graph_evaluation.edge_count == 0.0

            # if coverage and inclusion are 100%...
            if full_node_cov_and_incl and full_edge_cov_and_incl:
                # ... and gold coverage is 100% ...
                if full_gold_coverage:
                    graph_eval_dir = Path(complete_graphs_dir, graph_name)
                # or ...
                else:
                    # if results are generated (but the gold ones aren't covered) ...
                    if len(graph_evaluation.generated_results) > 0:
                        graph_eval_dir = Path(full_inclusion_w_results, graph_name)
                    # if there are no results
                    else:
                        graph_eval_dir = Path(full_inclusion_no_results, graph_name)
            # if coverage and inclusion are NOT 100% ...
            else:
                # ... and gold coverage is 100% ...
                if full_gold_coverage:
                    graph_eval_dir = Path(gold_covered_but_incomplete, graph_name)
                else:
                    graph_eval_dir = Path(true_incomplete, graph_name)

            # store all eval files for the graph
            Path.mkdir(graph_eval_dir, parents=True, exist_ok=True)
            with open(Path(graph_eval_dir, graph_name + "_evaluation.txt"), "w") as file:
                file.write(graph_report)
            with open(Path(graph_eval_dir, graph_name + "_evaluation.json"), "w") as file:
                file.write(json.dumps(graph_evaluation.get_top_level_dict_representation(), indent=4))

            # store json file for the nodes
            # create directory for node_evaluation jsons
            nodes_dir = Path(graph_eval_dir, "nodes")
            Path.mkdir(nodes_dir, parents=True, exist_ok=True)
            for node_evaluation_key in graph_evaluation.node_evaluations:
                with open(Path(nodes_dir, node_evaluation_key + "_evaluation.json"), "w") as file:
                    file.write(json.dumps(graph_evaluation.node_evaluations[node_evaluation_key].get_dict_representation(), indent=4))

            # store json file for the edges
            # create directory for edge_evaluation jsons
            edges_dir = Path(graph_eval_dir, "edges")
            Path.mkdir(edges_dir, parents=True, exist_ok=True)
            for edge_evaluation in graph_evaluation.edge_evaluations:
                with open(Path(edges_dir, edge_evaluation.edge_name + "_" + edge_evaluation.parent_node_name
                                          + "_to_" + edge_evaluation.child_node_name + "_evaluation.json"), "w") as file:
                    file.write(json.dumps(edge_evaluation.get_dict_representation(), indent=4))

            # write dot file
            POGGGraphUtil.write_graph_to_dot(graph_evaluation.graph, Path(graph_eval_dir, graph_name + ".dot"))
            # write graph json file
            POGGGraphUtil.write_graph_to_json(graph_evaluation.graph, Path(graph_eval_dir, graph_name + ".json"))


        # print graph_notes file
        with open(Path(run_eval_dir, self.evaluation.run_id + "_graph_notes.json"), "w") as file:
            # sort the graph names
            sorted_graph_notes = dict(sorted(graph_notes.items()))
            file.write(json.dumps(sorted_graph_notes, indent=4))
