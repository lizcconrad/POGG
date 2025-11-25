import os
import json
from pytest_cases import case

from pogg.lexicon.lexicon_builder import POGGLexiconEntry, POGGLexicon

"""
NOTE: FIXTURES COME FROM THE fixtures.py FILE IN THE SAME DIRECTORY AS THIS FILE
Each "case" in this file will modify things where needed and return necessary information for the tests
"""

class ConvertDictEntry:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry

    GENERAL DESCRIPTION OF TEST CASES:
        Convert a node or edge entry in JSON format into a POGGLexiconEntry object
    """

    @staticmethod
    def case_node_birthdayCandle():
        """
        DESCRIPTION:
            Node entry for "birthday candle"

        CASE NOTES:
            Node entry is nested so this tests the basic case as well as the recursive branch

        RETURNS:
            - JSON key for lexicon entry
            - JSON version of lexicon entry
            - gold POGGLexiconEntry object
        """
        node_json_key = "birthdayCandle"
        node_json_value = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_candle_n_1",
                "intrinsic_variable_properties": {}
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_birthday_n_1",
                "intrinsic_variable_properties": {}
            }
        }

        # create the gold object
        candle_entry = POGGLexiconEntry("head_noun_sement", "noun", {
            "predicate": "_candle_n_1",
            "intrinsic_variable_properties": {}
        })

        birthday_entry = POGGLexiconEntry("non_head_noun_sement", "noun", {
            "predicate": "_birthday_n_1",
            "intrinsic_variable_properties": {}
        })

        gold_node_entry = POGGLexiconEntry("birthdayCandle", "compound_noun", {
            "head_noun_sement": candle_entry,
            "non_head_noun_sement": birthday_entry,
        })

        return node_json_key, node_json_value, gold_node_entry

    @staticmethod
    def case_edge_flavor():
        """
        DESCRIPTION:
            Edge entry for "flavor"

        PARAMS:
            - individual_lexicon_dict_entries_dir: from data_dir_fixtures.py
            - gold_node_POGG_LexiconEntry_birthdayCandle: from gold_object_fixtures.py

        RETURNS:
            - JSON key for lexicon entry
            - JSON version of lexicon entry
            - gold POGGLexiconEntry object
        """
        edge_json_key = "flavor"
        edge_json_value = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": "parent",
            "non_head_noun_sement": "child"
        }

        # create the gold object
        gold_edge_entry = POGGLexiconEntry("flavor", "compound_noun", {
            "head_noun_sement": "parent",
            "non_head_noun_sement": "child"
        })

        return edge_json_key, edge_json_value, gold_edge_entry


class CreateLexiconSkeleton:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.create_lexicon_skeleton

    GENERAL DESCRIPTION OF TEST CASES:
        Read in JSON containing graph information and produce a lexicon skeleton and compare to a gold version of the skeleton
    """

    @staticmethod
    def case_basic(graph_jsons_dir, lexicon_skeletons_dir):
        """
        CASE NOTES:
            Covers the basic branches where each node and edge has a unique lexicon key specified

        PARAMS:
            - graph_jsons_dir: from data_dir_fixtures.py
            - lexicon_skeletons_dir: from data_dir_fixtures.py

        RETURNS:
            - graph information in JSON format
            - gold lexicon skeleton to compare against
        """
        test_graph = json.load(open(os.path.join(graph_jsons_dir, "basic_graph.json")))
        gold_skeleton = json.load(open(os.path.join(lexicon_skeletons_dir, "basic_lexicon_skeleton.json")))
        return test_graph, gold_skeleton

    @staticmethod
    def case_mult_nodes_same_lex_skel_key(graph_jsons_dir, lexicon_skeletons_dir):
        """
        CASE NOTES:
            Covers the branches where more than one node has the same lexicon key
            This includes (1) the case where two nodes with names that don't match the lexicon_key have the same lexicon_key,
            and (2) the case where there is no lexicon_key specified on a node but the "guess" resolves to an existing key

        PARAMS:
            - graph_jsons_dir: from data_dir_fixtures.py
            - lexicon_skeletons_dir: from data_dir_fixtures.py

        RETURNS:
            - graph information in JSON format
            - gold lexicon skeleton to compare against
        """
        test_graph = json.load(open(os.path.join(graph_jsons_dir, "mult_nodes_same_lex_skel_key.json")))
        gold_skeleton = json.load(open(os.path.join(lexicon_skeletons_dir, "basic_lexicon_skeleton.json")))
        return test_graph, gold_skeleton

    @staticmethod
    def case_mult_edges_same_lex_skel_key(graph_jsons_dir, lexicon_skeletons_dir):
        """
        CASE NOTES:
            Covers the branches where more than one edge has the same lexicon key
            This includes (1) the case where two edge with names that don't match the lexicon_key have the same lexicon_key,
            and (2) the case where there is no lexicon_key specified on a edge but the "guess" resolves to an existing key

        PARAMS:
            - graph_jsons_dir: from data_dir_fixtures.py
            - lexicon_skeletons_dir: from data_dir_fixtures.py

        RETURNS:
            - graph information in JSON format
            - gold lexicon skeleton to compare against
        """

        test_graph = json.load(open(os.path.join(graph_jsons_dir, "mult_edges_same_lex_skel_key.json")))
        gold_skeleton = json.load(open(os.path.join(lexicon_skeletons_dir, "mult_edges_same_lex_skel_key_lexicon_skeleton.json")))
        return test_graph, gold_skeleton

    @staticmethod
    def case_nodes_introduced_via_edge_members(graph_jsons_dir, lexicon_skeletons_dir):
        """
        CASE NOTES:
            Covers the branches where an edge has a parent and child that are not already included as node_keys, so they must be added to node_keys

        PARAMS:
            - graph_jsons_dir: from data_dir_fixtures.py
            - lexicon_skeletons_dir: from data_dir_fixtures.py

        RETURNS:
            - graph information in JSON format
            - gold lexicon skeleton to compare against
        """

        test_graph = json.load(open(os.path.join(graph_jsons_dir, "nodes_introduced_via_edge_members.json")))
        gold_skeleton = json.load(open(os.path.join(lexicon_skeletons_dir, "nodes_introduced_via_edge_members_lexicon_skeleton.json")))
        return test_graph, gold_skeleton


class ReadLexiconFromDirectory:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder_cases.read_lexicon_from_directory

    GENERAL DESCRIPTION OF TEST CASES:
        Read in lexicon information from a provided directory and compare to a gold object
    """

    """
    CASES:
        1. basic branches, typical lexicon
        2. blank files; set lexicon to defauly empty lexicon 
        3. nonexistent file, throw error  
    """

    @staticmethod
    @case(tags='success')
    def case_basic(lexicon_directories_dir):
        # gold node information
        candle_entry = POGGLexiconEntry("head_noun_sement", "noun", {
            "predicate": "_candle_n_1",
            "intrinsic_variable_properties": {}
        })
        birthday_entry = POGGLexiconEntry("non_head_noun_sement", "noun", {
            "predicate": "_birthday_n_1",
            "intrinsic_variable_properties": {}
        })
        gold_node_entry = POGGLexiconEntry("birthdayCandle", "compound_noun", {
            "head_noun_sement": candle_entry,
            "non_head_noun_sement": birthday_entry,
        })
        node_entries = {
            "birthdayCandle": gold_node_entry
        }

        # gold edge information
        edge_entries = {
            "flavor": POGGLexiconEntry("flavor", "compound_noun",
                                       {
                                            "head_noun_sement": "parent",
                                            "non_head_noun_sement": "child"
                                        })
        }

        # gold lexicon object
        gold_POGGLexicon = POGGLexicon("basic", lexicon_directories_dir, node_entries, edge_entries)


        # return the lexicon name, directory where the sample lexicon is stored, and gold object
        return "basic", os.path.join(lexicon_directories_dir, "basic"), gold_POGGLexicon

    @staticmethod
    @case(tags='success')
    def case_blank_files(lexicon_directories_dir):
        return "empty", os.path.join(lexicon_directories_dir, "blank_files"), POGGLexicon("empty", "", {}, {})

    @staticmethod
    @case(tags='failure')
    def case_nonexistent_file(tmp_path):
        # tmp_path is a builtin fixture from pytest
        # just returning an empty dir so the function attempts to read from a nonexistent file
        return tmp_path


class ValidateNodeEntry:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_node_entry

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for a node entry in the lexicon and confirm whether it's valid or raises the expected error
    """

    """
    CASES:
        VALID
            1. empty entry
            2. complete node entry
            3. node entry with failure message (i.e. has been "fixed" and needs the message removed)
            4. complete nested node entry

        INVALID
            1. comp_fxn doesn't exist
            2. parameter not a parameter of given comp_fxn
            3. nested comp_fxn doesn't exist
            4. nested parameter not a parameter of given comp_fxn
    """

    @staticmethod
    @case(tags='success')
    def case_empty_entry():
        return {"comp_fxn": ""}

    @staticmethod
    @case(tags='success')
    def case_complete_entry():
        return {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1",
            "intrinsic_variable_properties": {}
        }

    @staticmethod
    @case(tags='success')
    def case_fixed_entry_w_failure_msg():
        # the node is valid because it has been "fixed" and the failure message should be removed
        return {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1",
            "intrinsic_variable_properties": {},
            "failure_msg": "oopsies!"
        }

    @staticmethod
    @case(tags='success')
    def case_nested_entry():
        return {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_candle_n_1",
                "intrinsic_variable_properties": {}
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_birthday_n_1",
                "intrinsic_variable_properties": {}
            }
        }


    @staticmethod
    @case(tags='failure')
    def case_comp_fxn_doesnt_exist():
        entry_value = {
             "comp_fxn": "not_real",
             "predicate": "doesnt_matter"
        }
        # should raise an AttributeError
        return entry_value, AttributeError

    @staticmethod
    @case(tags='failure')
    def case_nonexistent_parameter():
        entry_value = {
             "comp_fxn": "noun",
            "not_real": "gotcha!"
         }
        # should raise a KeyError
        return entry_value, KeyError

    @staticmethod
    @case(tags='failure')
    def case_nested_nonexistent_comp_fxn():
        entry_value = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_candle_n_1"
            },
            "non_head_noun_sement": {
                "comp_fxn": "nuh uh!",
                "predicate": "teehee"
            }
        }
        # should raise an AttributeError
        return entry_value, AttributeError

    @staticmethod
    @case(tags='failure')
    def case_nested_nonexistent_parameter():
        entry_value = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_candle_n_1"
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun",
                "not_real": "gotcha!"
            }
        }
        # should raise a KeyError
        return entry_value, KeyError


class ValidateEdgeEntry:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.validate_edge_entry

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for an edge entry in the lexicon and confirm whether it's valid or raises the expected error
    """

    """
    CASES:
        VALID
            1. empty entry
            2. complete edge entry
            3. edge entry with failure message (i.e. has been "fixed" and needs the message removed)

        INVALID
            1. comp_fxn doesn't exist
            2. parameter not a parameter of given comp_fxn
            3. parameter value must be "parent" or "child" but isn't
    """

    @staticmethod
    @case(tags='success')
    def case_empty_entry():
        return {"comp_fxn": ""}

    @staticmethod
    @case(tags='success')
    def case_complete_entry():
        return {
            "comp_fxn": "compound_noun",
            "head_noun_sement": "parent",
            "non_head_noun_sement": "child"
        }

    @staticmethod
    @case(tags='success')
    def case_fixed_entry_w_failure_msg():
        return {
            "comp_fxn": "compound_noun",
            "head_noun_sement": "parent",
            "non_head_noun_sement": "child",
            "failure_msg": "oopsies!"
        }


    @staticmethod
    @case(tags='failure')
    def case_nonexistent_comp_fxn():
        entry_value = {
            "comp_fxn": "not_real",
            "doesnt_matter": "gotcha!"
        }
        # should raise an AttributeError
        return entry_value, AttributeError

    @staticmethod
    @case(tags='failure')
    def case_nonexistent_parameter():
        entry_value = {
            "comp_fxn": "compound_noun",
            "not_real": "oopsies!"
        }
        # should raise an KeyError
        return entry_value, KeyError

    @staticmethod
    @case(tags='failure')
    def case_bad_param_value():
        # values should be "parent" and "child"
        entry_value = {
             "comp_fxn": "compound_noun",
             "head_noun_sement": "mommy",
             "non_head_noun_sement": "baby"
        }
        # should raise an ValueError
        return entry_value, ValueError


class CheckNodeEntryCompletion:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_node_entry_completion

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for a node entry in the lexicon and confirm whether it's complete or not.

        For each case, return the entry along with the expected result (True, False)
    """

    """
    CASES:
        COMPLETE
            1. completed node entry
            2. completed nested node entry

        INCOMPLETE
            1. empty
            2. missing a parameter
            2. parameter not filled out

    """

    @staticmethod
    def case_complete_entry():
        entry = {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1",
            "intrinsic_variable_properties": {}
        }
        return entry, True

    @staticmethod
    def case_nested_complete_entry():
        entry = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_candle_n_1",
                "intrinsic_variable_properties": {}
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "_birthday_n_1",
                "intrinsic_variable_properties": {}
            }
        }
        return entry, True

    @staticmethod
    def case_empty_entry():
        entry = {
            "comp_fxn": ""
        }
        return entry, False


    @staticmethod
    def case_missing_param():
        entry = {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1"
        }
        return entry, False

    @staticmethod
    def case_unfilled_param():
        entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return entry, False


class CheckEdgeEntryCompletion:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.check_edge_entry_completion

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for an edge entry in the lexicon and confirm whether it's complete or not.

        For each case, return the entry along with the expected result (True, False)
    """

    """
    CASES:
        COMPLETE
            1. completed edge entry
    
        INCOMPLETE
            1. empty
            2. missing a parameter
            2. parameter not filled out
    
    """

    @staticmethod
    def case_complete_entry():
        entry = {
            "comp_fxn": "relative_direction",
            "direction_predicate": "_north_a_1",
            "figure_sement": "parent",
            "ground_sement": "child"
        }
        return entry, True

    @staticmethod
    def case_empty_entry():
        entry = {
            "comp_fxn": ""
        }
        return entry, False

    @staticmethod
    def case_missing_param():
        entry = {
            "comp_fxn": "noun",
            "predicate": "_cake_n_1"
        }
        return entry, False

    @staticmethod
    def case_unfilled_param():
        entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return entry, False


class ExpandNodeEntry:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_node_entry

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for a node entry in the lexicon and expand where appropriate with more information

        For each case, return the input entry along with the expected gold result
    """

    """
    CASES:
        1. IN: empty entry, OUT: empty entry
        2. IN: entry w/ top level comp_fxn, OUT: expansion w/ top level comp_fxn's params
        3. IN: entry w/ top level comp_fxn that has a recursive param, OUT: expansion w/ top level comp_fxn's params
        4. IN: entry w/ nested comp_fxn, OUT: expansion w/ nested comp_fxn's params
        5. IN: fully expanded entry, OUT: fully expanded entry
    """

    @staticmethod
    def case_empty_entry():
        empty = {
            "comp_fxn": ""
        }
        return empty, empty

    @staticmethod
    def case_comp_fxn_given():
        in_entry = {
            "comp_fxn": "noun"
        }
        gold_expanded_entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return in_entry, gold_expanded_entry

    @staticmethod
    def case_comp_fxn_given_w_recursive_param():
        in_entry = {
             "comp_fxn": "compound_noun"
        }
        gold_expanded_entry = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": ""
            },
            "non_head_noun_sement": {
                "comp_fxn": ""
            }
        }
        return in_entry, gold_expanded_entry

    @staticmethod
    def case_nested_comp_fxn_params():
        in_entry = {
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun"
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun"
            }
        }
        gold_expanded_entry ={
            "comp_fxn": "compound_noun",
            "head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "",
                "intrinsic_variable_properties": {}
            },
            "non_head_noun_sement": {
                "comp_fxn": "noun",
                "predicate": "",
                "intrinsic_variable_properties": {}
            }
        }
        return in_entry, gold_expanded_entry

    @staticmethod
    def case_already_expanded_entry():
        expanded_entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return expanded_entry, expanded_entry


class ExpandEdgeEntry:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.expand_edge_entry

    GENERAL DESCRIPTION OF TEST CASES:
        Provide JSON for an edge entry in the lexicon and expand where appropriate with more information

        For each case, return the input entry along with the expected gold result
    """

    """
    CASES:
        1. IN: empty entry, OUT: empty entry
        2. IN: entry w/ comp_fxn, OUT: expansion w/ comp_fxn's params'
        3. IN: fully expanded entry, OUT: fully expanded entry
    """

    @staticmethod
    def case_empty_entry():
        empty = {
            "comp_fxn": ""
        }
        return empty, empty

    @staticmethod
    def case_comp_fxn_given():
        in_entry = {
            "comp_fxn": "noun"
        }
        gold_expanded_entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return in_entry, gold_expanded_entry

    @staticmethod
    def case_already_expanded_entry():
        expanded_entry = {
            "comp_fxn": "noun",
            "predicate": "",
            "intrinsic_variable_properties": {}
        }
        return expanded_entry, expanded_entry


class LoadLatestLexiconJSONData:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.load_latest_lexicon_json_data

    GENERAL DESCRIPTION OF TEST CASES:
        Load latest JSON data from a lexicon directory (for the purpose of expanding further or creating a final POGGLexicon object)

        For each case, return the directory with the JSON data along with the gold expected result
    """

    """
    CASES:
        1. sample lexicon with information in _complete, _incomplete, and _invalid 
        2. empty lexicon (i.e. has empty JSON dictionaries)
        3. lexicon with blank files
    """

    @staticmethod
    def case_sample_lexicon(lexicon_directories_dir):
        sample_lexicon_dir = os.path.join(lexicon_directories_dir, "sample_w_data_in_each_file")
        gold_latest_complete = json.load(open(os.path.join(sample_lexicon_dir, "gold_latest_complete_entries.json")))
        gold_latest_updated = json.load(open(os.path.join(sample_lexicon_dir, "gold_latest_updated_entries.json")))

        return sample_lexicon_dir, gold_latest_complete, gold_latest_updated

    @staticmethod
    def case_empty_lexicon(lexicon_directories_dir):
        empty_lexicon_dir = os.path.join(lexicon_directories_dir, "empty_lexicon")
        gold_latest_complete = {
            "node_keys": {},
            "edge_keys": {}
        }
        gold_latest_updated = gold_latest_complete.copy()

        return empty_lexicon_dir, gold_latest_complete, gold_latest_updated

    @staticmethod
    def case_blank_lexicon(lexicon_directories_dir):
        empty_lexicon_dir = os.path.join(lexicon_directories_dir, "blank_files")
        gold_latest_complete = {
            "node_keys": {},
            "edge_keys": {}
        }
        gold_latest_updated = gold_latest_complete.copy()

        return empty_lexicon_dir, gold_latest_complete, gold_latest_updated


class DumpLexiconJSONData:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.dump_lexicon_json_data

    GENERAL DESCRIPTION OF TEST CASES:
        Given some JSON data, dump it into a lexicon directory

        For each case, return a tmp_path along with data to dump. The test just needs to compare this data with whatever is written in the files
    """

    """
    CASES:
        1. example JSON data
        2. None data 
    """

    @staticmethod
    def case_example_json_data(tmp_path, lexicon_directories_dir):
        sample_lexicon_dir = os.path.join(lexicon_directories_dir, "sample_w_data_in_each_file")
        complete = json.load(open(os.path.join(sample_lexicon_dir, "sample_lexicon_complete_entries.json")))
        incomplete = json.load(open(os.path.join(sample_lexicon_dir, "sample_lexicon_incomplete_entries.json")))
        invalid = json.load(open(os.path.join(sample_lexicon_dir, "sample_lexicon_invalid_entries.json")))
        all_entries = json.load(open(os.path.join(sample_lexicon_dir, "sample_lexicon_all_entries.json")))

        """
        RETURNS
            1. tmp_path to dump data
            2. complete_entries
            3. incomplete_entries
            4. invalid_entries
            5. gold_complete_entries (same as complete)
            6. gold_incomplete_entries (same as incomplete)
            7. gold_invalid_entries (same as invalid)
            8. gold_all_entries (same as all)
        """
        return tmp_path, complete, incomplete, invalid, complete, incomplete, invalid, all_entries

    @staticmethod
    def case_none_json_data(tmp_path, lexicon_directories_dir):
        empty_lexicon = {
            "node_keys": {},
            "edge_keys": {}
        }

        """
        RETURNS
            1. tmp_path to dump data
            2. None
            3. None
            4. None
            5. default empty lexicon
            6. default empty lexicon
            7. default empty lexicon
            8. default empty lexicon
        """
        return tmp_path, None, None, None, empty_lexicon.copy(), empty_lexicon.copy(), empty_lexicon.copy(), empty_lexicon.copy()


class AddNewGraphDataToLexicon:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.add_new_graph_data_to_lexicon

    GENERAL DESCRIPTION OF TEST CASES:
        Given a newly generated lexicon skeleton, add new entries to the lexicon_incomplete_entries file; compare to gold expected version of file

        For each case, return a tmp_path to store information, the initial information to dump, the new skeleton, and gold expected information
    """

    @staticmethod
    def case_new_entries_added(tmp_path, lexicon_directories_dir, lexicon_skeletons_dir):
        lexicon_dir = os.path.join(lexicon_directories_dir, "sample_w_data_in_each_file")
        initial_incomplete = json.load(open(os.path.join(lexicon_dir, "sample_lexicon_incomplete_entries.json")))
        initial_all = json.load(open(os.path.join(lexicon_dir, "sample_lexicon_all_entries.json")))

        new_skeleton = json.load(open(os.path.join(lexicon_skeletons_dir, "sample_plus_extra_graph_info_lexicon_skeleton.json")))

        gold_updated_incomplete = json.load(open(os.path.join(lexicon_dir, "gold_latest_incomplete_entries_w_new_graph_info.json")))
        gold_updated_all = json.load(open(os.path.join(lexicon_dir, "gold_latest_all_entries_w_new_graph_info.json")))

        return tmp_path, initial_incomplete, initial_all, new_skeleton, gold_updated_incomplete, gold_updated_all


class UpdateLexiconFiles:
    """
    FUNCTION BEING TESTED:
        - pogg.lexicon.lexicon_builder.POGGLexiconUtil.update_lexicon_files

    GENERAL DESCRIPTION OF TEST CASES:
        Read in lexicon files and update them as needed (e.g. expand edited entries, move invalid ones to invalid file); compare to gold expected version of file

        For each case, return the the directory to read from, and the gold expected results
    """

    """
    CASES:
        1. example JSON data
    """
    @staticmethod
    def case_basic_updated_lexicon(tmp_path, lexicon_directories_dir):
        lexicon_dir = os.path.join(lexicon_directories_dir, "worked_on")

        test_complete = json.load(open(os.path.join(lexicon_dir, "worked_on_lexicon_complete_entries.json")))
        test_incomplete = json.load(open(os.path.join(lexicon_dir, "worked_on_lexicon_incomplete_entries.json")))
        test_invalid = json.load(open(os.path.join(lexicon_dir, "worked_on_lexicon_invalid_entries.json")))
        test_all = json.load(open(os.path.join(lexicon_dir, "worked_on_lexicon_all_entries.json")))

        # copy lexicon data to the temporary path
        with (open(os.path.join(tmp_path, "worked_on_complete_entries.json"), 'w') as complete_f,
            open(os.path.join(tmp_path, "worked_on_incomplete_entries.json"), 'w') as incomplete_f,
            open(os.path.join(tmp_path, "worked_on_invalid_entries.json"), 'w') as invalid_f,
              open(os.path.join(tmp_path, "worked_on_all_entries.json"), 'w') as all_f):
            json.dump(test_complete, complete_f)
            json.dump(test_incomplete, incomplete_f)
            json.dump(test_invalid, invalid_f)
            json.dump(test_all, all_f)

        gold_updated_complete = json.load(open(os.path.join(lexicon_dir, "updated_complete_entries.json")))
        gold_updated_incomplete = json.load(open(os.path.join(lexicon_dir, "updated_incomplete_entries.json")))
        gold_updated_invalid = json.load(open(os.path.join(lexicon_dir, "updated_invalid_entries.json")))
        gold_updated_all = json.load(open(os.path.join(lexicon_dir, "updated_all_entries.json")))

        return tmp_path, gold_updated_complete, gold_updated_incomplete, gold_updated_invalid, gold_updated_all



