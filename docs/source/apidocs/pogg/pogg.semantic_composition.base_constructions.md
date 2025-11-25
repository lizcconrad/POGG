# {py:mod}`pogg.semantic_composition.base_constructions`

```{py:module} pogg.semantic_composition.base_constructions
```

```{autodoc2-docstring} pogg.semantic_composition.base_constructions
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SingleWordConstructionsMixin <pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin>`
  - ```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin
    :summary:
    ```
* - {py:obj}`BaseConstructionsMixin <pogg.semantic_composition.base_constructions.BaseConstructionsMixin>`
  - ```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin
    :summary:
    ```
* - {py:obj}`SemanticComposition <pogg.semantic_composition.base_constructions.SemanticComposition>`
  - ```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SemanticComposition
    :summary:
    ```
````

### API

`````{py:class} SingleWordConstructionsMixin
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin
```

````{py:method} basic(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.basic

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.basic
```

````

````{py:method} adjective(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.adjective

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.adjective
```

````

````{py:method} determiner(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.determiner

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.determiner
```

````

````{py:method} named_entity(name: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.named_entity

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.named_entity
```

````

````{py:method} noun(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.noun

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.noun
```

````

````{py:method} preposition(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.preposition

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.preposition
```

````

````{py:method} pronoun(intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.pronoun

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.pronoun
```

````

````{py:method} quantifier(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.quantifier

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.quantifier
```

````

````{py:method} verb(predicate: str, intrinsic_variable_properties: dict = None) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.verb

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin.verb
```

````

`````

`````{py:class} BaseConstructionsMixin
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin
```

````{py:method} prenominal_adjective(adjective_sement: pogg.my_delphin.my_delphin.SEMENT, nominal_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.prenominal_adjective

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.prenominal_adjective
```

````

````{py:method} compound_noun(head_noun_sement: pogg.my_delphin.my_delphin.SEMENT, non_head_noun_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.compound_noun

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.compound_noun
```

````

````{py:method} prepositional_relationship(preposition_predicate: str, figure_sement: pogg.my_delphin.my_delphin.SEMENT, ground_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.prepositional_relationship

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.prepositional_relationship
```

````

````{py:method} relative_direction(direction_predicate: str, figure_sement: pogg.my_delphin.my_delphin.SEMENT, ground_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.relative_direction

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.relative_direction
```

````

````{py:method} possessive(possessor_sement: pogg.my_delphin.my_delphin.SEMENT, possessed_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.possessive

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.possessive
```

````

````{py:method} quantify(quantifier_sement: pogg.my_delphin.my_delphin.SEMENT, quantified_sement: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.base_constructions.BaseConstructionsMixin.quantify

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.BaseConstructionsMixin.quantify
```

````

`````

````{py:class} SemanticComposition(semantic_algebra: pogg.semantic_composition.semantic_algebra.SemanticAlgebra)
:canonical: pogg.semantic_composition.base_constructions.SemanticComposition

Bases: {py:obj}`pogg.semantic_composition.base_constructions.SingleWordConstructionsMixin`, {py:obj}`pogg.semantic_composition.base_constructions.BaseConstructionsMixin`

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SemanticComposition
```

```{rubric} Initialization
```

```{autodoc2-docstring} pogg.semantic_composition.base_constructions.SemanticComposition.__init__
```

````
