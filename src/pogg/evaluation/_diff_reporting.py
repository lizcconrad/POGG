import datetime
from pathlib import Path
import json
from prettytable import PrettyTable

from pogg.evaluation._diff import POGGEvaluationDiff, POGGGraphEvaluationDiff

class POGGDiffReporting:
    # functions that are used at multiple levels of granularity
    @staticmethod
    def build_sem_fxns_used_overview_table(eval_diff):
        base_run_eval = eval_diff.base_eval
        comparison_run_eval = eval_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_fxns_used_table = PrettyTable([
            "Metric",
            "Base Run Value",
            "Comparison Run Value",
            "Delta (Comparison minus Base)"])
        sem_fxns_used_table.title = "SEMANTIC FUNCTIONS USED METRICS"
        sem_fxns_used_table.align = "l"

        sem_fxns_used_table.add_row([
            "Semantic Algebra Fxns Used Count",
            len(base_run_eval.sem_alg_fxns_used),
            len(comparison_run_eval.sem_alg_fxns_used),
            len(comparison_run_eval.sem_alg_fxns_used) - len(base_run_eval.sem_alg_fxns_used),
        ])

        sem_fxns_used_table.add_row([
            "Semantic Algebra Fxns Used Coverage",
            base_run_eval.sem_alg_fxns_used_coverage,
            comparison_run_eval.sem_alg_fxns_used_coverage,
            comparison_run_eval.sem_alg_fxns_used_coverage - base_run_eval.sem_alg_fxns_used_coverage
        ])

        sem_fxns_used_table.add_row([
            "Semantic Composition Fxns Used Count",
            len(base_run_eval.sem_comp_fxns_used),
            len(comparison_run_eval.sem_comp_fxns_used),
            len(comparison_run_eval.sem_comp_fxns_used) - len(base_run_eval.sem_comp_fxns_used),
        ])

        sem_fxns_used_table.add_row([
            "Semantic Composition Fxns Used Coverage",
            base_run_eval.sem_comp_fxns_used_coverage,
            comparison_run_eval.sem_comp_fxns_used_coverage,
            comparison_run_eval.sem_comp_fxns_used_coverage - base_run_eval.sem_comp_fxns_used_coverage
        ])
        return sem_fxns_used_table

    @staticmethod
    def build_sem_alg_fxns_used_detail_table(eval_diff):
        base_run_eval = eval_diff.base_eval
        comparison_run_eval = eval_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_fxns_used_table = PrettyTable([
            "Function",
            "Base Run Times Used",
            "Comparison Times Used"])
        sem_fxns_used_table.title = "SEMANTIC ALGEBRA FUNCTIONS USED METRICS"
        sem_fxns_used_table.align = "l"

        all_alg_fxns = sorted(set(list(base_run_eval.sem_alg_fxns_available) + list(comparison_run_eval.sem_alg_fxns_available)))
        for fxn in all_alg_fxns:
            if fxn in base_run_eval.sem_alg_fxns_available:
                if fxn in base_run_eval.sem_alg_fxns_used:
                    base_run_used_count = base_run_eval.sem_alg_fxns_used[fxn]
                else:
                    base_run_used_count = 0
            else:
                base_run_used_count = "N/A"

            if fxn in comparison_run_eval.sem_alg_fxns_available:
                if fxn in comparison_run_eval.sem_alg_fxns_used:
                    comparison_run_used_count = comparison_run_eval.sem_alg_fxns_used[fxn]
                else:
                    comparison_run_used_count = 0
            else:
                comparison_run_used_count = "N/A"

            sem_fxns_used_table.add_row([
                fxn,
                base_run_used_count,
                comparison_run_used_count
            ])
        return sem_fxns_used_table

    @staticmethod
    def build_sem_comp_fxns_used_detail_table(eval_diff):
        base_run_eval = eval_diff.base_eval
        comparison_run_eval = eval_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_fxns_used_table = PrettyTable([
            "Function",
            "Base Run Times Used",
            "Comparison Times Used"])
        sem_fxns_used_table.title = "SEMANTIC COMPOSITION FUNCTIONS USED METRICS"
        sem_fxns_used_table.align = "l"

        all_comp_fxns = sorted(set(list(base_run_eval.sem_comp_fxns_available) + list(comparison_run_eval.sem_comp_fxns_available)))
        for fxn in all_comp_fxns:
            if fxn in base_run_eval.sem_comp_fxns_available:
                if fxn in base_run_eval.sem_comp_fxns_used:
                    base_run_used_count = base_run_eval.sem_comp_fxns_used[fxn]
                else:
                    base_run_used_count = 0
            else:
                base_run_used_count = "N/A"

            if fxn in comparison_run_eval.sem_comp_fxns_available:
                if fxn in comparison_run_eval.sem_comp_fxns_used:
                    comparison_run_used_count = comparison_run_eval.sem_comp_fxns_used[fxn]
                else:
                    comparison_run_used_count = 0
            else:
                comparison_run_used_count = "N/A"

            sem_fxns_used_table.add_row([
                fxn,
                base_run_used_count,
                comparison_run_used_count
            ])
        return sem_fxns_used_table


class POGGGraphDiffReporting:
    ### TABLES ###
    @staticmethod
    def build_node_metrics_table(nodes, title):
        nodes_table = PrettyTable([
            "Node",
            "Base Covered",
            "Base Included",
            "Comparison Covered",
            "Comparison Included",
            #"Base Inclusion Comment",
            "Base Generation Comment",
            #"Comparison Inclusion Comment",
            "Comparison Generation Comment", ])
        nodes_table.title = title
        nodes_table.align = "l"

        for node_key in sorted(nodes):
            base_node_eval = nodes[node_key]['base_node_eval']
            comparison_node_eval = nodes[node_key]['comparison_node_eval']
            nodes_table.add_row([
                node_key,
                base_node_eval.node_covered,
                base_node_eval.node_included,
                comparison_node_eval.node_covered,
                comparison_node_eval.node_included,
                #base_node_eval.inclusion_comment,
                base_node_eval.generation_comment,
                #comparison_node_eval.inclusion_comment,
                comparison_node_eval.generation_comment,
            ])

        return nodes_table

    @staticmethod
    def build_edge_metrics_table(edges, title):
        edges_table = PrettyTable([
            "Edge",
            "Base Covered",
            "Base Included",
            "Comparison Covered",
            "Comparison Included",
            # "Base Inclusion Comment",
            "Base Generation Comment",
            # "Comparison Inclusion Comment",
            "Comparison Generation Comment", ])
        edges_table.title = title
        edges_table.hrules = True
        edges_table.align = "l"

        for edge in sorted(edges, key=lambda edge: edge['edge_info']):
            base_edge_eval = edge['base_edge_eval']
            comparison_edge_eval = edge['comparison_edge_eval']
            edges_table.add_row([
                f"({",\n".join(edge['edge_info'])})",
                base_edge_eval.edge_covered,
                base_edge_eval.edge_included,
                comparison_edge_eval.edge_covered,
                comparison_edge_eval.edge_included,
                #base_edge_eval.inclusion_comment,
                base_edge_eval.generation_comment,
                #comparison_edge_eval.inclusion_comment,
                comparison_edge_eval.generation_comment,
            ])

        return edges_table

    @staticmethod
    def build_node_SEMENT_table(nodes, title):
        node_sement_table = PrettyTable([
            "Node",
            "Base SEMENT",
            "Comparison SEMENT",])
        node_sement_table.title = title
        node_sement_table.hrules = True
        node_sement_table.align = "l"
        node_sement_table.max_width["Base SEMENT"] = 80
        node_sement_table.max_width["Comparison SEMENT"] = 80

        for node_key in nodes:
            base_node_eval = nodes[node_key]['base_node_eval']
            comparison_node_eval = nodes[node_key]['comparison_node_eval']
            node_sement_table.add_row([
                node_key,
                base_node_eval.generated_SEMENT_string,
                comparison_node_eval.generated_SEMENT_string
            ])

        return node_sement_table

    @staticmethod
    def build_edge_SEMENT_table(edges, title):
        edge_SEMENT_table = PrettyTable([
            "Edge",
            "Base SEMENT",
            "Comparison SEMENT"])
        edge_SEMENT_table.title = title
        edge_SEMENT_table.align = "l"
        edge_SEMENT_table.hrules = True
        edge_SEMENT_table.align = "l"
        edge_SEMENT_table.max_width["Edge"] = 80
        edge_SEMENT_table.max_width["Base SEMENT"] = 80
        edge_SEMENT_table.max_width["Comparison SEMENT"] = 80

        for edge in sorted(edges, key=lambda edge: edge['edge_info']):
            base_edge_eval = edge['base_edge_eval']
            comparison_edge_eval = edge['comparison_edge_eval']
            edge_SEMENT_table.add_row([
                f"({",\n".join(edge['edge_info'])})",
                base_edge_eval.generated_SEMENT_string,
                comparison_edge_eval.generated_SEMENT_string
            ])

        return edge_SEMENT_table


    ### FILES ###
    @staticmethod
    def build_graph_level_diff_report(graph_evaluation_diff, changed_nodes, unchanged_nodes, changed_edges, unchanged_edges):
        report = f"GRAPH NAME: {graph_evaluation_diff.graph_name}\n\n"
        report += "=================== CHANGED NODE TABLES ===================\n"
        report += str(POGGGraphDiffReporting.build_node_metrics_table(changed_nodes, "CHANGED NODE METRICS")) + "\n\n"
        report += str(POGGGraphDiffReporting.build_node_SEMENT_table(changed_nodes, "CHANGED NODE SEMENTS")) + "\n"
        report += "===========================================================\n\n\n"
        report += "=================== CHANGED EDGE TABLES ===================\n"
        report += str(POGGGraphDiffReporting.build_edge_metrics_table(changed_edges, "CHANGED EDGE METRICS")) + "\n"
        report += str(POGGGraphDiffReporting.build_edge_SEMENT_table(changed_edges, "CHANGED EDGE SEMENTS")) + "\n"
        report += "===========================================================\n\n\n\n\n\n"
        report += "================== UNCHANGED NODE TABLES ==================\n"
        report += str(POGGGraphDiffReporting.build_node_metrics_table(unchanged_nodes, "UNCHANGED NODE METRICS")) + "\n"
        report += str(POGGGraphDiffReporting.build_node_SEMENT_table(unchanged_nodes, "UNCHANGED NODE SEMENTS")) + "\n"
        report += "===========================================================\n\n\n"
        report += "=================== CHANGED EDGE TABLES ===================\n"
        report += str(POGGGraphDiffReporting.build_edge_metrics_table(unchanged_edges, "UNCHANGED EDGE METRICS")) + "\n"
        report += str(POGGGraphDiffReporting.build_edge_SEMENT_table(unchanged_edges, "UNCHANGED EDGE SEMENTS")) + "\n"
        report += "===========================================================\n\n\n"
        return report


    @staticmethod
    def store_graph_diff_report(graph_evaluation_diff, graph_eval_diff_path):
        base_run_eval = graph_evaluation_diff.base_graph_eval
        comparison_run_eval = graph_evaluation_diff.comparison_graph_eval
        unchanged_nodes = {}
        changed_nodes = {}
        unchanged_edges = []
        changed_edges = []

        # categorize nodes
        for node_key in base_run_eval.node_evaluations:
            base_node_eval = base_run_eval.node_evaluations[node_key]
            comparison_node_eval = comparison_run_eval.node_evaluations[node_key]
            if (base_node_eval.node_covered == comparison_node_eval.node_covered and
                base_node_eval.node_included == comparison_node_eval.node_included):
                unchanged_nodes[node_key] = {
                    "node_key": node_key,
                    "base_node_eval": base_node_eval,
                    "comparison_node_eval": comparison_node_eval,
                }
            else:
                changed_nodes[node_key] = {
                    "node_key": node_key,
                    "base_node_eval": base_node_eval,
                    "comparison_node_eval": comparison_node_eval,
                }

        # categorize edges
        for base_edge_eval in base_run_eval.edge_evaluations:
            parent_name = base_edge_eval.parent_node_name
            child_name = base_edge_eval.child_node_name
            edge_name = base_edge_eval.edge_name
            edge_data = base_edge_eval.edge_props
            comparison_edge_eval = comparison_run_eval.get_edge_evaluation(parent_name, child_name, edge_data)

            if (base_edge_eval.edge_covered == comparison_edge_eval.edge_covered and
                base_edge_eval.edge_included == comparison_edge_eval.edge_included):
                unchanged_edges.append({
                    "edge_info": (parent_name, edge_name, child_name),
                    "base_edge_eval": base_edge_eval,
                    "comparison_edge_eval": comparison_edge_eval
                })
            else:
                changed_edges.append({
                    "edge_info": (parent_name, edge_name, child_name),
                    "base_edge_eval": base_edge_eval,
                    "comparison_edge_eval": comparison_edge_eval
                })


        with open(Path(graph_eval_diff_path, f"{base_run_eval.graph_name}_diff_report.txt"), "w") as f:
            f.write(str(POGGGraphDiffReporting.build_graph_level_diff_report(graph_evaluation_diff,
                                                                             changed_nodes, unchanged_nodes, changed_edges, unchanged_edges)))


class POGGDatasetDiffReporting:
    ### TABLES ###
    @staticmethod
    def build_diff_metadata_table(dataset_diff):
        base_run_dataset_eval = dataset_diff.base_eval
        comparison_run_dataset_eval = dataset_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        metadata_table = PrettyTable([
            "",
            "Dataset Name",
            "Experiment Name",
            "Run ID",])
        metadata_table.title = "DIFF INFORMATION"
        metadata_table.align = "l"

        metadata_table.add_row([
            "Base Run",
            base_run_dataset_eval.dataset_name,
            base_run_dataset_eval.experiment_name,
            base_run_dataset_eval.run_id
        ])

        metadata_table.add_row([
            "Comparison Run",
            comparison_run_dataset_eval.dataset_name,
            comparison_run_dataset_eval.experiment_name,
            comparison_run_dataset_eval.run_id
        ])

        return metadata_table

    @staticmethod
    def build_dataset_metadata_diff_table(dataset_diff):
        base_run_dataset_eval = dataset_diff.base_eval
        comparison_run_dataset_eval = dataset_diff.comparison_eval

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
            dataset_diff.graph_count_delta
        ])

        metadata_diff_table.add_row([
            "Number of Nodes in Dataset",
            base_run_dataset_eval.full_node_count,
            comparison_run_dataset_eval.full_node_count,
            dataset_diff.full_node_count_delta
        ])

        metadata_diff_table.add_row([
            "Number of Edges in Dataset",
            base_run_dataset_eval.full_edge_count,
            comparison_run_dataset_eval.full_edge_count,
            dataset_diff.full_edge_count_delta
        ])

        return metadata_diff_table

    @staticmethod
    def build_graph_metrics_diff_table(dataset_diff):
        base_run_dataset_eval = dataset_diff.base_eval
        comparison_run_dataset_eval = dataset_diff.comparison_eval

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
            dataset_diff.graph_SEMENT_count_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced a SEMENT (% coverage)",
            base_run_dataset_eval.graph_SEMENT_coverage,
            comparison_run_dataset_eval.graph_SEMENT_coverage,
            dataset_diff.graph_SEMENT_coverage_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced text results (count)",
            base_run_dataset_eval.graphs_with_text_count,
            comparison_run_dataset_eval.graphs_with_text_count,
            dataset_diff.graphs_with_text_count_delta
        ])

        graph_metrics_diff_table.add_row([
            "Graphs that produced text results (% coverage)",
            base_run_dataset_eval.graphs_with_text_coverage,
            comparison_run_dataset_eval.graphs_with_text_coverage,
            dataset_diff.graphs_with_text_coverage_delta
        ])

        return graph_metrics_diff_table

    @staticmethod
    def build_sem_fxns_count_delta(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        # if there are deltas here that means the dataset changed!!!
        sem_fxns_count_table = PrettyTable([
            "",
            "Base Run Count",
            "Comparison Run Count",
            "Delta (Comparison minus Base)"])
        sem_fxns_count_table.title = "SEMANTIC FUNCTIONS AVAILABLE METRICS"
        sem_fxns_count_table.align = "l"

        sem_fxns_count_table.add_row([
            "Semantic Algebra Functions",
            len(base_run_dataset_eval.sem_alg_fxns_available),
            len(comparison_run_dataset_eval.sem_alg_fxns_available),
            evaluation_diff.sem_alg_fxns_available_count_delta
        ])

        sem_fxns_count_table.add_row([
            "Semantic Composition Functions",
            len(base_run_dataset_eval.sem_comp_fxns_available),
            len(comparison_run_dataset_eval.sem_comp_fxns_available),
            evaluation_diff.sem_comp_fxns_available_count_delta
        ])

        return sem_fxns_count_table

    @staticmethod
    def build_sem_alg_fxns_available_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        sem_alg_fxns_available = base_run_dataset_eval.sem_alg_fxns_available.copy()
        sem_alg_fxns_available.extend(comparison_run_dataset_eval.sem_alg_fxns_available)

        sem_alg_fxns_available_diff_table = PrettyTable([
            "Function",
            "Available in base run?",
            "Available in comparison run?"])
        sem_alg_fxns_available_diff_table.title = "SEMANTIC ALGEBRA FUNCTIONS AVAILABLE"
        sem_alg_fxns_available_diff_table.align = "l"

        for fxn in sorted(sem_alg_fxns_available):
            sem_alg_fxns_available_diff_table.add_row([
                fxn,
                fxn in base_run_dataset_eval.sem_alg_fxns_available,
                fxn in comparison_run_dataset_eval.sem_alg_fxns_available,
            ])


        return sem_alg_fxns_available_diff_table

    @staticmethod
    def build_sem_comp_functions_available_diff_table(evaluation_diff):
        base_run_dataset_eval = evaluation_diff.base_eval
        comparison_run_dataset_eval = evaluation_diff.comparison_eval

        sem_comp_fxns_available = base_run_dataset_eval.sem_comp_fxns_available.copy()
        sem_comp_fxns_available.extend(comparison_run_dataset_eval.sem_comp_fxns_available)

        sem_comp_fxns_available_diff_table = PrettyTable([
            "Function",
            "Available in base run?",
            "Available in comparison run?"])
        sem_comp_fxns_available_diff_table.title = "SEMANTIC COMPOSITION FUNCTIONS AVAILABLE"
        sem_comp_fxns_available_diff_table.align = "l"

        for fxn in sem_comp_fxns_available:
            sem_comp_fxns_available_diff_table.add_row([
                fxn,
                fxn in base_run_dataset_eval.sem_comp_fxns_available,
                fxn in comparison_run_dataset_eval.sem_comp_fxns_available,
            ])

        return sem_comp_fxns_available_diff_table

    @staticmethod
    def build_simple_graphs_table(graph_list, table_title):
        graphs_table = PrettyTable(["Graph Name"])
        graphs_table.title = table_title
        graphs_table.align = "l"

        for graph_name in sorted(graph_list):
            graphs_table.add_row([graph_name])

        return graphs_table

        # TODO: this is actually dataset level specific ... move back into POGGDatasetReporting and make equiv for graph level
        # TODO: remove "ASCII" from all names it's ridiculous 
    @staticmethod
    def build_node_metrics_diff_table(evaluation_diff):
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
    def build_edge_metrics_diff_table(evaluation_diff):
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


    ### FILES ###
    @staticmethod
    def build_dataset_level_diff_report(dataset_evaluation_diff):
        report = str(POGGDatasetDiffReporting.build_diff_metadata_table(dataset_evaluation_diff)) + "\n\n\n"
        report += str(POGGDatasetDiffReporting.build_dataset_metadata_diff_table(dataset_evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_graph_metrics_diff_table(dataset_evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_node_metrics_diff_table(dataset_evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_edge_metrics_diff_table(dataset_evaluation_diff)) + "\n\n"
        return report

    @staticmethod
    def build_dataset_level_sem_comp_report(dataset_evaluation_diff):
        report = str(POGGDatasetDiffReporting.build_sem_fxns_count_delta(dataset_evaluation_diff)) + "\n\n"
        report += str(POGGDiffReporting.build_sem_fxns_used_overview_table(dataset_evaluation_diff)) + "\n\n\n"
        report += str(POGGDiffReporting.build_sem_comp_fxns_used_detail_table(dataset_evaluation_diff)) + "\n\n\n"
        report += str(POGGDiffReporting.build_sem_alg_fxns_used_detail_table(dataset_evaluation_diff)) + "\n\n\n"

        report += str(POGGDatasetDiffReporting.build_sem_alg_fxns_available_table(dataset_evaluation_diff)) + "\n\n\n"
        report += str(POGGDatasetDiffReporting.build_sem_comp_functions_available_diff_table(dataset_evaluation_diff)) + "\n\n\n"

        return report

    @staticmethod
    def build_graph_diff_overview_report(base_only_graphs, comparison_only_graphs, changed_graphs, unchanged_graphs):
        report = str(POGGDatasetDiffReporting.build_simple_graphs_table(changed_graphs, "CHANGED GRAPHS")) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_simple_graphs_table(unchanged_graphs, "UNCHANGED GRAPHS")) + "\n\n"
        if len(base_only_graphs) > 0:
            report += str(POGGDatasetDiffReporting.build_simple_graphs_table(base_only_graphs, "GRAPHS ONLY IN BASE RUN")) + "\n\n"
        if len(comparison_only_graphs) > 0:
            report += str(POGGDatasetDiffReporting.build_simple_graphs_table(comparison_only_graphs, "GRAPHS ONLY IN COMPARISON RUN"))
        return report

    ### DUMP FUNCTIONS ###
    @staticmethod
    def store_dataset_graph_diff_reports(graph_diff_path, base_run, comparison_run):

        graph_names = set(base_run.graph_evaluations.keys())
        graph_names.update(comparison_run.graph_evaluations.keys())
        base_only_graphs = []
        comparison_only_graphs = []
        changed_graphs = []
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
                    changed_graphs.append(graph_name)
                    changed_graphs_path = Path(graph_diff_path, "changed_graphs")
                    changed_graphs_path.mkdir(parents=True, exist_ok=True)
                    POGGGraphDiffReporting.store_graph_diff_report(graph_eval_diff, changed_graphs_path)

                else:
                    unchanged_graphs.append(graph_name)


        with open(Path(graph_diff_path, "graphs_diff_overview.txt"), "w") as f:
            f.write(POGGDatasetDiffReporting.build_graph_diff_overview_report(base_only_graphs,
                                                comparison_only_graphs, changed_graphs, unchanged_graphs))



    @staticmethod
    def store_diff_report(diff_path, base_run, comparison_run):
        print(f"Storing diff report for {base_run.experiment_name} and {comparison_run.experiment_name}...")

        eval_diff = POGGEvaluationDiff(base_run, comparison_run)

        # probably put this in POGGDatasetReporting ... maybe more store_evaluation_report there too
        now = datetime.datetime.now()
        diff_report_id = now.strftime("%m%d%Y_%H%M%S")
        eval_diff_path = Path(diff_path, "dataset_diff_report")

        # create the directory to store the diff report
        eval_diff_path.mkdir(parents=True, exist_ok=True)

        # 1. store the metadata about the diff report
        diff_metadata_json = {
            "diff_report_id": diff_report_id,
            "dataset_name": base_run.dataset_name,
            "base_run_data": base_run.get_POGG_metrics_dict(),
            "comparison_run_data": comparison_run.get_POGG_metrics_dict()
        }
        with open(Path(eval_diff_path, "diff_metadata.json"), 'w') as f:
            f.write(json.dumps(diff_metadata_json, indent=4))

        # 2. store the deltas for all the metrics
        # dataset_diff_report_json = eval_diff.get_dict_representation()
        # with open(Path(eval_diff_path, "dataset_diff.json"), 'w') as f:
        #     f.write(json.dumps(dataset_diff_report_json, indent=4))

        # 3. store readable text report of dataset-level deltas
        with open(Path(eval_diff_path, "dataset_level_metrics_diff.txt"), 'w') as f:
            f.write(POGGDatasetDiffReporting.build_dataset_level_diff_report(eval_diff))

        # 4. store readable text report of semantic composition functions
        with open(Path(eval_diff_path, "semantic_composition_functions_diff.txt"), 'w') as f:
            f.write(POGGDatasetDiffReporting.build_dataset_level_sem_comp_report(eval_diff))


        # 5. store readable graph reports
        graph_diff_reports_path = Path(eval_diff_path, "graph_diffs")
        graph_diff_reports_path.mkdir(parents=True, exist_ok=True)
        POGGDatasetDiffReporting.store_dataset_graph_diff_reports(graph_diff_reports_path, base_run, comparison_run)
