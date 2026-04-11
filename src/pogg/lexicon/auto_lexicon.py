import re
from itertools import permutations
import json
import inspect
from delphin import ace
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.my_delphin import sementcodecs
from pogg.semantic_composition.sement_util import POGGSEMENTUtil
from pogg.lexicon.lexicon_builder import POGGLexiconEntry, POGGLexiconUtil

# TODO: i don't like this here but it's fine for now...
NOUN_SYNOPSES = [
    {"roles": [{"name": "ARG0", "value": "x"}]},
    {"roles": [{"name": "ARG0", "value": "x"}, {"name": "ARG1", "value": "i"}]},
]


class POGGLexiconAutoFiller:
    def __init__(self, pogg_config, template_file):
        self.templates = {}

        self.pogg_config = pogg_config
        self.semantic_algebra = SemanticAlgebra(pogg_config)
        self.semantic_composition = SemanticComposition(self.semantic_algebra)
        self.converter = POGGGraphConverter(self.semantic_composition)
        
        self.template_file = template_file
        
        self.read_templates_from_file(template_file)

    def read_templates_from_file(self, template_file: str):
        with open(template_file) as f:
            templates_json = json.load(f)

        for template_key in templates_json:
            template  = {
                "example": templates_json[template_key]["example"],
                "lexical_entry_template": templates_json[template_key]["lexical_entry_template"],
                "lexical_entry": POGGLexiconUtil.convert_dict_entry_to_POGGLexiconEntry(template_key, templates_json[template_key]["lexical_entry_template"]),
                "placeholders": self.determine_template_placeholders(templates_json[template_key]["lexical_entry_template"], []),
                # "SEMENT_str": templates_json[template_key]["SEMENT_str"]
            }
            self.templates[template_key] = template


    def determine_template_placeholders(self, template_entry, placeholders_list):
        for key in template_entry.keys():
            if key != "comp_fxn":
                # if the value is a string 
                if isinstance(template_entry[key], str):
                    placeholders_list.append(template_entry[key])
                # if it is a dict, recurse and pass in the list
                else:
                    self.determine_template_placeholders(template_entry[key], placeholders_list)
        return placeholders_list


    def dump_templates_to_file(self, template_file: str):
        dumpable_json = {}
        with open(template_file, "w") as f:
            for template_key, template_entry in self.templates.items():
                dumpable_entry = {
                    "example": template_entry["example"],
                    "lexical_entry_template": template_entry["lexical_entry_template"],
                    # "SEMENT_str": template_entry["SEMENT_str"]
                }
                dumpable_json[template_key] = dumpable_entry

            json.dump(dumpable_json, f, indent=4)


    def get_ERG_parse_MRSes(self, to_parse):
        # get the ERG parse for a node to attempt to match against a template
        # just return the first result
        with ace.ACEParser(self.pogg_config.grammar_location) as parser:
            parser_response = parser.interact(to_parse)

            mrs_objs = [sementcodecs.decode(r['mrs']) for r in parser_response.results()]
            for mrs_obj in mrs_objs:
                # replace all quantifiers with abstract_q
                # the generic quantifiers i use do not match the ERG output usually
                for rel in mrs_obj.rels:
                    if rel.predicate.endswith("_q"):
                        rel.predicate = "abstract_q"
            return mrs_objs

    def get_template_SEMENT(self, template):
        if "SEMENT_str" in template and template["SEMENT_str"] != "":
            template_mrs = sementcodecs.decode(template["SEMENT_str"])
        else:
            template_lexent = template["lexical_entry"]
            template_mrs = self.converter.get_SEMENT(template_lexent.composition_function_name, template_lexent.parameters)
            template_mrs = self.semantic_algebra.prepare_for_generation(template_mrs)

            # replace all quantifiers with abstract_q
            # the generic quantifiers i use do not match the ERG output usually
            for rel in template_mrs.rels:
                if rel.predicate.endswith("_q"):
                    rel.predicate = "abstract_q"

            # save the string for later
            template["SEMENT_str"] = sementcodecs.encode(template_mrs)

        return template_mrs

    @staticmethod
    def get_placeholder_filler_candidates(erg_mrs):
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

    @staticmethod
    def get_placeholder_to_filler_mapping_candidates(template, placeholder_filler_candidates):
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

    @staticmethod
    def fill_placeholders(SEMENT_obj, mapping):
        duplicate_SEMENT = POGGSEMENTUtil.duplicate_sement(SEMENT_obj)
        for rel in duplicate_SEMENT.rels:
            if rel.predicate in mapping:
                rel.predicate = mapping[rel.predicate]
                continue
            elif 'CARG' in rel.args and rel.args['CARG'] in mapping:
                rel.args['CARG'] = mapping[rel.args['CARG']]
        return duplicate_SEMENT

    def check_for_template_match(self, template, erg_mrs):
        if erg_mrs is not None:
            template_SEMENT = self.get_template_SEMENT(template)

            if POGGSEMENTUtil.is_sement_isomorphic_ignore_predicate_labels(template_SEMENT, erg_mrs):

                placeholder_candidates = self.get_placeholder_filler_candidates(erg_mrs)

                # create a list of acceptable mappings
                mapping_candidates = self.get_placeholder_to_filler_mapping_candidates(template, placeholder_candidates)

                # attempt full isomorphism with all mapping_candidates
                for mapping in mapping_candidates:
                    altered_template_SEMENT = self.fill_placeholders(template_SEMENT, mapping)

                    # ignore var props
                    if POGGSEMENTUtil.is_sement_isomorphic(altered_template_SEMENT, erg_mrs, False):
                        return self.fill_template(template, mapping)

        return  None

    @staticmethod
    def fill_template(template, mapping):
        # hacky but easier
        template_string = json.dumps(template["lexical_entry_template"])
        for placeholder, filler in mapping.items():
            template_string = template_string.replace(placeholder, filler)
        filled_in_template = json.loads(template_string)

        return filled_in_template

    def find_and_fill_template(self, string_to_parse):
        erg_MRSes = self.get_ERG_parse_MRSes(string_to_parse)
        for erg_MRS in erg_MRSes:
            for template_name, template in self.templates.items():
                filled_in_template = self.check_for_template_match(template, erg_MRS)

                if filled_in_template is not None:
                    # add auto flag
                    filled_in_template["auto"] = {
                        "auto_filled": True,
                        "template_used": template_name,
                    }
                    return filled_in_template
        return None


    def compare_lexical_entry_structures(self, template_entry, new_entry):
        # check to see if a lexical entry matches an existing template already
        # if it doesn't it can be added as a new template

        for key in template_entry.keys():
            if key in new_entry.keys():
                # check comp_fxn
                if key == "comp_fxn":
                    # False if no match
                    if new_entry[key] != template_entry[key]:
                        return False
                # if the key isn't comp_fxn, check if they're both the same type
                elif type(template_entry[key]) == type(new_entry[key]):
                    # both dicts, recurse
                    if isinstance(template_entry[key], dict):
                        # if this doesn't return True, return False, otherwise keep going
                        if not self.compare_lexical_entry_structures(template_entry[key], new_entry[key]):
                            return False
                # if not comp_fxn or matching types, then False
                else:
                    return False
            # key not in both, False
            else:
                return False
        return True
            
    def look_for_new_templates(self, lexicon_json):
        new_templates = {}

        all_entries = lexicon_json["node_keys"]
        all_entries.update(lexicon_json["edge_keys"])


        for entry_name, entry in all_entries.items():
            # if already marked as auto, skip
            if "auto" in entry.keys():
                continue

            match_found = False
            for _, template in self.templates.items():
                template_entry = template["lexical_entry_template"]
                if self.compare_lexical_entry_structures(template_entry, entry):
                    # match found, not new
                    match_found = True
                    break

            if not match_found:
                new_templates[f"TEMPLATE_{entry_name}"] = entry

        return new_templates

    def dump_new_templates(self, lexicon_json):
        new_templates = self.look_for_new_templates(lexicon_json)
        for new_template_name, new_template in new_templates.items():
            self.templates[new_template_name] = {
                "example": "",
                "lexical_entry_template": new_template,
            }

        self.dump_templates_to_file(self.template_file)
