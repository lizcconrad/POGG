# {py:mod}`pogg.evaluation.reporting`

```{py:module} pogg.evaluation.reporting
```

```{autodoc2-docstring} pogg.evaluation.reporting
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`POGGGraphReporting <pogg.evaluation.reporting.POGGGraphReporting>`
  - ```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting
    :summary:
    ```
* - {py:obj}`POGGDatasetReporting <pogg.evaluation.reporting.POGGDatasetReporting>`
  - ```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetReporting
    :summary:
    ```
* - {py:obj}`POGGDatasetDiffReporting <pogg.evaluation.reporting.POGGDatasetDiffReporting>`
  - ```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting
    :summary:
    ```
````

### API

`````{py:class} POGGGraphReporting
:canonical: pogg.evaluation.reporting.POGGGraphReporting

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting
```

````{py:method} build_ASCII_nodes_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_nodes_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_nodes_table
```

````

````{py:method} build_ASCII_nodes_SEMENT_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_nodes_SEMENT_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_nodes_SEMENT_table
```

````

````{py:method} build_ASCII_edges_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_edges_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_edges_table
```

````

````{py:method} build_ASCII_edges_SEMENT_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_edges_SEMENT_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_edges_SEMENT_table
```

````

````{py:method} build_ASCII_graph_metrics_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_metrics_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_metrics_table
```

````

````{py:method} build_ASCII_graph_SEMENT_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_SEMENT_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_SEMENT_table
```

````

````{py:method} build_ASCII_gold_outputs_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_gold_outputs_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_gold_outputs_table
```

````

````{py:method} build_ASCII_graph_generated_text_table(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_generated_text_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_generated_text_table
```

````

````{py:method} build_ASCII_graph_report_detail(graph_eval)
:canonical: pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_report_detail
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGGraphReporting.build_ASCII_graph_report_detail
```

````

`````

`````{py:class} POGGDatasetReporting
:canonical: pogg.evaluation.reporting.POGGDatasetReporting

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetReporting
```

````{py:method} build_ASCII_dataset_metrics_table(dataset_eval)
:canonical: pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_dataset_metrics_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_dataset_metrics_table
```

````

````{py:method} build_ASCII_graphs_report_summary(dataset_eval)
:canonical: pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_graphs_report_summary
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_graphs_report_summary
```

````

````{py:method} build_ASCII_dataset_report(dataset_eval)
:canonical: pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_dataset_report
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetReporting.build_ASCII_dataset_report
```

````

`````

`````{py:class} POGGDatasetDiffReporting
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting
```

````{py:method} build_ASCII_metadata_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_metadata_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_metadata_diff_table
```

````

````{py:method} build_ASCII_graph_metrics_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_graph_metrics_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_graph_metrics_diff_table
```

````

````{py:method} build_ASCII_node_metrics_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_node_metrics_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_node_metrics_diff_table
```

````

````{py:method} build_ASCII_edge_metrics_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_edge_metrics_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_edge_metrics_diff_table
```

````

````{py:method} build_ASCII_sem_alg_functions_available_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_sem_alg_functions_available_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_sem_alg_functions_available_diff_table
```

````

````{py:method} build_ASCII_sem_comp_functions_available_diff_table(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_sem_comp_functions_available_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_sem_comp_functions_available_diff_table
```

````

````{py:method} build_ASCII_dataset_diff_report(evaluation_diff)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_dataset_diff_report
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.build_ASCII_dataset_diff_report
```

````

````{py:method} store_diff_report(evaluation_path, base_run, comparison_run)
:canonical: pogg.evaluation.reporting.POGGDatasetDiffReporting.store_diff_report
:staticmethod:

```{autodoc2-docstring} pogg.evaluation.reporting.POGGDatasetDiffReporting.store_diff_report
```

````

`````
