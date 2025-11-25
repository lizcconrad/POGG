import os
from delphin import ace
from delphin.codecs import simplemrs
from pogg.pogg_config import POGGConfig
import pogg.semantic_composition.semantic_algebra as semantic_algebra
from pogg.my_delphin import my_delphin, sementcodecs
import pogg.semantic_composition.sement_util as sement_util
from delphin import mrs, codecs
from copy import deepcopy
import tabulate

pogg_config = POGGConfig("data/config.yml")

gold_sement_str = """
        [ TOP: h105
          INDEX: e101
          RELS: < [ _believe_v_1 LBL: h105 ARG0: e101 ARG1: i102 ARG2: u103 ARG3: h104 ]
                  [ _sleep_v_1 LBL: h115 ARG0: e113 ARG1: x106 ]
                  [ udef_q LBL: h109 ARG0: x106 RSTR: h107 BODY: h108 ]
                  [ _cat_n_1 LBL: h112 ARG0: x106 ] >
          HCONS: < h107 qeq h112 u103 qeq h115 >
          SLOTS: < ARG1: i102 ARG3: h104 > ]
        """

actual_sement_str = """
        [ TOP: h0
  INDEX: e1
  RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
          [ udef_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
          [ _cat_n_1 LBL: h9 ARG0: x10 ]
          [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10111 ] >
  SLOTS: < ARG1: i2 ARG3: h4 >
  HCONS: < h7 qeq h9 h4 qeq h11 > ]
        """

gold_sement = sementcodecs.decode(gold_sement_str)
actual_sement = sementcodecs.decode(actual_sement_str)

overlap_eqs, gold_eqs, actual_eqs = sement_util.find_var_eq_overlaps(gold_sement, actual_sement)
overlap_hcons, gold_hcons, actual_hcons = sement_util.find_hcons_overlaps(gold_sement, actual_sement)


print(sement_util._build_overlap_eqs_table(overlap_eqs))
print(sement_util._build_nonoverlap_eqs_table(gold_eqs, "gold"))
print(sement_util._build_nonoverlap_eqs_table(actual_eqs, "actual"))

print(sement_util._build_overlap_hcons_table(overlap_hcons))
print(sement_util._build_nonoverlap_hcons_table(gold_hcons, "gold"))
print(sement_util._build_nonoverlap_hcons_table(actual_hcons, "actual"))








### PARSER SANDBOX ###
with ace.ACEParser(pogg_config.grammar_location) as parser, ace.ACEGenerator(pogg_config.grammar_location, ['-r', 'root_frag']) as generator:
    parser_response = parser.interact("Liz ate a cookie")
    for r in parser_response.results():
        mrs_obj = simplemrs.decode(r['mrs'])
        print(simplemrs.encode(mrs_obj, indent=True))

