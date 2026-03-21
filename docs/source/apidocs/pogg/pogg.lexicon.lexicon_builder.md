# {py:mod}`pogg.lexicon.lexicon_builder`

```{py:module} pogg.lexicon.lexicon_builder
```

```{autodoc2-docstring} pogg.lexicon.lexicon_builder
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`POGGLexiconEntry <pogg.lexicon.lexicon_builder.POGGLexiconEntry>`
  - ```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconEntry
    :summary:
    ```
* - {py:obj}`POGGLexicon <pogg.lexicon.lexicon_builder.POGGLexicon>`
  - ```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon
    :summary:
    ```
* - {py:obj}`POGGLexiconUtil <pogg.lexicon.lexicon_builder.POGGLexiconUtil>`
  - ```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil
    :summary:
    ```
````

### API

`````{py:class} POGGLexiconEntry
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconEntry

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconEntry
```

````{py:attribute} key
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconEntry.key
:type: str
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconEntry.key
```

````

````{py:attribute} composition_function_name
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconEntry.composition_function_name
:type: str
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconEntry.composition_function_name
```

````

````{py:attribute} parameters
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconEntry.parameters
:type: dict
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconEntry.parameters
```

````

`````

`````{py:class} POGGLexicon
:canonical: pogg.lexicon.lexicon_builder.POGGLexicon

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon
```

````{py:attribute} name
:canonical: pogg.lexicon.lexicon_builder.POGGLexicon.name
:type: str
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon.name
```

````

````{py:attribute} directory
:canonical: pogg.lexicon.lexicon_builder.POGGLexicon.directory
:type: str
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon.directory
```

````

````{py:attribute} node_entries
:canonical: pogg.lexicon.lexicon_builder.POGGLexicon.node_entries
:type: typing.Dict[str, pogg.lexicon.lexicon_builder.POGGLexiconEntry]
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon.node_entries
```

````

````{py:attribute} edge_entries
:canonical: pogg.lexicon.lexicon_builder.POGGLexicon.edge_entries
:type: typing.Dict[str, pogg.lexicon.lexicon_builder.POGGLexiconEntry]
:value: >
   None

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexicon.edge_entries
```

````

`````

`````{py:class} POGGLexiconUtil
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil
```

````{py:method} initialize_lexicon_directory(lexicon_name, lexicon_directory, lexicon_skeleton=None)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.initialize_lexicon_directory
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.initialize_lexicon_directory
```

````

````{py:method} convert_dict_entry_to_POGGLexiconEntry(entry_key, dict_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry
```

````

````{py:method} convert_POGGLexiconEntry_to_dict_entry(pogg_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.convert_POGGLexiconEntry_to_dict_entry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.convert_POGGLexiconEntry_to_dict_entry
```

````

````{py:method} create_lexicon_skeleton(graph_json)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.create_lexicon_skeleton
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.create_lexicon_skeleton
```

````

````{py:method} read_lexicon_from_directory(lexicon_name, lexicon_directory)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.read_lexicon_from_directory
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.read_lexicon_from_directory
```

````

````{py:method} validate_node_entry(node_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_node_entry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_node_entry
```

````

````{py:method} validate_edge_entry(edge_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_edge_entry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_edge_entry
```

````

````{py:method} check_node_entry_completion(node_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_node_entry_completion
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_node_entry_completion
```

````

````{py:method} check_edge_entry_completion(edge_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_edge_entry_completion
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_edge_entry_completion
```

````

````{py:method} expand_node_entry(node_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_node_entry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_node_entry
```

````

````{py:method} expand_edge_entry(edge_entry)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_edge_entry
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_edge_entry
```

````

````{py:method} load_latest_lexicon_json_data(lexicon_directory)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.load_latest_lexicon_json_data
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.load_latest_lexicon_json_data
```

````

````{py:method} dump_lexicon_json_data(lexicon_directory, complete, incomplete, invalid)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_lexicon_json_data
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_lexicon_json_data
```

````

````{py:method} add_new_graph_data_to_lexicon(lexicon_name, lexicon_directory, new_lexicon_skeleton)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.add_new_graph_data_to_lexicon
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.add_new_graph_data_to_lexicon
```

````

````{py:method} update_lexicon_files(lexicon_directory)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.update_lexicon_files
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.update_lexicon_files
```

````

````{py:method} dump_complete_lexicon_object_to_json(lexicon_dump_file_path, lexicon_object)
:canonical: pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_complete_lexicon_object_to_json
:staticmethod:

```{autodoc2-docstring} pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_complete_lexicon_object_to_json
```

````

`````
