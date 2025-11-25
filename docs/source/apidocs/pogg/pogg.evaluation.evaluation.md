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
````

### API

`````{py:class} POGGNodeEvaluation(node_name, node_props)
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

`````

`````{py:class} POGGEdgeEvaluation(edge_name, edge_props, parent, child)
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

`````

`````{py:class} POGGGraphEvaluation(graph, graph_name)
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

````{py:method} set_wrapped_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.set_wrapped_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.set_wrapped_SEMENT
```

````

````{py:method} set_collapsed_SEMENT(sement)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.set_collapsed_SEMENT

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.set_collapsed_SEMENT
```

````

````{py:method} get_node_evaluation(node_name)
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.get_node_evaluation

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.get_node_evaluation
```

````

````{py:method} get_edge_evaluation(parent, child, edge_data)
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

````{py:method} mark_all_uncovered()
:canonical: pogg.evaluation.evaluation.POGGGraphEvaluation.mark_all_uncovered

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGGraphEvaluation.mark_all_uncovered
```

````

`````

`````{py:class} POGGEvaluation(dataset_name)
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

````{py:method} calculate_metrics()
:canonical: pogg.evaluation.evaluation.POGGEvaluation.calculate_metrics

```{autodoc2-docstring} pogg.evaluation.evaluation.POGGEvaluation.calculate_metrics
```

````

`````
