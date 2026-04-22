"""
This module contains the POGG class, which has key objects as instance attributes (e.g. `POGGDataset` and `POGGGraphConverter`).
It also has instance methods for running the POGG data-to-text algorithm .

[See usage examples here.](project:/usage_nbs/pogg/pogg_routine_usage.ipynb)
"""
import copy
import os
from typing import List
import datetime
from pathlib import Path
import json
import re
from delphin import ace
from typing import List, Dict, overload

from pogg.lexicon.auto_lexicon import POGGLexiconAutoFiller
from pogg.lexicon.lexicon_builder import POGGLexiconUtil, POGGLexicon
from pogg.data_handling.pogg_dataset import POGGDataset
from pogg.evaluation.evaluation import POGGEvaluation, POGGGraphEvaluation
from pogg.pogg_config import POGGCompositionConfig
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.data_handling.graph_util import POGGGraphUtil
from pogg.semantic_composition.sement_util import POGGSEMENTUtil
from pogg.evaluation.reporting import POGGGraphReporting, POGGDatasetReporting


#
# class POGGExperiment:
#     """
#     Holds all key objects necessary to run the data-to-text algorithm.
#     """
#
#     # def run_POGG_data_to_text_algorithm_on_single_graph(self, given_graph_name, graph_object=None):
#     #     """
#     #     Run the POGG data-to-text algorithm on a single graph.
#     #     If no object is given, the function searches for a file with the given graph name in the data directory.
#     #     Otherwise, it uses the provided object.
#     #
#     #     **Parameters**
#     #     | Parameter | Type | Description | Default |
#     #     | --------- | ---- | ----------- | ------- |
#     #     | `given_graph_name` | `str` | name of the graph | -- |
#     #     | `graph_object` | `dict` or `DiGraph` | either a NetworkX graph or a graph in the POGG JSON format | `None` |
#     #
#     #     **Returns**
#     #     | Type | Description |
#     #     | ---- | ----------- |
#     #     | `POGGGraphEvaluation` | evaluation object with results of running the data-to-text algorithm on the given graph |
#     #     """
#     #
#     #     graph = None
#     #
#     #     if graph_object is not None:
#     #         if isinstance(graph_object, dict):
#     #             graph = POGGGraphUtil.build_graph(graph_object)
#     #         else:
#     #             graph = graph_object
#     #     else:
#     #         for graph_name in os.listdir(dataset.graph_json_dir):
#     #             graph_name_stem = graph_name.split('.')[0]
#     #             graph_path = os.path.join(dataset.graph_json_dir, graph_name)
#     #
#     #             # if the path does not point to a JSON file, skip it
#     #             if not os.path.isfile(graph_path) or not graph_path.endswith('.json'):
#     #                 continue
#     #
#     #             if graph_name_stem == given_graph_name:
#     #                 print(f"Converting {graph_path}...")
#     #                 graph_json = json.load(open(graph_path))
#     #                 graph = POGGGraphUtil.build_graph(graph_json)
#     #                 break
#     #
#     #         if graph is None:
#     #             raise FileNotFoundError(f"Graph {given_graph_name} not found")
#     #
#     #     graph_evaluation = POGGGraphEvaluation(graph, given_graph_name)
#     #
#     #
#     #     # store the gold outputs in the evaluation object
#     #     try:
#     #         with open(Path(dataset.gold_outputs_dir, given_graph_name + ".txt"), "r") as gold_outputs_file:
#     #             graph_evaluation.gold_outputs = gold_outputs_file.read().splitlines()
#     #     except FileNotFoundError:
#     #         # no gold outputs
#     #         graph_evaluation.gold_outputs = []
#     #
#     #     # 3. Perform graph -> SEMENT conversion and save result to evaluation object
#     #     sement = self.graph_converter.convert_graph_to_SEMENT(graph, graph_evaluation, None)
#     #     graph_evaluation.set_SEMENT(sement)
#     #
#     #     # 4. If SEMENT is created, perform English text generation
#     #     if sement is not None:
#     #         # collapse EQs for easier reading
#     #         collapsed_sement = POGGSEMENTUtil.overwrite_eqs(sement)
#     #         graph_evaluation.set_collapsed_SEMENT(collapsed_sement)
#     #
#     #         final_sement = self.semantic_algebra.prepare_for_generation(sement)
#     #         graph_evaluation.set_prepped_SEMENT(final_sement)
#     #
#     #         with ace.ACEGenerator(self.pogg_config.grammar_location, ['-r', 'root_frag']) as generator:
#     #             response = generator.interact(graph_evaluation.prepped_SEMENT_string)
#     #             results = response.results()
#     #
#     #         # 5. Store results in evaluation object
#     #         for r in results:
#     #             graph_evaluation.generated_results.append(r['surface'])
#     #
#     #     # 6. Calculate evaluation metrics
#     #     graph_evaluation.calculate_metrics()
#     #
#     #     return graph_evaluation
#     #
#




class POGGExperiment:
    def __init__(self, composition_config: Path | str | POGGCompositionConfig, experiment_dict: Dict, sub_experiments: List=None):

        self.experiment_name = experiment_dict["experiment_name"]
        self.full_data_split_name = experiment_dict["full_data_split_name"]
        self.lexicon_name = experiment_dict["lexicon_name"]
        self.leaf = experiment_dict["leaf"]

        self.SEMENT_processing = experiment_dict["SEMENT_processing"]
        self.result_processing = experiment_dict["result_processing"]

        self.data_dir = Path(experiment_dict["experiment_data_dir"])
        self.lexicon_dir = Path(experiment_dict["experiment_lex_dir"])
        self.evaluation_dir = Path(experiment_dict["experiment_eval_dir"])

        if self.leaf:
            self.graph_dot_dir = Path(experiment_dict["graph_dot_dir"])
            self.graph_json_dir = Path(experiment_dict["graph_json_dir"])
            self.graph_png_dir = Path(experiment_dict["graph_png_dir"])

        if sub_experiments:
            self.sub_experiments = copy.copy(sub_experiments)
            graphs_to_aggregate = [x.dataset.graphs for x in self.sub_experiments]
            self.dataset = POGGDataset(self.full_data_split_name, graphs_to_aggregate)
        else:
            self.sub_experiments = None
            self.dataset = POGGDataset(self.full_data_split_name, self.graph_json_dir)

        if "inherited_lexicons" in experiment_dict:
            inherited_lexicon_paths = [Path(x) for x in experiment_dict["inherited_lexicons"]]
        else:
            inherited_lexicon_paths = None
        self.lexicon = POGGLexicon(self.lexicon_name, self.lexicon_dir, self.dataset, inherited_lexicon_paths)
        self.graph_converter = POGGGraphConverter(composition_config, self.lexicon)
        self.evaluation = POGGEvaluation(self.experiment_name)


    def run_POGG_data_to_text_single_graph(self, graph_name, graph_dict):
        graph_obj = graph_dict["graph"]
        gold_outputs = graph_dict["gold_outputs"]

        # try to find evaluation information from subexperiment
        if self.sub_experiments:
            for sub_experiment in self.sub_experiments:
                if graph_name in sub_experiment.dataset.graphs:
                    print(f"Found evaluation for {graph_name} in subexperiment... copying...")
                    graph_evaluation = sub_experiment.evaluation.graph_evaluations[graph_name]
                    return graph_evaluation

        # if evaluation from a subexperiment was not found, proceed with conversion
        graph_evaluation = POGGGraphEvaluation(graph_obj, graph_name)
        graph_evaluation.gold_outputs = gold_outputs

        # Perform graph -> SEMENT conversion and save result to evaluation object
        sement = self.graph_converter.convert_graph_to_SEMENT(graph_obj, graph_evaluation, None)
        graph_evaluation.set_SEMENT(sement)

        # If SEMENT is created, perform English text generation
        if sement is not None:
            # collapse EQs for easier reading
            collapsed_sement = POGGSEMENTUtil.overwrite_eqs(sement)
            graph_evaluation.set_collapsed_SEMENT(collapsed_sement)

            final_sement = self.graph_converter.semantic_algebra.prepare_for_generation(sement)
            graph_evaluation.set_prepped_SEMENT(final_sement)

            with ace.ACEGenerator(self.graph_converter.composition_config.grammar_location, ['-r', 'root_frag']) as generator:
                response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                results = response.results()

            # Store results in evaluation object
            for r in results:
                graph_evaluation.generated_results.append(r['surface'])

        #Calculate evaluation metrics
        graph_evaluation.calculate_metrics()

        return graph_evaluation


    def run_experiment(self):
        """
        Run the POGG data-to-text algorithm on a dataset.
        """

        # 0. store run metadata
        now = datetime.datetime.now()
        self.evaluation.run_id = now.strftime("%m%d%Y_%H%M%S")
        self.evaluation.dataset_location = self.data_dir
        self.evaluation.lexicon = self.lexicon

        # TODO: a little hacky but oh well...
        self.evaluation.sem_alg_fxns_available = set(
            [method_name for method_name in dir(SemanticAlgebra)
             if callable(getattr(SemanticAlgebra, method_name)) and not re.match("__.*__", method_name)])
        self.evaluation.sem_alg_fxns_available.remove('_get_slots')
        self.evaluation.sem_alg_fxns_available.remove('prepare_for_generation')

        self.evaluation.sem_comp_fxns_available = set(
            [method_name for method_name in dir(SemanticComposition)
                if callable(getattr(SemanticComposition, method_name)) and not re.match("__.*__", method_name)])

        for i, graph_tuple in enumerate(self.dataset.graphs.items()):
            graph_name = graph_tuple[0]
            graph_dict = graph_tuple[1]
            print(f"Converting {graph_name} (graph {i + 1} of {len(self.dataset.graphs)})...")

            # convert graph, get eval obj back
            graph_evaluation = self.run_POGG_data_to_text_single_graph(graph_name, graph_dict)

            # add to POGGEvaluation
            self.evaluation.add_graph(graph_dict["graph"], graph_name, graph_evaluation)

        # Calculate metrics for full dataset
        self.evaluation.calculate_metrics()
        return self.evaluation


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

        # 0. create the directory for this run's evaluation
        run_eval_dir = Path(self.evaluation_dir, f"{self.full_data_split_name}_eval")
        Path(run_eval_dir).mkdir(parents=True, exist_ok=True)

        # create a file for notes about each graph
        graph_notes = {}

        # 1. store the metadata for the eval
        eval_metadata = {
            "run_id": self.evaluation.run_id,
            "experiment_name": self.experiment_name,
            "dataset_name": self.full_data_split_name,
            "dataset_location": str(self.evaluation.dataset_location),
            "semantic_algebra_functions_available": sorted(list(self.evaluation.sem_alg_fxns_available)),
            "semantic_composition_functions_available": sorted(list(self.evaluation.sem_comp_fxns_available)),
        }

        # 2. dump the lexicon
        POGGLexiconUtil.dump_complete_lexicon_object_to_json(Path(run_eval_dir, "lexicon.json"), self.evaluation.lexicon)

        with open(Path(run_eval_dir, 'eval_metadata.json'), 'w') as f:
            f.write(json.dumps(eval_metadata, indent=4))

        # 3. store eval files for whole dataset
        with open(Path(run_eval_dir, 'dataset_eval.json'), 'w') as f:
            f.write(json.dumps(self.evaluation.get_top_level_dict_representation(), indent=4))

        with open(Path(run_eval_dir, 'dataset_report.txt'), 'w') as f:
            f.write(POGGDatasetReporting.build_ASCII_dataset_report(eval_metadata, self.evaluation))



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

                # TODO: make this more robust...
                # remove slashes from node_key if they're there
                file_name_node_key = re.sub(r"[\./\"]", "_", node_evaluation_key)
                with open(Path(nodes_dir, file_name_node_key + "_evaluation.json"), "w") as file:
                    file.write(json.dumps(graph_evaluation.node_evaluations[node_evaluation_key].get_dict_representation(), indent=4))

            # store json file for the edges
            # create directory for edge_evaluation jsons
            edges_dir = Path(graph_eval_dir, "edges")
            Path.mkdir(edges_dir, parents=True, exist_ok=True)

            for edge_evaluation in graph_evaluation.edge_evaluations:
                # TODO: make this more robust...
                # remove slashes from node_key if they're there
                file_name_edge_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)
                file_name_parent_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)
                file_name_child_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)

                with open(Path(edges_dir, file_name_edge_name + "_" + file_name_parent_name
                                          + "_to_" + file_name_child_name + "_evaluation.json"), "w") as file:
                    file.write(json.dumps(edge_evaluation.get_dict_representation(), indent=4))

            # write dot file
            POGGGraphUtil.write_graph_to_dot(graph_evaluation.graph, Path(graph_eval_dir, graph_name + ".dot"))
            # write graph json file
            POGGGraphUtil.write_graph_to_json(graph_evaluation.graph, graph_evaluation.gold_outputs, Path(graph_eval_dir, graph_name + ".json"))


        # print graph_notes file
        with open(Path(run_eval_dir, self.evaluation.run_id + "_graph_notes.json"), "w") as file:
            # sort the graph names
            sorted_graph_notes = dict(sorted(graph_notes.items()))
            file.write(json.dumps(sorted_graph_notes, indent=4))


class POGGExperimentConfig:
    def __init__(self, composition_config_path: Path | str, experiment_config_path: Path | str, run_name: str=None):
        with open(experiment_config_path, "r") as f:
            config_json = json.load(f)
            # dump back to string and do EXPERIMENT_RUN_PLACEHOLDER replacement
            config_string = json.dumps(config_json)
            if run_name is None:
                now = datetime.datetime.now()
                run_name = now.strftime("%m%d%Y_%H%M%S")
            else:
                anchor = config_json["evaluation_run_anchor"]
                anchor = anchor.replace("EXPERIMENT_RUN_PLACEHOLDER", run_name)
                if os.path.isdir(anchor):
                    non_existent = False
                    counter = 1
                    while not non_existent:
                        new_run_name = f"{run_name}_{counter}"
                        anchor = anchor.replace(run_name, new_run_name)
                        run_name = new_run_name
                        if not os.path.isdir(anchor):
                            non_existent = True
                        else:
                            counter +=1

            config_string = config_string.replace("EXPERIMENT_RUN_PLACEHOLDER", run_name)
            config_json = json.loads(config_string)

        for key in config_json:
            if key != "splits":
                setattr(self, key, config_json[key])

        self.composition_config = POGGCompositionConfig(composition_config_path)
        self.experiments = {}
        self._create_experiment_objects(config_json, self.experiments)


    def _create_experiment_objects(self, current_json_split, current_exp_obj_dict):
        subsplit_experiments = {}
        if "splits" in current_json_split:
            current_exp_obj_dict["splits"] = {}
            for subsplit_key, subsplit in current_json_split["splits"].items():

                current_exp_obj_dict["splits"][subsplit_key] = {}

                # recurse down to sub-splits
                result = self._create_experiment_objects(subsplit, current_exp_obj_dict["splits"][subsplit_key])
                for key in result:
                    if key in subsplit_experiments:
                        subsplit_experiments[key].extend(result[key])
                    else:
                        subsplit_experiments[key] = result[key]

        # use results to build aggregate-level experiments
        if "experiments" in current_json_split:
            for exp_key, exp in current_json_split["experiments"].items():
                # if it's NOT a leaf experiment, aggregate experiment objects from subsplits
                if not exp["leaf"]:
                    # create experiment object from exp + subsplit_exps
                    exp_obj = POGGExperiment(self.composition_config, exp, subsplit_experiments[exp_key])
                    # add to the experiment_dict
                    current_exp_obj_dict[exp_key] = exp_obj
                else:
                    # create experiment object
                    exp_obj = POGGExperiment(self.composition_config, exp)
                    # add to the experiment_dict
                    current_exp_obj_dict[exp_key] = exp_obj

                    # add to collection of subsplit_experiments
                    if exp_key not in subsplit_experiments:
                        subsplit_experiments[exp_key] = [exp_obj]
                    else:
                        subsplit_experiments[exp_key].append(exp_obj)

        return subsplit_experiments

    def get_leaf_lexicons(self, experiments=None, leaf_lexicons=None):
        if experiments is None:
            experiments = self.experiments
        if leaf_lexicons is None:
            leaf_lexicons = set()

        for key, obj in experiments.items():
            if isinstance(obj, POGGExperiment):
                if obj.leaf:
                    leaf_lexicons.add(obj.lexicon)
            else:
                self.get_leaf_lexicons(obj, leaf_lexicons)

        return list(leaf_lexicons)


    def get_ancestor_lexicons(self, lexicon, experiment=None, ancestor_lexicons=None):
        if experiment is None:
            experiment = self.experiments
        if ancestor_lexicons is None:
            ancestor_lexicons = set()

        if isinstance(experiment, POGGExperiment):
            if experiment.leaf:
                return
            else:
                for sub_experiment in experiment.sub_experiments:
                   if lexicon == sub_experiment.lexicon:
                       ancestor_lexicons.add(experiment.lexicon)
        else:
            for val in experiment.values():
                self.get_ancestor_lexicons(lexicon, val, ancestor_lexicons)

        return ancestor_lexicons

    def get_experiment(self, *args):
        args_copy = copy.copy(list(args))
        current_dict_level = self.experiments
        for arg in args:
            current_arg = args_copy.pop(0)

            # if it's the last argument, check for an experiment at the current level
            if len(args_copy) == 0:
                try:
                    experiment = current_dict_level[current_arg]
                except KeyError:
                    raise KeyError(f"No experiment called {current_arg} at path {".".join(args)}")

            else:
                current_dict_level = current_dict_level["splits"][current_arg]

        return experiment


    def get_all_experiments(self, experiment_type=None, current_dict_level=None, experiments=None):
        if current_dict_level is None:
            current_dict_level = self.experiments
        if experiments is None:
            experiments = []

        for key, val in current_dict_level.items():
            if isinstance(val, POGGExperiment):
                if experiment_type is not None:
                    if val.experiment_name == experiment_type:
                        experiments.append(val)
                else:
                    experiments.append(val)
            else:
                self.get_all_experiments(experiment_type, val, experiments)

        return experiments


    def run_all_experiments(self):
        experiments = self.get_all_experiments()

        for i, experiment in enumerate(experiments):
            print(f"Running {experiment.full_data_split_name}__{experiment.experiment_name} (experiment {i + 1} of {len(experiments)})...")
            experiment.run_experiment()
            experiment.store_evaluation_report()



