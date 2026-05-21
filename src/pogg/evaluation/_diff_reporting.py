import datetime
from pathlib import Path
import json
from prettytable import PrettyTable
from pogg.evaluation._diff import POGGEvaluationDiff, POGGGraphEvaluationDiff

class POGGDatasetDiffReporting:
    @staticmethod
    def build_ASCII_metadata_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        metadata_diff_table = PrettyTable([
            "Metadata Metric",
            "Base Run Value",
            "Comparison Run Value",
            "Delta (Comparison minus Base)"])
        metadata_diff_table.title = "DATASET METADATA METRIC DELTAS"
        metadata_diff_table.align = "l"

        metadata_diff_table.add_row([
            "Number of Graphs in Dataset",
            base_run_dataset_eval.graph_count,
            comparison_run_dataset_eval.graph_count,
            evaluation_diff.graph_count_delta
        ])

        metadata_diff_table.add_row([
            "Number of Nodes in Dataset",
            base_run_dataset_eval.full_node_count,
            comparison_run_dataset_eval.full_node_count,
            evaluation_diff.full_node_count_delta
        ])

        metadata_diff_table.add_row([
            "Number of Edges in Dataset",
            base_run_dataset_eval.full_edge_count,
            comparison_run_dataset_eval.full_edge_count,
            evaluation_diff.full_edge_count_delta
        ])

        return metadata_diff_table

    @staticmethod
    def build_ASCII_graph_metrics_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        graph_metrics_diff_table = PrettyTable([
            "Graph Evaluation Metric",
            "Base Run Value",
            "Comparison Run Value",
            "Delta (Comparison minus Base)"])
        graph_metrics_diff_table.title = "DATASET GRAPH EVALUATION METRIC DELTAS"
        graph_metrics_diff_table.align = "l"

        graph_metrics_diff_table.add_row([
            "Graphs that produced a SEMENT (count)",
            base_run_dataset_eval.graph_SEMENT_count,
            comparison_run_dataset_eval.graph_SEMENT_count,
            evaluation_diff.graph_SEMENT_count_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced a SEMENT (% coverage)",
            base_run_dataset_eval.graph_SEMENT_coverage,
            comparison_run_dataset_eval.graph_SEMENT_coverage,
            evaluation_diff.graph_SEMENT_coverage_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced text results (count)",
            base_run_dataset_eval.graphs_with_text_count,
            comparison_run_dataset_eval.graphs_with_text_count,
            evaluation_diff.graphs_with_text_count_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced text results (% coverage)",
            base_run_dataset_eval.graphs_with_text_coverage,
            comparison_run_dataset_eval.graphs_with_text_coverage,
            evaluation_diff.graphs_with_text_coverage_delta
        ])

        return graph_metrics_diff_table

    @staticmethod
    def build_ASCII_node_metrics_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        node_metrics_diff_table = PrettyTable([
            "Node Evaluation Metric",
            "Base Run Value",
            "Comparison Run Value",
            "Delta (Comparison minus Base)"])
        node_metrics_diff_table.title = "DATASET NODE METRIC DELTAS"
        node_metrics_diff_table.align = "l"

        node_metrics_diff_table.add_row([
            "Node Count",
            base_run_dataset_eval.full_node_count,
            comparison_run_dataset_eval.full_node_count,
            evaluation_diff.full_node_count_delta
        ], divider=True)

        node_metrics_diff_table.add_row([
            "Nodes Covered (count)",
            base_run_dataset_eval.full_nodes_covered,
            comparison_run_dataset_eval.full_nodes_covered,
            evaluation_diff.full_nodes_covered_delta
        ])

        node_metrics_diff_table.add_row([
            "Node Coverage",
            base_run_dataset_eval.full_node_coverage,
            comparison_run_dataset_eval.full_node_coverage,
            evaluation_diff.full_node_coverage_delta
        ], divider=True)

        node_metrics_diff_table.add_row([
            "Nodes Included (count)",
            base_run_dataset_eval.full_nodes_included,
            comparison_run_dataset_eval.full_nodes_included,
            evaluation_diff.full_nodes_included_delta
        ])

        node_metrics_diff_table.add_row([
            "Node Inclusion",
            base_run_dataset_eval.full_node_inclusion,
            comparison_run_dataset_eval.full_node_inclusion,
            evaluation_diff.full_node_inclusion_delta
        ])

        return node_metrics_diff_table

    @staticmethod
    def build_ASCII_edge_metrics_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        edge_metrics_diff_table = PrettyTable([
            "Edge Evaluation Metric",
            "Base Run Value",
            "Comparison Run Value",
            "Delta (Comparison minus Base)"])
        edge_metrics_diff_table.title = "DATASET EDGE METRIC DELTAS"
        edge_metrics_diff_table.align = "l"

        edge_metrics_diff_table.add_row([
            "Edge Count",
            base_run_dataset_eval.full_edge_count,
            comparison_run_dataset_eval.full_edge_count,
            evaluation_diff.full_edge_count_delta
        ], divider=True)

        edge_metrics_diff_table.add_row([
            "Edges Covered (count)",
            base_run_dataset_eval.full_edges_covered,
            comparison_run_dataset_eval.full_edges_covered,
            evaluation_diff.full_edges_covered_delta
        ])

        edge_metrics_diff_table.add_row([
            "Edge Coverage",
            base_run_dataset_eval.full_edge_coverage,
            comparison_run_dataset_eval.full_edge_coverage,
            evaluation_diff.full_edge_coverage_delta
        ], divider=True)

        edge_metrics_diff_table.add_row([
            "Edges Included (count)",
            base_run_dataset_eval.full_edges_included,
            comparison_run_dataset_eval.full_edges_included,
            evaluation_diff.full_edges_included_delta
        ])

        edge_metrics_diff_table.add_row([
            "Edge Inclusion",
            base_run_dataset_eval.full_edge_inclusion,
            comparison_run_dataset_eval.full_edge_inclusion,
            evaluation_diff.full_edge_inclusion_delta
        ])

        return edge_metrics_diff_table

    @staticmethod
    def build_ASCII_sem_alg_functions_available_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_alg_fxns_available_diff_table = PrettyTable([
            "Available in base run only",
            "Available in base run only (count)",
            "Available in comparison run only",
            "Available in comparison run only (count)"])
        sem_alg_fxns_available_diff_table.title = "SEMANTIC ALGEBRA FUNCTIONS AVAILABLE DELTAS"
        sem_alg_fxns_available_diff_table.align = "l"

        sem_alg_fxns_available_diff_table.add_row([
            sorted(list(evaluation_diff.base_only_sem_alg_fxns)),
            evaluation_diff.base_only_sem_alg_fxns_count,
            sorted(list(evaluation_diff.comparison_only_sem_alg_fxns)),
            evaluation_diff.comparison_only_sem_alg_fxns_count
        ])

        return sem_alg_fxns_available_diff_table

    @staticmethod
    def build_ASCII_sem_comp_functions_available_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_comp_fxns_available_diff_table = PrettyTable([
            "Available in base run only",
            "Available in base run only (count)",
            "Available in comparison run only",
            "Available in comparison run only (count)"])
        sem_comp_fxns_available_diff_table.title = "SEMANTIC COMPOSITION FUNCTIONS AVAILABLE DELTAS"
        sem_comp_fxns_available_diff_table.align = "l"

        sem_comp_fxns_available_diff_table.add_row([
            sorted(list(evaluation_diff.base_only_sem_comp_fxns)),
            evaluation_diff.base_only_sem_comp_fxns_count,
            sorted(list(evaluation_diff.comparison_only_sem_comp_fxns)),
            evaluation_diff.comparison_only_sem_comp_fxns_count
        ])

        return sem_comp_fxns_available_diff_table

    # @staticmethod
    # def build_ASCII_sem_comp_functions_used_diff_table(evaluation_diff):
    #     base_run_dataset_eval = evaluation_diff.base_run
    #     comparison_run_dataset_eval = evaluation_diff.comparison_run
    #
    #     sem_comp_fxns_used_diff_table = PrettyTable([
    #         "Used in base run only",
    #         "Used in base run only (count)",
    #         "Used in comparison run only",
    #         "Used in comparison run only (count)"])
    #     sem_comp_fxns_used_diff_table.title = "SEMANTIC COMPOSITION FUNCTIONS USED DELTAS"
    #     sem_comp_fxns_used_diff_table.align = "l"
    #
    #     sem_comp_fxns_used_diff_table.add_row([
    #         sorted(list(base_run_dataset_eval.sem_comp_fxns_used)),
    #         evaluation_diff.base_only_sem_comp_fxns_count,
    #         sorted(list(comparison_run_dataset_eval.sem_comp_fxns_used)),
    #         evaluation_diff.comparison_only_sem_comp_fxns_count
    #     ])
    #
    #     return sem_comp_fxns_used_diff_table

    @staticmethod
    def build_ASCII_graph_metrics_diff_report(evaluation_diff):
        report = f"DATASET: {evaluation_diff.experiment_name}\n"
        report += f"BASE RUN ID: {evaluation_diff.base_eval.run_id}\n"
        report += f"COMPARISON RUN ID: {evaluation_diff.comparison_eval.run_id}\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_metadata_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_graph_metrics_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_node_metrics_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_edge_metrics_diff_table(evaluation_diff)) + "\n\n"
        return report

    @staticmethod
    def store_diff_report(evaluation_path, base_run, comparison_run):
        eval_diff = POGGEvaluationDiff(base_run, comparison_run)

        # probably put this in POGGDatasetReporting ... maybe more store_evaluation_report there too
        now = datetime.datetime.now()
        diff_report_id = now.strftime("%m%d%Y_%H%M%S")
        eval_diff_path = Path(evaluation_path, "diff_report")

        # create the directory to store the diff report
        eval_diff_path.mkdir(parents=True, exist_ok=True)

        # 1. store the metadata about the diff report
        diff_metadata_json = {
            "diff_report_id": diff_report_id,
            "dataset_name": base_run.dataset_name,
            "base_run_data": base_run.get_top_level_dict_representation(),
            "comparison_run_data": comparison_run.get_top_level_dict_representation()
        }
        with open(Path(eval_diff_path, "diff_metadata.json"), 'w') as f:
            f.write(json.dumps(diff_metadata_json, indent=4))

        # 2. store the deltas for all the metrics
        data_diff_report_json = eval_diff.get_dict_representation()
        with open(Path(eval_diff_path, "dataset_diff.json"), 'w') as f:
            f.write(json.dumps(data_diff_report_json, indent=4))

        # 3. store readable text report of dataset deltas
        with open(Path(eval_diff_path, "graph_metrics_diff.txt"), 'w') as f:
            f.write(POGGDatasetDiffReporting.build_ASCII_graph_metrics_diff_table(eval_diff))

        unchanged_graphs_path = Path(eval_diff_path, "unchanged_graphs")
        changed_graphs_path = Path(eval_diff_path, "changed_graphs")

        graph_names = set(base_run.graph_evaluations.keys())
        graph_names.update(comparison_run.graph_evaluations.keys())
        base_only_graphs = []
        comparison_only_graphs = []
        unchanged_graphs = []
        for graph_name in graph_names:
            if graph_name not in base_run.graph_evaluations.keys():
                comparison_only_graphs.append(graph_name)
            elif graph_name not in comparison_run.graph_evaluations.keys():
                base_only_graphs.append(graph_name)
            else:
                base_graph_eval = base_run.graph_evaluations[graph_name]
                comparison_graph_eval = comparison_run.graph_evaluations[graph_name]
                graph_eval_diff = POGGGraphEvaluationDiff(graph_name, base_graph_eval, comparison_graph_eval)

                if graph_eval_diff.diff_detected:
                    graph_diff_dir = Path(changed_graphs_path, graph_name)
                    graph_diff_dir.mkdir(parents=True, exist_ok=True)
                    with open(Path(graph_diff_dir, "graph_diff.json"), 'w') as f:
                        f.write(json.dumps(graph_eval_diff.get_dict_representation(), indent=4))
                else:
                    unchanged_graphs.append(graph_name)

        with open(Path(eval_diff_path, "unchanged_graphs.txt"), 'w') as f:
            f.write("\n".join(unchanged_graphs))
