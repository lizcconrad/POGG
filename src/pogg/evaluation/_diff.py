from pathlib import Path

class POGGGraphEvaluationDiff:
    def __init__(self, graph_name, base_graph_eval, comparison_graph_eval):
        self.graph_name = graph_name

        self.base_graph_eval = base_graph_eval
        self.comparison_graph_eval = comparison_graph_eval

        self.node_count_delta = self.comparison_graph_eval.node_count - self.base_graph_eval.node_count
        self.nodes_covered_delta = self.comparison_graph_eval.nodes_covered - self.base_graph_eval.nodes_covered
        self.node_coverage_delta = self.comparison_graph_eval.node_coverage - self.base_graph_eval.node_coverage
        self.nodes_included_delta = self.comparison_graph_eval.nodes_included - self.base_graph_eval.nodes_included
        self.node_inclusion_delta = self.comparison_graph_eval.node_inclusion - self.base_graph_eval.node_inclusion

        self.edge_count_delta = self.comparison_graph_eval.edge_count - self.base_graph_eval.edge_count
        self.edges_covered_delta = self.comparison_graph_eval.edges_covered - self.base_graph_eval.edges_covered
        self.edge_coverage_delta = self.comparison_graph_eval.edge_coverage - self.base_graph_eval.edge_coverage
        self.edges_included_delta = self.comparison_graph_eval.edges_included - self.base_graph_eval.edges_included
        self.edge_inclusion_delta = self.comparison_graph_eval.edge_inclusion - self.base_graph_eval.edge_inclusion

        self.sem_comp_fxns_used_delta = set(self.comparison_graph_eval.sem_comp_fxns_used) - set(
            self.base_graph_eval.sem_comp_fxns_used)
        self.sem_comp_fxns_used_delta_count = len(self.sem_comp_fxns_used_delta)

        # flag to determine if there was a change
        self.metrics_changed = self.get_changed_metrics()
        self.diff_detected = len(self.metrics_changed) > 0

    def get_changed_metrics(self):
        metrics_changed = []
        if self.node_count_delta != 0:
            metrics_changed.append("node_count")
        if self.edge_count_delta != 0:
            metrics_changed.append("edge_count")

        if self.nodes_covered_delta != 0:
            metrics_changed.append("nodes_covered")
        if self.node_coverage_delta != 0:
            metrics_changed.append("node_coverage")
        if self.nodes_included_delta != 0:
            metrics_changed.append("nodes_included")
        if self.node_inclusion_delta != 0:
            metrics_changed.append("node_inclusion")

        if self.edges_covered_delta != 0:
            metrics_changed.append("edges_covered")
        if self.edge_coverage_delta != 0:
            metrics_changed.append("edge_coverage")
        if self.edges_included_delta != 0:
            metrics_changed.append("edges_included")
        if self.edge_inclusion_delta != 0:
            metrics_changed.append("edge_inclusion")

        return metrics_changed

    def get_dict_representation(self):
        return {
            "graph_name": self.graph_name,

            "node_count_delta": self.node_count_delta,
            "nodes_covered_delta": self.nodes_covered_delta,
            "node_coverage_delta": self.node_coverage_delta,
            "nodes_included_delta": self.nodes_included_delta,
            "node_inclusion_delta": self.node_inclusion_delta,

            "edge_count_delta": self.edge_count_delta,
            "edges_covered_delta": self.edges_covered_delta,
            "edge_coverage_delta": self.edge_coverage_delta,
            "edges_included_delta": self.edges_included_delta,
            "edge_inclusion_delta": self.edge_inclusion_delta,

            "sem_comp_fxns_used_delta": sorted(list(self.sem_comp_fxns_used_delta)),
            "sem_comp_fxns_used_delta_count": self.sem_comp_fxns_used_delta_count,
        }


class POGGEvaluationDiff:
    """
    A `POGGEvaluationDiff` object stores information comparing evaluation metrics between two runs on the same dataset.
    """

    def __init__(self, base_eval, comparison_eval, diff_path=None):
        """
        Initialize the `POGGEvaluation` object by providing the name of the dataset.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `previous_run` | `POGGEvaluation` | evaluation object for one run of POGG's data-to-text algorithm |
        | `current_run` | `POGGEvaluation` | evaluation object for another, more recent, run of POGG's data-to-text algorithm on the same dataset |
        """

        self.base_eval = base_eval
        self.comparison_eval = comparison_eval
        if diff_path:
            self.diff_path = diff_path

        # check that run was performed on the same dataset
        # TODO: right now just using dataset name as the check for this
        # TODO: a better check would actually confirm the graphs are the same
        if self.base_eval.experiment_name != self.comparison_eval.experiment_name:
            raise ValueError(
                "Dataset names do not match; runs were not performed on the same dataset, so a diff report can't be created")

        self.experiment_name = self.base_eval.experiment_name

        # TODO: first key is graph name and has previous_run:POGGGraphEvaluation and current_run:POGGGraphEvaluation
        self.graph_evaluations = {}
        self.graph_evaluation_diffs = {}
        graph_names = set(self.base_eval.graph_evaluations.keys())
        graph_names.update(set(self.comparison_eval.graph_evaluations.keys()))
        for graph_name in graph_names:
            previous_graph_eval = self.base_eval.graph_evaluations[graph_name]
            current_graph_eval = self.comparison_eval.graph_evaluations[graph_name]
            self.graph_evaluations[graph_name] = {
                "previous_run": previous_graph_eval,
                "current_run": current_graph_eval,
            }
            self.graph_evaluation_diffs[graph_name] = POGGGraphEvaluationDiff(graph_name, previous_graph_eval,
                                                                              current_graph_eval)

        # deltas of evaluation metrics
        self.graph_count_delta = self.comparison_eval.graph_count - self.base_eval.graph_count
        self.graph_SEMENT_count_delta = self.comparison_eval.graph_SEMENT_count - self.base_eval.graph_SEMENT_count
        # TODO: is this how you calculate percentage changes....?
        self.graph_SEMENT_coverage_delta = self.comparison_eval.graph_SEMENT_coverage - self.base_eval.graph_SEMENT_coverage
        # NOT number of results, but number that generated text
        self.graphs_with_text_count_delta = self.comparison_eval.graphs_with_text_count - self.base_eval.graphs_with_text_count
        self.graphs_with_text_coverage_delta = self.comparison_eval.graph_SEMENT_coverage - self.base_eval.graph_SEMENT_coverage

        self.full_node_count_delta = self.comparison_eval.full_node_count - self.base_eval.full_node_count
        self.full_nodes_covered_delta = self.comparison_eval.full_nodes_covered - self.base_eval.full_nodes_covered
        self.full_nodes_included_delta = self.comparison_eval.full_nodes_included - self.base_eval.full_nodes_included
        self.full_node_coverage_delta = self.comparison_eval.full_node_coverage - self.base_eval.full_node_coverage
        self.full_node_inclusion_delta = self.comparison_eval.full_node_inclusion - self.base_eval.full_node_inclusion
        self.full_edge_count_delta = self.comparison_eval.full_edge_count - self.base_eval.full_edge_count
        self.full_edges_covered_delta = self.comparison_eval.full_edges_covered - self.base_eval.full_edges_covered
        self.full_edges_included_delta = self.comparison_eval.full_edges_included - self.base_eval.full_edges_included
        self.full_edge_coverage_delta = self.comparison_eval.full_edge_coverage - self.base_eval.full_edge_coverage
        self.full_edge_inclusion_delta = self.comparison_eval.full_edge_inclusion - self.base_eval.full_edge_inclusion

        # TODO: should be quantitative as well as listing what new functions were added
        self.base_only_sem_alg_fxns = set([fxn for fxn in self.base_eval.sem_alg_fxns_available if
                                           fxn not in self.comparison_eval.sem_alg_fxns_available])
        self.base_only_sem_alg_fxns_count = len(self.base_only_sem_alg_fxns)
        self.comparison_only_sem_alg_fxns = set([fxn for fxn in self.comparison_eval.sem_alg_fxns_available if
                                                 fxn not in self.base_eval.sem_alg_fxns_available])
        self.comparison_only_sem_alg_fxns_count = len(self.comparison_only_sem_alg_fxns)

        self.base_only_sem_comp_fxns = set([fxn for fxn in self.base_eval.sem_comp_fxns_available if
                                            fxn not in self.comparison_eval.sem_comp_fxns_available])
        self.base_only_sem_comp_fxns_count = len(self.base_only_sem_comp_fxns)
        self.comparison_only_sem_comp_fxns = set([fxn for fxn in self.comparison_eval.sem_comp_fxns_available if
                                                  fxn not in self.base_eval.sem_comp_fxns_available])
        self.comparison_only_sem_comp_fxns_count = len(self.comparison_only_sem_comp_fxns)

        self.sem_comp_fxns_used_base = self.base_eval.sem_comp_fxns_used
        self.sem_comp_fxns_used_comparison = self.comparison_eval.sem_comp_fxns_used
        self.sem_comp_fxns_used_count_delta = self.comparison_eval.sem_comp_fxns_used_count - self.base_eval.sem_comp_fxns_used_count
        self.sem_comp_fxns_used_coverage_delta = self.comparison_eval.sem_comp_fxns_used_coverage - self.base_eval.sem_comp_fxns_used_coverage

    def get_dict_representation(self):
        return {
            'graph_count_delta': self.graph_count_delta,
            'graph_SEMENT_count_delta': self.graph_SEMENT_count_delta,
            'graph_SEMENT_coverage_delta': self.graph_SEMENT_coverage_delta,
            'graphs_with_text_count_delta': self.graphs_with_text_count_delta,
            'graphs_with_text_coverage_delta': self.graphs_with_text_coverage_delta,

            'full_node_count_delta': self.full_node_count_delta,
            'full_nodes_covered_delta': self.full_nodes_covered_delta,
            'full_nodes_included_delta': self.full_nodes_included_delta,
            'full_node_coverage_delta': self.full_node_coverage_delta,
            'full_node_inclusion_delta': self.full_node_inclusion_delta,

            'full_edge_count_delta': self.full_edge_count_delta,
            'full_edges_covered_delta': self.full_edges_covered_delta,
            'full_edges_included_delta': self.full_edges_included_delta,
            'full_edge_coverage_delta': self.full_edge_coverage_delta,
            'full_edge_inclusion_delta': self.full_edge_inclusion_delta,

            'base_only_sem_alg_fxns': sorted(list(self.base_only_sem_alg_fxns)),
            'base_only_sem_alg_fxns_count': self.base_only_sem_alg_fxns_count,
            'comparison_only_sem_alg_fxns': sorted(list(self.comparison_only_sem_alg_fxns)),
            'comparison_only_sem_alg_fxns_count': self.comparison_only_sem_alg_fxns_count,

            'base_only_sem_comp_fxns': sorted(list(self.base_only_sem_comp_fxns)),
            'base_only_sem_comp_fxns_count': self.base_only_sem_comp_fxns_count,
            'comparison_only_sem_comp_fxns': sorted(list(self.comparison_only_sem_comp_fxns)),
            'comparison_only_sem_comp_fxns_count': self.comparison_only_sem_comp_fxns_count,

            'sem_comp_fxns_used_base': sorted(list(self.sem_comp_fxns_used_base)),
            'sem_comp_fxns_used_comparison': sorted(list(self.sem_comp_fxns_used_comparison)),
            'sem_comp_fxns_used_count_delta': self.sem_comp_fxns_used_count_delta,
            'sem_comp_fxns_used_coverage_delta': self.sem_comp_fxns_used_coverage_delta
        }


class POGGEvaluationDiffConfig:
    def __init__(self, diff_config_path: Path | str):
        with open(diff_config_path, 'r') as f:
            config_json = json.load(f)

        for key in config_json:
            if key != "diffs":
                setattr(self, key, config_json[key])

        self.diff_setups = {}
        self._create_diff_objects(config_json, self.diff_setups)

    def _create_diff_objects(self, current_json_split, current_dict):
        subsplit_diffs = {}
        if "splits" in current_json_split:
            current_dict["splits"] = {}
            for subsplit_key, subsplit in current_json_split["splits"].items():

                current_dict["splits"][subsplit_key] = {}

                # recurse down to sub-splits
                result = self._create_diff_objects(subsplit, current_dict["splits"][subsplit_key])
                for key in result:
                    if key in subsplit_diffs:
                        subsplit_diffs[key].extend(result[key])
                    else:
                        subsplit_diffs[key] = result[key]

        # use results to build aggregate-level diffs
        if "diffs" in current_json_split:
            for diff_key, diff in current_json_split["diffs"].items():
                # read in eval object from baseline_dir and comparison_dir
                baseline_eval_dir = Path(diff["baseline_dir"], diff["eval_dir_name"])
                comparison_eval_dir = Path(diff["comparison_dir"], diff["eval_dir_name"])

                basline_eval = POGGEvaluation(evaluation_dir=baseline_eval_dir)
                comparison_eval = POGGEvaluation(evaluation_dir=comparison_eval_dir)

                eval_diff = POGGEvaluationDiff(basline_eval, comparison_eval, diff["diff_dir"])

                # if it's NOT a leaf diff, aggregate diff objects from subsplits
                if not diff["leaf"]:
                    # add to the diff_dict
                    current_dict[diff_key] = eval_diff
                else:
                    # add to the diff_dict
                    current_dict[diff_key] = eval_diff

                    # add to collection of subsplit_diffs
                    if diff_key not in subsplit_diffs:
                        subsplit_diffs[diff_key] = [eval_diff]
                    else:
                        subsplit_diffs[diff_key].append(eval_diff)

        return subsplit_diffs

    def get_all_diffs(self, current_dict_level=None, diffs=None):
        if current_dict_level is None:
            current_dict_level = self.diff_setups
        if diffs is None:
            diffs = []

        for key, val in current_dict_level.items():
            if isinstance(val, POGGEvaluationDiff):
                diffs.append(val)
            else:
                self.get_all_diffs(val, diffs)

        return diffs