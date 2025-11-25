# functions to aid in outputting reports
from prettytable import PrettyTable

class POGGNodeReporting:
    @staticmethod
    def build_ASCII_node_row(node_eval):
        return [
            node_eval.node_name,
            node_eval.node_covered,
            node_eval.node_included,
            node_eval.generation_comment,
            node_eval.generated_SEMENT_string
        ]

    @staticmethod
    def build_ASCII_edge_row(edge_eval):
        return [
            edge_eval.edge_name,
            edge_eval.parent_node_name,
            edge_eval.child_node_name,
            edge_eval.edge_covered,
            edge_eval.edge_included,
            edge_eval.generation_comment,
            edge_eval.generated_SEMENT_string
        ]

class POGGGraphReporting:
    @staticmethod
    def build_ASCII_nodes_table(graph_eval):
        nodes_table = PrettyTable(["Node", "Node Covered", "Node Included", "Comment", "Generated SEMENT"])
        nodes_table.align = "l"
        nodes_table.max_width["Comment"] = 20
        nodes_table.max_width["Generated SEMENT"] = 80

        for key in graph_eval.node_evaluations.keys():
            node_eval = graph_eval.node_evaluations[key]
            nodes_table.add_row(POGGNodeReporting.build_ASCII_node_row(node_eval))

        return nodes_table

    @staticmethod
    def build_ASCII_edges_table(graph_eval):
        edges_table = PrettyTable(["Edge", "Parent", "Child", "Edge Covered", "Edge Included", "Comment", "Generated SEMENT"])
        edges_table.align = "l"
        edges_table.max_width["Comment"] = 20
        edges_table.max_width["Generated SEMENT"] = 80
        for edge_eval in graph_eval.edge_evaluations:
            edges_table.add_row(POGGNodeReporting.build_ASCII_edge_row(edge_eval))

        return edges_table

    @staticmethod
    def build_ASCII_graph_metrics_table(graph_eval):
        metrics_table = PrettyTable(["Metric", "Value"])
        metrics_table.title = "EVALUATION METRICS"
        metrics_table.align = "l"

        metrics_table.add_row(["Generated Text Results", len(graph_eval.generated_results)], divider=True)
        metrics_table.add_row(["Node Count", graph_eval.node_count])
        metrics_table.add_row(["Node Coverage", graph_eval.node_coverage])
        metrics_table.add_row(["Node Inclusion", graph_eval.node_inclusion], divider=True)
        metrics_table.add_row(["Edge Count", graph_eval.edge_count])
        metrics_table.add_row(["Edge Coverage", graph_eval.edge_coverage])
        metrics_table.add_row(["Edge Inclusion", graph_eval.edge_inclusion])


        return metrics_table

    @staticmethod
    def build_ASCII_graph_sement_table(graph_eval):
        sement_table = PrettyTable(["Version", "SEMENT"])
        sement_table.title = "GENERATED SEMENTS"
        sement_table.align = "l"
        sement_table.max_width["SEMENT"] = 80

        sement_table.add_row(["Original", graph_eval.generated_SEMENT_string], divider=True)
        sement_table.add_row(["EQs Collapsed", graph_eval.collapsed_SEMENT_string], divider=True)
        sement_table.add_row(["Wrapped", graph_eval.wrapped_SEMENT_string])

        return sement_table


    @staticmethod
    def build_ASCII_graph_generated_text_table(graph_eval):
        gen_text_table = PrettyTable(["#", "Generated Text"])
        gen_text_table.title = "GENERATED ENGLISH TEXT"
        gen_text_table.align = "l"

        for i, txt in enumerate(sorted(graph_eval.generated_results)):
            gen_text_table.add_row([i + 1, txt])

        return gen_text_table

    @staticmethod
    def build_ASCII_graph_report_detail(graph_eval):
        report = f"GRAPH NAME: {graph_eval.graph_name}\n\n"
        report += str(POGGGraphReporting.build_ASCII_graph_sement_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_graph_metrics_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_nodes_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_edges_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_graph_generated_text_table(graph_eval)) + "\n\n"
        return report


class POGGDatasetReporting:
    @staticmethod
    def build_ASCII_dataset_metrics_table(dataset_eval):
        metrics_table = PrettyTable(["Metric", "Value"])
        metrics_table.title = "EVALUATION METRICS"
        metrics_table.align = "l"

        metrics_table.add_row(["Graph Count", dataset_eval.graph_count])
        metrics_table.add_row(["Graphs that produced SEMENTs", dataset_eval.graph_SEMENT_count])
        metrics_table.add_row(["Graphs w/ SEMENTs coverage", dataset_eval.graph_SEMENT_coverage])
        metrics_table.add_row(["Graphs that generated text", dataset_eval.graphs_with_text_count])
        metrics_table.add_row(["Graphs w/ text coverage", dataset_eval.graph_text_coverage], divider=True)

        metrics_table.add_row(["Total Node Count", dataset_eval.full_node_count])
        metrics_table.add_row(["Total Nodes Covered", dataset_eval.full_nodes_covered])
        metrics_table.add_row(["Total Nodes Included", dataset_eval.full_nodes_included])
        metrics_table.add_row(["Total Node Coverage", dataset_eval.full_node_coverage])
        metrics_table.add_row(["Total Node Inclusion", dataset_eval.full_node_inclusion], divider=True)

        metrics_table.add_row(["Total Edge Count", dataset_eval.full_edge_count])
        metrics_table.add_row(["Total Edges Covered", dataset_eval.full_edges_covered])
        metrics_table.add_row(["Total Edges Included", dataset_eval.full_edges_included])
        metrics_table.add_row(["Total Edge Coverage", dataset_eval.full_edge_coverage])
        metrics_table.add_row(["Total Edge Inclusion", dataset_eval.full_edge_inclusion], divider=True)

        return metrics_table

    @staticmethod
    def build_ASCII_graphs_report_summary(dataset_eval):
        graphs_summary_table = PrettyTable([
            "Graph Name",
            "Generated SEMENT?",
            "# of text results",
            "Nodes",
            "Node Coverage",
            "Node Inclusion",
            "Edges",
            "Edge Coverage",
            "Edge Inclusion"])
        graphs_summary_table.title = "GRAPH SUMMARIES"
        graphs_summary_table.align = "l"

        sorted_graph_evals = sorted(dataset_eval.graph_evaluations, key=lambda x: x.graph_name)
        for graph_eval in sorted_graph_evals:
            graphs_summary_table.add_row([
                graph_eval.graph_name,
                (graph_eval.generated_SEMENT is not None),
                len(graph_eval.generated_results),
                graph_eval.node_count,
                graph_eval.node_coverage,
                graph_eval.node_inclusion,
                graph_eval.edge_count,
                graph_eval.edge_coverage,
                graph_eval.edge_inclusion
            ])

        return graphs_summary_table

    @staticmethod
    def build_ASCII_dataset_report(dataset_eval):
        report = f"DATASET: {dataset_eval.dataset_name}\n\n"
        report += str(POGGDatasetReporting.build_ASCII_dataset_metrics_table(dataset_eval)) + "\n\n"
        report += str(POGGDatasetReporting.build_ASCII_graphs_report_summary(dataset_eval)) + "\n\n"
        return report
