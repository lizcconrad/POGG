"""
The reporting module contains the `POGGGraphReporting` and `POGGDatasetReporting` classes
that contain functions to aid in printing readable reports that summarize evaluation information about parts of a dataset
that has gone through the data-to-text algorithm.

[See usage examples here.](project:/usage_nbs/pogg/evaluation/reporting_usage.ipynb)
"""
import datetime
from pathlib import Path
import json
from prettytable import PrettyTable
from pogg.evaluation.evaluation import POGGEvaluationDiff, POGGGraphEvaluationDiff

class POGGGraphReporting:
    """
    The `POGGGraphReporting` class contains static functions for building ASCII tables detailing evaluation information
    about a directed graph in a dataset.
    """

    @staticmethod
    def build_ASCII_nodes_table(graph_eval):
        """
        Build an ASCII table detailing evaluation information about every node in a graph.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGNodeEvaluation` object for each ndoe are included in each row of the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `node_name` | name of the node |
        | `node_covered` | whether it was covered during graph-to-SEMENT conversion (i.e. generated a SEMENT) |
        | `node_included` | whether it contributed semantically to the final SEMENT |
        | `generation_comment` | comment about why a SEMENT failed to generate if applicable |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation information for all nodes in a graph |
        """

        nodes_table = PrettyTable(["Node", "Node Covered", "Node Included", "Coverage Comment", "Inclusion Comment"])
        nodes_table.title = "NODE METRICS"
        nodes_table.align = "l"

        for key in graph_eval.node_evaluations.keys():
            node_eval = graph_eval.node_evaluations[key]

            if node_eval.node_covered:
                coverage_comment = "Covered"
            else:
                coverage_comment = node_eval.generation_comment

            if node_eval.node_included:
                inclusion_comment = "Included"
            else:
                inclusion_comment = node_eval.inclusion_comment

            nodes_table.add_row([
                node_eval.node_name,
                node_eval.node_covered,
                node_eval.node_included,
                coverage_comment,
                inclusion_comment
            ])

        return nodes_table

    @staticmethod
    def build_ASCII_nodes_SEMENT_table(graph_eval):
        """
        Build an ASCII table showing the generated SEMENT for each node in a graph, if it exists.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGNodeEvaluation` object for each ndoe are included in each row of the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `node_name` | name of the node |
        | `generated_SEMENT_string` | generated SEMENT encoded as a string |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation information for all nodes in a graph |
        """

        nodes_table = PrettyTable(["Node", "Generated SEMENT"])
        nodes_table.title = "NODE SEMENTS"
        nodes_table.hrules = True
        nodes_table.align = "l"
        nodes_table.max_width["Generated SEMENT"] = 80

        for key in graph_eval.node_evaluations.keys():
            node_eval = graph_eval.node_evaluations[key]
            nodes_table.add_row([
                node_eval.node_name,
                node_eval.generated_SEMENT_string
            ])

        return nodes_table

    @staticmethod
    def build_ASCII_edges_table(graph_eval):
        """
        Build an ASCII table detailing evaluation information about every edge in a graph.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGEdgeEvaluation` for each edge object are included in each row of the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `edge_name` | name of the edge |
        | `parent_node_name` | name of the parent node |
        | `child_node_name` | name of the child node |
        | `edge_covered` | whether it was covered during graph-to-SEMENT conversion (i.e. generated a SEMENT) |
        | `edge_included` | whether it contributed semantically to the final SEMENT |
        | `generation_comment` | comment about why a SEMENT failed to generate if applicable |
        | `generated_SEMENT_string` | generated SEMENT encoded as a string |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation information for all edges in a graph |
        """

        edges_table = PrettyTable(["Edge", "Parent", "Child", "Edge Covered", "Edge Included", "Coverage Comment", "Inclusion Comment"])
        edges_table.title = "EDGE METRICS"
        # edges_table.max_width["Coverage Comment"] = 20
        # edges_table.max_width["Inclusion Comment"] = 20
        edges_table.align = "l"

        for edge_eval in graph_eval.edge_evaluations:
            if edge_eval.edge_covered:
                coverage_comment = "Covered"
            else:
                coverage_comment = edge_eval.generation_comment

            if edge_eval.edge_included:
                inclusion_comment = "Included"
            else:
                inclusion_comment = edge_eval.inclusion_comment

            edges_table.add_row([
                edge_eval.edge_name,
                edge_eval.parent_node_name,
                edge_eval.child_node_name,
                edge_eval.edge_covered,
                edge_eval.edge_included,
                coverage_comment,
                inclusion_comment
            ])

        return edges_table

    @staticmethod
    def build_ASCII_edges_SEMENT_table(graph_eval):
        """
         Build an ASCII table showing the generated SEMENT for each edge in a graph, if it exists.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGEdgeEvaluation` for each edge object are included in each row of the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `edge_name` | name of the edge |
        | `generated_SEMENT_string` | generated SEMENT encoded as a string |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation information for all edges in a graph |
        """

        edges_table = PrettyTable(
            ["Edge", "Parent", "Child", "Generated SEMENT"])
        edges_table.title = "EDGE SEMENTS"
        edges_table.hrules = True
        edges_table.align = "l"
        edges_table.max_width["Generated SEMENT"] = 80
        for edge_eval in graph_eval.edge_evaluations:
            edges_table.add_row([
                edge_eval.edge_name,
                edge_eval.parent_node_name,
                edge_eval.child_node_name,
                edge_eval.generated_SEMENT_string
            ])

        return edges_table

    @staticmethod
    def build_ASCII_graph_metrics_table(graph_eval):
        """
        Build an ASCII table detailing evaluation metrics for one directed graph in a dataset.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGGraphEvaluation` object are included in the table:

        | Attribute | Description |
        | --------- | ----------- |
        | length of `generated_results` | number of text results generated |
        | `node_count` | number of nodes in the graph |
        | `node_coverage` | percentage of nodes covered (i.e. those that generated a SEMENT) |
        | `node_inclusion` | percentage of nodes that contributed semantically to the final result |
        | `edge_count` | number of edges in the graph |
        | `edge_coverage` | percentage of edges covered (i.e. those that generated a SEMENT) |
        | `edge_inclusion` | percentage of edges that contributed semantically to the final result |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation metrics for a graph |
        """

        metrics_table = PrettyTable(["Metric", "Value"])
        metrics_table.title = "EVALUATION METRICS"
        metrics_table.align = "l"

        metrics_table.add_row(["Generated Text Results", len(graph_eval.generated_results)])
        metrics_table.add_row(["Generated Gold Results", len(graph_eval.generated_gold_outputs)])
        metrics_table.add_row(["Generated Gold Results Coverage", graph_eval.gold_output_generation_coverage], divider=True)
        metrics_table.add_row(["Node Count", graph_eval.node_count])
        metrics_table.add_row(["Nodes Covered", graph_eval.nodes_covered])
        metrics_table.add_row(["Nodes Included", graph_eval.nodes_included], divider=True)
        metrics_table.add_row(["Node Coverage", graph_eval.node_coverage])
        metrics_table.add_row(["Node Inclusion", graph_eval.node_inclusion], divider=True)
        metrics_table.add_row(["Edge Count", graph_eval.edge_count])
        metrics_table.add_row(["Edges Covered", graph_eval.edges_covered])
        metrics_table.add_row(["Edges Included", graph_eval.edges_included], divider=True)
        metrics_table.add_row(["Edge Coverage", graph_eval.edge_coverage])
        metrics_table.add_row(["Edge Inclusion", graph_eval.edge_inclusion])


        return metrics_table

    @staticmethod
    def build_ASCII_graph_SEMENT_table(graph_eval):
        """
        Build an ASCII table showing the SEMENTs associated with a particular directed graph.
        If an error caused generation to fail, print the error instead.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGGraphEvaluation` object are included in the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `generated_SEMENT_string`| original SEMENT generated for the graph encoded as a string |
        | `collapsed_SEMENT_string`| SEMENT string that is isomorphic to the original SEMENT but with EQs collapsed to one value |
        | `prepped_SEMENT_string`| SEMENT string that has been prepared for generation by the ERG (not necessarily strictly isomorphic to the original) |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the SEMENTs associated with a graph |
        """

        sement_table = PrettyTable(["Version", "SEMENT"])
        sement_table.title = "GENERATED SEMENTS"
        sement_table.align = "l"
        sement_table.max_width["SEMENT"] = 80

        sement_table.add_row(["Original", graph_eval.generated_SEMENT_string], divider=True)
        sement_table.add_row(["EQs Collapsed", graph_eval.collapsed_SEMENT_string], divider=True)
        sement_table.add_row(["Prepped", graph_eval.prepped_SEMENT_string], divider=True)

        # if there's a generation comment, add it
        if graph_eval.generation_comment is not None:
            sement_table.add_row(["Generation Comment", graph_eval.generation_comment])

        return sement_table


    @staticmethod
    def build_ASCII_gold_outputs_table(graph_eval):
        """
        Build an ASCII table listing the generated English text results that the ERG generated for the SEMENT associated with the graph.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the generated English text results for a graph |
        """

        gold_text_table = PrettyTable(["Gold Output", "Generated?"])
        gold_text_table.title = "GOLD OUTPUTS"
        gold_text_table.align = "l"

        for gold_output in sorted(list(graph_eval.gold_outputs)):
            gold_text_table.add_row([gold_output, gold_output in graph_eval.generated_gold_outputs])

        return gold_text_table

    @staticmethod
    def build_ASCII_graph_generated_text_table(graph_eval):
        """
        Build an ASCII table listing the generated English text results that the ERG generated for the SEMENT associated with the graph.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the generated English text results for a graph |
        """

        gen_text_table = PrettyTable(["#", "Generated Text"])
        gen_text_table.title = "GENERATED ENGLISH TEXT"
        gen_text_table.align = "l"

        for i, txt in enumerate(sorted(graph_eval.generated_results)):
            gen_text_table.add_row([i + 1, txt])

        return gen_text_table

    @staticmethod
    def build_ASCII_graph_report_detail(graph_eval):
        """
        Build a report for an individual graph that includes tables about the nodes, edges, evaluation metrics,
        SEMENTs, and generated text results.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_eval` | `POGGGraphEvaluation` | `POGGGraphEvaluation` object to build the report for |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `str` | string that concatenates all relevant tables for the graph and can be printed to a file |
        """

        report = f"GRAPH NAME: {graph_eval.graph_name}\n\n"
        report += str(POGGGraphReporting.build_ASCII_graph_metrics_table(graph_eval)) + "\n\n"

        report += str(POGGGraphReporting.build_ASCII_gold_outputs_table(graph_eval)) + "\n\n"

        report += str(POGGGraphReporting.build_ASCII_nodes_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_edges_table(graph_eval)) + "\n\n"

        report += str(POGGGraphReporting.build_ASCII_graph_SEMENT_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_nodes_SEMENT_table(graph_eval)) + "\n\n"
        report += str(POGGGraphReporting.build_ASCII_edges_SEMENT_table(graph_eval)) + "\n\n"

        report += str(POGGGraphReporting.build_ASCII_graph_generated_text_table(graph_eval)) + "\n\n"
        return report


class POGGDatasetReporting:
    """
    The `POGGDatasetReporting` class contains static functions for building ASCII tables detailing evaluation information
    about a dataset.
    """

    @staticmethod
    def build_ASCII_dataset_metrics_table(dataset_eval):
        """
        Build an ASCII table detailing evaluation metrics for a dataset.

        :::{info} Attributes included in the table
        :collapsible:
        The following attributes from the `POGGEvaluation` object are included in the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `graph_count` | number of graphs in the dataset |
        | `graph_SEMENT_count` | number of graphs that generated a SEMENT |
        | `graph_SEMENT_coverage` | percentage of graphs that generated a SEMENT |
        | `graphs_with_text_count` | number of graphs that generated English text results |
        | `graph_text_coverage` | percentage of graphs that generated English text results |
        | `total_node_count` | total number of nodes in the dataset |
        | `total_nodes_covered` | total number of nodes that generated a SEMENT during graph-to-SEMENT conversion |
        | `total_nodes_included` | total number of nodes that contributed semantically to the final SEMENT for the graph |
        | `total_node_coverage` | percentage of nodes that generated a SEMENT during graph-to-SEMENT conversion |
        | `total_node_inclusion` | perctengae of nodes that contributed semantically to the final SEMENT for the graph |
        | `total_edge_count` | total number of edges in the dataset |
        | `total_edges_covered` | total number of edges that generated a SEMENT during graph-to-SEMENT conversion |
        | `total_edges_included` | total number of edges that contributed semantically to the final SEMENT for the graph |
        | `total_edge_coverage` | percentage of edges that generated a SEMENT during graph-to-SEMENT conversion |
        | `total_edge_inclusion` | perctengae of edges that contributed semantically to the final SEMENT for the graph |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `dataset_eval` | `POGGEvaluation` | `POGGEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table of the evaluation metrics for a graph |
        """

        metrics_table = PrettyTable(["Metric", "Value"])
        metrics_table.title = "EVALUATION METRICS"
        metrics_table.align = "l"

        metrics_table.add_row(["Graph Count", dataset_eval.graph_count])
        metrics_table.add_row(["Graphs that produced SEMENTs", dataset_eval.graph_SEMENT_count])
        metrics_table.add_row(["Graphs w/ SEMENTs coverage", dataset_eval.graph_SEMENT_coverage])
        metrics_table.add_row(["Graphs that generated text", dataset_eval.graphs_with_text_count])
        metrics_table.add_row(["Graphs w/ text coverage", dataset_eval.graphs_with_text_coverage], divider=True)

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

        metrics_table.add_row(["# Semantic Composition Functions Available", len(dataset_eval.sem_comp_fxns_available)])
        metrics_table.add_row(["# Semantic Composition Functions Used", len(dataset_eval.sem_comp_fxns_used)])
        metrics_table.add_row(["# Semantic Composition Function Coverage", dataset_eval.sem_comp_fxns_used_coverage])

        return metrics_table

    @staticmethod
    def build_ASCII_graphs_report_summary(dataset_eval):
        """
        Build an ASCII table detailing evaluation metrics for each graph in a dataset.

        :::{info} Attributes included in each row of the table
        :collapsible:
        The following attributes from each `POGGGraphEvaluation` object for the dataset are included in the table:

        | Attribute | Description |
        | --------- | ----------- |
        | `graph_name` | name of the graph |
        | whether `generated_SEMENT` is `None` | whether there's a SEMENT associated with the graph |
        | length of `generated_results` | number of text results generated |
        | `node_count` | number of nodes in the graph |
        | `node_coverage` | percentage of nodes that generated a SEMENT for the graph |
        | `node_inclusion` | percentage of nodes that contributed semantically to the final SEMENT for the graph |
        | `edge_count` | number of edges in the graph |
        | `edge_coverage` | percentage of edges that generated a SEMENT for the graph |
        | `edge_inclusion` | percentage of edges that contributed semantically to the final SEMENT for the graph |
        :::

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `dataset_eval` | `POGGEvaluation` | `POGGEvaluation` object to build the table from |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `PrettyTable` | ASCII table summarizing metrics for each graph in the dataset |
        """

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

        for graph_eval_key in sorted(dataset_eval.graph_evaluations.keys()):
            graph_eval = dataset_eval.graph_evaluations[graph_eval_key]
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
        """
        Build a report for a dataset that includes a table of evaluation metrics for the whole dataset and a table
        summarizing metrics for each graph in the dataset.

         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `dataset_eval` | `POGGEvaluation` | `POGGEvaluation` object to build the report for |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `str` | string that concatenates all relevant tables for the dataset can be printed to a file |
        """

        report = f"DATASET: {dataset_eval.dataset_name}\n\n"
        report += str(POGGDatasetReporting.build_ASCII_dataset_metrics_table(dataset_eval)) + "\n\n"
        report += str(POGGDatasetReporting.build_ASCII_graphs_report_summary(dataset_eval)) + "\n\n"
        return report




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
            evaluation_diff.graph_text_coverage_delta
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
    def build_ASCII_dataset_diff_report(evaluation_diff):
        report = f"DATASET: {evaluation_diff.dataset_name}\n"
        report += f"BASE RUN ID: {evaluation_diff.base_eval.run_id}\n"
        report += f"COMPARISON RUN ID: {evaluation_diff.comparison_eval.run_id}\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_metadata_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_graph_metrics_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_node_metrics_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_edge_metrics_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_sem_comp_functions_available_diff_table(evaluation_diff)) + "\n\n"
        report += str(POGGDatasetDiffReporting.build_ASCII_sem_alg_functions_available_diff_table(evaluation_diff)) + "\n\n"
        return report


    @staticmethod
    def store_diff_report(evaluation_path, base_run, comparison_run):
        eval_diff = POGGEvaluationDiff(base_run, comparison_run)

        # probably put this in POGGDatasetReporting ... maybe more store_evaluation_report there too
        now = datetime.datetime.now()
        diff_report_id = now.strftime("%m%d%Y_%H%M%S")
        eval_diff_path = Path(evaluation_path, "diff_reports", diff_report_id)

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
        with open(Path(eval_diff_path, "dataset_diff.txt"), 'w') as f:
            f.write(POGGDatasetDiffReporting.build_ASCII_dataset_diff_report(eval_diff))

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