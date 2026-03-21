# {py:mod}`pogg.semantic_composition.sement_util`

```{py:module} pogg.semantic_composition.sement_util
```

```{autodoc2-docstring} pogg.semantic_composition.sement_util
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`POGGSEMENTUtil <pogg.semantic_composition.sement_util.POGGSEMENTUtil>`
  - ```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil
    :summary:
    ```
````

### API

`````{py:class} POGGSEMENTUtil
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil
```

````{py:method} add_intrinsic_variable_property(sement, property_name, property_value)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.add_intrinsic_variable_property
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.add_intrinsic_variable_property
```

````

````{py:method} get_key_rel(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_key_rel
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_key_rel
```

````

````{py:method} duplicate_sement(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.duplicate_sement
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.duplicate_sement
```

````

````{py:method} group_equalities(equalities)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.group_equalities
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.group_equalities
```

````

````{py:method} get_most_specified_variable(eq_vars)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_most_specified_variable
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_most_specified_variable
```

````

````{py:method} overwrite_eqs(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.overwrite_eqs
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.overwrite_eqs
```

````

````{py:method} check_if_quantified(check_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.check_if_quantified
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.check_if_quantified
```

````

````{py:method} is_sement_isomorphic(s1: pogg.my_delphin.my_delphin.SEMENT, s2: pogg.my_delphin.my_delphin.SEMENT) -> bool
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.is_sement_isomorphic
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.is_sement_isomorphic
```

````

````{py:method} create_variable_roles_dict(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_variable_roles_dict
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_variable_roles_dict
```

````

````{py:method} create_hcons_list(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_hcons_list
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_hcons_list
```

````

````{py:method} create_icons_list(sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_icons_list
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_icons_list
```

````

````{py:method} find_slot_overlaps(gold_sement, actual_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_slot_overlaps
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_slot_overlaps
```

````

````{py:method} find_var_eq_overlaps(gold_sement, actual_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_var_eq_overlaps
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_var_eq_overlaps
```

````

````{py:method} find_hcons_overlaps(gold_sement, actual_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_hcons_overlaps
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_hcons_overlaps
```

````

````{py:method} find_icons_overlaps(gold_sement, actual_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_icons_overlaps
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_icons_overlaps
```

````

````{py:method} _build_overlap_slots_table(overlap_slots)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_slots_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_slots_table
```

````

````{py:method} _build_nonoverlap_slots_table(nonoverlap_slots, table_type)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_slots_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_slots_table
```

````

````{py:method} _build_overlap_eqs_table(overlap_eqs)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_eqs_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_eqs_table
```

````

````{py:method} _build_overlap_eqs_prop_diff_table(overlap_eqs_prop_diff)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_eqs_prop_diff_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_eqs_prop_diff_table
```

````

````{py:method} _build_nonoverlap_eqs_table(nonoverlap_eqs, table_type)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_eqs_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_eqs_table
```

````

````{py:method} _build_overlap_hcons_table(overlap_hcons)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_hcons_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_hcons_table
```

````

````{py:method} _build_nonoverlap_hcons_table(nonoverlap_hcons, table_type)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_hcons_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_hcons_table
```

````

````{py:method} _build_overlap_icons_table(overlap_icons)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_icons_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_icons_table
```

````

````{py:method} _build_nonoverlap_icons_table(nonoverlap_icons, table_type)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_icons_table
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_icons_table
```

````

````{py:method} build_isomorphism_report(gold_sement, actual_sement)
:canonical: pogg.semantic_composition.sement_util.POGGSEMENTUtil.build_isomorphism_report
:staticmethod:

```{autodoc2-docstring} pogg.semantic_composition.sement_util.POGGSEMENTUtil.build_isomorphism_report
```

````

`````
