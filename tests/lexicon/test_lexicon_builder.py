import glob
import pytest
from pytest_cases import parametrize_with_cases

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_lexicon_builder_cases import *

from pogg.lexicon.lexicon_builder import POGGLexiconUtil, POGGLexiconEntry


class TestPOGGLexiconEntry:
    """
    Tests POGGLexiconEntry class
    """
    pass

class TestPOGGLexicon:
    """
    Tests POGGLexicon class
    """
    pass

class TestPOGGLexiconUtil:
    """
    Tests POGGLexiconUtil class
    """
    def assert_POGGLexiconEntry_equality(self, test_entry, gold_entry):
        assert test_entry.key == gold_entry.key
        assert test_entry.composition_function_name == gold_entry.composition_function_name
        for param in test_entry.parameters:
            if isinstance(test_entry.parameters[param], POGGLexiconEntry):
                assert self.assert_POGGLexiconEntry_equality(test_entry.parameters[param], gold_entry.parameters[param])
            else:
                assert test_entry.parameters[param] == gold_entry.parameters[param]

        return True

    ## TESTS ##
    @staticmethod
    def test_initialize_lexicon_directory_files_created(tmp_path):
        POGGLexiconUtil.initialize_lexicon_directory("test", tmp_path)

        assert os.path.isfile(os.path.join(tmp_path, "test_lexicon_complete_entries.json"))
        assert os.path.isfile(os.path.join(tmp_path, "test_lexicon_incomplete_entries.json"))
        assert os.path.isfile(os.path.join(tmp_path, "test_lexicon_invalid_entries.json"))
        assert os.path.isfile(os.path.join(tmp_path, "test_lexicon_all_entries.json"))

    @staticmethod
    def test_initialize_lexicon_directory_file_not_overwriting_contents(tmp_path):

        # initialize files with dummy data
        test_lexicon_complete_json = os.path.join(tmp_path, "test_lexicon_complete_entries.json")
        test_lexicon_incomplete_json = os.path.join(tmp_path, "test_lexicon_incomplete_entries.json")
        test_lexicon_invalid_json = os.path.join(tmp_path, "test_lexicon_invalid_entries.json")
        test_lexicon_all_json = os.path.join(tmp_path, "test_lexicon_all_entries.json")
        files = [test_lexicon_complete_json, test_lexicon_incomplete_json, test_lexicon_invalid_json, test_lexicon_all_json]

        for file in files:
            with open(file, 'w') as f:
                f.write("dummy data")

        POGGLexiconUtil.initialize_lexicon_directory("test", tmp_path)

        for file in files:
            with open(file) as f:
                assert f.read() == "dummy data"

    @staticmethod
    def test_initialize_lexicon_directory_file_contents(tmp_path):
        POGGLexiconUtil.initialize_lexicon_directory("test", tmp_path)

        test_lexicon_complete_json = json.load(open(os.path.join(tmp_path, "test_lexicon_complete_entries.json")))
        test_lexicon_incomplete_json = json.load(open(os.path.join(tmp_path, "test_lexicon_incomplete_entries.json")))
        test_lexicon_invalid_json = json.load(open(os.path.join(tmp_path, "test_lexicon_invalid_entries.json")))
        test_lexicon_all_json = json.load(open(os.path.join(tmp_path, "test_lexicon_all_entries.json")))

        gold_empty = {
            "node_keys": {},
            "edge_keys": {}
        }

        assert gold_empty == test_lexicon_complete_json
        assert gold_empty == test_lexicon_incomplete_json
        assert gold_empty == test_lexicon_invalid_json
        assert gold_empty == test_lexicon_all_json


    @parametrize_with_cases("test_json_entry_key, test_json_entry_val, gold_POGGLexiconEntry", cases=ConvertDictEntry)
    def test_convert_dict_entry_to_POGGLexiconEntry(self, gold_POGGLexiconEntry, test_json_entry_key, test_json_entry_val):
        test_lex_entry = POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(test_json_entry_key, test_json_entry_val)
        assert self.assert_POGGLexiconEntry_equality(test_lex_entry, gold_POGGLexiconEntry)


    @parametrize_with_cases("graph_json, gold_lexicon_skeleton", cases=CreateLexiconSkeleton)
    def test_create_lexicon_skeleton(self, graph_json, gold_lexicon_skeleton):
        test_skeleton = POGGLexiconUtil.create_lexicon_skeleton(graph_json)
        assert test_skeleton == gold_lexicon_skeleton


    @parametrize_with_cases("lex_name, dir_with_sample_lex, gold_POGGLexicon", cases=ReadLexiconFromDirectory, has_tag="success")
    def test_read_lexicon_from_directory(self, lex_name, dir_with_sample_lex, gold_POGGLexicon):
        read_lexicon = POGGLexiconUtil.read_lexicon_from_directory(lex_name, dir_with_sample_lex)

        assert read_lexicon.name == gold_POGGLexicon.name

        assert read_lexicon.node_entries == gold_POGGLexicon.node_entries
        assert read_lexicon.edge_entries == gold_POGGLexicon.edge_entries


    @parametrize_with_cases("dir_with_sample_lex", cases=ReadLexiconFromDirectory, has_tag="failure")
    def test_read_lexicon_from_directory_nonexistent_file(self, dir_with_sample_lex):
        with pytest.raises(IndexError):
            POGGLexiconUtil.read_lexicon_from_directory("nonexistent_file", dir_with_sample_lex)


    @parametrize_with_cases("entry", cases=ValidateNodeEntry, has_tag="success")
    def test_validate_node_entry(self, entry):
        assert POGGLexiconUtil.validate_node_entry(entry)


    @parametrize_with_cases("entry, err_type", cases=ValidateNodeEntry, has_tag="failure")
    def test_validate_node_entry_invalid(self, entry, err_type):
        with pytest.raises(err_type):
            POGGLexiconUtil.validate_node_entry(entry)

    @parametrize_with_cases("entry", cases=ValidateEdgeEntry, has_tag="success")
    def test_validate_edge_entry(self, entry):
        assert POGGLexiconUtil.validate_edge_entry(entry)

    @parametrize_with_cases("entry, err_type", cases=ValidateEdgeEntry, has_tag="failure")
    def test_validate_edge_entry_invalid(self, entry, err_type):
        with pytest.raises(err_type):
            POGGLexiconUtil.validate_edge_entry(entry)


    @parametrize_with_cases("entry, result", cases=CheckNodeEntryCompletion)
    def test_check_node_entry_completion(self, entry, result):
        assert POGGLexiconUtil.check_node_entry_completion(entry) == result

    @parametrize_with_cases("entry, result", cases=CheckEdgeEntryCompletion)
    def test_check_edge_entry_completion(self, entry, result):
        assert POGGLexiconUtil.check_edge_entry_completion(entry) == result

    @parametrize_with_cases("in_entry, gold_expanded_entry", cases=ExpandNodeEntry)
    def test_expand_node_entry(self, in_entry, gold_expanded_entry):
        assert POGGLexiconUtil.expand_node_entry(in_entry) == gold_expanded_entry

    @parametrize_with_cases("in_entry, gold_expanded_entry", cases=ExpandEdgeEntry)
    def test_expand_edge_entry(self, in_entry, gold_expanded_entry):
        assert POGGLexiconUtil.expand_edge_entry(in_entry) == gold_expanded_entry

    @parametrize_with_cases("lexicon_dir, gold_latest_complete, gold_latest_updated", cases=LoadLatestLexiconJSONData)
    def test_load_latest_lexicon_json_data(self, lexicon_dir, gold_latest_complete, gold_latest_updated):
        test_latest_complete, test_latest_updated = POGGLexiconUtil.load_latest_lexicon_json_data(lexicon_dir)
        assert test_latest_complete == gold_latest_complete
        assert test_latest_updated == gold_latest_updated

    @parametrize_with_cases("tmp_path, complete, incomplete, invalid, gold_complete, gold_incomplete, gold_invalid, gold_all",
                            cases=DumpLexiconJSONData)
    def test_dump_lexicon_json_data(self, tmp_path, complete, incomplete, invalid, gold_complete, gold_incomplete, gold_invalid, gold_all):
        # create empty lexicon files
        open(os.path.join(tmp_path, "test_complete_entries.json"), "w").close()
        open(os.path.join(tmp_path, "test_incomplete_entries.json"), "w").close()
        open(os.path.join(tmp_path, "test_invalid_entries.json"), "w").close()
        open(os.path.join(tmp_path, "test_all_entries.json"), "w").close()

        POGGLexiconUtil.dump_lexicon_json_data(tmp_path, complete, incomplete, invalid)

        complete_file_contents = json.load(open(glob.glob(os.path.join(tmp_path, "test_complete_entries.json"))[0]))
        incomplete_file_contents = json.load(open(glob.glob(os.path.join(tmp_path, "test_incomplete_entries.json"))[0]))
        invalid_file_contents = json.load(open(glob.glob(os.path.join(tmp_path, "test_invalid_entries.json"))[0]))
        all_file_contents = json.load(open(glob.glob(os.path.join(tmp_path, "test_all_entries.json"))[0]))

        assert complete_file_contents == gold_complete
        assert incomplete_file_contents == gold_incomplete
        assert invalid_file_contents == gold_invalid
        assert all_file_contents == gold_all

    @parametrize_with_cases("tmp_path, initial_incomplete, initial_all, new_skeleton, gold_updated_incomplete, gold_updated_all",
                            cases=AddNewGraphDataToLexicon)
    def test_add_new_graph_data_to_lexicon(self, tmp_path, initial_incomplete, initial_all, new_skeleton, gold_updated_incomplete, gold_updated_all):
        # dump the incomplete_ and all_entries into files in the tmp_path
        with (open(os.path.join(tmp_path, "test_lexicon_incomplete_entries.json"), "w") as incomplete_file,
              open(os.path.join(tmp_path, "test_lexicon_all_entries.json"), "w") as all_file):
            json.dump(initial_incomplete, incomplete_file, indent=4)
            json.dump(initial_all, all_file, indent=4)

        POGGLexiconUtil.add_new_graph_data_to_lexicon("test", tmp_path, new_skeleton)

        # load new file contents
        test_updated_incomplete = json.load(open(os.path.join(tmp_path, "test_lexicon_incomplete_entries.json")))
        test_updated_all = json.load(open(os.path.join(tmp_path, "test_lexicon_all_entries.json")))

        assert test_updated_incomplete == gold_updated_incomplete
        assert test_updated_all == gold_updated_all


    @parametrize_with_cases("lexicon_dir, gold_updated_complete, gold_updated_incomplete, gold_updated_invalid, gold_updated_all",
                            cases=UpdateLexiconFiles)
    def test_update_lexicon_files(self, lexicon_dir, gold_updated_complete, gold_updated_incomplete, gold_updated_invalid, gold_updated_all):
        POGGLexiconUtil.update_lexicon_files(lexicon_dir)


        assert json.load(open(os.path.join(lexicon_dir, "worked_on_complete_entries.json"))) == gold_updated_complete
        assert json.load(open(os.path.join(lexicon_dir, "worked_on_incomplete_entries.json"))) == gold_updated_incomplete
        assert json.load(open(os.path.join(lexicon_dir, "worked_on_invalid_entries.json"))) == gold_updated_invalid
        assert json.load(open(os.path.join(lexicon_dir, "worked_on_all_entries.json"))) == gold_updated_all