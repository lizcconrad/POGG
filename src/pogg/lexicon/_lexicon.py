import os
from pathlib import Path
import copy
from typing import List
import json

from pogg.data_handling import POGGDataset, POGGDataSplit

from pogg.lexicon._lexicon_entry import POGGLexiconEntry
from pogg.lexicon._auto_lexicon import POGGLexiconAutoFiller


class POGGLexicon:
    def __init__(self, lexicon_path, dataset: POGGDataset,
                 imported_lexicon_paths: List = None, auto_filler: POGGLexiconAutoFiller = None):

        # set name to be last part of path
        self.name = lexicon_path.split("/")[-1]

        self.directory = lexicon_path
        self.imported_lexicon_paths = imported_lexicon_paths
        self.all_entries_file = Path(self.directory, f"{self.name}_lexicon_all_entries.json")
        self.approved_entries_file = Path(self.directory, f"{self.name}_lexicon_approved_entries.json")
        self.workspace_file = Path(self.directory, f"{self.name}_lexicon_workspace.json")

        self.all_node_entries = {}
        self.all_edge_entries = {}
        self.workspace_node_entries = {}
        self.workspace_edge_entries = {}
        # approved entries only
        self.node_entries = {}
        self.edge_entries = {}

        self.auto_filler = auto_filler

        self.dataset = dataset
        if len(self.dataset.data_splits.keys()) > 1:
            raise ValueError(f"Unable to determine top data split: {self.dataset.data_splits}")

        top_split_key = list(dataset.data_splits.keys())[0]
        self.top_data_split = dataset.data_splits[top_split_key]["data_split_object"]

        # if all_entries doesn't exist, initialize the directory
        if not os.path.isfile(self.all_entries_file):
            self._initialize_lexicon_directory()

        # read in information from directory (which already existed or was just initialized)
        self._read_from_directory()

    def _initialize_lexicon_directory(self):
        # make lexicon dirs
        Path(self.directory).mkdir(parents=True, exist_ok=True)
        skeleton = self._create_lexicon_skeleton()

        # dump blank lexicon file to approved_entries_file
        if self.imported_lexicon_paths:
            imported_node_entries, imported_edge_entries = self._import_lexicons()

            # update entries in the skeleton
            for key in imported_node_entries:
                skeleton["node_entries"][key] = imported_node_entries[key].convert_to_dict_format()
            for key in imported_edge_entries:
                skeleton["edge_entries"][key] = imported_edge_entries[key].convert_to_dict_format()


        # dump skeleton into all_entries_file and workspace_file
        with (open(self.all_entries_file, "w") as all_f,
              open(self.workspace_file, "w") as workspace_f):
            json.dump(skeleton, all_f, indent=4)
            json.dump(skeleton, workspace_f, indent=4)

        # dump empty approved file; update will pull any approved entries from skeleton
        with open(self.approved_entries_file, "w") as approved_f:
            json.dump({
                "node_entries": {},
                "edge_entries": {}
            }, approved_f, indent=4)


    def _create_lexicon_skeleton(self):
        default_entry = {
            "lexicon_entry": {
                "comp_fxn": ""
            },
            "auto_info": {
                "string_to_parse": "",
                "template_used": "",
                "blocked_templates": [],
                "attempted_templates": [],
            },
            "flags": {
                "auto_filled": False,
                "complete": False,
                "approved": False,
                "invalid": False,
                "create_template_from": False
            }

        }

        lexicon_skeleton = {
            "node_entries": {},
            "edge_entries": {}
        }

        for node in self.dataset.node_keys:
            lexicon_skeleton["node_entries"][node] = default_entry.copy()
            lexicon_skeleton["node_entries"][node]["entry_type"] = "node"
        for edge in self.dataset.edge_keys:
            lexicon_skeleton["edge_entries"][edge] = default_entry.copy()
            lexicon_skeleton["edge_entries"][edge]["entry_type"] = "edge"

        # sort the node_entries
        lexicon_skeleton["node_entries"] = dict(sorted(lexicon_skeleton["node_entries"].items()))
        # sort the edge_entries
        lexicon_skeleton["edge_entries"] = dict(sorted(lexicon_skeleton["edge_entries"].items()))

        return lexicon_skeleton

    def _read_from_file(self, file):
        with open(file, "r") as f:
            file_json = json.load(f)

        entries_dict = {
            "node_entries": {},
            "edge_entries": {}
        }

        for node_key, node_entry in file_json['node_entries'].items():
            entry_obj = POGGLexiconEntry(node_key, node_entry)
            entries_dict["node_entries"][node_key] = entry_obj

        for edge_key, edge_entry in file_json['edge_entries'].items():
            entry_obj = POGGLexiconEntry(edge_key, edge_entry)
            entries_dict["edge_entries"][edge_key] = entry_obj

        return entries_dict

    def _read_from_directory(self):
        all_entries_dict = self._read_from_file(self.all_entries_file)
        self.all_node_entries = all_entries_dict["node_entries"]
        self.all_edge_entries = all_entries_dict["edge_entries"]

        workspace_entries_dict = self._read_from_file(self.workspace_file)
        self.workspace_node_entries = workspace_entries_dict["node_entries"]
        self.workspace_edge_entries = workspace_entries_dict["edge_entries"]

        approved_entries_dict = self._read_from_file(self.approved_entries_file)
        # remove entries that have been marked as not approved anymore
        for node_key in copy.copy(approved_entries_dict["node_entries"]):
            if not approved_entries_dict["node_entries"][node_key].approved:
                approved_entries_dict["node_entries"].pop(node_key)
        for edge_key in copy.copy(approved_entries_dict["edge_entries"]):
            if not approved_entries_dict["edge_entries"][edge_key].approved:
                approved_entries_dict["edge_entries"].pop(edge_key)

        self.node_entries = approved_entries_dict["node_entries"]
        self.edge_entries = approved_entries_dict["edge_entries"]

    def _import_lexicons(self):
        imported_node_entries = {}
        imported_edge_entries = {}
        for path in self.imported_lexicon_paths:
            imported_lexicon = POGGLexicon(path, self.dataset)
            imported_node_entries.update(imported_lexicon.all_node_entries)
            imported_edge_entries.update(imported_lexicon.all_edge_entries)
        return imported_node_entries, imported_edge_entries


    def update_lexicon_files(self):
        for node_key, node_entry in copy.deepcopy(self.workspace_node_entries).items():
            # if it's already approved, move it
            if node_entry.approved:
                self.node_entries[node_key] = node_entry
                self.all_node_entries[node_key] = node_entry
                # remove from workspace if approved
                self.workspace_node_entries.pop(node_key)
                continue

            # if template_used in blocked_templates then clear out the entry
            if node_entry.template_used in node_entry.blocked_templates:
                new_entry = POGGLexiconEntry(node_key)
                # carry over some information
                new_entry.entry_type = node_entry.entry_type
                new_entry.string_to_parse = node_entry.string_to_parse
                new_entry.blocked_templates = node_entry.blocked_templates
                new_entry.attempted_templates = node_entry.attempted_templates
                node_entry = new_entry

            # if not, try auto filling
            if self.auto_filler:
                self.auto_filler.auto_fill_entry(node_entry)
            # if it wasn't auto filled, expand it
            if not node_entry.auto_filled:
                node_entry.expand_entry()


            self.all_node_entries[node_key] = node_entry
            self.workspace_node_entries[node_key] = node_entry
            # TODO: if auto approve when complete is on
            if node_entry.approved:
                self.node_entries[node_key] = node_entry
                self.all_node_entries[node_key] = node_entry
                # remove from workspace if approved
                self.workspace_node_entries.pop(node_key)

        for edge_key, edge_entry in copy.deepcopy(self.workspace_edge_entries).items():
            edge_entry.expand_entry()
            self.all_edge_entries[edge_key] = edge_entry
            self.workspace_edge_entries[edge_key] = edge_entry
            if edge_entry.approved:
                self.edge_entries[edge_key] = edge_entry
                self.all_edge_entries[edge_key] = edge_entry
                # remove from workspace if approved
                self.workspace_edge_entries.pop(edge_key)

        self._dump_to_file(self.all_node_entries, self.all_edge_entries, self.all_entries_file)
        self._dump_to_file(self.workspace_node_entries, self.workspace_edge_entries, self.workspace_file)
        self._dump_to_file(self.node_entries, self.edge_entries, self.approved_entries_file)

    def _dump_to_file(self, node_entries, edge_entries, file):
        json_only = {
            "node_entries": {},
            "edge_entries": {}
        }

        for node_key, node_entry in node_entries.items():
            json_only["node_entries"][node_key] = node_entry.convert_to_dict_format()
        for edge_key, edge_entry in edge_entries.items():
            json_only["edge_entries"][edge_key] = edge_entry.convert_to_dict_format()

        # sort the node_keys
        json_only['node_entries'] = dict(sorted(json_only['node_entries'].items()))
        # sort the edge_keys
        json_only['edge_entries'] = dict(sorted(json_only['edge_entries'].items()))

        with open(file, "w") as f:
            json.dump(json_only, f, indent=4)

    def dump_all_lexicon_entries_to_file(self, file):
        self._dump_to_file(self.all_node_entries, self.all_edge_entries, file)


    def set_workspace_split(self, split: POGGDataSplit, removal_splits: List[POGGDataSplit]=None):
        new_workspace = {
            "node_entries": {},
            "edge_entries": {}
        }

        # start with given split
        working_split = copy.deepcopy(split)
        if removal_splits:
            for removal_split in removal_splits:
                working_split.node_keys = working_split.node_keys.difference(removal_split.node_keys)
                working_split.edge_keys = working_split.edge_keys.difference(removal_split.edge_keys)

        for node in working_split.node_keys:
            # if already approved, skip
            if node in self.node_entries:
                continue
            elif node in self.workspace_node_entries:
                new_workspace["node_entries"][node] = self.workspace_node_entries[node]
            else:
                new_workspace["node_entries"][node] = self.all_node_entries[node]
        for edge in working_split.edge_keys:
            # if already approved, skip
            if edge in self.edge_entries:
                continue
            elif edge in self.workspace_edge_entries:
                new_workspace["edge_entries"][edge] = self.workspace_edge_entries[edge]
            else:
                new_workspace["edge_entries"][edge] = self.all_edge_entries[edge]

        self.workspace_node_entries = new_workspace["node_entries"]
        self.workspace_edge_entries = new_workspace["edge_entries"]


