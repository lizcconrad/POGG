# {py:mod}`pogg.semantic_composition.composition_mixins.base_constructions`

```{py:module} pogg.semantic_composition.composition_mixins.base_constructions
```

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`BaseConstructionsMixin <pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin>`
  - ```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin
    :summary:
    ```
````

### API

`````{py:class} BaseConstructionsMixin
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin
```

````{py:method} ARG1_relative_clause(verb_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ARG1_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ARG2_SEMENT: pogg.my_delphin.my_delphin.SEMENT)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ARG1_relative_clause

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ARG1_relative_clause
```

````

````{py:method} ARG2_relative_clause(verb_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ARG2_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ARG1_SEMENT: pogg.my_delphin.my_delphin.SEMENT = None)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ARG2_relative_clause

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ARG2_relative_clause
```

````

````{py:method} prenominal_adjective(adjective_SEMENT: pogg.my_delphin.my_delphin.SEMENT, nominal_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.prenominal_adjective

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.prenominal_adjective
```

````

````{py:method} nonrestrictive_adjectival_relative_clause(adjective_SEMENT: pogg.my_delphin.my_delphin.SEMENT, nominal_SEMENT: pogg.my_delphin.my_delphin.SEMENT)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.nonrestrictive_adjectival_relative_clause

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.nonrestrictive_adjectival_relative_clause
```

````

````{py:method} compound_noun(head_noun_SEMENT: pogg.my_delphin.my_delphin.SEMENT, non_head_noun_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.compound_noun

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.compound_noun
```

````

````{py:method} negation(negated_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.negation

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.negation
```

````

````{py:method} object_of_noun(head_noun_SEMENT: pogg.my_delphin.my_delphin.SEMENT, object_noun_SEMENT: pogg.my_delphin.my_delphin.SEMENT)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.object_of_noun

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.object_of_noun
```

````

````{py:method} object_of_verb(verb_SEMENT: pogg.my_delphin.my_delphin.SEMENT, object_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.object_of_verb

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.object_of_verb
```

````

````{py:method} cardinal_modifier(number_SEMENT: pogg.my_delphin.my_delphin.SEMENT, modified_SEMENT: pogg.my_delphin.my_delphin.SEMENT)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.cardinal_modifier

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.cardinal_modifier
```

````

````{py:method} ordinal_modifier(number_SEMENT: pogg.my_delphin.my_delphin.SEMENT, modified_SEMENT: pogg.my_delphin.my_delphin.SEMENT)
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ordinal_modifier

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.ordinal_modifier
```

````

````{py:method} subject_of_verb(verb_SEMENT: pogg.my_delphin.my_delphin.SEMENT, subject_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.subject_of_verb

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.subject_of_verb
```

````

````{py:method} passive_participle_modifier(participle_SEMENT: pogg.my_delphin.my_delphin.SEMENT, modified_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.passive_participle_modifier

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.passive_participle_modifier
```

````

````{py:method} present_participle_modifier(participle_SEMENT: pogg.my_delphin.my_delphin.SEMENT, modified_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.present_participle_modifier

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.present_participle_modifier
```

````

````{py:method} prepositional_relationship(preposition_predicate: str, figure_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ground_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.prepositional_relationship

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.prepositional_relationship
```

````

````{py:method} relative_direction(direction_predicate: str, figure_SEMENT: pogg.my_delphin.my_delphin.SEMENT, ground_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.relative_direction

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.relative_direction
```

````

````{py:method} possessive(possessor_SEMENT: pogg.my_delphin.my_delphin.SEMENT, possessed_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.possessive

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.possessive
```

````

````{py:method} quantify(quantifier_SEMENT: pogg.my_delphin.my_delphin.SEMENT, quantified_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.quantify

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.quantify
```

````

````{py:method} quantify_generic(quantified_SEMENT: pogg.my_delphin.my_delphin.SEMENT) -> pogg.my_delphin.my_delphin.SEMENT
:canonical: pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.quantify_generic

```{autodoc2-docstring} pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.quantify_generic
```

````

`````
