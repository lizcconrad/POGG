import re
import copy
from itertools import permutations
import json
from delphin import ace, mrs

from pogg_semantics.pogg_config import POGGCompositionConfig
from pogg_semantics.my_delphin import sementcodecs
from pogg_semantics.semantic_composition import SemanticAlgebra, SEMENTUtil

from pogg.graph_to_SEMENT import POGGGraphConverter

from pogg.lexicon._lexicon_entry import POGGLexiconEntry


class POGGLexiconAutoFiller:
    def __init__(self, composition_config,
                 template_files,
                 global_blocked_templates,
                 auto_approve=False,
                 string_processing_fxn=None,
                 dump_file=None,
                 auto_create_templates=False):

        if isinstance(composition_config, POGGCompositionConfig):
            self.composition_config = composition_config
        else:
            self.composition_config = POGGCompositionConfig(composition_config)
        self.semantic_algebra = SemanticAlgebra(self.composition_config)
        self.converter = POGGGraphConverter(self.composition_config)

        self.templates = {}
        for file in template_files:
            self._read_templates_from_file(file)

        # remove global blocks
        for blocked_template in global_blocked_templates:
            self.templates.pop(blocked_template)

        self.auto_approve = auto_approve
        self.string_processing_fxn = string_processing_fxn
        self.dump_file = dump_file
        self.auto_create_templates = auto_create_templates


    def _read_templates_from_file(self, template_file: str):
        try:
            with open(template_file, "r") as f:
                try:
                    templates_json = json.load(f)
                except json.JSONDecodeError:
                    templates_json = {}
        except FileNotFoundError:
            with open(template_file, "w") as f:
                pass
            templates_json = {}

        for template_key in templates_json:
            template  = {
                "example": templates_json[template_key]["example"],
                "lexical_entry_template": templates_json[template_key]["lexical_entry_template"],
                "lexical_entry": POGGLexiconEntry(template_key, templates_json[template_key]["lexical_entry_template"]),
                "placeholders": self._determine_template_placeholders(templates_json[template_key]["lexical_entry_template"], []),
                # "SEMENT_str": templates_json[template_key]["SEMENT_str"]
            }
            self.templates[template_key] = template

    def _determine_template_placeholders(self, template_entry, placeholders_list):
        for key in template_entry.keys():
            if key != "comp_fxn":
                # if the value is a string
                if isinstance(template_entry[key], str):
                    placeholders_list.append(template_entry[key])
                # if it is a dict, recurse and pass in the list
                elif isinstance(template_entry[key], dict):
                    self._determine_template_placeholders(template_entry[key], placeholders_list)
                # if it's null
                else:
                    continue
        return placeholders_list

    def _get_template_SEMENT(self, template):
        if "SEMENT_str" in template and template["SEMENT_str"] != "":
            template_mrs = sementcodecs.decode(template["SEMENT_str"])
        else:
            template_lexent = template["lexical_entry"]
            template_mrs = self.converter.get_SEMENT(template_lexent.composition_function_name,
                                                         template_lexent.parameters)
            template_mrs = self.semantic_algebra.prepare_for_generation(template_mrs)

            # replace all quantifiers with abstract_q
            # the generic quantifiers i use do not match the ERG output usually
            for rel in template_mrs.rels:
                if rel.predicate.endswith("_q"):
                    rel.predicate = "abstract_q"

            # save the string for later
            template["SEMENT_str"] = sementcodecs.encode(template_mrs)

        return template_mrs

    def _get_ERG_parse_MRSes(self, to_parse):
        # get the ERG parse for a node to attempt to match against a template
        # just return the first result
        with ace.ACEParser(self.composition_config.grammar_location) as parser:
            parser_response = parser.interact(to_parse)

            # if there's a parser issue, just skip it
            try:
                mrs_objs = [sementcodecs.decode(r['mrs']) for r in parser_response.results()]
            except mrs._exceptions.MRSSyntaxError as e:
                return []

            for mrs_obj in mrs_objs:
                # replace all quantifiers with abstract_q
                # the generic quantifiers i use do not match the ERG output usually
                for rel in mrs_obj.rels:
                    if rel.predicate.endswith("_q"):
                        rel.predicate = "abstract_q"
            return mrs_objs

    def _get_filler_candidates(self, erg_mrs):
        # look through the MRS for potential candidates that could fill in placeholders in the template
        placeholder_candidates = []

        # for each REL in the erg_mrs...
        for rel in erg_mrs.rels:
            # get the placeholder candidate from the EP
            if 'CARG' in rel.args:
                placeholder_candidates.append(rel.args['CARG'])
            # skip words not in SEMI
            elif rel.predicate.endswith("_u_unknown"):
                continue
            # otherwise try to find pos
            else:
                try:
                    pos = re.match(r".*_([a-z])(_.+)*", rel.predicate).group(1)
                    if pos != "q":
                        placeholder_candidates.append(rel.predicate)
                # couldn't guess pos, probably abstract, skip
                except AttributeError:
                    continue

        return placeholder_candidates

    def _get_filler_mapping_candidates(self, template, placeholder_filler_candidates):
        # get a list of possible mappings e.g.
        """[{
            "template_placeholder_1": "filler_candidate1"
            "template_placeholder_2": "filler_candidate2"
        },
        {
            "template_placeholder_1": "filler_candidate2"
            "template_placeholder_2": "filler_candidate1"
        }]
        """
        # create a list of acceptable mappings
        mapping_candidates = []

        # get permutations of placeholder_candidates where length matches the # of placeholders
        placeholder_perms = permutations(placeholder_filler_candidates, len(template["placeholders"]))

        for perm in placeholder_perms:
            mapping = {}
            for i, placeholder in enumerate(sorted(template["placeholders"])):
                candidate_filler = perm[i]

                # try to get pos labels
                try:
                    placeholder_pos = re.match(r".*_([a-z])(_.+)", placeholder).group(1)
                except AttributeError:
                    placeholder_pos = None

                try:
                    candidate_filler_pos = re.match(r".*_([a-z])(_.+)", candidate_filler).group(1)
                except AttributeError:
                    candidate_filler_pos = None

                # check that the candidate_filler from the permutation
                # is legitimate for the placeholder in the template (i.e. pos should match)
                if placeholder_pos == candidate_filler_pos:
                    mapping[placeholder] = candidate_filler
                else:
                    continue
            if len(mapping.keys()) == len(template["placeholders"]):
                mapping_candidates.append(mapping)

        return mapping_candidates

    def _find_correct_placeholder_mapping(self, template, erg_mrs):
        if erg_mrs is not None:
            template_SEMENT = self._get_template_SEMENT(template)

            if SEMENTUtil.is_sement_isomorphic_ignore_predicate_labels(template_SEMENT, erg_mrs):

                placeholder_candidates = self._get_filler_candidates(erg_mrs)

                # create a list of acceptable mappings
                mapping_candidates = self._get_filler_mapping_candidates(template, placeholder_candidates)

                # attempt full isomorphism with all mapping_candidates
                for mapping in mapping_candidates:
                    altered_template_SEMENT = self._fill_placeholders(template_SEMENT, mapping)

                    # ignore var props
                    if SEMENTUtil.is_sement_isomorphic(altered_template_SEMENT, erg_mrs, False):
                        return mapping

        return  None

    def _fill_placeholders(self, SEMENT_obj, mapping):
        duplicate_SEMENT = SEMENTUtil.duplicate_sement(SEMENT_obj)
        for rel in duplicate_SEMENT.rels:
            if rel.predicate in mapping:
                rel.predicate = mapping[rel.predicate]
                continue
            elif 'CARG' in rel.args and rel.args['CARG'] in mapping:
                rel.args['CARG'] = mapping[rel.args['CARG']]
        return duplicate_SEMENT

    def _fill_template(self, template, mapping):
        # hacky but easier
        template_string = json.dumps(template["lexical_entry_template"])
        for placeholder, filler in mapping.items():
            template_string = template_string.replace(placeholder, filler)
        filled_in_template = json.loads(template_string)

        return filled_in_template

    def _find_and_fill_template(self, lexicon_entry):

        erg_MRSes = self._get_ERG_parse_MRSes(lexicon_entry.string_to_parse)

        for template_name, template in self.templates.items():
            for erg_MRS in erg_MRSes:

                # skip blocked/already attempted templates
                if template_name in lexicon_entry.blocked_templates or template_name in lexicon_entry.attempted_templates:
                    continue

                mapping = self._find_correct_placeholder_mapping(template, erg_MRS)

                if mapping is not None:
                    print(f"AUTO FILLING {lexicon_entry.key} with {template_name}...")
                    filled_template = self._fill_template(template, mapping)
                    lexicon_entry.entry_in_dict_format = filled_template
                    lexicon_entry.template_used = template_name
                    lexicon_entry.auto_filled = True
                    lexicon_entry.validate_entry()
                    lexicon_entry.check_entry_completion()

                    if self.auto_approve:
                        print(f"...... auto-approve ON ... approved {lexicon_entry.key}...")
                        lexicon_entry.approved = True

                    # add as an attempt when it works
                    lexicon_entry.attempted_templates.add(template_name)
                    return

            # add template to attempted templates
            lexicon_entry.attempted_templates.add(template_name)

    def auto_fill_entry(self, lexicon_entry: POGGLexiconEntry):
        # skip if "blocked_templates" says "all"
        # or skip if all templates have been marked as blocked or attempted
        blocked_and_attempted = copy.copy(lexicon_entry.blocked_templates)
        blocked_and_attempted.update(lexicon_entry.attempted_templates)

        # CASES:
        # 1. block "all"
        # 2. template_used != "" and != blocked_templates ... i.e. entry is complete but not yet approved but not marked as wrong either
        # 3. # of blocked+attempted templates == # of total templates
        if ("all" in lexicon_entry.blocked_templates or
                (lexicon_entry.template_used != "" and lexicon_entry.template_used not in lexicon_entry.blocked_templates)
                or len(blocked_and_attempted) == len(self.templates)):
            print(f"All templates blocked or attempted for '{lexicon_entry.key}'... skipping...")
            return

        # if a string is already provided in the entry, use that
        if lexicon_entry.string_to_parse == "":
            if self.string_processing_fxn:
                lexicon_entry.string_to_parse = self.string_processing_fxn(lexicon_entry.key)
            else:
                lexicon_entry.string_to_parse = lexicon_entry.key

        self._find_and_fill_template(lexicon_entry)


    def _compare_lexical_entry_structures(self, template_entry, new_entry_dict):
        # check to see if a lexical entry matches an existing template already
        # if it doesn't it can be added as a new template

        for key in template_entry.keys():
            if key in new_entry_dict.keys():
                # check comp_fxn
                if key == "comp_fxn":
                    # False if no match
                    if new_entry_dict[key] != template_entry[key]:
                        return False
                # if the key isn't comp_fxn, check if they're both the same type
                elif type(template_entry[key]) == type(new_entry_dict[key]):
                    # both dicts, recurse
                    if isinstance(template_entry[key], dict):
                        # if this doesn't return True, return False, otherwise keep going
                        if not self._compare_lexical_entry_structures(template_entry[key], new_entry_dict[key]):
                            return False
                # if not comp_fxn or matching types, then False
                else:
                    return False
            # key not in both, False
            else:
                return False
        return True

    def _look_for_new_templates(self, entries):
        new_templates = {}

        for entry_key, entry in entries.items():
            potential_template = {
                "example": entry.template_example_string,
                "lexical_entry_template": entry.entry_in_dict_format
            }

            # try doing a temporary JSON dump -- if it fails don't use this as a new template
            try:
                json_string = json.dumps(potential_template)
                json_temp = json.loads(json_string)
            except json.JSONDecodeError:
                continue

            # if the entry was manually marked as a new template, add to new_templates
            if entry.create_template_from:
                if entry.name_of_created_template != "":
                    template_name = entry.name_of_created_template
                else:
                    template_name = f"TEMPLATE_{entry_key}"
                if template_name not in self.templates:
                    new_templates[template_name] = potential_template
                    self.templates[template_name] = potential_template

            # if auto_create_templates is on, look for new ones via comparison
            # downside of this is that it won't catch cases where the lexical entry template has the same structure
            # but the resulting MRS has different ARG structures
            # e.g. _cat_n_1 vs. _bag_n_of ... look the same in the lexicon but the MRS is different
            if self.auto_create_templates:
                match_found = False
                for _, template in self.templates.items():
                    template_entry = template["lexical_entry_template"]
                    if self._compare_lexical_entry_structures(template_entry, entry.entry_in_dict_format):
                        # match found, not new
                        match_found = True
                        break

                # no match found i.e. new template
                if not match_found:
                    entry.create_template_from = True
                    new_templates[f"TEMPLATE_{entry_key}"] = potential_template
                    self.templates[f"TEMPLATE_{entry_key}"] = potential_template

        return new_templates

    def _dump_templates_to_file(self, templates_to_dump=None):
        if templates_to_dump is None:
            templates_to_dump = self.templates

        if self.dump_file is None:
            raise ValueError("No template dump file specified.")

        try:
            with open(self.dump_file, "r") as f:
                try:
                    dumpable_json = json.load(f)
                except json.JSONDecodeError:
                    dumpable_json = {}
        except FileNotFoundError:
            dumpable_json = {}

        with open(self.dump_file, "w") as f:
            for template_key, template in templates_to_dump.items():
                dumpable_entry = {
                    "example": template["example"],
                    "lexical_entry_template": template["lexical_entry_template"],
                    # "SEMENT_str": template_entry["SEMENT_str"]
                }
                dumpable_json[template_key] = dumpable_entry
            json.dump(dumpable_json, f, indent=4)

    def dump_new_templates(self, entries):
        new_templates = self._look_for_new_templates(entries)

        # dump newly found ones
        self._dump_templates_to_file(new_templates)
