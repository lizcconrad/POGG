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

from pogg_semantics.pogg_config import POGGCompositionConfig
from pogg_semantics.semantic_composition import SemanticAlgebra, SemanticComposition, SEMENTUtil

from pogg.lexicon import POGGLexicon, POGGLexiconAutoFiller
from pogg.data_handling import POGGDataset, POGGDataSplit, POGGGraphUtil
from pogg.evaluation import (POGGEvaluation, POGGGraphEvaluation, POGGDataPointEvaluation,
                             POGGGraphReporting, POGGDataPointReporting, POGGDatasetReporting)
from pogg.graph_to_SEMENT import POGGGraphConverter


class POGGExperiment:
    def __init__(self,
                 lexicon: POGGLexicon,
                 data_split: POGGDataSplit,
                 split_info: Dict,
                 experiment_dict: Dict,
                 sub_experiments: List = None):

        self.data_split = data_split
        self.lexicon = lexicon

        self.composition_config = POGGCompositionConfig(experiment_dict["composition_config"])

        self.experiment_name = experiment_dict["experiment_name"]
        self.SEMENT_processing = experiment_dict["SEMENT_processing"]
        self.result_processing = experiment_dict["result_processing"]

        # check if the output/report dir exists already, add a counter if so
        output_dir = experiment_dict["experiment_output_dir"]
        # if os.path.isdir(experiment_dict["experiment_output_dir"]):
        #     non_existent = False
        #     counter = 1
        #     while not non_existent:
        #         output_dir = f"{experiment_dict["experiment_output_dir"]}_{counter}"
        #         if not os.path.isdir(output_dir):
        #             non_existent = True
        #         else:
        #             counter += 1
        self.output_dir = output_dir

        report_dir = experiment_dict["experiment_report_dir"]
        # if os.path.isdir(experiment_dict["experiment_report_dir"]):
        #     non_existent = False
        #     counter = 1
        #     while not non_existent:
        #         report_dir = f"{experiment_dict["experiment_report_dir"]}_{counter}"
        #         if not os.path.isdir(report_dir):
        #             non_existent = True
        #         else:
        #             counter += 1
        self.report_dir = report_dir

        self.full_data_split_name = split_info["full_data_split_name"]
        self.data_dir = Path(split_info["split_data_dir"])
        self.root = split_info["root"]
        self.leaf = split_info["leaf"]

        if self.leaf:
            self.graph_dot_dir = Path(split_info["graph_dot_dir"])
            self.graph_json_dir = Path(split_info["graph_json_dir"])
            self.graph_png_dir = Path(split_info["graph_png_dir"])

        self.graph_converter = POGGGraphConverter(self.composition_config, self.lexicon)
        self.evaluation = POGGEvaluation(self.experiment_name)

        self.sub_experiments = sub_experiments


    def run_POGG_data_to_text_single_graph(self, graph_name, graph_dict):
        graph_obj = graph_dict["graph"]
        gold_outputs = graph_dict["gold_outputs"]

        # try to find evaluation information from subexperiment
        if self.sub_experiments:
            for sub_experiment in self.sub_experiments:
                for data_point_name, data_point_eval in sub_experiment.evaluation.data_point_evaluations.items():
                    for sub_exp_graph_eval_key, sub_exp_graph_eval in data_point_eval.graph_evaluations.items():
                        if graph_dict["graph_json"] == sub_exp_graph_eval.graph_json:
                            print(
                                f"Found evaluation for {graph_name} in subexperiment {sub_experiment.full_data_split_name} ({sub_exp_graph_eval_key})... copying...")
                            # TODO: can't do deepcopy so the SEMENTs inside this object are the same object as the original
                            # i don't think this matters anywhere because i should be doing duplicate_SEMENT() anywhere i want to modify
                            # but should probably make this more robust
                            graph_evaluation = copy.copy(sub_exp_graph_eval)

                            # change the name of the graph from the graph_name in the subexperiment to the name of the graph in the current experiment
                            graph_evaluation.graph_name = graph_name

                            return graph_evaluation


        # try to find evaluation information from other graphs already generated for this split
        # that is, sometimes the same graph is used across multiple data points so avoid recomposing/generating
        for data_point_eval_key, data_point_eval in self.evaluation.data_point_evaluations.items():
            for graph_key, graph in data_point_eval.graphs.items():
                if graph_dict["graph_json"] == graph["graph_json"]:
                    print(
                        f"Found evaluation for {graph_name} in from previous data point ({data_point_eval.data_point_name})... copying...")
                    # TODO: can't do deepcopy so the SEMENTs inside this object are the same object as the original
                    # i don't think this matters anywhere because i should be doing duplicate_SEMENT() anywhere i want to modify
                    # but should probably make this more robust
                    graph_evaluation = copy.copy(data_point_eval.graph_evaluations[graph_key])

                    # change the name of the graph from the graph_name in the subexperiment to the name of the graph in the current experiment
                    graph_evaluation.graph_name = graph_name

                    return graph_evaluation



        # if evaluation from a subexperiment was not found, proceed with conversion
        graph_evaluation = POGGGraphEvaluation(graph_name, graph_dict)

        # Perform graph -> SEMENT conversion and save result to evaluation object
        sement = self.graph_converter.convert_graph_to_SEMENT(graph_obj, graph_evaluation, None)
        graph_evaluation.set_SEMENT(sement)

        # If SEMENT is created, perform English text generation
        if sement is not None:
            # collapse EQs for easier reading
            collapsed_sement = SEMENTUtil.overwrite_eqs(sement)
            graph_evaluation.set_collapsed_SEMENT(collapsed_sement)

            final_sement = self.graph_converter.semantic_algebra.prepare_for_generation(sement)
            graph_evaluation.set_prepped_SEMENT(final_sement)

            # TODO: make this configurable, for now just choose one or the other
            with ace.ACEGenerator(self.graph_converter.composition_config.grammar_location, ['-r', 'root_gen_nopass']) as generator:
                response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                results = response.results()

            # if there aren't results using nopass, ease up and allow passive,
            if len(results) == 0:
                with ace.ACEGenerator(self.graph_converter.composition_config.grammar_location, ['-r', 'root_gen']) as generator:
                    response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                    results = response.results()

            # if still no results from generating full sentences, try fragments
            if len(results) == 0:
                with ace.ACEGenerator(self.graph_converter.composition_config.grammar_location, ['-r', 'root_frag']) as generator:
                    response = generator.interact(graph_evaluation.prepped_SEMENT_string)
                    results = response.results()

            # Store results in evaluation object
            for r in results:
                graph_evaluation.generated_results.add(r['surface'])

        #Calculate evaluation metrics
        graph_evaluation.calculate_metrics()

        return graph_evaluation

    def run_POGG_data_to_text_single_data_point(self, data_point_name, data_point_dict):

        data_point_evaluation = POGGDataPointEvaluation(data_point_name, data_point_dict)

        for graph_name, graph_dict in data_point_dict["graphs"].items():
            print(f"Converting {graph_name}...")

            # convert graph, get eval obj back
            graph_evaluation = self.run_POGG_data_to_text_single_graph(graph_name, graph_dict)

            # TODO: add to POGGDataPointEvaluation
            data_point_evaluation.add_graph(graph_name, graph_evaluation)

            # add to POGGEvaluation
            # TODO: don't do this separately in the future but for now just leave it
            self.evaluation.add_graph(graph_name, graph_evaluation)

        # return POGGDataPointEvaluation
        data_point_evaluation.calculate_metrics()
        return data_point_evaluation

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

        data_point_counter = 0
        for data_point_name, data_point in self.data_split.data_points.items():
            data_point_counter += 1
            print(f"Converting {data_point_name} (data_point {data_point_counter} of {len(self.data_split.data_points.keys())})...")
            data_point_evaluation = self.run_POGG_data_to_text_single_data_point(data_point_name, data_point)

            # TODO: WEE WOO
            self.evaluation.add_data_point(data_point_name, data_point_evaluation)

        # Calculate metrics for full dataset
        self.evaluation.calculate_metrics()
        return self.evaluation


    # def store_evaluation_report(self):
    #     """
    #     Store an evaluation report after running the data-to-text algorithm on the dataset.
    #
    #     See the dropdown for the structure of the report's directory.
    #     Note that most JSON files are just meant to enable reading in the evaluation report later for comparing metrics between runs.
    #     The `txt` files, on the other hand are meant to be human-readable for analyzing the results yourself.
    #
    #     :::{info} Directory structure of the report
    #     :collapsible:
    #     ```txt
    #     - evaluation/                   <-- evaluation output from POGG algorithm will be stored here
    #         - single_runs/              <-- evaluation reports from this function are stored here
    #             - 20260702_123456/      <-- each run's top level directory is named after the time that the run started
    #                 - 20260702_123456_graph_notes.json      <-- take notes here about the results of each graph if desired
    #                 - eval_metadata.json
    #                 - dataset_eval.json
    #                 - lexicon.json
    #                 - dataset_report.txt    <-- readable report of the dataset-level metrics
    #                 - complete_graphs/      <-- graphs with full element coverage, inclusion, and gold results generated
    #                     - graph_name/
    #                         - nodes/            <-- contains JSON files of node evaluation information
    #                         - edges/            <-- contains JSON files of edge evaluation information
    #                         - graph_name_evaluation.json
    #                         - graph_name_evaluation.txt     <-- readable report of the graph-level metrics
    #                         - graph_name.dot
    #                         - graph_name.json
    #                 - incomplete_graphs/
    #                     - full_inclusion/
    #                         - full_inclusion_no_results/    <-- all elements included in final MRS, but no text results generated
    #                         - full_inclusion_w_results/     <-- all elements included in final MRS, but *gold* text results not generated
    #                     - gold_covered/                     <-- not all elements included in final MRS, but all gold text results generated
    #                     - true_incomplete/                  <-- none of the above
    #     ```
    #     :::
    #
    #     **Returns**
    #     | Type | Description |
    #     | ---- | ----------- |
    #     | `None` | -- |
    #     """
    #
    #    # TODO: add metadata to txt report then move metadata into the dataset_eval json
    #
    #     # 0. create the directory for this run's evaluation
    #     run_eval_dir = Path(self.output_dir, f"{self.full_data_split_name}_eval")
    #     Path(run_eval_dir).mkdir(parents=True, exist_ok=True)
    #
    #     # create a file for notes about each graph
    #     graph_notes = {}
    #
    #     # 1. store the metadata for the eval
    #     eval_metadata = {
    #         "run_id": self.evaluation.run_id,
    #         "experiment_name": self.experiment_name,
    #         "dataset_name": self.full_data_split_name,
    #         "dataset_location": str(self.evaluation.dataset_location),
    #         "semantic_algebra_functions_available": sorted(list(self.evaluation.sem_alg_fxns_available)),
    #         "semantic_composition_functions_available": sorted(list(self.evaluation.sem_comp_fxns_available)),
    #     }
    #
    #     with open(Path(run_eval_dir, 'eval_metadata.json'), 'w') as f:
    #         f.write(json.dumps(eval_metadata, indent=4))
    #
    #     # 2. dump all entries
    #     self.lexicon.dump_all_lexicon_entries_to_file(Path(run_eval_dir, f"{self.lexicon.name}_lexicon_all_entries.json"))
    #
    #     # 3. store eval files for whole dataset
    #     with open(Path(run_eval_dir, 'dataset_eval.json'), 'w') as f:
    #         f.write(json.dumps(self.evaluation.get_top_level_dict_representation(), indent=4))
    #
    #     with open(Path(run_eval_dir, 'dataset_report.txt'), 'w') as f:
    #         f.write(POGGDatasetReporting.build_dataset_report(eval_metadata, self.evaluation))
    #
    #
    #
    #     # 4. store eval files for graphs
    #     complete_graphs_dir = Path(run_eval_dir, "complete_graphs")
    #     incomplete_graphs_dir = Path(run_eval_dir, "incomplete_graphs")
    #
    #     full_inclusion_dir = Path(incomplete_graphs_dir, "full_inclusion")
    #     full_inclusion_w_results = Path(full_inclusion_dir, "full_inclusion_w_results")
    #     full_inclusion_no_results = Path(full_inclusion_dir, "full_inclusion_no_results")
    #
    #     gold_covered_but_incomplete = Path(incomplete_graphs_dir, "gold_covered")
    #
    #     true_incomplete = Path(incomplete_graphs_dir, "true_incomplete")
    #
    #
    #     Path.mkdir(complete_graphs_dir, parents=True, exist_ok=True)
    #     Path.mkdir(incomplete_graphs_dir, parents=True, exist_ok=True)
    #     Path.mkdir(full_inclusion_dir, parents=True, exist_ok=True)
    #     Path.mkdir(full_inclusion_w_results, parents=True, exist_ok=True)
    #     Path.mkdir(full_inclusion_no_results, parents=True, exist_ok=True)
    #     Path.mkdir(gold_covered_but_incomplete, parents=True, exist_ok=True)
    #     Path.mkdir(true_incomplete, parents=True, exist_ok=True)
    #
    #     for graph_name in self.evaluation.graph_evaluations:
    #         graph_notes[graph_name] = {
    #             "tags": {
    #             }
    #         }
    #
    #         graph_evaluation = self.evaluation.graph_evaluations[graph_name]
    #
    #         # add some tags
    #         if graph_evaluation.node_coverage == 1.0:
    #             graph_notes[graph_name]["tags"]["full_node_coverage"] = ""
    #         if graph_evaluation.edge_coverage == 1.0:
    #             graph_notes[graph_name]["tags"]["full_edge_coverage"] = ""
    #         if graph_evaluation.node_inclusion == 1.0:
    #             graph_notes[graph_name]["tags"]["full_node_inclusion"] = ""
    #         if graph_evaluation.edge_inclusion == 1.0:
    #             graph_notes[graph_name]["tags"]["full_edge_inclusion"] = ""
    #
    #         if graph_evaluation.generated_SEMENT is None:
    #             graph_notes[graph_name]["tags"]["no_SEMENT"] = ""
    #         else:
    #             graph_notes[graph_name]["tags"]["generated_SEMENT"] = ""
    #
    #         if len(graph_evaluation.generated_results) == 0:
    #             graph_notes[graph_name]["tags"]["no_text_results"] = ""
    #         else:
    #             graph_notes[graph_name]["tags"]["generated_text_results"] = ""
    #
    #         if graph_evaluation.gold_output_generation_coverage == 1.0:
    #             graph_notes[graph_name]["tags"]["full_gold_generation_coverage"] = ""
    #         if graph_evaluation.generation_comment and "cycle" in graph_evaluation.generation_comment.lower():
    #             graph_notes[graph_name]["tags"]["cycle"] = ""
    #
    #         graph_report = POGGGraphReporting.build_graph_report_detail(graph_evaluation)
    #
    #         # determine which subdirectory the graph's eval folder goes in
    #         full_gold_coverage = graph_evaluation.gold_output_generation_coverage == 1.0
    #         full_node_cov_and_incl = graph_evaluation.node_coverage == 1.0 and graph_evaluation.node_inclusion == 1.0
    #         full_edge_cov_and_incl = (graph_evaluation.edge_coverage == 1.0 and graph_evaluation.edge_inclusion == 1.0) or graph_evaluation.edge_count == 0.0
    #
    #         # if coverage and inclusion are 100%...
    #         if full_node_cov_and_incl and full_edge_cov_and_incl:
    #             # ... and gold coverage is 100% ...
    #             if full_gold_coverage:
    #                 graph_eval_dir = Path(complete_graphs_dir, graph_name)
    #             # or ...
    #             else:
    #                 # if results are generated (but the gold ones aren't covered) ...
    #                 if len(graph_evaluation.generated_results) > 0:
    #                     graph_eval_dir = Path(full_inclusion_w_results, graph_name)
    #                 # if there are no results
    #                 else:
    #                     graph_eval_dir = Path(full_inclusion_no_results, graph_name)
    #         # if coverage and inclusion are NOT 100% ...
    #         else:
    #             # ... and gold coverage is 100% ...
    #             if full_gold_coverage:
    #                 graph_eval_dir = Path(gold_covered_but_incomplete, graph_name)
    #             else:
    #                 graph_eval_dir = Path(true_incomplete, graph_name)
    #
    #         # store all eval files for the graph
    #         Path.mkdir(graph_eval_dir, parents=True, exist_ok=True)
    #         with open(Path(graph_eval_dir, graph_name + "_evaluation.txt"), "w") as file:
    #             file.write(graph_report)
    #         with open(Path(graph_eval_dir, graph_name + "_evaluation.json"), "w") as file:
    #             file.write(json.dumps(graph_evaluation.get_top_level_dict_representation(), indent=4))
    #
    #         # store json file for the nodes
    #         # create directory for node_evaluation jsons
    #         nodes_dir = Path(graph_eval_dir, "nodes")
    #         Path.mkdir(nodes_dir, parents=True, exist_ok=True)
    #         for node_evaluation_key in graph_evaluation.node_evaluations:
    #
    #             # TODO: make this more robust...
    #             # remove slashes from node_key if they're there
    #             file_name_node_key = re.sub(r"[\./\"]", "_", node_evaluation_key)
    #             with open(Path(nodes_dir, file_name_node_key + "_evaluation.json"), "w") as file:
    #                 file.write(json.dumps(graph_evaluation.node_evaluations[node_evaluation_key].get_dict_representation(), indent=4))
    #
    #         # store json file for the edges
    #         # create directory for edge_evaluation jsons
    #         edges_dir = Path(graph_eval_dir, "edges")
    #         Path.mkdir(edges_dir, parents=True, exist_ok=True)
    #
    #         for edge_evaluation in graph_evaluation.edge_evaluations:
    #             # TODO: make this more robust...
    #             # remove slashes from node_key if they're there
    #             file_name_edge_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)
    #             file_name_parent_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)
    #             file_name_child_name = re.sub(r"[\./\"]", "_", edge_evaluation.edge_name)
    #
    #             with open(Path(edges_dir, file_name_edge_name + "_" + file_name_parent_name
    #                                       + "_to_" + file_name_child_name + "_evaluation.json"), "w") as file:
    #                 file.write(json.dumps(edge_evaluation.get_dict_representation(), indent=4))
    #
    #         # write dot file
    #         POGGGraphUtil.write_graph_to_dot(graph_evaluation.graph, Path(graph_eval_dir, graph_name + ".dot"))
    #         # write graph json file
    #         POGGGraphUtil.write_graph_to_json(graph_evaluation.graph, graph_evaluation.gold_outputs, Path(graph_eval_dir, graph_name + ".json"))
    #
    #
    #     # print graph_notes file
    #     with open(Path(run_eval_dir, "graph_notes.json"), "w") as file:
    #         # sort the graph names
    #         sorted_graph_notes = dict(sorted(graph_notes.items()))
    #         file.write(json.dumps(sorted_graph_notes, indent=4))

    def store_experiment_results(self):
        # 0. create the directory for this run's evaluation
        run_eval_dir = Path(self.output_dir, f"{self.full_data_split_name}_eval")
        Path(run_eval_dir).mkdir(parents=True, exist_ok=True)

        # create a file for notes about each graph
        graph_notes = {}

        # 1. store the metadata for the eval
        eval_metadata = {
            "run_id": self.evaluation.run_id,
            "experiment_name": self.experiment_name,
            "grammar_location": self.composition_config.grammar_location,
            "SEMI_location": self.composition_config.SEMI_location,
            "dataset_name": self.full_data_split_name,
            "dataset_location": str(self.evaluation.dataset_location),
            "semantic_algebra_functions_available": sorted(list(self.evaluation.sem_alg_fxns_available)),
            "semantic_composition_functions_available": sorted(list(self.evaluation.sem_comp_fxns_available)),

        }

        with open(Path(run_eval_dir, 'run_metadata.json'), 'w') as f:
            f.write(json.dumps(eval_metadata, indent=4))

        # 2. store lexicon (a little redundant to do this for every split but sometimes I just run one split so whatever)
        self.lexicon.dump_all_lexicon_entries_to_file(Path(run_eval_dir, "lexicon_all_entries.json"))

        # 3. store eval files for whole dataset
        with open(Path(run_eval_dir, 'dataset_metrics.json'), 'w') as f:
            f.write(json.dumps(self.evaluation.get_POGG_metrics_dict(), indent=4))

        # 4. store eval files for each data point
        for data_point_name, data_point_evaluation in self.evaluation.data_point_evaluations.items():
            data_point_output_dir = Path(run_eval_dir, "data_points", data_point_name)
            Path.mkdir(data_point_output_dir, parents=True, exist_ok=True)

            # with open(Path(data_point_output_dir, data_point_name + ".json"), "w") as f:
            #     json.dump(data_point_evaluation.graph_json, f, indent=4)

            with open(Path(data_point_output_dir, data_point_name + "_metrics.json"), "w") as f:
                metrics_dict = data_point_evaluation.get_POGG_metrics_dict()
                json.dump(metrics_dict, f, indent=4)

            # 4. store eval files for each graph
            for graph_name, graph_evaluation in data_point_evaluation.graph_evaluations.items():
                graph_output_dir = Path(data_point_output_dir, "graphs", graph_name)
                Path.mkdir(graph_output_dir, parents=True, exist_ok=True)

                with open(Path(graph_output_dir, graph_name + ".json"), "w") as f:
                    json.dump(graph_evaluation.graph_json, f, indent=4)

                with open(Path(graph_output_dir, graph_name + "_metrics.json"), "w") as f:
                    json.dump(graph_evaluation.get_POGG_metrics_dict(), f, indent=4)

                with open(Path(graph_output_dir, graph_name + "_text_outputs.json"), "w") as f:
                    json.dump(graph_evaluation.get_text_outputs_dict(), f, indent=4)


    def _make_report_graph_directories(self):
        graph_report_dir = Path(self.report_dir, "graphs")
        graph_report_dir.mkdir(parents=True, exist_ok=True)
        complete_graphs = Path(graph_report_dir, "complete")
        complete_graphs.mkdir(parents=True, exist_ok=True)
        incomplete_graphs = Path(graph_report_dir, "incomplete")
        incomplete_graphs.mkdir(parents=True, exist_ok=True)
        full_inclusion = Path(incomplete_graphs, "full_inclusion")
        full_inclusion.mkdir(parents=True, exist_ok=True)
        gold_covered = Path(incomplete_graphs, "gold_covered")
        gold_covered.mkdir(parents=True, exist_ok=True)
        full_inclusion_no_results = Path(full_inclusion, "full_inclusion_no_results")
        full_inclusion_no_results.mkdir(parents=True, exist_ok=True)
        full_inclusion_w_results = Path(full_inclusion, "full_inclusion_w_results")
        full_inclusion_w_results.mkdir(parents=True, exist_ok=True)
        true_incomplete = Path(incomplete_graphs, "true_incomplete")
        true_incomplete.mkdir(parents=True, exist_ok=True)
        return complete_graphs, full_inclusion_w_results, full_inclusion_no_results, gold_covered, true_incomplete

    def store_experiment_report(self, dataset_report=True, data_point_reports=True, graph_reports=True, dot_files=True):
        if dataset_report:
            Path(self.report_dir).mkdir(parents=True, exist_ok=True)
            with open(Path(self.report_dir, "dataset_report.txt"), "w") as f:
                f.write(POGGDatasetReporting.build_dataset_report(self))


        if data_point_reports:
            data_point_reports_dir = Path(self.report_dir, "data_points")

            for data_point_name, data_point_eval in self.evaluation.data_point_evaluations.items():

                current_data_point_dir = Path(data_point_reports_dir, data_point_name)
                Path(current_data_point_dir).mkdir(parents=True, exist_ok=True)

                with open(Path(current_data_point_dir, data_point_name + "_report.txt"), "w") as f:
                    f.write(POGGDataPointReporting.build_data_point_report(data_point_eval))


                # now loop through graphs...
                if graph_reports:
                    graph_report_dir = Path(current_data_point_dir, "graphs")
                    Path(graph_report_dir).mkdir(parents=True, exist_ok=True)
                    for graph_name, graph_eval in data_point_eval.graph_evaluations.items():
                        with open(Path(graph_report_dir, graph_name + "_report.txt"), "w") as f:
                            f.write(POGGGraphReporting.build_graph_report_detail(graph_eval))

                        if dot_files:
                            with open(Path(graph_report_dir, graph_name + ".dot"), "w") as f:
                                POGGGraphUtil.write_graph_to_dot(graph_eval.graph, f)




class POGGExperimentsConfig:
    def __init__(self, experiment_config_path: Path | str, run_name: str=None):
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
                    previous_run_name = run_name
                    while not non_existent:
                        new_run_name = f"{run_name}_{counter}"
                        anchor = anchor.replace(previous_run_name, new_run_name)
                        if not os.path.isdir(anchor):
                            non_existent = True
                        else:
                            counter +=1
                            previous_run_name = new_run_name
                    run_name = new_run_name

            config_string = config_string.replace("EXPERIMENT_RUN_PLACEHOLDER", run_name)
            config_json = json.loads(config_string)

        for key in config_json:
            if key != "splits":
                setattr(self, key, config_json[key])

        self.dataset = POGGDataset(config_json)
        self.lexicons = self._create_lexicon_objects(config_json)

        self.experiments = {}
        self._create_experiment_objects(config_json, self.experiments)

    def _create_lexicon_objects(self, config_json):
        lexicons = {}
        for key, val in config_json["lexicons"].items():
            lexicons[key] = POGGLexicon(val["lexicon_dir"], self.dataset)
        return lexicons


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
            split_info = current_json_split["split_info"]

            data_split = self.dataset.get_data_split(*split_info["data_split_path"])

            for exp_key, exp in current_json_split["experiments"].items():
                lexicon = self.lexicons[exp["lexicon_name"]]

                # if it's NOT a leaf experiment, aggregate experiment objects from subsplits
                if not split_info["leaf"]:
                    # create experiment object from exp + subsplit_exps
                    # comp_config, lexicon, data_split, experiment_dict, sub_experiments
                    exp_obj = POGGExperiment(lexicon, data_split,
                                             split_info, exp, copy.copy(subsplit_experiments[exp_key]))
                    # add to the experiment_dict
                    current_exp_obj_dict[exp_key] = exp_obj
                else:
                    # create experiment object
                    exp_obj = POGGExperiment(lexicon, data_split, split_info, exp)
                    # add to the experiment_dict
                    current_exp_obj_dict[exp_key] = exp_obj

                    # add to collection of subsplit_experiments
                    if exp_key not in subsplit_experiments:
                        subsplit_experiments[exp_key] = [exp_obj]
                    else:
                        subsplit_experiments[exp_key].append(exp_obj)

        return subsplit_experiments


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


    def get_single_experiment(self, *args):
        args_copy = copy.copy(list(args))
        current_dict_level = self.experiments["splits"]
        for arg in args:
            current_arg = args_copy.pop(0)

            # if it's the second to last argument, data split found; grab experiment
            if len(args_copy) == 1:
                exp_arg = args_copy.pop(0)
                try:
                    experiment = current_dict_level[current_arg][exp_arg]
                    return experiment
                except KeyError:
                    raise KeyError(f"No experiment named {exp_arg} split at path {".".join(args[0:-1])}")

            else:
                current_dict_level = current_dict_level[current_arg]["splits"]