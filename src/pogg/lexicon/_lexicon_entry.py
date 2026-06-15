import copy
import inspect

from pogg_semantics.semantic_composition import SemanticComposition

class POGGLexiconEntry:
    def __init__(self, lexicon_key, entry_information=None):
        if entry_information is None:
            entry_information = {
                # default to "node" type
                "entry_type": "node",
                "lexicon_entry": {
                    "comp_fxn": ""
                }
            }
        # if the entry_information is not none but is only the lexicon_entry dictionary, wrap it
        else:
            if "comp_fxn" in entry_information:
                entry_information = {
                    "entry_type": "node",
                    "lexicon_entry": entry_information
                }

        if "auto_info" not in entry_information:
            entry_information["auto_info"] = {
                "string_to_parse": "",
                "template_used": "",
                "blocked_templates": set(),
                "attempted_templates": set()
            }

        self.key = lexicon_key
        self.entry_type = entry_information["entry_type"]

        self.entry_in_dict_format = entry_information["lexicon_entry"]
        self.composition_function_name = self.entry_in_dict_format["comp_fxn"]
        self.parameters = copy.deepcopy(self.entry_in_dict_format)
        # parameters is everything besides "comp_fxn"
        self.parameters.pop("comp_fxn")

        if "flags" not in entry_information:
            entry_information["flags"] = {
                "auto_filled": False,
                "complete": False,
                "approved": False,
                "valid": False,
                "create_template_from": False
            }

        # only add auto_info and flags for top-level entries
        for key, val in entry_information["auto_info"].items():
            if key == "blocked_templates" or key == "attempted_templates":
                setattr(self, key, set(val))
            else:
                setattr(self, key, val)
        for key, val in entry_information["flags"].items():
            setattr(self, key, val)

        self.validate_entry()
        if self.valid:
            self.check_entry_completion()

        # create nested objects
        self._convert_dict_format_to_POGGLexiconEntry_objects()


    def validate_entry(self):
        try:
            if self.entry_type == "node":
                self.valid = self._validate_node_entry(self.entry_in_dict_format)
            else:
                self.valid = self._validate_edge_entry(self.entry_in_dict_format)
        except (AttributeError, KeyError, ValueError) as err:
            self.entry_in_dict_format = err.args[1]
            self.valid = False
            # mark as incomplete as well
            self.complete = False

        return self.valid

    def check_entry_completion(self):
        if self.entry_type == "node":
            self.complete = self._check_node_entry_completion(self.entry_in_dict_format)
        else:
            self.complete = self._check_edge_entry_completion(self.entry_in_dict_format)
        return self.complete

    def expand_entry(self):
        self.validate_entry()
        if self.valid:
            self.check_entry_completion()
            if not self.complete:
                if self.entry_type == "node":
                    self._expand_node_entry(self.entry_in_dict_format)
                else:
                    self._expand_edge_entry(self.entry_in_dict_format)


    def _validate_node_entry(self, node_entry):
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
            comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
            parameters = inspect.signature(comp_fxn_obj).parameters

            # check that the parameters in the node_entry are legitimate
            for key in node_entry.keys():
                if key != "comp_fxn" and key != "auto":
                    if key not in parameters:
                        node_entry["failure_msg"] = f"{key} is not a parameter of {comp_fxn_name}"
                        raise KeyError(node_entry["failure_msg"], node_entry)

                    # if it is legitimate AND the type is SEMENT, validation needs to recurse
                    elif parameters[key].annotation.__name__ == "SEMENT":
                        self._validate_node_entry(node_entry[key])


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

    def _validate_edge_entry(self, edge_entry):
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
            comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
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
                            self._validate_node_entry(edge_entry[key])
                        else:
                            edge_entry[
                                "failure_msg"] = f"{key} should have a value of 'parent' or 'child', introduce a SEMENT via a comp_fxn, or be set to 'null' if it's an optional argument"
                            raise ValueError(edge_entry["failure_msg"], edge_entry)
                    else:
                        continue
        except AttributeError as err:
            # raised when getattr() above fails
            edge_entry["failure_msg"] = f"{comp_fxn_name} is not an existing Semantic Composition Function"
            raise AttributeError(err.args[0], edge_entry)

        return True

    def _check_node_entry_completion(self, node_entry):
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
        comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that AREN'T SEMENTs
            # "advanced" users can use them if they want
            # TODO: way to turn this on or off?
            if param_name == 'self' or (
                    param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
                continue

            # if the parameter from the signature is in the node entry...
            if param_name in node_entry.keys():
                # recurse for SEMENT parameters
                if param_information.annotation.__name__ == "SEMENT":
                    # if the SEMENT type parameter is optional and the value is set to None, keep going
                    if param_information.default is not inspect.Parameter.empty and node_entry[param_name] is None:
                        continue
                    # if the SEMENT type parameter is NOT optional and has no value, entry is not complete
                    elif not self._check_node_entry_completion(node_entry[param_name]):
                        return False

                if node_entry[param_name] == "":
                    return False
            else:
                return False

        return True

    def _check_edge_entry_completion(self, edge_entry):
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
        comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # go through each parameter and check that it's (1) in the entry and (2) has a value
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and parameters with default values that AREN'T SEMENTs (e.g. intrinsic_variable_properties dict)
            # 'advanced' users can add them if they want
            # TODO: toggle?
            # if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
            if param_name == 'self':
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
                    if not self._check_node_entry_completion(edge_entry[param_name]):
                        return False
                    else:
                        continue
            else:
                return False

        return True

    def _expand_node_entry(self, node_entry):
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
        comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that aren't SEMENTs (e.g. intrinsic_variable_properties dict)
            # if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
            # EDIT: putting optional ones back
            if param_name == 'self':
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
            # e.g., if the top level comp_fxn is "prenominal_adjective"
            # then the parameters (adjective_sement, nominal_sement) will themselves to be expanded with comp_fxn info
            else:
                if param_information.annotation.__name__ == "SEMENT":
                    self._expand_node_entry(node_entry[param_name])
                else:
                    pass

        return node_entry

    def _expand_edge_entry(self, edge_entry):
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
        comp_fxn_obj = getattr(SemanticComposition, comp_fxn_name)
        parameters = inspect.signature(comp_fxn_obj).parameters

        # expand entry using parameters
        for param_name in parameters.keys():
            # param_information includes the type of the parameter
            param_information = parameters[param_name]

            # skip 'self' and optional parameters that aren't SEMENTs (e.g. intrinsic_variable_properties dict)
            # if param_name == 'self' or (param_information.annotation.__name__ != "SEMENT" and param_information.default is not inspect.Parameter.empty):
            # EDIT: putting optional parameters back
            if param_name == 'self':
                continue
            # if the param_name is not in the entry, add it with an appropriate "empty" value for the user to fill in
            elif param_information.annotation.__name__ == "dict":
                edge_entry[param_name] = {}
            elif param_name not in edge_entry:
                edge_entry[param_name] = ""
            # if it is in the entry, the type is SEMENT, and the value is not "parent" or "child", recurse down for further expansion
            elif (param_information.annotation.__name__ == "SEMENT"
                  and not (edge_entry[param_name] == "parent" or edge_entry[param_name] == "child")):
                self._expand_edge_entry(edge_entry[param_name])
            else:
                pass

        return edge_entry

    def _convert_dict_format_to_POGGLexiconEntry_objects(self, dict_key=None, dict_entry=None):

        if dict_key is None:
            dict_key = self.key

        if dict_entry is None:
            dict_entry = self.entry_in_dict_format
            entry = self
        else:
            entry = POGGLexiconEntry(dict_key, dict_entry)

        for param_name in dict_entry.keys():
            if param_name != "comp_fxn":
                param_value = dict_entry[param_name]

                # if the parameter is a dict with its own "comp_fxn" then make a sub POGGLexiconEntry
                if type(param_value) is dict and "comp_fxn" in param_value:
                    param_value = self._convert_dict_format_to_POGGLexiconEntry_objects(param_name, param_value)
                # add value to parameters_dict
                entry.parameters[param_name] = param_value

        return entry

    def convert_to_dict_format(self):
        entry = {}
        entry["entry_type"] = self.entry_type
        entry["lexicon_entry"] = self.entry_in_dict_format
        entry["auto_info"] = {
            "template_used": self.template_used,
            "blocked_templates": sorted(list(self.blocked_templates)),
            "attempted_templates": sorted(list(self.attempted_templates)),
            "string_to_parse": self.string_to_parse
        }
        entry["flags"] = {
            "auto_filled": self.auto_filled,
            "complete": self.complete,
            "approved": self.approved,
            "valid": self.valid,
            "create_template_from": self.create_template_from
        }
        return entry
