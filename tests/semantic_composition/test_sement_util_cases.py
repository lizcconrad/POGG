import os
from pytest_cases import case
from delphin.mrs import HCons
# just assume sementcodecs works...
import pogg.my_delphin.sementcodecs as sementcodecs
from pogg.semantic_composition import sement_util


class DuplicateSement:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.duplicate_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a SEMENT to duplicate, the test should ensure the duplicate is a copy with separate object IDs
    """

    """
    SUCCESS CASES
        1. any SEMENT to duplicate
    """

    @staticmethod
    def case_a_tasty_cookie(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement


class GroupEqualities:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.group_equalities

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a set of "ungrouped" equalities (e.g. x1=x2 and x1=x3) and the gold grouping (x1=x2=x3) and compare result to gold grouping
    """

    @staticmethod
    def case_equalities():
        eqs = [("x1", "x2"), ("x3", "x4"), ("x1", "x4"), ("x5", "x6")]

        # result of grouping should equal this
        gold_groups = [{"x1", "x2", "x3", "x4"}, {"x5", "x6"}]

        return eqs, gold_groups


class GetMostSpecifiedVariable:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.get_most_specified_variable

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a list of variables and the "most specified" (i.e. most specific typed) one, ensure the result of get_most_specified_variable matches answer
    """

    """
    SUCCESS CASES
        1. list of variables
        2. set of variables
    """

    @staticmethod
    def case_list_of_variables():
        # x3 is most specific
        return ["u1", "i2", "x3"], "x3"

    @staticmethod
    def case_set_of_variables():
        # x3 is most specific
        return {"u1", "i2", "x3"}, "x3"


class OverwriteEqs:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.overwrite_eqs

    GENERAL DESCRIPTION OF TEST CASES:
        For these cases, the cases themselves will call the function to be tested.
        This is because for each case a specific set of variable identities must be confirmed, and that comes from the result SEMENT.
        So each case will return a list of lists of semantic roles that should be equal and the test will confirm that they are
    """

    """
    SUCCESS CASES
        1. simple test, "give a cookie"
        2. hcon_hi, whether the overwrite works when the hi-handle of a handle constraint is a member of an EQ (don't think this ever even happens but testing anyway) 
        3. hcon_lo, whether the overwrite works wehn the lo-handle of a handle constraint is a member of an EQ 
        4. empty EQs list
        5. None EQs list 
    """

    @staticmethod
    @case(tags="eqs")
    def case_simple_eqs(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "give_a_cookie_1_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        new_sement = sement_util.overwrite_eqs(sement)

        # for the sement "give a cookie" ...
        # a.ARG0 = cookie.ARG0 = give.ARG1
        # TOP = give.LBL
        # INDEX = give.ARG0
        # (a.RSTR qeq cookie.LBL) <-- check in hcons version of test

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_arg0 = r.args['ARG0']
            else:
                give_lbl = r.label
                give_arg0 = r.args['ARG0']
                give_arg1 = r.args['ARG1']

        eqs = [
            (a_arg0, cookie_arg0, give_arg1),
            (new_sement.top, give_lbl),
            (new_sement.index, give_arg0)
        ]
        return eqs

    @staticmethod
    @case(tags="hcons")
    def case_simple_hcons(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "give_a_cookie_1_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        # for the sement "give a cookie" ...
        # a.ARG0 = cookie.ARG0 = give.ARG1
        # TOP = give.LBL
        # INDEX = give.ARG0
        # a.RSTR qeq cookie.LBL <-- this is what's being checked here

        # in this case gold_hcons should not change from what's already in the file
        # no member of any handle constraint is part of an eq so it should stay the same
        gold_hcons = sement.hcons
        new_sement = sement_util.overwrite_eqs(sement)

        hcons = new_sement.hcons
        return hcons, gold_hcons

    @staticmethod
    @case(tags="eqs")
    def case_hcon_lo_eqs(sement_util_test_dir):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        new_sement = sement_util.overwrite_eqs(sement)
        # for the sement "a tasty cookie"
        # the following should all be true if the overwrite worked:
        # INDEX = a.ARG0 = cookie.ARG0 = tasty.ARG1
        # cookie.LBL = tasty.LBL
        # a.RSTR qeq cookie.LBL=tasty.LBL <-- check in hcons version of test

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_lbl = r.label
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_lbl = r.label
                cookie_arg0 = r.args['ARG0']
            else:
                tasty_lbl = r.label
                tasty_arg1 = r.args['ARG1']


        eqs = [
            (new_sement.index, a_arg0, cookie_arg0, tasty_arg1),
            (cookie_lbl, tasty_lbl)
        ]
        return eqs


    @staticmethod
    @case(tags="hcons")
    def case_hcon_lo_hcons(sement_util_test_dir):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        # for the sement "a tasty cookie"
        # the following should all be true if the overwrite worked:
        # TOP = a.LBL
        # INDEX = a.ARG0 = cookie.ARG0 = tasty.ARG1
        # cookie.LBL = tasty.LBL
        # a.RSTR qeq cookie.LBL=tasty.LBL <-- this is what's being checked here

        # gold_hcons written by hand by looking at a_tasty_cookie_sement.txt
        # h0 (from tasty) = h3 (from cookie) and get_most_specified_variable should return h0 because it starts with a sorted list
        gold_hcons = [HCons("h7", "qeq", "h0")]

        new_sement = sement_util.overwrite_eqs(sement)
        hcons = new_sement.hcons

        return hcons, gold_hcons

    @staticmethod
    @case(tags="eqs")
    def case_hcon_hi_eqs(sement_util_test_dir):
        # checks whether overwrite works when the hi-handle of a handle constraint is a member of an eq
        # normally, hcon.hi should never be a memeber of an eq
        # but sometimes hcon.hi is of type u and must be constrained down to h so an "artificial" eq is added

        sement_file = os.path.join(sement_util_test_dir, "probably_sleeps_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        new_sement = sement_util.overwrite_eqs(sement)

        # for the sement "probably sleeps"
        # the following should all be true if the overwrite worked:
        # TOP = probable.LBL
        # INDEX = sleep.ARG0
        # probable.ARG1 = some made up h variable, add this to check because they should collapse too
        # probable.ARG1 qeq sleep.LBL <-- check in hcons version of test


        for r in new_sement.rels:
            if r.predicate == "_probable_a_1":
                probable_lbl = r.label
                probable_arg1 = r.args['ARG1']
            else:
                sleep_arg0 = r.args['ARG0']

        # hard coded from looking at probably_sleeps_sement.txt
        made_up_h = "h6"

        eqs = [
            (new_sement.top, probable_lbl),
            (new_sement.index, sleep_arg0),
            (probable_arg1, made_up_h)
        ]
        return eqs

    @staticmethod
    @case(tags="hcons")
    def case_hcon_hi_hcons(sement_util_test_dir):
        # checks whether overwrite works when the hi-handle of a handle constraint is a member of an eq
        # normally, hcon.hi should never be a memeber of an eq
        # but sometimes hcon.hi is of type u and must be constrained down to h so an "artificial" eq is added
        sement_file = os.path.join(sement_util_test_dir, "probably_sleeps_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        # for the sement "probably sleeps"
        # the following should all be true if the overwrite worked:
        # TOP = probable.LBL
        # INDEX = sleep.ARG0
        # probable.ARG1 = some made up h variable, add this to check because they should collapse too
        # probable.ARG1 qeq sleep.LBL <-- check in hcons version of test

        # gold_hcons written by hand by looking at a_tasty_cookie_sement.txt
        # h0 (from tasty) = h3 (from cookie) and get_most_specified_variable should return h0 because it starts with a sorted list
        gold_hcons = [HCons("h6", "qeq", "h3")]

        new_sement = sement_util.overwrite_eqs(sement)
        hcons = new_sement.hcons

        return hcons, gold_hcons

    @staticmethod
    @case(tags="empty")
    def case_empty_eqs(sement_util_test_dir):
        # when EQs are empty, original SEMENT and new SEMENT should match
        sement_file = os.path.join(sement_util_test_dir, "unquantified_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        new_sement = sement_util.overwrite_eqs(sement)
        return sement, new_sement

    @staticmethod
    @case(tags="empty")
    def case_none_eqs(sement_util_test_dir):
        # when EQs are empty, original SEMENT and new SEMENT should match
        sement_file = os.path.join(sement_util_test_dir, "unquantified_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        # set eqs to None to account for that case
        sement.eqs = None
        new_sement = sement_util.overwrite_eqs(sement)
        return sement, new_sement

    @staticmethod
    @case(tags="preservation")
    def case_preservation(sement_util_test_dir):
        # ensure that the EQs in the original SEMENT are not altered
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        eqs_pre_rewrite = sement.eqs.copy()

        new_sement = sement_util.overwrite_eqs(sement)

        # return eqs as saved before rewrite and the eqs on the original object after rewrite
        return eqs_pre_rewrite, sement.eqs

class CheckIfQuantified:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.check_if_quantified

    GENERAL DESCRIPTION OF TEST CASES:
        Just return the SEMENT and have the test check if it's quantified and whether the result is as expected :)
    """

    """
    TRUE CASES
        1. noun
        2. noun phrase
        
    FALSE CASES
        1. unquantified noun 
    """

    @staticmethod
    @case(tags="true")
    def case_noun(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "quantified_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement

    @staticmethod
    @case(tags="true")
    def case_noun_phrase(sement_util_test_dir):
        # note this SEMENT is a little bungled, the INDEX is tasty.ARG1 when really it would be cookie.ARG0
        # but check_if_quantified checks whether the INDEX "or something eq to the INDEX" is the ARG0 of an EP with RSTR
        # so this captures the "or something eq to the INDEX"
        # which may never happen... but just in case
        sement_file = os.path.join(sement_util_test_dir, "quantified_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement

    @staticmethod
    @case(tags="false")
    def case_unquantified_noun(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "unquantified_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement


class IsSementIsomorphic:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.is_sement_isomorphic

    GENERAL DESCRIPTION OF TEST CASES:
        Return two SEMENTs, the expected result of isomorphism comparison and compare the actual result of comparison to the expected result
    """

    """
    TRUE CASES
        1. two versions of "give a cookie"

    FALSE CASES
        1. one correct version of "give a cookie" and one broken version of "give a cookie"
    """

    @staticmethod
    def case_give_a_cookie_true(sement_util_test_dir):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        sement_file_1 = os.path.join(sement_util_test_dir, "give_a_cookie_1_sement.txt")
        sement_1 = sementcodecs.decode(open(sement_file_1).read())

        sement_file_2 = os.path.join(sement_util_test_dir, "give_a_cookie_2_sement.txt")
        sement_2 = sementcodecs.decode(open(sement_file_2).read())

        return sement_1, sement_2, True

    @staticmethod
    def case_give_a_cookie_false(sement_util_test_dir):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        # but also the TOP is incorrect in this one (refers to LBL of 'cookie' not 'give')
        # so they should not be isomorphic
        sement_file_1 = os.path.join(sement_util_test_dir, "give_a_cookie_1_sement.txt")
        sement_1 = sementcodecs.decode(open(sement_file_1).read())

        sement_file_2 = os.path.join(sement_util_test_dir, "give_a_cookie_wrong_top_sement.txt")
        sement_2 = sementcodecs.decode(open(sement_file_2).read())

        return sement_1, sement_2, False

class CreateVariableRolesDict:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.create_variable_roles_dict

    GENERAL DESCRIPTION OF TEST CASES:
        "create_variable_roles_dict" makes a dictionary where the key is a variable and the value is a list of semantic roles that variable fills
        For the tests, provide a SEMENT and the expected variable roles dictionary, test should compare result to expected dictionary
    """

    """
    SUCCESS CASES
        1. collapsed "a tasty cookie" SEMENT 

    FAILURE CASES
        1. uncollapsed SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_collapsed_a_tasty_cookie(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        gold_roles_dict = {
            'h0': ["_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            'e1': ["_tasty_a_1.ARG0"],
            'x4': ["INDEX", "_a_q.ARG0", "_cookie_n_1.ARG0", "_tasty_a_1.ARG1"],
            'h5': ["_a_q.LBL"],
            'h6': ["TOP"],
            'h7': ["_a_q.RSTR"],
            'h8': ["_a_q.BODY"]
        }

        return sement, gold_roles_dict

    @staticmethod
    @case(tags="failure")
    def case_uncollapsed_a_tasty_cookie(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement

class CreateHConsList:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.create_hcons_list

    GENERAL DESCRIPTION OF TEST CASES:
        "create_hcons_list" makes a list of the handle constraints where each entry is a dictionary detailing which predicate labels are members of the hi and lo handles
        hi handles should never have more than one member in their role set, but lo might, e.g. "tasty cookie" where tasty and cookie share a label
        For the tests, provide a SEMENT and the expected hcons list, test should compare result to expected dictionary
    """

    """
    SUCCESS CASES
        1. collapsed "a tasty cookie" SEMENT 

    FAILURE CASES
        1. uncollapsed SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_collapsed_a_tasty_cookie(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        sement = sementcodecs.decode(open(sement_file).read())

        gold_hcons_list = [{
            "hi_role_set": ["_a_q.RSTR"],
            "lo_role_set": ["_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            "hi_var": "h7",
            "lo_var": "h0",
        }]

        return sement, gold_hcons_list

    @staticmethod
    @case(tags="failure")
    def case_uncollapsed_a_tasty_cookie(sement_util_test_dir):
        sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        sement = sementcodecs.decode(open(sement_file).read())
        return sement

class FindSlotOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.find_slot_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_slot_overlaps" produces three lists:
            1. list of unfilled semantic slots that match between two SEMENTs
            2. list of unfilled semantic slots found only in the "gold" SEMENT
            3. list of unfilled semantic slots found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_slot_overlaps to the expected
    """

    """
    SUCCESS CASES
        1. two SEMENTs with different sets of slots to ensure there's something in each list to check 

    FAILURE CASES
        1. uncollapsed gold SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        2. uncollapsed actual SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_two_dissimilar_sements(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "believe_cats_sleep_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "believe_cats_sleep_broken_hcons_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        gold_overlap_slots = [{
            "slot": ['_believe_v_1.ARG1'],
            "gold_var": "i2",
            "actual_var": "i02"
        }]

        gold_gold_slots = [{
            "slot": ['_believe_v_1.ARG3'],
            "gold_var": "h4",
        }]

        gold_actual_slots = [{
            "slot": ['_believe_v_1.ARG2'],
            "actual_var": "u03",
        }]

        return gold_sement, actual_sement, gold_overlap_slots, gold_gold_slots, gold_actual_slots

    @staticmethod
    @case(tags="failure")
    def case_gold_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

class FindVarEqOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.find_var_eq_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_slot_overlaps" produces three lists:
            1. list of semantic role identity sets that match between two SEMENTs
            2. list of semantic role identity sets found only in the "gold" SEMENT
            3. list of semantic role identity sets found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_slot_overlaps to the expected
    """

    """
    SUCCESS CASES
        1. two SEMENTs with different sets of variable role identities to ensure there's something in each list to check 

    FAILURE CASES
        1. uncollapsed gold SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        2. uncollapsed actual SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_two_dissimilar_sements(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "tasty_cookie_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "tasty_cookie_broken_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

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

        return gold_sement, actual_sement, gold_overlap_eqs, gold_gold_eqs, gold_actual_eqs

    @staticmethod
    @case(tags="failure")
    def case_gold_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

class FindHConsOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.find_hcons_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_hcons_overlaps" produces three lists:
            1. list of handle constraints that match between two SEMENTs
            2. list of handle constraints found only in the "gold" SEMENT
            3. list of handle constraints found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_slot_overlaps to the expected
    """

    """
    SUCCESS CASES
        1. two SEMENTs with different sets of handle constraints to ensure there's something in each list to check 

    FAILURE CASES
        1. uncollapsed gold SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        2. uncollapsed actual SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_two_dissimilar_sements(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "believe_cats_sleep_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # this SEMENT doesn't include handle constraint between _believe_v_1.ARG2 and _sleep_v_1.LBL
        actual_sement_file = os.path.join(sement_util_test_dir, "believe_cats_sleep_broken_hcons_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

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

        return gold_sement, actual_sement, gold_overlap_hcons, gold_gold_hcons, gold_actual_hcons

    @staticmethod
    @case(tags="failure")
    def case_gold_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(sement_util_test_dir):
        gold_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement_collapsed.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        actual_sement_file = os.path.join(sement_util_test_dir, "a_tasty_cookie_sement.txt")
        actual_sement = sementcodecs.decode(open(actual_sement_file).read())

        return gold_sement, actual_sement

class BuildTable:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.sement_util._build_overlap_slots_table
        - pogg.semantic_composition.sement_util._build_nonoverlap_slots_table
        - pogg.semantic_composition.sement_util._build_overlap_eqs_table
        - pogg.semantic_composition.sement_util._build_nonoverlap_eqs_table
        - pogg.semantic_composition.sement_util._build_overlap_hcons_table
        - pogg.semantic_composition.sement_util._build_nonoverlap_hcons_table

    GENERAL DESCRIPTION OF TEST CASES:
        Build the table given some data and provide the expected table, the built table, and have the test compare the strings
    """

    """
    SUCCESS CASES
        1. _build_overlap_slots_table
        2. _build_nonoverlap_slots_table
        3. _build_ovelerlap_eqs_table
        4. _build_nonoverlap_eqs_table
        5. _build_overlap_hcons_table
        6. _build_nonoverlap_hcons_table  
    """

    @staticmethod
    def case_overlap_slots_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "slots_overlap_table.txt")).read()

        mock_overlap_slots = [{
            "slot": ["slot1"],
            "gold_var": "x1",
            "actual_var": "x01"
        }, {
            "slot": ["slot2"],
            "gold_var": "x2",
            "actual_var": "x02"
        }]

        test_overlap_table = sement_util._build_overlap_slots_table(mock_overlap_slots)

        return gold_table, test_overlap_table

    @staticmethod
    def case_gold_nonoverlap_slots_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "slots_gold_nonoverlap_table.txt")).read()

        mock_nonoverlap_slots = [{
            "slot": ["slot1"],
            "gold_var": "x1",
        }, {
            "slot": ["slot2"],
            "gold_var": "x2",
        }]

        test_nonoverlap_table = sement_util._build_nonoverlap_slots_table(mock_nonoverlap_slots, "gold")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_actual_nonoverlap_slots_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "slots_actual_nonoverlap_table.txt")).read()

        mock_nonoverlap_slots = [{
            "slot": ["slot1"],
            "actual_var": "x1",
        }, {
            "slot": ["slot2"],
            "actual_var": "x2",
        }]

        test_nonoverlap_table = sement_util._build_nonoverlap_slots_table(mock_nonoverlap_slots, "actual")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_overlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_overlap_table.txt")).read()

        mock_overlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
            "actual_var": "x01"
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
            "actual_var": "x02"
        }]

        test_overlap_table = sement_util._build_overlap_eqs_table(mock_overlap_eqs)

        return gold_table, test_overlap_table

    @staticmethod
    def case_gold_nonoverlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_gold_nonoverlap_table.txt")).read()

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
        }]

        test_nonoverlap_table = sement_util._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "gold")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_actual_nonoverlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_actual_nonoverlap_table.txt")).read()

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "actual_var": "x1",
        }, {
            "eq_set": ["role3", "role4"],
            "actual_var": "x2",
        }]

        test_nonoverlap_table = sement_util._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "actual")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_overlap_hcons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "hcons_overlap_table.txt")).read()

        mock_overlap_hcons = [{
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

        test_overlap_table = sement_util._build_overlap_hcons_table(mock_overlap_hcons)

        return gold_table, test_overlap_table

    @staticmethod
    def case_gold_nonoverlap_hcons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "hcons_gold_nonoverlap_table.txt")).read()

        mock_nonoverlap_hcons = [{
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

        test_nonoverlap_table = sement_util._build_nonoverlap_hcons_table(mock_nonoverlap_hcons, "gold")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_actual_nonoverlap_hcons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "hcons_actual_nonoverlap_table.txt")).read()

        mock_nonoverlap_hcons = [{
            "hi_role_set": ["role0", "role1"],
            "lo_role_set": ["role2", "role3"],
            "actual_hi_var": "h0",
            "actual_lo_var": "h1",
        }, {
            "hi_role_set": ["role4"],
            "lo_role_set": ["role5"],
            "actual_hi_var": "h2",
            "actual_lo_var": "h3",
        }]

        test_nonoverlap_table = sement_util._build_nonoverlap_hcons_table(mock_nonoverlap_hcons, "actual")

        return gold_table, test_nonoverlap_table


class BuildIsomorphismReport:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.build_isomorphism_report

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to build an isomorphism report with and the expected report; test compares resulting report to expected
    """

    """
    SUCCESS CASES
        1. two different SEMENTs with overlapping information
        2. two SEMENTs with no overlapping information
        3. two identical SEMENTs
    """

    @staticmethod
    def case_paritally_discrepant_sements(sement_util_test_dir):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report.txt")).read()

        report_file_1 = os.path.join(sement_util_test_dir, "report_sement1.txt")
        report_sement_1 = sementcodecs.decode(open(report_file_1).read())

        report_file_2 = os.path.join(sement_util_test_dir, "report_sement2.txt")
        report_sement_2 = sementcodecs.decode(open(report_file_2).read())

        return report_sement_1, report_sement_2, gold_report

    @staticmethod
    def case_fully_discrepant_sements(sement_util_test_dir):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report_no_consistencies.txt")).read()

        report_file_1 = os.path.join(sement_util_test_dir, "cookie_sement.txt")
        report_sement_1 = sementcodecs.decode(open(report_file_1).read())

        report_file_2 = os.path.join(sement_util_test_dir, "cake_sement.txt")
        report_sement_2 = sementcodecs.decode(open(report_file_2).read())

        return report_sement_1, report_sement_2, gold_report

    @staticmethod
    def case_no_discrepancies(sement_util_test_dir):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report_no_discrepancies.txt")).read()

        report_file_1 = os.path.join(sement_util_test_dir, "report_sement1.txt")
        report_sement_1 = sementcodecs.decode(open(report_file_1).read())

        report_file_2 = os.path.join(sement_util_test_dir, "report_sement3.txt")
        report_sement_2 = sementcodecs.decode(open(report_file_2).read())

        return report_sement_1, report_sement_2, gold_report

