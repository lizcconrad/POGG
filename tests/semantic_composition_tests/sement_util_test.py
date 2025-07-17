import unittest.mock
import os
from pogg.pogg_config import POGGConfig
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
import pogg.my_delphin.sementcodecs as sementcodecs
import pogg.semantic_composition.sement_util as sement_util
import re

class TestSEMENTUtilFunctions(unittest.TestCase):
    """
    Tests functions included in the semantic algebra
    """
    def setUp(self):
        # create a POGGConfig object that points to a real grammar for testing functionality
        self.top_test_dir = os.getenv("TEST_WORKING_DIR")
        self.test_dir = os.path.join(self.top_test_dir, "test_data/semantic_composition/sement_util")
        self.pogg_config = POGGConfig(os.path.join(self.top_test_dir, "test_data/test_config.yml"))


    def decode_sement_string(self, filename):
        return sementcodecs.decode(open(os.path.join(self.test_dir, filename)).read())


    def test_duplicate_sement(self):
        sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        duplicate_sement = sement_util.duplicate_sement(sement)

        self.assertEqual(sement, duplicate_sement, "Duplicated SEMENT does not match original")
        # assert Object ids are different
        self.assertNotEqual(id(sement.rels), id(duplicate_sement.rels), "IDs for RELS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy")
        self.assertNotEqual(id(sement.slots), id(duplicate_sement.slots),
                            "IDs for SLOTS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy")
        self.assertNotEqual(id(sement.eqs), id(duplicate_sement.eqs),
                            "IDs for EQs list on both original and duplicate SEMENT match, indicating pass by reference and not a copy")
        self.assertNotEqual(id(sement.hcons), id(duplicate_sement.hcons),
                            "IDs for HCONS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy")
        self.assertNotEqual(id(sement.icons), id(duplicate_sement.icons),
                            "IDs for ICONS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy")


    def test_group_equalities(self):
        eqs = [("x1", "x2"), ("x3", "x4"), ("x1", "x4"), ("x5", "x6")]

        # result of grouping should equal this
        gold_groups = [{"x1", "x2", "x3", "x4"}, {"x5", "x6"}]

        grouped_eqs = sement_util.group_equalities(eqs)

        self.assertCountEqual(gold_groups, grouped_eqs)

    def test_get_most_specified_variable(self):
        vars = ["u1", "i2", "x3"]

        most_specified_var = sement_util.get_most_specified_variable(vars)

        # x3 is most specific
        self.assertEqual(most_specified_var, vars[2])

    def test_overwrite_eqs(self):
        test_sement = self.decode_sement_string("give_a_cookie_1_sement.txt")

        new_sement = sement_util.overwrite_eqs(test_sement)

        # for the sement "give a cookie"
        # the following should all be the same if the overwrite worked:
        # a.ARG0 = cookie.ARG0 = give.ARG1

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_arg0 = r.args['ARG0']
            else:
                give_lbl = r.label
                give_arg0 = r.args['ARG0']
                give_arg1 = r.args['ARG1']


        # original equality check
        self.assertTrue(a_arg0 == cookie_arg0 == give_arg1)
        # make sure TOP is back to being the LBL of cookie
        self.assertTrue(new_sement.top == give_lbl)
        # make sure INDEX is back to being ARG0 of give
        self.assertTrue(new_sement.index == give_arg0)

    def test_overwrite_eqs_hcon_lo(self):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        # this case was unaccounted for above
        a_tasty_cookie_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        new_sement = sement_util.overwrite_eqs(a_tasty_cookie_sement)

        # for the sement "a tasty cookie"
        # the following should all be the same if the overwrite worked:
        # a.ARG0 = cookie.ARG0 = tasty.ARG1
        # cookie.LBL = tasty.LBL

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_lbl = r.label
                cookie_arg0 = r.args['ARG0']
            else:
                tasty_lbl = r.label
                tasty_arg1 = r.args['ARG1']

        # original equality check
        self.assertTrue(a_arg0 == cookie_arg0 == tasty_arg1)
        # make sure TOP == cookie.lbl == tasty.lbl
        self.assertTrue(new_sement.top == cookie_lbl == tasty_lbl)

    def test_overwrite_eqs_hcon_hi(self):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        # this case was unaccounted for above
        probably_sleeps_sement = self.decode_sement_string("probably_sleeps_sement.txt")
        new_sement = sement_util.overwrite_eqs(probably_sleeps_sement)

        # there should be a QEQ between _probable_a_1.ARG1 and _sleep_v_1.LBL
        # and the hi handle should be type h

        for r in new_sement.rels:
            if r.predicate == "_probable_a_1":
                probable_arg1 = r.args['ARG1']
            else:
                sleep_lbl = r.label

        # make sure there's just one hcon
        self.assertTrue(len(new_sement.hcons) == 1, "More than one handle constraint")

        # get the handle constraint
        hcon = new_sement.hcons[0]
        # check that the hi-handle is the ARG1 of probable
        self.assertTrue(hcon.hi == probable_arg1, "ARG1 of _probable_a_1 not hi-handle in handle constraint")
        # check that probable_arg1 is of type h
        self.assertTrue(probable_arg1[0] == "h", "hi-handle not of type h")
        # check that the lo-handle is the LBL of sleep
        self.assertTrue(hcon.lo == sleep_lbl, "LBL of _sleep_v_1 not lo-handle in handle constraint")



    def test_overwrite_eqs_empty(self):
        test_sement = self.decode_sement_string("unquantified_cookie_sement.txt")
        self.assertEqual(test_sement, sement_util.overwrite_eqs(test_sement))


    def test_overwrite_eqs_none(self):
        test_sement = self.decode_sement_string("unquantified_cookie_sement.txt")
        test_sement.eqs = None
        self.assertEqual(test_sement, sement_util.overwrite_eqs(test_sement))


    def test_original_eqs_preserved(self):
        # test to make sure the EQs in the original SEMENT are not eliminated
        # i.e. computation should not alter original EQ list, that SEMENT object should stay intact
        test_sement = self.decode_sement_string("give_a_cookie_1_sement.txt")

        eqs_pre_rewrite = test_sement.eqs.copy()
        sement_util.overwrite_eqs(test_sement)
        self.assertEqual(eqs_pre_rewrite, test_sement.eqs)


    def test_check_if_quantified_true_noun(self):
        # test to confirm a quantified noun SEMENT passes check_if_quantified
        test_sement = self.decode_sement_string("quantified_cookie_sement.txt")
        self.assertTrue(sement_util.check_if_quantified(test_sement))

    def test_check_if_quantified_true_noun_phrase(self):
        # test to confirm a quantified noun phrase SEMENT passes check_if_quantified
        # note this SEMENT is a little bungled, the INDEX is tasty.ARG1 when really it would be cookie.ARG0
        # but check_if_quantified checks whether the INDEX "or something eq to the INDEX" is the ARG0 of an EP with RSTR
        # so this capture sthe "or something eq to the INDEX"
        # which may never happen... but just in case
        test_sement = self.decode_sement_string("quantified_tasty_cookie_sement.txt")
        self.assertTrue(sement_util.check_if_quantified(test_sement))

    def test_check_if_quantified_false(self):
        # test to confirm an unquantified noun SEMENT fails check_if_quantified
        test_sement = self.decode_sement_string("unquantified_cookie_sement.txt")
        self.assertFalse(sement_util.check_if_quantified(test_sement))


    def test_is_sement_isomorphic_true(self):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        sement_1 = self.decode_sement_string("give_a_cookie_1_sement.txt")
        sement_2 = self.decode_sement_string("give_a_cookie_2_sement.txt")

        self.assertTrue(sement_util.is_sement_isomorphic(sement_1, sement_2))


    def test_is_sement_isomorphic_false(self):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        # but also the TOP is incorrect in this one (refers to LBL of 'cookie' not 'give')
        # so they should not be isomorphic
        correct_sement = self.decode_sement_string("give_a_cookie_1_sement.txt")
        broken_sement = self.decode_sement_string("give_a_cookie_wrong_top_sement.txt")

        self.assertFalse(sement_util.is_sement_isomorphic(correct_sement, broken_sement))

    def test_create_variable_roles_dict(self):
        # test using a collapsed SEMENT so that there's no risk of nondeterminism when choosing the representative variable
        a_tasty_cookie_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")

        gold_roles_dict = {
            'h0': ["_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            'e1': ["_tasty_a_1.ARG0"],
            'x4': ["INDEX", "_a_q.ARG0", "_cookie_n_1.ARG0", "_tasty_a_1.ARG1"],
            'h5': ["_a_q.LBL"],
            'h7': ["_a_q.RSTR"],
            'h8': ["_a_q.BODY"],
            'h9': ["TOP"]
        }

        a_tasty_cookie_roles_dict = sement_util.create_variable_roles_dict(a_tasty_cookie_sement)
        self.assertEqual(gold_roles_dict, a_tasty_cookie_roles_dict, 
                         "Gold: {} \nActual:{}".format(gold_roles_dict, a_tasty_cookie_roles_dict))

    def test_create_variable_roles_dict_valueerror(self):
        a_tasty_cookie_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        self.assertRaises(ValueError, sement_util.create_variable_roles_dict, a_tasty_cookie_sement)

    def test_create_hcons_list(self):
        # test using a collapsed SEMENT so that there's no risk of nondeterminism when choosing the representative variable
        a_tasty_cookie_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")

        gold_hcons_list = [{
            "hi_role_set": ["_a_q.RSTR"],
            "lo_role_set": ["_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            "hi_var": "h7",
            "lo_var": "h0",
        }]
        
        a_tasty_cookie_hcons_list = sement_util.create_hcons_list(a_tasty_cookie_sement)

        self.assertEqual(gold_hcons_list, a_tasty_cookie_hcons_list,
                         "Gold: {} \nActual:{}".format(gold_hcons_list, a_tasty_cookie_hcons_list))

    def test_create_hcons_list_valueerror(self):
        a_tasty_cookie_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        self.assertRaises(ValueError, sement_util.create_hcons_list, a_tasty_cookie_sement)

    def test_find_slots_overlaps(self):
        gold_sement = self.decode_sement_string("believe_cats_sleep_sement_collapsed.txt")
        actual_sement = self.decode_sement_string("believe_cats_sleep_broken_hcons_sement.txt")

        gold_overlap_slots = [{
            "slot": "_believe_v_1.ARG1",
            "gold_var": "i2",
            "actual_var": "i02"
        }]

        gold_gold_slots = [{
            "slot": "_believe_v_1.ARG3",
            "gold_var": "h4",
        }]

        gold_actual_slots = [{
            "slot": "_believe_v_1.ARG2",
            "actual_var": "u03",
        }]

        test_overlap_slots, test_gold_slots, test_actual_slots = sement_util.find_slot_overlaps(gold_sement, actual_sement)

        self.assertEqual(gold_overlap_slots, test_overlap_slots,
                         "Gold Overlap: {} \nActual Overlap:{}".format(gold_overlap_slots, test_overlap_slots))
        self.assertEqual(gold_gold_slots, test_gold_slots,
                         "Gold Gold: {} \nActual Gold:{}".format(gold_gold_slots, test_gold_slots))
        self.assertEqual(gold_actual_slots, test_actual_slots,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_actual_slots, test_actual_slots))


    def test_find_slot_overlaps_gold_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_slot_overlaps, uncollapsed_sement, collapsed_sement)

    def test_find_slot_overlaps_actual_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_slot_overlaps, collapsed_sement, uncollapsed_sement)

    def test_find_var_eq_overlaps(self):
        # use collapsed version to avoid nondeterminism in representative variable
        gold_tasty_cookie_sement = self.decode_sement_string("tasty_cookie_sement_collapsed.txt")
        # this SEMENT doesn't include the equivalence between the LBLs of tasty and cookie
        broken_tasty_cookie_sement = self.decode_sement_string("tasty_cookie_broken_sement.txt")

        gold_overlap_eqs = [{
            "eq_set": ["INDEX", "_cookie_n_1.ARG0", "_tasty_a_1.ARG1"],
            "gold_var": "x4",
            "actual_var": "x04"
        }, {
            "eq_set": ["_tasty_a_1.ARG0"],
            "gold_var": "e1",
            "actual_var": "e01"
        }]

        gold_gold_eqs = [{
            "eq_set": ["TOP", "_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            "gold_var": "h0"
        }]

        gold_actual_eqs = [{
            "eq_set": ["TOP", "_cookie_n_1.LBL"],
            "actual_var": "h03"
        }, {
            "eq_set": ["_tasty_a_1.LBL"],
            "actual_var": "h00"
        }]

        test_overlap_eqs, test_gold_eqs, test_actual_eqs = sement_util.find_var_eq_overlaps(gold_tasty_cookie_sement, broken_tasty_cookie_sement)

        self.assertEqual(gold_overlap_eqs, test_overlap_eqs,
                         "Gold Overlap: {} \nActual Overlap:{}".format(gold_overlap_eqs, test_overlap_eqs))
        self.assertEqual(gold_gold_eqs, test_gold_eqs,
                         "Gold Gold: {} \nActual Gold:{}".format(gold_gold_eqs, test_gold_eqs))
        self.assertEqual(gold_actual_eqs, test_actual_eqs,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_actual_eqs, test_actual_eqs))

    def test_find_var_eq_overlaps_gold_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_var_eq_overlaps, uncollapsed_sement, collapsed_sement)

    def test_find_var_eq_overlaps_actual_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_var_eq_overlaps, collapsed_sement, uncollapsed_sement)


    def test_find_hcons_overlaps(self):
        # use collapsed version to avoid nondeterminism in representative variable
        gold_believe_cats_sleep_sement = self.decode_sement_string("believe_cats_sleep_sement_collapsed.txt")
        # this SEMENT doesn't include handle constraint between _believe_v_1.ARG2 and _sleep_v_1.LBL
        broken_believe_cats_sleep_sement = self.decode_sement_string("believe_cats_sleep_broken_hcons_sement.txt")

        gold_overlap_hcons = [{
            "hi_role_set": ["udef_q.RSTR"],
            "lo_role_set": ["_cat_n_1.LBL"],
            "gold_hi_var": "h7",
            "gold_lo_var": "h9",
            "actual_hi_var": "h07",
            "actual_lo_var": "h09",
        }]

        gold_gold_hcons = [{
            "hi_role_set": ["_believe_v_1.ARG2"],
            "lo_role_set": ["_sleep_v_1.LBL"],
            "gold_hi_var": "u3",
            "gold_lo_var": "h11",
        }]

        gold_actual_hcons = [{
            "hi_role_set": ["_believe_v_1.ARG3"],
            "lo_role_set": ["_sleep_v_1.LBL"],
            "actual_hi_var": "h04",
            "actual_lo_var": "h011",
        }]

        test_overlap_hcons, test_gold_hcons, test_actual_hcons = sement_util.find_hcons_overlaps(gold_believe_cats_sleep_sement,
                                                                                            broken_believe_cats_sleep_sement)

        self.assertEqual(gold_overlap_hcons, test_overlap_hcons,
                         "Gold Overlap: {} \nActual Overlap: {}".format(gold_overlap_hcons, test_overlap_hcons))
        self.assertEqual(gold_gold_hcons, test_gold_hcons,
                         "Gold Gold: {} \nActual Gold:{}".format(gold_gold_hcons, test_gold_hcons))
        self.assertEqual(gold_actual_hcons, test_actual_hcons,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_actual_hcons, test_actual_hcons))

    def test_find_hcons_overlaps_gold_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_hcons_overlaps, uncollapsed_sement, collapsed_sement)

    def test_find_hcons_overlaps_actual_valueerror(self):
        uncollapsed_sement = self.decode_sement_string("a_tasty_cookie_sement.txt")
        collapsed_sement = self.decode_sement_string("a_tasty_cookie_sement_collapsed.txt")
        self.assertRaises(ValueError, sement_util.find_hcons_overlaps, collapsed_sement, uncollapsed_sement)

    def test__build_overlap_eqs_table(self):
        gold_eq_table = """Role Set                     Gold Var    Actual Var
        ---------------------------  ----------  ------------
        ['role0', 'role1', 'role2']  x1          x01
        ['role3', 'role4']           x2          x02"""

        mock_overlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
            "actual_var": "x01"
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
            "actual_var": "x02"
        }]

        test_overlap_eq_table = sement_util._build_overlap_eqs_table(mock_overlap_eqs)

        gold_chars = [c for c in gold_eq_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_overlap_eq_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_eq_table, test_overlap_eq_table))

    def test__build_nonoverlap_gold_eqs_table(self):
        gold_eq_table = """Role Set                     Gold Var
        ---------------------------  ----------
        ['role0', 'role1', 'role2']  x1
        ['role3', 'role4']           x2"""

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
        }]

        test_nonoverlap_eq_table = sement_util._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "gold")

        gold_chars = [c for c in gold_eq_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_nonoverlap_eq_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_eq_table, test_nonoverlap_eq_table))

    def test__build_nonoverlap_actual_eqs_table(self):
        gold_eq_table = """Role Set                     Actual Var
        ---------------------------  ----------
        ['role0', 'role1', 'role2']  x1
        ['role3', 'role4']           x2"""

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "actual_var": "x1",
        }, {
            "eq_set": ["role3", "role4"],
            "actual_var": "x2",
        }]

        test_nonoverlap_eq_table = sement_util._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "actual")

        gold_chars = [c for c in gold_eq_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_nonoverlap_eq_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                        "Gold Actual: {} \nActual Actual:{}".format(gold_eq_table, test_nonoverlap_eq_table))

    def test__build_overlap_hcons_table(self):
        gold_hcons_table = """Hi Role Set            Lo Role Set         Gold QEQ       Actual QEQ
        ---------------------  ------------------  -------------  ------------
        ['role0', 'role1']        ['role2', 'role3']    h0 qeq h1  h00 qeq h01
        ['role4']        ['role5']    h2 qeq h3  h02 qeq h03"""

        mock_overlap_eqs = [{
            "hi_role_set": ["role0", "role1"],
            "lo_role_set": ["role2", "role3"],
            "gold_hi_var": "h0",
            "gold_lo_var": "h1",
            "actual_hi_var": "h00",
            "actual_lo_var": "h01",
        }, {
            "hi_role_set": ["role4"],
            "lo_role_set": ["role5"],
            "gold_hi_var": "h2",
            "gold_lo_var": "h3",
            "actual_hi_var": "h02",
            "actual_lo_var": "h03",
        }]

        test_overlap_hcons_table = sement_util._build_overlap_hcons_table(mock_overlap_eqs)

        gold_chars = [c for c in gold_hcons_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_overlap_hcons_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_hcons_table, test_overlap_hcons_table))

    def test__build_nonoverlap_gold_hcons_table(self):
        gold_hcons_table = """Hi Role Set            Lo Role Set         Gold QEQ
        ---------------------  ------------------  -------------
        ['role0', 'role1']        ['role2', 'role3']    h0 qeq h1
        ['role4']        ['role5']    h2 qeq h3"""

        mock_overlap_eqs = [{
            "hi_role_set": ["role0", "role1"],
            "lo_role_set": ["role2", "role3"],
            "gold_hi_var": "h0",
            "gold_lo_var": "h1",
        }, {
            "hi_role_set": ["role4"],
            "lo_role_set": ["role5"],
            "gold_hi_var": "h2",
            "gold_lo_var": "h3",
        }]

        test_nonoverlap_hcons_table = sement_util._build_nonoverlap_hcons_table(mock_overlap_eqs, "gold")

        gold_chars = [c for c in gold_hcons_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_nonoverlap_hcons_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_hcons_table, test_nonoverlap_hcons_table))

    def test__build_nonoverlap_actual_hcons_table(self):
        gold_hcons_table = """Hi Role Set            Lo Role Set      Actual QEQ
        ---------------------  ------------------  -------------  ------------
        ['role0', 'role1']        ['role2', 'role3']    h00 qeq h01
        ['role4']        ['role5']    h02 qeq h03"""

        mock_overlap_eqs = [{
            "hi_role_set": ["role0", "role1"],
            "lo_role_set": ["role2", "role3"],
            "actual_hi_var": "h00",
            "actual_lo_var": "h01",
        }, {
            "hi_role_set": ["role4"],
            "lo_role_set": ["role5"],
            "actual_hi_var": "h02",
            "actual_lo_var": "h03",
        }]

        test_noverlap_hcons_table = sement_util._build_nonoverlap_hcons_table(mock_overlap_eqs, "actual")

        gold_chars = [c for c in gold_hcons_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_noverlap_hcons_table if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_hcons_table, test_noverlap_hcons_table))

    def test_build_isomorphism_report(self):
        gold_report = open(os.path.join(self.test_dir, "gold_isomorphism_report.txt")).read()

        report_sement1 = self.decode_sement_string("report_sement1.txt")
        report_sement2 = self.decode_sement_string("report_sement2.txt")

        test_report = sement_util.build_isomorphism_report(report_sement1, report_sement2)

        gold_chars = [c for c in gold_report if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_report if re.match(r'[^\s=-]', c)]

        self.assertEqual(gold_chars, test_chars,
                         "Gold Actual: {} \nActual Actual:{}".format(gold_report, test_report))