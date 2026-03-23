import os
from pytest_cases import case, fixture
from delphin.mrs import HCons
# just assume sementcodecs works...
import pogg.my_delphin.sementcodecs as sementcodecs
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

@fixture
def cake_SEMENT():
    SEMENT_str = """[ TOP: h3
        INDEX: x4 [ NUM: sg ]
        RELS: < [ _cake_n_1 LBL: h3 ARG0: x4 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def cookie_SEMENT():
    SEMENT_str = """[ TOP: h1
        INDEX: x2 [ NUM: pl ]
        RELS: < [ _cookie_n_1 LBL: h1 ARG0: x2 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def unquantified_cookie_SEMENT():
    SEMENT_str = """[ TOP: h0
        INDEX: x1
        RELS: < [ _cookie_n_1 LBL: h0 ARG0: x1 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def quantified_cookie_SEMENT():
    SEMENT_str = """[ TOP: h6
        INDEX: x1
        RELS: <
            [ _udef_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
            [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
        EQS: < x1 eq x5 >
        SLOTS: < BODY: h3 >
        HCONS: < h2 qeq h4 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def tasty_cookie_SEMENT_collapsed():
    SEMENT_str = """[ TOP: h0
      INDEX: x4 [ NUM: sg PERS: 3 ]
      RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 [ TENSE: pres ] ARG1: x4 ]
              [ _cookie_n_1 LBL: h0 ARG0: x4 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def tasty_cookie_SEMENT_broken():
    SEMENT_str = """[ TOP: h03
      INDEX: x04 [ NUM: sg PERS: 3 ]
      RELS: < [ _tasty_a_1 LBL: h00 ARG0: e01 [ TENSE: untensed ] ARG1: x04 ]
              [ _cookie_n_1 LBL: h03 ARG0: x04 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def a_tasty_cookie_SEMENT():
    SEMENT_str = """[ TOP: h6
        INDEX: x4
        RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: u2 ]
              [ _cookie_n_1 LBL: h3 ARG0: x4 ]
              [ _a_q LBL: h5 ARG0: x6 RSTR: h7 BODY: h8 ] >
        EQS: < u2 eq x4 eq x6 h0 eq h3  >
        SLOTS: < BODY: h8 >
        HCONS: < h7 qeq h3 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def a_tasty_cookie_SEMENT_collapsed():
    SEMENT_str = """[ TOP: h6
      INDEX: x4
      RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
              [ _cookie_n_1 LBL: h0 ARG0: x4 ]
              [ _a_q LBL: h5 ARG0: x4 RSTR: h7 BODY: h8 ] >
      SLOTS: < BODY: h8 >
      HCONS: < h7 qeq h0 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def quantified_tasty_cookie_SEMENT():
    SEMENT_str = """[ TOP: h9
        INDEX: i8
        RELS: <
            [ _udef_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
            [ _cookie_n_1 LBL: h4 ARG0: x5 ]
            [ _tasty_a_1 LBL: h6 ARG0: e7 ARG1: i8 ] >
        SLOTS: < BODY: h3 >
        EQS: < x1 eq x5 eq i8 h4 eq h6 >
        HCONS: < h2 qeq h6 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def no_key_rel_SEMENT():
    SEMENT_str = """[ TOP: h0
      INDEX: x10
      RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 [ TENSE: pres ] ARG1: x4 ]
              [ _cookie_n_1 LBL: h0 ARG0: x4 ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def give_a_cookie_SEMENT_1():
    SEMENT_str = """[ TOP: h0101
        INDEX: e1101 [e NUM: sg]
        RELS: <
            [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13]
            [ _cookie_n_1 LBL: h6 ARG0: x7 ]
            [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ]
        >
        EQS: < x11 eq x7 eq i2 h0101 eq h0 e1 eq e1101 >
        SLOTS: < ARG2: u3 ARG3: i4 >
        HCONS: < h12 qeq h6 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def give_a_cookie_SEMENT_2():
    SEMENT_str = """[ TOP: h011
        INDEX: e111 [e NUM: sg]
        RELS: <
            [ _give_v_1 LBL: h011 ARG0: e111 ARG1: i211 ARG2: u311 ARG3: i411 ]
            [ _a_q LBL: h1011 ARG0: x1111 RSTR: h1211 BODY: h1311]
            [ _cookie_n_1 LBL: h611 ARG0: x711 ]
        >
        EQS: < x1111 eq x711 x711 eq i211 >
        SLOTS: < ARG2: u311 ARG3: i411 >
        HCONS: < h1211 qeq h611 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def give_a_cookie_SEMENT_wrong_top():
    SEMENT_str = """[ TOP: h611
        INDEX: e111 [e NUM: sg]
        RELS: <
            [ _give_v_1 LBL: h011 ARG0: e111 ARG1: i211 ARG2: u311 ARG3: i411 ]
            [ _a_q LBL: h1011 ARG0: x1111 RSTR: h1211 BODY: h1311]
            [ _cookie_n_1 LBL: h611 ARG0: x711 ]
        >
        EQS: < x1111 eq x711 x711 eq i2 >
        SLOTS: < ARG2: u311 ARG3: i411 >
        HCONS: < h1211 qeq h611 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def probably_sleeps_SEMENT():
    SEMENT_str = """[ TOP: h0
        INDEX: e4
        RELS: < [ _probable_a_1 LBL: h0 ARG0: i1 ARG1: u2 ]
            [ _sleep_v_1 LBL: h3 ARG0: e4 ARG1: i5 ] >
        EQS: < u2 eq h6 >
        HCONS: < u2 qeq h3 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def break_icons_eq_SEMENT():
    SEMENT_str = """[ TOP: h0
      INDEX: e1
      RELS: < [ _break_v_cause LBL: h0 ARG0: e2 ARG1: x3 ARG2: x4 ] >
      EQS: < e1 eq e2 >
      SLOTS: < ARG1: x3 ARG2: x4 >
      ICONS: < e2 topic x4 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def broken_window_SEMENT():
    SEMENT_str = """[ TOP: h6
      INDEX: e6
      RELS: < [ _window_n_1 LBL: h3 ARG0: x4 ]
              [ _break_v_cause LBL: h5 ARG0: e6 ARG1: x7 ARG2: x8 ] >
      EQS: < x4 eq x8 h0 eq h3  >
      SLOTS: < ARG1: x7 >
      ICONS: < e6 topic x8 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def old_broken_window_SEMENT():
    SEMENT_str = """[ TOP: h6
      INDEX: x4
      RELS: < [ _old_a_1 LBL: h0 ARG0: e1 ARG1: u2 ]
              [ _window_n_1 LBL: h3 ARG0: x4 ]
              [ _break_v_cause LBL: h5 ARG0: e6 ARG1: x7 ARG2: x8 ] >
      EQS: < u2 eq x4 eq x8 h0 eq h3  >
      SLOTS: < ARG1: x7 >
      ICONS: < e6 topic x8 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def believe_cats_sleep_SEMENT():
    SEMENT_str = """[ TOP: h0
      INDEX: e1
      RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
              [ udef_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
              [ _cat_n_1 LBL: h9 ARG0: x10 ]
              [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
      SLOTS: < ARG1: i2 ARG3: h4 >
      HCONS: < h7 qeq h9 u3 qeq h11 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def believe_cats_sleep_SEMENT_broken_hcons():
    SEMENT_str = """[ TOP: h00
      INDEX: e01
      RELS: < [ _believe_v_1 LBL: h00 ARG0: e01 ARG1: i02 ARG2: u03 ARG3: h04 ]
              [ udef_q LBL: h05 ARG0: x010 RSTR: h07 BODY: h08 ]
              [ _cat_n_1 LBL: h09 ARG0: x010 ]
              [ _sleep_v_1 LBL: h011 ARG0: e012 ARG1: x010 ] >
      SLOTS: < ARG1: i02 ARG2: u03 >
      HCONS: < h07 qeq h09 h04 qeq h011 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def old_broken_window_collapsed_SEMENT():
    SEMENT_str = """[ TOP: h6
      INDEX: x4
      RELS: < [ _old_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
              [ _window_n_1 LBL: h0 ARG0: x4 ]
              [ _break_v_cause LBL: h5 ARG0: e6 ARG1: x7 ARG2: x4 ] >
      SLOTS: < ARG1: x7 >
      ICONS: < e6 topic x4 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def liz_SEMENT():
    SEMENT_str = """[ TOP: h3
        INDEX: x4
        RELS: < [ named LBL: h3 ARG0: x4 CARG: "Liz" ] > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def icons_overlap_fake_SEMENT_1():
    SEMENT_str = """[ TOP: h0
      INDEX: e1
      RELS: < [ _verb_1 LBL: h0 ARG0: e1 ARG1: x2 ARG2: x3 ARG3: x4 ] >
      SLOTS: < ARG1: x2 ARG2: x3 ARG3: x4 >
      ICONS: < e1 topic x2 e1 topic x3 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def icons_overlap_fake_SEMENT_2():
    SEMENT_str = """[ TOP: h00
      INDEX: e01
      RELS: < [ _verb_1 LBL: h00 ARG0: e01 ARG1: x02 ARG2: x03 ARG3: x04 ] >
      SLOTS: < ARG1: x02 ARG2: x03 ARG3: x04 >
      ICONS: < e01 topic x02 e01 topic x04 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def report_SEMENT_1():
    SEMENT_str = """[ TOP: h0
      INDEX: e1 [ TENSE: pres ]
      RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
              [ _the_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
              [ _cat_n_1 LBL: h9 ARG0: x10 [ NUM: sg ] ]
              [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
      SLOTS: < ARG1: i2 ARG3: h4 >
      HCONS: < h7 qeq h9 u3 qeq h11 >
      ICONS: < e1 topic h7 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def report_SEMENT_2():
    SEMENT_str = """[ TOP: h00
      INDEX: e01 [ TENSE: pres ]
      RELS: < [ _believe_v_1 LBL: h00 ARG0: e01 ARG1: i02 ARG2: u03 ARG3: h04 [ PROP: x ] ]
              [ _the_q LBL: h05 ARG0: x010 RSTR: h07 BODY: h08 ]
              [ _cat_n_1 LBL: h09 ARG0: x010 ]
              [ _sleep_v_1 LBL: h011 ARG0: e012 ARG1: x010111 ] >
      SLOTS: < ARG1: i02 ARG2: u03 >
      HCONS: < h07 qeq h09 h04 qeq h011 >
      ICONS: < e01 topic h08 > ]"""
    return sementcodecs.decode(SEMENT_str)

@fixture
def report_SEMENT_3():
    SEMENT_str = """[ TOP: h00
      INDEX: e01 [ TENSE: pres ]
      RELS: < [ _believe_v_1 LBL: h00 ARG0: e01 ARG1: i02 ARG2: u03 ARG3: h04 ]
              [ _the_q LBL: h05 ARG0: x010 RSTR: h07 BODY: h08 ]
              [ _cat_n_1 LBL: h09 ARG0: x010 [ NUM: sg ] ]
              [ _sleep_v_1 LBL: h011 ARG0: e012 ARG1: x010 ] >
      SLOTS: < ARG1: i02 ARG3: h04 >
      HCONS: < h07 qeq h09 u03 qeq h011 >
      ICONS: < e01 topic h07 > ]"""
    return sementcodecs.decode(SEMENT_str)


class AddIntrinsicVariableProperty:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.add_intrinsic_variable_property

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a SEMENT and a variable property to add, assert that the variable has the property after function call
    """

    """
    SUCCESS CASES
        1. simple SEMENT
        2. simple SEMENT with property already set
    """

    @staticmethod
    def case_a_tasty_cookie(a_tasty_cookie_SEMENT):
        sement = a_tasty_cookie_SEMENT

        # the variable that changes here is x4
        gold_changed_var = "x4"

        return sement, "NUM", "sg", gold_changed_var

    @staticmethod
    def case_a_tasty_cookie_prop_set(tasty_cookie_SEMENT_collapsed):
        sement = tasty_cookie_SEMENT_collapsed

        # the variable that changes here is x4
        gold_changed_var = "x4"

        return sement, "NUM", "sg", gold_changed_var


class GetKeyRel:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_key_rel

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a SEMENT and the predicate that should be retrieved when getting key rel, assert result's predicate label matches
    """

    """
    SUCCESS CASES
        1. simple SEMENT
        
    FAILURE CASES:
        1. no key rel found
    """

    @staticmethod
    @case(tags="success")
    def case_a_tasty_cookie(a_tasty_cookie_SEMENT):
        sement = a_tasty_cookie_SEMENT

        gold_key_rel_pred = "_cookie_n_1"

        return sement, gold_key_rel_pred

    @staticmethod
    @case(tags="failure")
    def case_no_key_rel(no_key_rel_SEMENT):
        sement = no_key_rel_SEMENT
        return sement


class DuplicateSement:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.duplicate_sement

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a SEMENT to duplicate, the test should ensure the duplicate is a copy with separate object IDs
    """

    """
    SUCCESS CASES
        1. any SEMENT to duplicate
    """

    @staticmethod
    def case_a_tasty_cookie(a_tasty_cookie_SEMENT):
        sement = a_tasty_cookie_SEMENT
        return sement


class GroupEqualities:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.group_equalities

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
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.get_most_specified_variable

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
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.overwrite_eqs

    GENERAL DESCRIPTION OF TEST CASES:
        For these cases, the cases themselves will call the function to be tested.
        This is because for each case a specific set of variable identities must be confirmed, and that comes from the result SEMENT.
        So each case will return a list of lists of semantic roles that should be equal and the test will confirm that they are
    """

    """
    SUCCESS CASES
        1. simple test, "give a cookie"
        2. hcon_hi, whether the overwrite works when the hi-handle of a handle constraint is a member of an EQ (don't think this ever even happens but testing anyway) 
        3. hcon_lo, whether the overwrite works when the lo-handle of a handle constraint is a member of an EQ
        4. icon_left, whether the overwrite works when the left variable of an individual constraint is a member of an EQ 
        5. icon_right, whether the overwrite works when the right variable of an individual constraint is a member of an EQ 
        6. empty EQs list
        7. None EQs list 
    """

    @staticmethod
    @case(tags="eqs")
    def case_simple_eqs(give_a_cookie_SEMENT_1):
        sement = give_a_cookie_SEMENT_1

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)

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
    def case_simple_hcons(give_a_cookie_SEMENT_1):
        sement = give_a_cookie_SEMENT_1

        # for the sement "give a cookie" ...
        # a.ARG0 = cookie.ARG0 = give.ARG1
        # TOP = give.LBL
        # INDEX = give.ARG0
        # a.RSTR qeq cookie.LBL <-- this is what's being checked here

        # in this case gold_hcons should not change from what's already in the file
        # no member of any handle constraint is part of an eq so it should stay the same
        gold_hcons = sement.hcons
        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)

        hcons = new_sement.hcons
        return hcons, gold_hcons

    @staticmethod
    @case(tags="eqs")
    def case_hcon_lo_eqs(a_tasty_cookie_SEMENT):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        sement = a_tasty_cookie_SEMENT

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        # for the sement "a tasty cookie"
        # the following should all be true if the overwrite worked:
        # INDEX = a.ARG0 = cookie.ARG0 = tasty.ARG1
        # cookie.LBL = tasty.LBL
        # a.RSTR qeq cookie.LBL=tasty.LBL <-- check in hcons version of test

        for r in new_sement.rels:
            if r.predicate == "_a_q":
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
    def case_hcon_lo_hcons(a_tasty_cookie_SEMENT):
        # checks whether overwrite works when the lo-handle of a handle constraint is a member of an eq
        sement = a_tasty_cookie_SEMENT

        # for the sement "a tasty cookie"
        # the following should all be true if the overwrite worked:
        # TOP = a.LBL
        # INDEX = a.ARG0 = cookie.ARG0 = tasty.ARG1
        # cookie.LBL = tasty.LBL
        # a.RSTR qeq cookie.LBL=tasty.LBL <-- this is what's being checked here

        # gold_hcons written by hand by looking at a_tasty_cookie_sement.txt
        # h0 (from tasty) = h3 (from cookie) and get_most_specified_variable should return h0 because it starts with a sorted list
        gold_hcons = [HCons("h7", "qeq", "h0")]

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        hcons = new_sement.hcons

        return hcons, gold_hcons

    @staticmethod
    @case(tags="eqs")
    def case_hcon_hi_eqs(probably_sleeps_SEMENT):
        # checks whether overwrite works when the hi-handle of a handle constraint is a member of an eq
        # normally, hcon.hi should never be a memeber of an eq
        # but sometimes hcon.hi is of type u and must be constrained down to h so an "artificial" eq is added
        sement = probably_sleeps_SEMENT
        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)

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
    def case_hcon_hi_hcons(probably_sleeps_SEMENT):
        # checks whether overwrite works when the hi-handle of a handle constraint is a member of an eq
        # normally, hcon.hi should never be a memeber of an eq
        # but sometimes hcon.hi is of type u and must be constrained down to h so an "artificial" eq is added
        sement = probably_sleeps_SEMENT

        # for the sement "probably sleeps"
        # the following should all be true if the overwrite worked:
        # TOP = probable.LBL
        # INDEX = sleep.ARG0
        # probable.ARG1 = some made up h variable, add this to check because they should collapse too
        # probable.ARG1 qeq sleep.LBL <-- check in hcons version of test

        # gold_hcons written by hand by looking at probably_sleeps_sement.txt
        gold_hcons = [HCons("h6", "qeq", "h3")]

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        hcons = new_sement.hcons

        return hcons, gold_hcons

    @staticmethod
    @case(tags="icons")
    def case_icon_left_var(break_icons_eq_SEMENT):
        # checks whether overwrite works when the left variable of an individual constraint is a member of an eq
        sement = break_icons_eq_SEMENT

        # for the sement "break" where the INDEX and break.ARG0 are members of an EQ and there's an icon between break.ARG0 and break.ARG2
        # the following should all be true if the overwrite worked:
        # INDEX = break.ARG0

        # gold_icons written by hand by looking at break_artificial_icon_eq.txt
        gold_icons = [HCons("e1", "topic", "x4")]

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        icons = new_sement.icons

        return icons, gold_icons

    @staticmethod
    @case(tags="icons")
    def case_icon_right_var(broken_window_SEMENT):
        # checks whether overwrite works when the right variable of an individual constraint is a member of an eq
        sement = broken_window_SEMENT

        # for the sement "break" where the INDEX and break.ARG0 are members of an EQ and there's an icon between break.ARG0 and break.ARG2
        # the following should all be true if the overwrite worked:
        # _break_v_cause.ARG2 = _window_n_1.ARG0

        # gold_icons written by hand by looking at break_artificial_icon_eq.txt
        gold_icons = [HCons("e6", "topic", "x4")]

        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        icons = new_sement.icons

        return icons, gold_icons

    @staticmethod
    @case(tags="empty")
    def case_empty_eqs(unquantified_cookie_SEMENT):
        # when EQs are empty, original SEMENT and new SEMENT should match
        sement = unquantified_cookie_SEMENT
        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        return sement, new_sement

    @staticmethod
    @case(tags="empty")
    def case_none_eqs(unquantified_cookie_SEMENT):
        # when EQs are empty, original SEMENT and new SEMENT should match
        sement = unquantified_cookie_SEMENT

        # set eqs to None to account for that case
        sement.eqs = None
        new_sement = POGGSEMENTUtil.overwrite_eqs(sement)
        return sement, new_sement

    @staticmethod
    @case(tags="preservation")
    def case_preservation(a_tasty_cookie_SEMENT):
        # ensure that the EQs in the original SEMENT are not altered
        sement = a_tasty_cookie_SEMENT

        eqs_pre_rewrite = sement.eqs.copy()

        # return eqs as saved before rewrite and the eqs on the original object after rewrite
        return eqs_pre_rewrite, sement.eqs


class CheckIfQuantified:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.check_if_quantified

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
    def case_noun(quantified_cookie_SEMENT):
        sement = quantified_cookie_SEMENT
        return sement

    @staticmethod
    @case(tags="true")
    def case_noun_phrase(quantified_tasty_cookie_SEMENT):
        # note this SEMENT is a little bungled, the INDEX is tasty.ARG1 when really it would be cookie.ARG0
        # but check_if_quantified checks whether the INDEX "or something eq to the INDEX" is the ARG0 of an EP with RSTR
        # so this captures the "or something eq to the INDEX"
        # which may never happen... but just in case
        sement = quantified_tasty_cookie_SEMENT
        return sement

    @staticmethod
    @case(tags="false")
    def case_unquantified_noun(unquantified_cookie_SEMENT):
        sement = unquantified_cookie_SEMENT
        return sement


class IsSementIsomorphic:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.is_sement_isomorphic

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
    def case_give_a_cookie_true(give_a_cookie_SEMENT_1, give_a_cookie_SEMENT_2):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        sement_1 = give_a_cookie_SEMENT_1
        sement_2 = give_a_cookie_SEMENT_2
        return sement_1, sement_2, True

    @staticmethod
    def case_give_a_cookie_false(give_a_cookie_SEMENT_1, give_a_cookie_SEMENT_wrong_top):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        # but also the TOP is incorrect in this one (refers to LBL of 'cookie' not 'give')
        # so they should not be isomorphic
        sement_1 = give_a_cookie_SEMENT_1
        sement_2 = give_a_cookie_SEMENT_wrong_top
        return sement_1, sement_2, False


class CreateVariableRolesDict:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_variable_roles_dict

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
    def case_collapsed_a_tasty_cookie(a_tasty_cookie_SEMENT_collapsed):
        sement = a_tasty_cookie_SEMENT_collapsed

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
    def case_uncollapsed_a_tasty_cookie(a_tasty_cookie_SEMENT):
        sement = a_tasty_cookie_SEMENT
        return sement


class CreateHConsList:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_hcons_list

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
    def case_collapsed_a_tasty_cookie(a_tasty_cookie_SEMENT_collapsed):
        sement = a_tasty_cookie_SEMENT_collapsed

        gold_hcons_list = [{
            "hi_role_set": ["_a_q.RSTR"],
            "lo_role_set": ["_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            "hi_var": "h7",
            "lo_var": "h0",
            "relation": "qeq"
        }]

        return sement, gold_hcons_list

    @staticmethod
    @case(tags="failure")
    def case_uncollapsed_a_tasty_cookie(a_tasty_cookie_SEMENT):
        sement = a_tasty_cookie_SEMENT
        return sement


class CreateIConsList:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.create_icons_list

    GENERAL DESCRIPTION OF TEST CASES:
        "create_icons_list" makes a list of the individual constraints where each entry is a dictionary detailing which variables are members of the constraint
        For the tests, provide a SEMENT and the expected icons list, test should compare result to expected dictionary
    """

    """
        SUCCESS CASES
            1. collapsed "old broken window" SEMENT 

        FAILURE CASES
            1. uncollapsed SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        """

    @staticmethod
    @case(tags="success")
    def case_collapsed_old_broken_window(old_broken_window_collapsed_SEMENT):
        sement = old_broken_window_collapsed_SEMENT

        gold_icons_list = [{
            "left_role_set": ["_break_v_cause.ARG0"],
            "right_role_set": [
                "INDEX",
                "_break_v_cause.ARG2",
                "_old_a_1.ARG1",
                "_window_n_1.ARG0"],
            "left_var": "e6",
            "right_var": "x4",
            "relation": "topic"
        }]

        return sement, gold_icons_list

    @staticmethod
    @case(tags="failure")
    def case_uncollapsed_old_broken_window(old_broken_window_SEMENT):
        sement = old_broken_window_SEMENT
        return sement


class FindSlotOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_slot_overlaps

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
    def case_two_dissimilar_sements(believe_cats_sleep_SEMENT, believe_cats_sleep_SEMENT_broken_hcons):
        gold_sement = believe_cats_sleep_SEMENT
        actual_sement = believe_cats_sleep_SEMENT_broken_hcons

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
    def case_gold_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT
        actual_sement = a_tasty_cookie_SEMENT_collapsed
        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT_collapsed
        actual_sement = a_tasty_cookie_SEMENT
        return gold_sement, actual_sement


class FindVarEqOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_var_eq_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_eq_overlaps" produces three lists:
            1. list of semantic role identity sets that match between two SEMENTs
            2. list of semantic role identity sets that match between two SEMENTs but have different variable properties
            3. list of semantic role identity sets found only in the "gold" SEMENT
            4. list of semantic role identity sets found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_eq_overlaps to the expected
    """

    """
    SUCCESS CASES
        1. two SEMENTs with different sets of variable role identities to ensure there's something in each list to check 
        2. two SEMENTs with a "named" predicate to test the CARG special case 

    FAILURE CASES
        1. uncollapsed gold SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        2. uncollapsed actual SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_two_dissimilar_sements(tasty_cookie_SEMENT_collapsed, tasty_cookie_SEMENT_broken):
        gold_sement = tasty_cookie_SEMENT_collapsed
        actual_sement = tasty_cookie_SEMENT_broken

        gold_overlap_eqs = [{
            "eq_set": ["INDEX", "_cookie_n_1.ARG0", "_tasty_a_1.ARG1"],
            "gold_var": "x4",
            "actual_var": "x04",
            "properties": { "NUM": "sg", "PERS": "3" }
        }]

        gold_prop_eqs = [{
            "eq_set": ["_tasty_a_1.ARG0"],
            "gold_var": "e1",
            "actual_var": "e01",
            "gold_properties": {"TENSE": "pres"},
            "actual_properties": {"TENSE": "untensed"}
        }]

        gold_gold_eqs = [{
            "eq_set": ["TOP", "_cookie_n_1.LBL", "_tasty_a_1.LBL"],
            "gold_var": "h0",
            "gold_properties": {}
        }]

        gold_actual_eqs = [{
            "eq_set": ["TOP", "_cookie_n_1.LBL"],
            "actual_var": "h03",
            "actual_properties": {}
        }, {
            "eq_set": ["_tasty_a_1.LBL"],
            "actual_var": "h00",
            "actual_properties": {}
        }]

        return gold_sement, actual_sement, gold_overlap_eqs, gold_prop_eqs, gold_gold_eqs, gold_actual_eqs

    @staticmethod
    @case(tags="success")
    def case_name(liz_SEMENT):
        gold_sement = liz_SEMENT
        actual_sement = liz_SEMENT

        gold_overlap_eqs = [
        {
            "eq_set": ["INDEX", "named.ARG0"],
            "gold_var": "x4",
            "actual_var": "x4",
            "properties": {}
        },
        {
            "eq_set": ["TOP", "named.LBL"],
            "gold_var": "h3",
            "actual_var": "h3",
            "properties": {}
        },
        {
            "eq_set": ["named.CARG"],
            "gold_var": "Liz",
            "actual_var": "Liz",
            "properties": {}
        }]

        return gold_sement, actual_sement, gold_overlap_eqs, [], [], []

    @staticmethod
    @case(tags="failure")
    def case_gold_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT
        actual_sement = a_tasty_cookie_SEMENT_collapsed
        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT_collapsed
        actual_sement = a_tasty_cookie_SEMENT
        return gold_sement, actual_sement


class FindHConsOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_hcons_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_hcons_overlaps" produces three lists:
            1. list of handle constraints that match between two SEMENTs
            2. list of handle constraints found only in the "gold" SEMENT
            3. list of handle constraints found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_hcons_overlaps to the expected
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
    def case_two_dissimilar_sements(believe_cats_sleep_SEMENT, believe_cats_sleep_SEMENT_broken_hcons):
        gold_sement = believe_cats_sleep_SEMENT

        # this SEMENT doesn't include handle constraint between _believe_v_1.ARG2 and _sleep_v_1.LBL
        actual_sement = believe_cats_sleep_SEMENT_broken_hcons

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
    def case_gold_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT
        actual_sement = a_tasty_cookie_SEMENT_collapsed
        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT_collapsed
        actual_sement = a_tasty_cookie_SEMENT
        return gold_sement, actual_sement


class FindIConsOverlaps:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.find_icons_overlaps

    GENERAL DESCRIPTION OF TEST CASES:
        "find_icons_overlaps" produces three lists:
            1. list of individual constraints that match between two SEMENTs
            2. list of individual constraints found only in the "gold" SEMENT
            3. list of individual constraints found only in the "actual" SEMENT

        Provide two SEMENTs, the expected values for the three lists, and compare result of find_icons_overlaps to the expected
    """

    """
    SUCCESS CASES
        1. two SEMENTs with different sets of individual constraints to ensure there's something in each list to check 

    FAILURE CASES
        1. uncollapsed gold SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
        2. uncollapsed actual SEMENT; to avoid nondeterminism in the selected representative variable, reject such SEMENTS from this function 
    """

    @staticmethod
    @case(tags="success")
    def case_two_dissimilar_sements(icons_overlap_fake_SEMENT_1, icons_overlap_fake_SEMENT_2):
        gold_sement = icons_overlap_fake_SEMENT_1
        actual_sement = icons_overlap_fake_SEMENT_2

        gold_overlap_icons = [{
            "left_role_set": ["INDEX", "_verb_1.ARG0"],
            "right_role_set": ["_verb_1.ARG1"],
            "gold_left_var": "e1",
            "gold_right_var": "x2",
            "actual_left_var": "e01",
            "actual_right_var": "x02",
            "relation": "topic"
        }]

        gold_gold_icons = [{
            "left_role_set": ["INDEX", "_verb_1.ARG0"],
            "right_role_set": ["_verb_1.ARG2"],
            "gold_left_var": "e1",
            "gold_right_var": "x3",
            "gold_relation": "topic"
        }]

        gold_actual_icons = [{
            "left_role_set": ["INDEX", "_verb_1.ARG0"],
            "right_role_set": ["_verb_1.ARG3"],
            "actual_left_var": "e01",
            "actual_right_var": "x04",
            "actual_relation": "topic"
        }]

        return gold_sement, actual_sement, gold_overlap_icons, gold_gold_icons, gold_actual_icons

    @staticmethod
    @case(tags="failure")
    def case_gold_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT
        actual_sement = a_tasty_cookie_SEMENT_collapsed
        return gold_sement, actual_sement

    @staticmethod
    @case(tags="failure")
    def case_actual_uncollapsed(a_tasty_cookie_SEMENT, a_tasty_cookie_SEMENT_collapsed):
        gold_sement = a_tasty_cookie_SEMENT_collapsed
        actual_sement = a_tasty_cookie_SEMENT
        return gold_sement, actual_sement


class BuildTable:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_slots_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_slots_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_eqs_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_eqs_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_hcons_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_hcons_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_overlap_icons_table
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil._build_nonoverlap_icons_table

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
        7. _build_overlap_icons_table
        8. _build_nonoverlap_icons_table  
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

        test_overlap_table = POGGSEMENTUtil._build_overlap_slots_table(mock_overlap_slots)

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

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_slots_table(mock_nonoverlap_slots, "gold")

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

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_slots_table(mock_nonoverlap_slots, "actual")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_overlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_overlap_table.txt")).read()

        mock_overlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
            "actual_var": "x01",
            "properties": { "NUM": "sg" }
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
            "actual_var": "x02",
            "properties": {}
        }]

        test_overlap_table = POGGSEMENTUtil._build_overlap_eqs_table(mock_overlap_eqs)

        return gold_table, test_overlap_table

    @staticmethod
    def case_gold_nonoverlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_gold_nonoverlap_table.txt")).read()

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "gold_var": "x1",
            "gold_properties": { "NUM": "sg" }
        }, {
            "eq_set": ["role3", "role4"],
            "gold_var": "x2",
            "gold_properties": {}
        }]

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "gold")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_actual_nonoverlap_eqs_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "eqs_actual_nonoverlap_table.txt")).read()

        mock_nonoverlap_eqs = [{
            "eq_set": ["role0", "role1", "role2"],
            "actual_var": "x1",
            "actual_properties": {"NUM": "sg"}
        }, {
            "eq_set": ["role3", "role4"],
            "actual_var": "x2",
            "actual_properties": {}
        }]

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_eqs_table(mock_nonoverlap_eqs, "actual")

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

        test_overlap_table = POGGSEMENTUtil._build_overlap_hcons_table(mock_overlap_hcons)

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

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_hcons_table(mock_nonoverlap_hcons, "gold")

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

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_hcons_table(mock_nonoverlap_hcons, "actual")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_overlap_icons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "icons_overlap_table.txt")).read()

        mock_overlap_icons = [{
            "left_role_set": ["role0", "role1"],
            "right_role_set": ["role2", "role3"],
            "gold_left_var": "e1",
            "gold_right_var": "x2",
            "actual_left_var": "e01",
            "actual_right_var": "x02",
            "relation": "topic"
        }, {
            "left_role_set": ["role4"],
            "right_role_set": ["role5"],
            "gold_left_var": "e3",
            "gold_right_var": "x4",
            "actual_left_var": "e03",
            "actual_right_var": "x04",
            "relation": "topic"
        }]

        test_overlap_table = POGGSEMENTUtil._build_overlap_icons_table(mock_overlap_icons)

        return gold_table, test_overlap_table

    @staticmethod
    def case_gold_nonoverlap_icons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "icons_gold_nonoverlap_table.txt")).read()

        mock_nonoverlap_icons = [{
            "left_role_set": ["role0", "role1"],
            "right_role_set": ["role2", "role3"],
            "gold_left_var": "e1",
            "gold_right_var": "x2",
            "gold_relation": "topic"
        }, {
            "left_role_set": ["role4"],
            "right_role_set": ["role5"],
            "gold_left_var": "e3",
            "gold_right_var": "x4",
            "gold_relation": "topic"
        }]

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_icons_table(mock_nonoverlap_icons, "gold")

        return gold_table, test_nonoverlap_table

    @staticmethod
    def case_actual_nonoverlap_icons_table(sement_util_test_dir):
        gold_table = open(os.path.join(sement_util_test_dir, "icons_actual_nonoverlap_table.txt")).read()

        mock_nonoverlap_icons = [{
            "left_role_set": ["role0", "role1"],
            "right_role_set": ["role2", "role3"],
            "actual_left_var": "e1",
            "actual_right_var": "x2",
            "actual_relation": "topic"
        }, {
            "left_role_set": ["role4"],
            "right_role_set": ["role5"],
            "actual_left_var": "e3",
            "actual_right_var": "x4",
            "actual_relation": "topic"
        }]

        test_nonoverlap_table = POGGSEMENTUtil._build_nonoverlap_icons_table(mock_nonoverlap_icons, "actual")

        return gold_table, test_nonoverlap_table


class BuildIsomorphismReport:
    """
    FUNCTION BEING TESTED:
        - pogg.semantic_composition.sement_util.POGGSEMENTUtil.build_isomorphism_report

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
    def case_partially_discrepant_sements(sement_util_test_dir, report_SEMENT_1, report_SEMENT_2):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report.txt")).read()
        report_sement_1 = report_SEMENT_1
        report_sement_2 = report_SEMENT_2
        return report_sement_1, report_sement_2, gold_report

    @staticmethod
    def case_fully_discrepant_sements(sement_util_test_dir, cookie_SEMENT, cake_SEMENT):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report_no_consistencies.txt")).read()
        report_sement_1 = cookie_SEMENT
        report_sement_2 = cake_SEMENT
        return report_sement_1, report_sement_2, gold_report

    @staticmethod
    def case_no_discrepancies(sement_util_test_dir, report_SEMENT_1, report_SEMENT_3):
        gold_report = open(os.path.join(sement_util_test_dir, "gold_isomorphism_report_no_discrepancies.txt")).read()
        report_sement_1 = report_SEMENT_1
        report_sement_2 = report_SEMENT_3
        return report_sement_1, report_sement_2, gold_report

