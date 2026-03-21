# {py:mod}`pogg.evaluation.evaluation`

```{py:module} pogg.evaluation.evaluation
```

```{autodoc2-docstring} pogg.evaluation.evaluation
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`POGGNodeEvaluation <pogg.evaluation.evaluation.POGGNodeEvaluation>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation
    :summary:
    ```
* - {py:obj}`POGGEdgeEvaluation <pogg.evaluation.evaluation.POGGEdgeEvaluation>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation
    :summary:
    ```
* - {py:obj}`POGGGraphEvaluation <pogg.evaluation.evaluation.POGGGraphEvaluation>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation
    :summary:
    ```
* - {py:obj}`POGGEvaluation <pogg.evaluation.evaluation.POGGEvaluation>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation
    :summary:
    ```
* - {py:obj}`POGGGraphEvaluationDiff <pogg.evaluation.evaluation.POGGGraphEvaluationDiff>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluationDiff
    :summary:
    ```
* - {py:obj}`POGGEvaluationDiff <pogg.evaluation.evaluation.POGGEvaluationDiff>`
  - ```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluationDiff
    :summary:
    ```
````

### API

`````{py:class} POGGNodeEvaluation(node_name, node_props, evaluation_file_path=None)
:canonical: pogg.evaluation.evaluation.POGGNodeEvaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation.__init__
```

````{py:method} set_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGNodeEvaluation.set_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation.set_SEMENT
```

````

````{py:method} get_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGNodeEvaluation.get_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation.get_dict_representation
```

````

````{py:method} create_evaluation_object_from_file(file_path)
:canonical: pogg.evaluation.evaluation.POGGNodeEvaluation.create_evaluation_object_from_file

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGNodeEvaluation.create_evaluation_object_from_file
```

````

`````

`````{py:class} POGGEdgeEvaluation(edge_name, edge_props, parent_name, child_name, evaluation_file_path=None)
:canonical: pogg.evaluation.evaluation.POGGEdgeEvaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation.__init__
```

````{py:method} set_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGEdgeEvaluation.set_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation.set_SEMENT
```

````

````{py:method} get_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGEdgeEvaluation.get_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation.get_dict_representation
```

````

````{py:method} create_evaluation_object_from_file(file_path)
:canonical: pogg.evaluation.evaluation.POGGEdgeEvaluation.create_evaluation_object_from_file

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEdgeEvaluation.create_evaluation_object_from_file
```

````

`````

`````{py:class} POGGGraphEvaluation(graph, graph_name, evaluation_dir=None)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.__init__
```

````{py:method} create_node_evaluations()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.create_node_evaluations

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.create_node_evaluations
```

````

````{py:method} create_edge_evaluations()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.create_edge_evaluations

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.create_edge_evaluations
```

````

````{py:method} set_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.set_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.set_SEMENT
```

````

````{py:method} set_collapsed_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.set_collapsed_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.set_collapsed_SEMENT
```

````

````{py:method} set_prepped_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.set_prepped_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.set_prepped_SEMENT
```

````

````{py:method} get_node_evaluation(node_name)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.get_node_evaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.get_node_evaluation
```

````

````{py:method} get_edge_evaluation(parent_name, child_name, edge_data)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.get_edge_evaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.get_edge_evaluation
```

````

````{py:method} determine_inclusion(root, ancestor_inclusion)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.determine_inclusion

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.determine_inclusion
```

````

````{py:method} calculate_metrics()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.calculate_metrics

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.calculate_metrics
```

````

````{py:method} get_top_level_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.get_top_level_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.get_top_level_dict_representation
```

````

````{py:method} mark_all_uncovered()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.mark_all_uncovered

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.mark_all_uncovered
```

````

````{py:method} create_evaluation_object_from_directory(evaluation_directory)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.create_evaluation_object_from_directory

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.create_evaluation_object_from_directory
```

````

`````

`````{py:class} POGGEvaluation(dataset_name=None, evaluation_dir=None)
:canonical: pogg.evaluation.evaluation.POGGEvaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.__init__
```

````{py:method} add_graph(graph, graph_name)
:canonical: pogg.evaluation.evaluation.POGGEvaluation.add_graph

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.add_graph
```

````

````{py:method} get_graph_evaluation(graph_name)
:canonical: pogg.evaluation.evaluation.POGGEvaluation.get_graph_evaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.get_graph_evaluation
```

````

````{py:method} calculate_metrics()
:canonical: pogg.evaluation.evaluation.POGGEvaluation.calculate_metrics

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.calculate_metrics
```

````

````{py:method} get_top_level_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGEvaluation.get_top_level_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.get_top_level_dict_representation
```

````

````{py:method} create_evaluation_object_from_directory(evaluation_directory)
:canonical: pogg.evaluation.evaluation.POGGEvaluation.create_evaluation_object_from_directory

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.create_evaluation_object_from_directory
```

````

`````

`````{py:class} POGGGraphEvaluationDiff(graph_name, base_graph_eval, comparison_graph_eval)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluationDiff

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluationDiff
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluationDiff.__init__
```

````{py:method} get_changed_metrics()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluationDiff.get_changed_metrics

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluationDiff.get_changed_metrics
```

````

````{py:method} get_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluationDiff.get_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluationDiff.get_dict_representation
```

````

`````

`````{py:class} POGGEvaluationDiff(base_eval, comparison_eval)
:canonical: pogg.evaluation.evaluation.POGGEvaluationDiff

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluationDiff
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluationDiff.__init__
```

````{py:method} get_dict_representation()
:canonical: pogg.evaluation.evaluation.POGGEvaluationDiff.get_dict_representation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluationDiff.get_dict_representation
```

````

`````
