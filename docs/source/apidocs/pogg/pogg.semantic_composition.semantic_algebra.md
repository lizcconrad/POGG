# {py:mod}`pogg.semantic_composition.semantic_algebra`

```{py:module} pogg.semantic_composition.semantic_algebra
```

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SemanticAlgebra <pogg.semantic_composition.semantic_algebra.SemanticAlgebra>`
  - ```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra
    :summary:
    ```
````

### API

`````{py:class} SemanticAlgebra(pogg_config: pogg.pogg_config.POGGConfig)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.__init__
```

````{py:method} _get_slots(ep)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra._get_slots

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra._get_slots
```

````

````{py:method} create_base_SEMENT(predicate, intrinsic_variable_properties=None, synopsis_dict=None)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_base_SEMENT

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_base_SEMENT
```

````

````{py:method} create_CARG_SEMENT(predicate, carg_value, intrinsic_variable_properties={})
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_CARG_SEMENT

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_CARG_SEMENT
```

````

````{py:method} op_non_scopal_argument_hook(functor, argument, slot_label)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_argument_hook

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_argument_hook
```

````

````{py:method} op_non_scopal_functor_hook(functor, argument, slot_label)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_functor_hook

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_functor_hook
```

````

````{py:method} op_scopal_argument_index(functor, argument, slot_label)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_argument_index

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_argument_index
```

````

````{py:method} op_scopal_functor_index(functor, argument, slot_label)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index
```

````

````{py:method} op_scopal_functor_index_argument_slots(functor, argument, slot_label)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index_argument_slots

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index_argument_slots
```

````

````{py:method} op_scopal_quantifier(functor, argument)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_quantifier

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_quantifier
```

````

````{py:method} prepare_for_generation(sement)
:canonical: pogg.semantic_composition.semantic_algebra.SemanticAlgebra.prepare_for_generation

```{autodoc2-docstring} pogg.semantic_composition.semantic_algebra.SemanticAlgebra.prepare_for_generation
```

````

`````
