"""
The lexicon_builder module contains the POGGLexiconBuilder and POGGLexicon classes that help the user put together
and store the lexicon for their dataset

[See usage examples here](project:/usage_nbs/pogg/lexicon/lexicon_builder_usage.ipynb)
"""
from dataclasses import dataclass
import os
import glob
import json
import inspect
from typing import Dict

import pogg.semantic_composition.semantic_composition


@dataclass(order=True)
class POGGLexiconEntry:
    """
    `POGGLexiconEntry` is a [dataclass](https://peps.python.org/pep-0557/#abstract).
    It stores information about an entry in the lexicon but doesn't have any logic of its own.

    **Parameters / Instance Attributes**

    Each parameter may also be accessed as an instance attribute.

    | Parameter | Type | Description | Default |
    | --------- | ---- | ------------ | ------ |
    | `key` | `str` | key to the lexicon entry | None |
    | `composition_function_name` | `str` | name of the function in the SemanticComposition class | None |
    | `parameters` | `dict` of `str:str` | parameters the composition function requires | None  |
    """


    key: str
    """
    Key to the lexicon entry.
    
    For example, the lexicon may have an entry whose key is `cake` and any node in a dataset of graphs that represents a cake 
    (e.g. a node called `cake1` or even just `cake`) will refer to this entry when determining how to generate a SEMENT representing that node. 
    """

    composition_function_name: str
    """
    Name of the function in the SemanticComposition class that graph elements that refer to this entry will generate from.
    
    For example, a lexicon entry whose key is `cake` would likely have a `composition_function_name` value of `noun` to reflect that nodes that refer to this entry
    should generate a SEMENT for a simple noun. 
    """

    parameters: dict
    """
    Parameters the composition function requires.
    
    For a lexicon entry whose and `composition_function_name` is `noun`, the parameters required, per the function signature of `noun` from the `SemanticComposition` class,
    will be `predicate` and `intrinsic_variable_properties` so the parameters for the lexicon entry may look something like this:
    
    ```
    {
        'predicate': '_cake_n_1',
        'intrinsic_variable_properties': {'NUM': 'sg'}
    }
    ``` 
    """


@dataclass
class POGGLexicon:
    """
    `POGGLexicon` is a [dataclass](https://peps.python.org/pep-0557/#abstract).
    It stores information about the lexicon such as where its stored and its entries.

    **Parameters / Instance Attributes**

    Each parameter may also be accessed as an instance attribute.

    | Parameter | Type | Description | Default |
    | --------- | ---- | ------------ | ------ |
    | `name` | `str` | name of the lexicon | None |
    | `directory` | `str` | path to the lexicon's files | None |
    | `node_entries` | `dict` of `str:POGGLexiconEntry` | dictionary of lexicon entries relevant for nodes in graphs | None  |
    | `edge_entries` | `dict` of `str:POGGLexiconEntry` | dictionary of lexicon entries relevant for edges in graphs | None  |
    """

    name: str
    """
    Name of the lexicon.
    """

    directory: str
    """
    Path to the lexicon's files.
    """

    node_entries: Dict[str, POGGLexiconEntry]
    """
    Dictionary of lexicon entries relevant for nodes in graphs.
    """

    edge_entries: Dict[str, POGGLexiconEntry]
    """
    Dictionary of lexicon entries relevant for edges in graphs.
    """

    # complete_entries_file: str = os.path.join(directory, f"{name}_lexicon_complete_entries.json")
    # incomplete_entries_file: str = os.path.join(directory, f"{name}_lexicon_incomplete_entries.json")
    # invalid_entries_file: str = os.path.join(directory, f"{name}_lexicon_invalid_entries.json")
    # all_entries_file: str = os.path.join(directory, f"{name}_lexicon_all_entries.json")




class POGGLexiconUtil:
    """Provides static functions for initializing, updating, and outputting lexicon information."""
    @staticmethod
    def initialize_lexicon_directory(lexicon_name, lexicon_directory, lexicon_skeleton=None):
        """
        Initialize the lexicon directory with 4 starter files:

        1. `lexicon_complete_entries.json` -- contains complete entries; this is the file that is loaded when making a `POGGLexicon` object
        2. `lexicon_incomplete_entries.json` -- contains incomplete entries; the user needs to fill these out to make them complete
        3. `lexicon_invalid_entries.json` -- contains invalid entries along with an error message for what makes them invalid
        4. `lexicon_all_entries.json` -- contains all complete, incomplete, and invalid entries

        Each file is prefixed with the `lexicon_name`.

        **Parameters**
        | Parameter | Type | Default | Description |
        | --------- | ---- | ------- | ----------- |
        | `lexicon_name` | `str` | -- | name of the lexicon, used as a prefix to all lexicon file names |
        | `lexicon_directory` | `str` | -- | path to directory where lexicon files should be stored |
        | `lexicon_skeleton` | `dict` | None | optional lexicon skeleton to dump into the `lexicon_incomplete_entries.json` file in the initialized directory |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `None` | -- |
        """

        files = []
        files.append(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_complete_entries.json"))
        files.append(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_incomplete_entries.json"))
        files.append(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_invalid_entries.json"))
        files.append(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_all_entries.json"))

        files.append(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_auto_entries.json"))

        starter_dict = {
            "node_keys": {},
            "edge_keys": {}
        }

        for file_name in files:
            if not os.path.isfile(file_name):
                with open(file_name, "w+") as f:
                    # if lexicon_skeleton is provided, dump it into the incomplete file instead of the starter dict
                    if lexicon_skeleton is not None and ("_incomplete_entries" in file_name or "_all_entries" in file_name):
                        json.dump(lexicon_skeleton, f, indent=4)
                    else:
                        json.dump(starter_dict, f, indent=4)
            else:
                pass

    @staticmethod
    def convert_dict_entry_to_POGGLexiconEntry(entry_key, dict_entry):
        """
        Converts an entry from the JSON format into a [POGGLexiconEntry](#pogg.lexicon.lexicon_builder.POGGLexiconEntry) object

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `entry_key` | `str` | key for the entry from the JSON object |
        | `dict_entry` | `dict` of `str:str` | value for the entry from the JSON object |

        ````{example} Dict entry example
        :collapsible:
        Node Entry Example
        ```
        "bright": {
            "comp_fxn": "adjective",
            "predicate": "_bright_a_1",
            "intrinsic_variable_properties": {}
        }
        ```

        Edge Entry Example
        ```
        "idColor": {
            "comp_fxn": "prenominal_adjective",
            "adjective_sement": "child",
            "nominal_sement": "parent"
        }
        ```
        ````

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGLexiconEntry` | `POGGLexiconEntry` object containing the information from the dict entry |
        """

        # make top level entry
        entry = POGGLexiconEntry(entry_key, dict_entry["comp_fxn"], {})
        for param_name in dict_entry.keys():
            if param_name != "comp_fxn":
                param_value = dict_entry[param_name]
                # if the parameter is a dict with its own "comp_fxn" then make a sub POGGLexiconEntry
                if type(param_value) is dict and "comp_fxn" in param_value:
                    param_value = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(param_name, param_value)
                # add value to parameters_dict
                entry.parameters[param_name] = param_value

        return entry

    @staticmethod 
    def convert_POGGLexiconEntry_to_dict_entry(pogg_entry):
        """
        Converts a [POGGLexiconEntry](#pogg.lexicon.lexicon_builder.POGGLexiconEntry) object into the JSON format

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `pogg_entry` | `POGGLexiocnEntry` | `POGGLexiconEntry` |

        ````{example} Dict entry example
        :collapsible:
        Node Entry Example
        ```
        "bright": {
            "comp_fxn": "adjective",
            "predicate": "_bright_a_1",
            "intrinsic_variable_properties": {}
        }
        ```

        Edge Entry Example
        ```
        "idColor": {
            "comp_fxn": "prenominal_adjective",
            "adjective_sement": "child",
            "nominal_sement": "parent"
        }
        ```
        ````

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `dict` | Dictionary in the JSON format that is found in the JSON lexicon files |
        """

        dict_entry = {
            "comp_fxn": pogg_entry.composition_function_name
        }
        for param_name in pogg_entry.parameters:
            if isinstance(pogg_entry.parameters[param_name], POGGLexiconEntry):
                dict_entry[param_name] = POGGLexiconUtil.convert_POGGLexiconEntry_to_dict_entry(pogg_entry.parameters[param_name])
            else:
                dict_entry[param_name] = pogg_entry.parameters[param_name]

        return dict_entry

    @staticmethod
    def create_lexicon_skeleton(graph_json):
        """
        Creates a lexicon skeleton based on the information in a graph JSON object.
        The skeleton is returned as a JSON object, which should be dumped to the `lexicon_incomplete_entries.json` file where the user must update it to add more information.

        ````{example} Skeleton example
        :collapsible:
        Imagine a graph with just one node, `cake`. Below is the information about that node contained in the resulting skeleton:
        ```
        "cake": {
            "comp_fxn": ""
        }
        ```
        Once the skeleton is dumped to `lexicon_incomplete_entries.json`, the user should then specify what composition function is appropriate from the `SemanticComposition` class (e.g. `noun`) and run `POGGLexiconUtil.update_lexicon_files`.
        This will result in the following:

        ```
        "cake": {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        ````

        The entry now has more information which was pulled from the requirements for the `noun` function. The user must also fill this out.
        This process continues until the lexicon update function detects that an entry is complete, at which point it will be moved over to `lexicon_complete_entries.json`.

        ````

        See the [How To Create a POGG Lexicon]() page for more details on the full process for creating a lexicon.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `graph_json` | JSON object | JSON object that contains information about all nodes and edges for all graphs in a dataset |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | JSON object | resulting lexicon skeleton in JSON format |
        """

        lexicon_skeleton = {
            'node_keys': {},
            'edge_keys': {}
        }

        # add keys for every node in graph_json
        # graph_json['nodes'] is a dict
        for node_name in graph_json['nodes'].keys():
            node_information = graph_json['nodes'][node_name]

            if 'lexicon_key' in node_information:
                node_lexicon_key = node_information['lexicon_key']
                # only add if it's not already been added to node_keys
                if node_lexicon_key not in lexicon_skeleton['node_keys']:
                    lexicon_skeleton['node_keys'][str(node_lexicon_key)] = {"comp_fxn": ""}
            else:
                # only add if it's not already been added to node_keys
                if node_name not in lexicon_skeleton['node_keys']:
                    lexicon_skeleton['node_keys'][str(node_name)] = {"comp_fxn": ""}


        # add keys for every edge in graph_json
        # graph_json['edges'] is a list
        for edge in graph_json['edges']:
            edge_name = edge['edge_name']

            if 'lexicon_key' in edge:
                edge_lexicon_key = edge['lexicon_key']
                # only add if it's not already been added to edge_keys
                if edge_lexicon_key not in lexicon_skeleton['edge_keys']:
                    lexicon_skeleton['edge_keys'][str(edge_lexicon_key)] = {"comp_fxn": ""}
            else:
                # only add if it's not already been added to edge_keys
                if edge_name not in lexicon_skeleton['edge_keys']:
                    lexicon_skeleton['edge_keys'][str(edge_name)] = {"comp_fxn": ""}

            # check that parent and child node are in lexicon_skeleton
            if not edge['parent_node'] in graph_json['nodes'].keys():
                lexicon_skeleton['node_keys'][str(edge['parent_node'])] = {"comp_fxn": ""}

            if not edge['child_node'] in graph_json['nodes'].keys():
                lexicon_skeleton['node_keys'][str(edge['child_node'])] = {"comp_fxn": ""}


        # sort the node_keys
        lexicon_skeleton['node_keys'] = dict(sorted(lexicon_skeleton['node_keys'].items()))
        # sort the edge_keys
        lexicon_skeleton['edge_keys'] = dict(sorted(lexicon_skeleton['edge_keys'].items()))


        return lexicon_skeleton

    @staticmethod
    def read_lexicon_from_directory(lexicon_name, lexicon_directory):
        """
        Given a directory containing lexicon information, read it in and store it in a `POGGLexicon` object

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_name` | `str` | name of the lexicon |
        | `lexicon_directory` | `str` | path to the lexicon's directory |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGLexicon` | the `POGGLexicon` object created from the data in the lexicon directory |
        """

        try:
            lexicon_filepath = glob.glob(os.path.join(lexicon_directory, "*_complete_entries.json"))[0]
        except IndexError as err:
            raise IndexError(f"No files in {os.path.abspath(lexicon_directory)} end in the pattern _complete_entries.json") from err


        return POGGLexiconUtil.read_lexicon_from_file(lexicon_name, lexicon_filepath)

    @staticmethod
    def read_lexicon_from_file(lexicon_name, lexicon_filepath):
        """
        Given a file containing lexicon information, read it in and store it in a `POGGLexicon` object

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_name` | `str` | name of the lexicon |
        | `lexicon_filepath` | `str` | path to the lexicon file |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `POGGLexicon` | the `POGGLexicon` object created from the data in the lexicon directory |
        """

        # ignore the lexicon directory when just reading from a file
        lexicon = POGGLexicon(lexicon_name, None, {}, {})

        # use this if a file is empty and JSON object can't be loaded
        empty_lexicon = {
            "node_keys": {},
            "edge_keys": {}
        }

        try:
            with open(lexicon_filepath, "r") as lexicon_file:
                try:
                    lexicon_json = json.load(lexicon_file)
                except json.decoder.JSONDecodeError:
                    lexicon_json = empty_lexicon.copy()
        except IndexError as err:
            raise IndexError(
                f"No such file {lexicon_filepath}") from err

        node_entries = lexicon_json["node_keys"]
        for key in node_entries.keys():
            lexicon.node_entries[key] = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(key, node_entries[key])

        edge_entries = lexicon_json["edge_keys"]
        for key in edge_entries.keys():
            lexicon.edge_entries[key] = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(key, edge_entries[key])

        return lexicon

    @staticmethod
    def validate_node_entry(node_entry):
        """
        Validate whether a node entry in the lexicon is legitimate.
        This function is used when updating lexicon files to check if any entries need to be moved to `lexicon_invalid_entries.json` for the user to fix.

        ````{info} What makes an entry invalid?
        :collapsible:

        1. A nonexistent semantic composition function is listed for `comp_fxn`
        2. A nonexistent parameter of the composition function is listed in the entry
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `node_entry` | `dict` | the node entry to validate |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `boolean` | result of the validation check |
        """
        # node_entry == "" -- when the inside of an edge is being treated as a "node" TODO ?
        # node_entry == {} -- node_entry not filled out (and missing "comp_fxn" for some reason...)
        # node_entry == None -- when a comp_fxn's parameter of type SEMENT is optional and the user is specifying they aren't including it
        if node_entry == "" or node_entry == {} or node_entry is None:
            return True

        comp_fxn_name = node_entry["comp_fxn"]
        # if comp_fxn_name is empty, it's incomplete, so just return
        if comp_fxn_name == "":
            return True

        # if there's an existing failure message, clear it out
        if "failure_msg" in node_entry:
            node_entry.pop("failure_msg")

        try:
            comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
            parameters = inspect.signature(comp_fxn_obj).parameters

            # check that the parameters in the node_entry are legitimate
            for key in node_entry.keys():
                if key != "comp_fxn" and key != "auto":
                    if key not in parameters:
                        node_entry["failure_msg"] = f"{key} is not a parameter of {comp_fxn_name}"
                        raise KeyError(node_entry["failure_msg"], node_entry)

                    # if it is legitimate AND the type is SEMENT, validation needs to recurse
                    elif parameters[key].annotation.__name__ == "SEMENT":
                        POGGLexiconUtil.validate_node_entry(node_entry[key])


        except AttributeError as err:
            # if there's an extra argument in the error then that means node_entry is being passed up
            # so the failure_msg should already be included from a previous level of the stack
            # and shouldn't be duplicated higher up
            if len(err.args) <= 1:
                node_entry["failure_msg"] = f"{comp_fxn_name} is not an existing Semantic Composition Function"
                raise AttributeError(node_entry["failure_msg"], node_entry)
            else:
                # pass the error up the stack using the existing error message
                raise AttributeError(err.args[0], node_entry)

        except KeyError as err:
            # err will either be the KeyError raised above or one that came from deeper in the stack
            # but we want to update with the highest level of "node_entry"
            # this is redundant if it's not nested but if it is it will provide the full node_entry in the final message
            raise KeyError(err.args[0], node_entry)

        return True

    @staticmethod
    def validate_edge_entry(edge_entry):
        """
        Validate whether an edge entry in the lexicon is legitimate.
        This function is used when updating lexicon files to check if any entries need to be moved to `lexicon_invalid_entries.json` for the user to fix.

        ````{info} What makes an entry invalid?
        :collapsible:

        1. A nonexistent semantic composition function is listed for `comp_fxn`
        2. A nonexistent parameter of the composition function is listed in the entry
        3. There aren't two parameters whose types are `SEMENT` with values of `"parent"` and `"child"`

        Regarding case 3, imagine an edge that specifies the flavor of a treat. Let's say that the edge exits from the node for the treat itself (e.g. "cake"),
        and points to the flavor (e.g. "vanilla"). For an edge like this, the entry would specify that the composition function is `compound_noun`.
        The two parameters of `compound_noun` are `head_noun_sement` and `non_head_noun_sement`. In this case, the `head_noun_sement` is the parent node,
        so the value should be `"parent"`, and the `non_head_noun_sement` is the child node, so the value should be `"child"`.
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `edge_entry` | `dict` | the edge entry to validate |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `boolean` | result of the validation check |
        """

        comp_fxn_name = edge_entry["comp_fxn"]
        # if comp_fxn_name is empty, it's incomplete, so just return

        # if there's an existing failure message, clear it out
        if "failure_msg" in edge_entry:
            edge_entry.pop("failure_msg")

        if comp_fxn_name == "":
            return True

        try:
            comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
            parameters = inspect.signature(comp_fxn_obj).parameters

            # check that the parameters in the edge_entry are legitimate
            for key in edge_entry.keys():
                if key != "comp_fxn":
                    if key not in parameters:
                        edge_entry["failure_msg"] = f"{key} is not a parameter of {comp_fxn_name}"
                        raise KeyError(edge_entry["failure_msg"], edge_entry)

                    # if it is legitimate AND the type is SEMENT, then the value should either be "parent" or "child"
                    elif parameters[key].annotation.__name__ == "SEMENT":
                        # if the value is empty, it's not complete so just continue
                        if edge_entry[key] == "":
                            continue
                        elif edge_entry[key] == "parent" or edge_entry[key] == "child":
                            continue
                        # if the edge is introducing another SEMENT directly, continue
                        elif isinstance(edge_entry[key], dict):
                            # if it's introducing its own SEMENT it should mimic a node entry
                            POGGLexiconUtil.validate_node_entry(edge_entry[key])
                        else:
                            edge_entry["failure_msg"] = f"{key} should have a value of 'parent' or 'child', introduce a SEMENT via a comp_fxn, or be set to 'null' if it's an optional argument"
                            raise ValueError(edge_entry["failure_msg"], edge_entry)
                    else:
                        continue
        except AttributeError as err:
            # raised when getattr() above fails
            edge_entry["failure_msg"] = f"{comp_fxn_name} is not an existing Semantic Composition Function"
            raise AttributeError(err.args[0], edge_entry)

        return True

    @staticmethod
    def check_node_entry_completion(node_entry):
        """
        Check whether a node entry in the lexicon is completely filled out.
        This function is used when updating lexicon files to check if any entries need to be moved to `lexicon_complete_entries.json`.

        ````{info} What makes an entry complete?
        :collapsible:

        1. It must have a composition function listed
        2. All non-optional parameters that composition function expects must be present and filled out for the entry

        For example:
        ```
        "cake": {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1"
        }
        ```
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `node_entry` | `dict` | the node entry to for completion |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `boolean` | result of the completion check |
        """

        # node_entry == "" -- when the inside of an edge is being treated as a "node" TODO ?
        if node_entry == "":
            return False

        comp_fxn_name = node_entry["comp_fxn"]

        if comp_fxn_name == "":
            return False

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that AREN'T SEMENTs
            # "advanced" users can use them if they want
            # TODO: way to turn this on or off?
            if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
                continue

            # if the parameter from the signature is in the node entry...
            if param_name in node_entry.keys():
                # recurse for SEMENT parameters
                if param_information.annotation.__name__ == "SEMENT":
                    # if the SEMENT type parameter is optional and the value is set to None, keep going
                    if param_information.default is not inspect.Parameter.empty and node_entry[param_name] is None:
                        continue
                    # if the SEMENT type parameter is NOT optional and has no value, entry is not complete
                    elif not POGGLexiconUtil.check_node_entry_completion(node_entry[param_name]):
                        return False

                if node_entry[param_name] == "":
                    return False
            else:
                return False

        return True

    @staticmethod
    def check_edge_entry_completion(edge_entry):
        """
        Check whether an edge entry in the lexicon is completely filled out.
        This function is used when updating lexicon files to check if any entries need to be moved to `lexicon_complete_entries.json`.

        ````{info} What makes an entry complete?
        :collapsible:

        1. It must have a composition function listed
        2. All non-optional parameters that composition function expects must be present and filled out for the entry*

        * If the optional parameter is of type `SEMENT` and the user does not want this SEMENT to be included in
        the construction then the value should be `null`

        For example:
        ```
        "flavor": {
            "comp_fxn": "compound_noun",
            "head_noun_sement": "parent",
            "non_head_noun_sement": "child"
        }
        ```
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `edge_entry` | `dict` | the edge entry to for completion |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `boolean` | result of the completion check |
        """

        comp_fxn_name = edge_entry["comp_fxn"]

        if comp_fxn_name == "":
            return False

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and parameters with default values that AREN'T SEMENTs (e.g. intrinsic_variable_properties dict)
            # 'advanced' users can add them if they want
            # TODO: toggle?
            if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
                continue

            if param_name in edge_entry.keys():
                # if it's empty
                if edge_entry[param_name] == "":
                    return False
                # if it's a SEMENT type parameter with a default value and the lexicon says "None" then keep going
                elif (param_information.annotation.__name__ == "SEMENT" and param_information.default is not inspect.Parameter.empty
                    and edge_entry[param_name] is None):
                    continue
                # if it introduces its own SEMENT
                elif isinstance(edge_entry[param_name], dict):
                    # check completion as a node
                    if not POGGLexiconUtil.check_node_entry_completion(edge_entry[param_name]):
                        return False
                    else:
                        continue
            else:
                return False

        return True

    @staticmethod
    def expand_node_entry(node_entry):
        """
        Expand a node entry when the user provides some information about it.
        This function is used when updating lexicon files.

        ````{example} Example of expansion
        :collapsible:

        Say we have the following node entry in `lexicon_incomplete_entries.json`:

        ```
        "cake": {
            "comp_fxn": ""
        }
        ```

        The user needs to specify what function from the `SemanticComposition` class is appropriate to generate a SEMENT for this node.
        In this case, `noun` is likely the most appropriate:

        ```
        "cake": {
            "comp_fxn": "noun"
        }
        ```

        Once the user does this and `update_lexicon_files` is run, the parameters required for the `noun` function will be
        inserted into the entry for the user to fill out:

        ```
        "cake": {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        ```

        This process continues for any parameters that continue requiring more information
        until the entry is detected to be complete and moved to `lexicon_complete_entries.json` during the `update_lexicon_files` call.
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `node_entry` | `dict` | the node entry to expand |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `dict` | the expanded node entry  |
        """

        # if the entry is empty or None, just return
        if node_entry == "" or node_entry is None:
            return node_entry

        # get the top level function name
        comp_fxn_name = node_entry['comp_fxn']

        # can't be expanded if comp_fxn is not filled in yet, so return as is
        if comp_fxn_name == "":
            return node_entry

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that aren't SEMENTs (e.g. intrinsic_variable_properties dict)
            if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
                continue
            # if the param_name is not in the entry, add it with an appropriate "empty" value for the user to fill in
            elif param_name not in node_entry:
                # if parameter's type is SEMENT then it requires its own composition
                if param_information.annotation.__name__ == "SEMENT":
                    node_entry[param_name] = {"comp_fxn": ""}
                # if parameter's type is dict insert empty dict
                elif param_information.annotation.__name__ == "dict":
                    node_entry[param_name] = {}
                # otherwise insert empty string
                else:
                    node_entry[param_name] = ""

            # if it is in the entry AND the type is SEMENT, recurse down for further expansion
            # e.g., if the top level comp_fxn is "prenominal_adjective,"
            # then the parameters (adjective_sement, nominal_sement) will themselves to be expanded with comp_fxn info
            else:
                if param_information.annotation.__name__ == "SEMENT":
                    POGGLexiconUtil.expand_node_entry(node_entry[param_name])
                else:
                    pass

        return node_entry

    @staticmethod
    def expand_edge_entry(edge_entry):
        """
        Expand an edge entry when the user provides some information about it.
        This function is used when updating lexicon files.

        ````{info} Example of expansion
        :collapsible:

        Say we have the following edge entry in `lexicon_incomplete_entries.json`:

        ```
        "flavor": {
            "comp_fxn": ""
        }
        ```

        The user needs to specify what function from the `SemanticComposition` class is appropriate to generate a SEMENT for this node.
        In this case, `compound_noun` is likely the most appropriate:

        ```
        "flavor": {
            "comp_fxn": "compound_noun"
        }
        ```

        Once the user does this and `update_lexicon_files` is run, the parameters required for the `noun` function will be
        inserted into the entry for the user to fill out:

        ```
        "flavor": {
            "comp_fxn": "noun",
            "head_noun_sement": "",
            "non_head_noun_sement": ""
        }
        ```

        This process continues for any parameters that continue requiring more information
        until the entry is detected to be complete and moved to `lexicon_complete_entries.json` during the `update_lexicon_files` call.
        ````

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `edge_entry` | `dict` | the edge entry to expand |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `dict` | the expanded edge entry  |
        """

        # TODO: this only comes up when we're treating the inside of an edge as a "node" and it hasn't been filled out yet
        # TODO: maybe a better way to deal with this...?
        # can't expand yet so just return
        if edge_entry == "":
            return edge_entry

        # get the top level function name
        comp_fxn_name = edge_entry['comp_fxn']

        # can't be expanded if comp_fxn is not filled in yet, so return as is
        if comp_fxn_name == "":
            return edge_entry

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.semantic_composition.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that aren't SEMENTs (e.g. intrinsic_variable_properties dict)
            if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
                continue
            # if the param_name is not in the entry, add it with an appropriate "empty" value for the user to fill in
            elif param_information.annotation.__name__ == "dict":
                edge_entry[param_name] = {}
            elif param_name not in edge_entry:
                edge_entry[param_name] = ""
            # if it is in the entry, the type is SEMENT, and the value is not "parent" or "child", recurse down for further expansion
            elif (param_information.annotation.__name__ == "SEMENT"
                  and not (edge_entry[param_name] == "parent" or edge_entry[param_name] == "child")):
                POGGLexiconUtil.expand_edge_entry(edge_entry[param_name])
            else:
                pass

        return edge_entry

    @staticmethod
    def load_latest_lexicon_json_data(lexicon_directory):
        """
        Load the latest information from the lexicon files in the provided directory.
        This is used during the `update_lexicon_files` call to update and move entries as appropriate when the user adds information to them.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_directory` | `str` | path to the lexicon's directory |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `dict` | latest entries from the `lexicon_complete_entries.json` file |
        | `dict` | latest entries from the `lexicon_incomplete_entries.json` and `lexicon_invalid_entries.json` files |
        """

        with (open(glob.glob(os.path.join(lexicon_directory, "*_complete_entries.json"))[0], "r") as complete_entries_file,
              open(glob.glob(os.path.join(lexicon_directory, "*_incomplete_entries.json"))[0], "r") as incomplete_entries_file,
              open(glob.glob(os.path.join(lexicon_directory, "*_invalid_entries.json"))[0],"r") as invalid_entries_file):

            # use this if a file is empty and JSON object can't be loaded
            empty_lexicon = {
                "node_keys": {},
                "edge_keys": {}
            }

            try:
                latest_complete_entries = json.load(complete_entries_file)
            except json.decoder.JSONDecodeError:
                latest_complete_entries = empty_lexicon.copy()

            try:
                updated_incomplete_entries = json.load(incomplete_entries_file)
            except json.decoder.JSONDecodeError:
                updated_incomplete_entries = empty_lexicon.copy()

            try:
                updated_invalid_entries = json.load(invalid_entries_file)
            except json.decoder.JSONDecodeError:
                updated_invalid_entries = empty_lexicon.copy()

            # include all entries in updated_entries
            # completed entries may be rendered invalid if the code changes
            updated_entries = {
                "node_keys": updated_incomplete_entries["node_keys"],
                "edge_keys": updated_incomplete_entries["edge_keys"],
            }

            updated_entries['node_keys'].update(updated_invalid_entries['node_keys'])
            updated_entries['edge_keys'].update(updated_invalid_entries['edge_keys'])

            updated_entries['node_keys'].update(latest_complete_entries['node_keys'])
            updated_entries['edge_keys'].update(latest_complete_entries['edge_keys'])


        return updated_entries

    @staticmethod
    def dump_lexicon_json_data(lexicon_directory, complete, incomplete, invalid):
        """
        Dump the entries for the lexicon into the appropriate files.
        This is used during the `update_lexicon_files` call to update and move entries as appropriate when the user adds information to them.

        This is distinct from [dump_complete_lexicon_object_to_json](#pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_complete_lexicon_object_to_json)
        in that this function is for updating the lexicon files as they are being edited.
        [dump_complete_lexicon_object_to_json](#pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_complete_lexicon_object_to_json), on the other hand,
        is for dumping a complete lexicon object to one JSON file to have a record of the state of the lexicon during a particular run of POGG's conversion algorithm.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_directory` | `str` | path to the lexicon's directory |
        | `complete` | `dict` | entries to be dumped to `lexicon_complete_entries.json` |
        | `incomplete` | `dict` | entries to be dumped to `lexicon_incomplete_entries.json` |
        | `invalid` | `dict` | entries to be dumped to `lexicon_invalid_entries.json` |

        **Returns**
        | Type |
        | ---- |
        | `None` |
        """

        with (open(glob.glob(os.path.join(lexicon_directory, "*_complete_entries.json"))[0], "w") as comp_file,
              open(glob.glob(os.path.join(lexicon_directory, "*_incomplete_entries.json"))[0], "w") as incomp_file,
              open(glob.glob(os.path.join(lexicon_directory, "*_invalid_entries.json"))[0], "w") as invalid_file,
              open(glob.glob(os.path.join(lexicon_directory, "*_all_entries.json"))[0], "w") as all_file):

            if complete is None:
                new_complete = {
                    "node_keys": {},
                    "edge_keys": {}
                }
            else:
                new_complete = {
                    "node_keys": dict(sorted(complete['node_keys'].items())),
                    "edge_keys": dict(sorted(complete['edge_keys'].items()))
                }

            if incomplete is None:
                new_incomplete = {
                    "node_keys": {},
                    "edge_keys": {}
                }
            else:
                new_incomplete = {
                    "node_keys": dict(sorted(incomplete['node_keys'].items())),
                    "edge_keys": dict(sorted(incomplete['edge_keys'].items()))
                }

            if invalid is None:
                new_invalid = {
                    "node_keys": {},
                    "edge_keys": {}
                }
            else:
                new_invalid = {
                    "node_keys": dict(sorted(invalid['node_keys'].items())),
                    "edge_keys": dict(sorted(invalid['edge_keys'].items()))
                }


            json.dump(new_complete, comp_file, indent=4)
            json.dump(new_incomplete, incomp_file, indent=4)
            json.dump(new_invalid, invalid_file, indent=4)

            all_entries = {
                "node_keys": {},
                "edge_keys": {}
            }
            all_entries['node_keys'].update(new_complete['node_keys'])
            all_entries['node_keys'].update(new_incomplete['node_keys'])
            all_entries['node_keys'].update(new_invalid['node_keys'])

            all_entries['edge_keys'].update(new_complete['edge_keys'])
            all_entries['edge_keys'].update(new_incomplete['edge_keys'])
            all_entries['edge_keys'].update(new_invalid['edge_keys'])

            all_entries['node_keys'] = dict(sorted(all_entries['node_keys'].items()))
            all_entries['edge_keys'] = dict(sorted(all_entries['edge_keys'].items()))

            json.dump(all_entries, all_file, indent=4)

        # find auto entries
        auto_entries = {
            "node_keys": {},
            "edge_keys": {}
        }
        for node_key, entry in all_entries['node_keys'].items():
            if "auto" in entry and entry["auto"]:
                auto_entries["node_keys"][node_key] = entry
        for edge_key, entry in all_entries['edge_keys'].items():
            if "auto" in entry and entry["auto"]:
                auto_entries["edge_keys"][edge_key] = entry
        # dump auto entries to auto file -- this is not to be edited, just to have a place to look for auto generated entries
        with open(glob.glob(os.path.join(lexicon_directory, "*_auto_entries.json"))[0], "w") as auto_file:
            json.dump(auto_entries, auto_file, indent=4)

    @staticmethod
    def add_new_graph_data_to_lexicon(lexicon_name, lexicon_directory, new_lexicon_skeleton):
        """
        If new graphs are added to the dataset, this function is used to add the new graph elements to the `lexicon_incomplete_entries.json` file.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_name` | `str` | name of the lexicon |
        | `lexicon_directory` | `str` | path to the lexicon's directory |
        | `new_lexicon_skeleton` | `dict` | new lexicon skeleton to merge with existing entries, produced from `create_lexicon_skeleton` with the new graph information |

        **Returns**
        | Type |
        | ---- |
        | `None` |
        """

        # load all entries
        curr_all = json.load(open(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_all_entries.json")))

        # remove any node_keys already present in lexicon
        # this prevents overwriting those entries with a "fresh" entry
        for node_key in new_lexicon_skeleton["node_keys"].copy():
            if node_key in curr_all["node_keys"]:
                new_lexicon_skeleton["node_keys"].pop(node_key)

        # remove any edge_keys already present in lexicon
        for edge_key in new_lexicon_skeleton["edge_keys"].copy():
            if edge_key in curr_all["edge_keys"]:
                new_lexicon_skeleton["edge_keys"].pop(edge_key)

        # load incomplete entries to add to it
        curr_incomplete = json.load(open(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_incomplete_entries.json")))

        # update incomplete entries and all entries with new entries
        curr_incomplete["node_keys"].update(new_lexicon_skeleton["node_keys"])
        curr_incomplete["edge_keys"].update(new_lexicon_skeleton["edge_keys"])
        curr_all["node_keys"].update(new_lexicon_skeleton["node_keys"])
        curr_all["edge_keys"].update(new_lexicon_skeleton["edge_keys"])

        with (open(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_incomplete_entries.json"), "w") as incomplete_file,
              open(os.path.join(lexicon_directory, f"{lexicon_name}_lexicon_all_entries.json"), "w") as all_file):
            # dump to files
            json.dump(curr_incomplete, incomplete_file, indent=4)
            json.dump(curr_all, all_file, indent=4)

    @staticmethod
    def augment_from_existing_lexicon(existing_lexicon_directory, lexicon_dict_to_augment):
        with open(glob.glob(os.path.join(existing_lexicon_directory, "*_complete_entries.json"))[0], "r") as complete_entries_file:
            existing_complete_lexicon_json = json.load(complete_entries_file)
            for key in existing_complete_lexicon_json["node_keys"]:
                if key not in lexicon_dict_to_augment:
                    lexicon_dict_to_augment["node_keys"][key] = existing_complete_lexicon_json["node_keys"][key]

            for key in existing_complete_lexicon_json["edge_keys"]:
                if key not in lexicon_dict_to_augment:
                    lexicon_dict_to_augment["edge_keys"][key] = existing_complete_lexicon_json["edge_keys"][key]

    @staticmethod
    def update_lexicon_files(lexicon_directory, existing_lexicon_paths=None):
        """
        Update the files in the lexicon directory based on new information provided by the user.
        For example, if the user added information to the incomplete entries they may need to be expanded or marked as complete and moved to `lexicon_complete_entries.json`.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_directory` | `str` | path to the lexicon's directory |

        **Returns**
        | Type |
        | ---- |
        | `None` |
        """

        updated_entries = POGGLexiconUtil.load_latest_lexicon_json_data(lexicon_directory)

        new_incomplete_entries = {
            'node_keys': {},
            'edge_keys': {}
        }
        new_invalid_entries = {
            'node_keys': {},
            'edge_keys': {}
        }

        new_complete_entries = {
            'node_keys': {},
            'edge_keys': {}
        }

        # update node entries
        for node_key in updated_entries['node_keys']:
            node_entry = updated_entries['node_keys'][node_key]

            # validate the entry
            try:
                POGGLexiconUtil.validate_node_entry(node_entry)
            except (AttributeError, KeyError, ValueError) as err:
                new_invalid_entries['node_keys'][node_key] = err.args[1]
                continue

            # check for entry completion
            if POGGLexiconUtil.check_node_entry_completion(node_entry):
                new_complete_entries['node_keys'][node_key] = node_entry
            else:
                # if not complete, try expanding it, then add to incomplete
                # it may already be maximally expanded,
                # but it definitely isn't complete and still should be updated by user
                new_incomplete_entries['node_keys'][node_key] = POGGLexiconUtil.expand_node_entry(node_entry)


        # update edge entries
        for edge_key in updated_entries['edge_keys']:
            edge_entry = updated_entries['edge_keys'][edge_key]

            # validate the entry
            try:
                POGGLexiconUtil.validate_edge_entry(edge_entry)
            except (AttributeError, KeyError, ValueError) as err:
                new_invalid_entries['edge_keys'][edge_key] = err.args[1]
                continue

            # check for entry completion
            if POGGLexiconUtil.check_edge_entry_completion(edge_entry):
                new_complete_entries['edge_keys'][edge_key] = edge_entry
            else:
                # if not complete, try expanding it, then add to incomplete
                # it may already be maximally expanded,
                # but it definitely isn't complete and still should be updated by user
                new_incomplete_entries['edge_keys'][edge_key] = POGGLexiconUtil.expand_edge_entry(edge_entry)


        # if existing lexicon paths are provided, augment the new_complete_entries with complete_entries from those lexicons
        try:
            for existing_path in existing_lexicon_paths:
                POGGLexiconUtil.augment_from_existing_lexicon(existing_path, new_complete_entries)
        except TypeError:
            pass


        POGGLexiconUtil.dump_lexicon_json_data(lexicon_directory, new_complete_entries, new_incomplete_entries,
                                               new_invalid_entries)

    @staticmethod
    def dump_complete_lexicon_object_to_json(lexicon_dump_file_path, lexicon_object):
        """
        Dump the entries from a complete lexicon object into one JSON file.
        This is distinct from [dump_lexicon_json_data](#pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_lexicon_json_data)
        in that this function is for outputting a complete lexicon object, usually to have a record of the state of the
        lexicon during a particular run of POGG's conversion algorithm.

        [dump_lexicon_json_data](#pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_lexicon_json_data), on the other hand,
        is used to update the lexicon files when they are being actively edited.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_dump_file_path` | `str` | path to the file where the JSON of the complete lexicon will be stored |
        | `lexicon_object` | `POGGLexicon` | lexicon object to dump |

        **Returns**
        | Type |
        | ---- |
        | `None` |
        """

        lexicon_json = {
            "name": lexicon_object.name,
            "node_keys": {},
            "edge_keys": {}
        }
        for node_key in lexicon_object.node_entries.keys():
            lexicon_json["node_keys"][node_key] = POGGLexiconUtil.convert_POGGLexiconEntry_to_dict_entry(lexicon_object.node_entries[node_key])
        for edge_key in lexicon_object.edge_entries.keys():
            lexicon_json["edge_keys"][edge_key] = POGGLexiconUtil.convert_POGGLexiconEntry_to_dict_entry(lexicon_object.edge_entries[edge_key])

        with open(lexicon_dump_file_path, "w") as lexicon_file:
            lexicon_file.write(json.dumps(lexicon_json, indent=4))


