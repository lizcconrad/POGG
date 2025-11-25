"""
The lexicon_builder module contains the POGGLexiconBuilder and POGGLexicon classes that help the user put together
and store the lexicon for their dataset

[See usage examples here](project:/usage_nbs/pogg/lexicon/lexicon_builder.ipynb)
"""
from dataclasses import dataclass
import os
import pathlib
import glob
import json
import inspect
from typing import Dict

import pogg.semantic_composition.base_constructions
from pogg.semantic_composition.base_constructions import SemanticComposition


@dataclass(order=True)
class POGGLexiconEntry:
    key: str
    composition_function_name: str
    parameters: dict

# TODO: POGGLexicon is a data class ... POGGLexiconUtil handles all the building, expanding, and exporting, but the lexicon just holds the info

@dataclass
class POGGLexicon:
    name: str
    directory: str
    node_entries: Dict[str, POGGLexiconEntry]
    edge_entries: Dict[str, POGGLexiconEntry]
    # complete_entries_file: str = os.path.join(directory, f"{name}_lexicon_complete_entries.json")
    # incomplete_entries_file: str = os.path.join(directory, f"{name}_lexicon_incomplete_entries.json")
    # invalid_entries_file: str = os.path.join(directory, f"{name}_lexicon_invalid_entries.json")
    # all_entries_file: str = os.path.join(directory, f"{name}_lexicon_all_entries.json")


class POGGLexiconUtil:
    @staticmethod
    def initialize_lexicon_directory(lexicon_name, lexicon_directory):
        """
        Initialize the lexicon directory with 4 starter files:

        1. `lexicon_complete_entries.json` -- contains complete entries; this is the file that is loaded when making a POGGLexicon object
        2. `lexicon_incomplete_entries.json` -- contains incomplete entries; the user needs to fill these out to make them complete
        3. `lexicon_invalid_entries.json` -- contains invalid entries along with an error message for what makes it invalid
        4. `lexicon_all_entries.json` -- contains all complete, incomplete, and invalid entries

        Each file is prefixed with the `lexicon_name` as well.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `lexicon_name` | `str` | name of the lexicon, used as a prefix to all lexicon file names |
        | `lexicon_directory` | `str` | path to directory where lexicon files should be stored |

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

        starter_dict = {
            "node_keys": {},
            "edge_keys": {}
        }

        for file in files:
            if not os.path.isfile(file):
                with open(file, "w+") as f:
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

        ````{info} Dict entry example
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
    def create_lexicon_skeleton(graph_json):
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
                    lexicon_skeleton['node_keys'][node_lexicon_key] = {"comp_fxn": ""}
            else:
                # only add if it's not already been added to node_keys
                if node_name not in lexicon_skeleton['node_keys']:
                    lexicon_skeleton['node_keys'][node_name] = {"comp_fxn": ""}


        # add keys for every edge in graph_json
        # graph_json['edges'] is a list
        for edge in graph_json['edges']:
            edge_name = edge['edge_name']

            if 'lexicon_key' in edge:
                edge_lexicon_key = edge['lexicon_key']
                # only add if it's not already been added to edge_keys
                if edge_lexicon_key not in lexicon_skeleton['edge_keys']:
                    lexicon_skeleton['edge_keys'][edge_lexicon_key] = {"comp_fxn": ""}
            else:
                # only add if it's not already been added to edge_keys
                if edge_name not in lexicon_skeleton['edge_keys']:
                    lexicon_skeleton['edge_keys'][edge_name] = {"comp_fxn": ""}

            # check that parent and child node are in lexicon_skeleton
            if not edge['parent_node'] in graph_json['nodes'].keys():
                lexicon_skeleton['node_keys'][edge['parent_node']] = {"comp_fxn": ""}

            if not edge['child_node'] in graph_json['nodes'].keys():
                lexicon_skeleton['node_keys'][edge['child_node']] = {"comp_fxn": ""}


        # sort the node_keys
        lexicon_skeleton['node_keys'] = dict(sorted(lexicon_skeleton['node_keys'].items()))
        # sort the edge_keys
        lexicon_skeleton['edge_keys'] = dict(sorted(lexicon_skeleton['edge_keys'].items()))


        return lexicon_skeleton


    @staticmethod
    def read_lexicon_from_directory(lexicon_name, lexicon_directory):
        lexicon = POGGLexicon(lexicon_name, lexicon_directory, {}, {})

        # use this if a file is empty and JSON object can't be loaded
        empty_lexicon = {
            "node_keys": {},
            "edge_keys": {}
        }

        try:
            with open(glob.glob(os.path.join(lexicon_directory, "*_complete_entries.json"))[0], "r") as complete_lexicon_file:
                try:
                    complete_lexicon = json.load(complete_lexicon_file)
                except json.decoder.JSONDecodeError:
                    complete_lexicon = empty_lexicon.copy()
        except IndexError as err:
            raise IndexError(f"No files in {os.path.abspath(lexicon_directory)} end in the pattern _complete_entries.json") from err

        node_entries = complete_lexicon["node_keys"]
        for key in node_entries.keys():
            lexicon.node_entries[key] = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(key, node_entries[key])

        edge_entries = complete_lexicon["edge_keys"]
        for key in edge_entries.keys():
            lexicon.edge_entries[key] = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(key, edge_entries[key])

        return lexicon

    @staticmethod
    def validate_node_entry(node_entry):
        comp_fxn_name = node_entry["comp_fxn"]
        # if comp_fxn_name is empty, it's incomplete, so just return
        if comp_fxn_name == "":
            return True

        # if there's an existing failure message, clear it out
        if "failure_msg" in node_entry:
            node_entry.pop("failure_msg")

        try:
            comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
            parameters = inspect.signature(comp_fxn_obj).parameters

            # check that the parameters in the node_entry are legitimate
            for key in node_entry.keys():
                if key != "comp_fxn":
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
        comp_fxn_name = edge_entry["comp_fxn"]
        # if comp_fxn_name is empty, it's incomplete, so just return

        # if there's an existing failure message, clear it out
        if "failure_msg" in edge_entry:
            edge_entry.pop("failure_msg")

        if comp_fxn_name == "":
            return True

        try:
            comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
            parameters = inspect.signature(comp_fxn_obj).parameters

            # check that the parameters in the edge_entry are legitimate
            for key in edge_entry.keys():
                if key != "comp_fxn":
                    if key not in parameters:
                        edge_entry["failure_msg"] = f"{key} is not a parameter of {comp_fxn_name}"
                        raise KeyError(edge_entry["failure_msg"], edge_entry)

                    # if it is legitimate AND the type is SEMENT, then the value should either be "parent" or "child"
                    elif parameters[key].annotation.__name__ == "SEMENT" and edge_entry[key] != "parent" and edge_entry[key] != "child":
                        edge_entry["failure_msg"] = f"{key} should have a value of 'parent' or 'child'"
                        raise ValueError(edge_entry["failure_msg"], edge_entry)
        except AttributeError as err:
            # raised when getattr() above fails
            edge_entry["failure_msg"] = f"{comp_fxn_name} is not an existing Semantic Composition Function"
            raise AttributeError(err.args[0], edge_entry)

        return True

    @staticmethod
    def check_node_entry_completion(node_entry):
        comp_fxn_name = node_entry["comp_fxn"]

        if comp_fxn_name == "":
            return False

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self'
            if param_name == 'self':
                continue

            if param_name in node_entry.keys():
                # recurse for SEMENT parameters
                if param_information.annotation.__name__ == "SEMENT":
                    return POGGLexiconUtil.check_node_entry_completion(node_entry[param_name])

                if node_entry[param_name] == "":
                    return False
            else:
                return False

        return True

    @staticmethod
    def check_edge_entry_completion(node_entry):
        comp_fxn_name = node_entry["comp_fxn"]

        if comp_fxn_name == "":
            return False

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self'
            if param_name == 'self':
                continue

            if param_name in node_entry.keys():
                if node_entry[param_name] == "":
                    return False
            else:
                return False

        return True


    @staticmethod
    def expand_node_entry(node_entry):
        # get the top level function name
        comp_fxn_name = node_entry['comp_fxn']

        # can't be expanded if comp_fxn is not filled in yet, so return as is
        if comp_fxn_name == "":
            return node_entry

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self'
            if param_name == 'self':
                continue
            # if the param_name is not in the entry, add it with an appropriate "empty" value for the user to fill in
            elif param_name not in node_entry:
                # if paramater's type is SEMENT then it requires its own composition
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
        # get the top level function name
        comp_fxn_name = edge_entry['comp_fxn']

        # can't be expanded if comp_fxn is not filled in yet, so return as is
        if comp_fxn_name == "":
            return edge_entry

        # get parameters for the comp_fxn
        comp_fxn_obj = getattr(pogg.semantic_composition.base_constructions.SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self'
            if param_name == 'self':
                continue
            # if the param_name is not in the entry, add it with an appropriate "empty" value for the user to fill in
            elif param_information.annotation.__name__ == "dict":
                edge_entry[param_name] = {}
            elif param_name not in edge_entry:
                edge_entry[param_name] = ""
            else:
                pass

        return edge_entry


    @staticmethod
    def load_latest_lexicon_json_data(lexicon_directory):
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

            updated_entries = {
                "node_keys": updated_incomplete_entries["node_keys"],
                "edge_keys": updated_incomplete_entries["edge_keys"],
            }
            updated_entries['node_keys'].update(updated_invalid_entries['node_keys'])
            updated_entries['edge_keys'].update(updated_invalid_entries['edge_keys'])

        return latest_complete_entries, updated_entries


    @staticmethod
    def dump_lexicon_json_data(lexicon_directory, complete, incomplete, invalid):
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


    @staticmethod
    def add_new_graph_data_to_lexicon(lexicon_name, lexicon_dir, new_lexicon_skeleton):
        """
        if new graphs are added to the dataset then new entries might need to be added to the lexicon

        skeleton is the new skeleton generated from the new graph information
        """
        # load all entries
        curr_all = json.load(open(os.path.join(lexicon_dir, f"{lexicon_name}_lexicon_all_entries.json")))

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
        curr_incomplete = json.load(open(os.path.join(lexicon_dir, f"{lexicon_name}_lexicon_incomplete_entries.json")))

        # update incomplete entries and all entries with new entries
        curr_incomplete["node_keys"].update(new_lexicon_skeleton["node_keys"])
        curr_incomplete["edge_keys"].update(new_lexicon_skeleton["edge_keys"])
        curr_all["node_keys"].update(new_lexicon_skeleton["node_keys"])
        curr_all["edge_keys"].update(new_lexicon_skeleton["edge_keys"])

        with (open(os.path.join(lexicon_dir, f"{lexicon_name}_lexicon_incomplete_entries.json"), "w") as incomplete_file,
            open(os.path.join(lexicon_dir, f"{lexicon_name}_lexicon_all_entries.json"), "w") as all_file):
            # dump to files
            json.dump(curr_incomplete, incomplete_file, indent=4)
            json.dump(curr_all, all_file, indent=4)


    @staticmethod
    def update_lexicon_files(lexicon_directory):
        latest_complete_entries, updated_entries = POGGLexiconUtil.load_latest_lexicon_json_data(lexicon_directory)

        new_incomplete_entries = {
            'node_keys': {},
            'edge_keys': {}
        }
        new_invalid_entries = {
            'node_keys': {},
            'edge_keys': {}
        }

        # update node entries
        for node_key in updated_entries['node_keys']:
            node_entry = updated_entries['node_keys'][node_key]

            # validate the entry
            try:
                POGGLexiconUtil.validate_node_entry(node_entry)
            except (AttributeError, KeyError) as err:
                new_invalid_entries['node_keys'][node_key] = err.args[1]
                continue

            # check for entry completion
            if POGGLexiconUtil.check_node_entry_completion(node_entry):
                latest_complete_entries['node_keys'][node_key] = node_entry
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
            except (AttributeError, KeyError) as err:
                new_invalid_entries['edge_keys'][edge_key] = err.args[1]
                continue

            # check for entry completion
            if POGGLexiconUtil.check_edge_entry_completion(edge_entry):
                latest_complete_entries['edge_keys'][edge_key] = edge_entry
            else:
                # if not complete, try expanding it, then add to incomplete
                # it may already be maximally expanded,
                # but it definitely isn't complete and still should be updated by user
                new_incomplete_entries['edge_keys'][edge_key] = POGGLexiconUtil.expand_edge_entry(edge_entry)


        POGGLexiconUtil.dump_lexicon_json_data(lexicon_directory, latest_complete_entries, new_incomplete_entries,
                                               new_invalid_entries)

