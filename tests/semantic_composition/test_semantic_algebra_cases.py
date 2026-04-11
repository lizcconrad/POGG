import os
from delphin import mrs
from pytest_cases import fixture

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs


class GetSlots:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra._get_slots

    GENERAL DESCRIPTION OF TEST CASES:
        Provide an EP and the slots to be found from it, compare result of _get_slots on the EP to the expected slots
    """

    """
    SUCCESS CASES
        1. verb EP
        2. quantifier EP
    """

    @staticmethod
    def case_verb():
        # create an EP
        give_EP = mrs.EP("_give_v_1", "h0", {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})

        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_slots = {"ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}

        return give_EP, golden_slots

    @staticmethod
    def case_quantifier():
        # create an EP
        give_EP = mrs.EP("_the_q", "h0", {'ARG0': 'x1', 'RSTR': 'h2', 'BODY': 'h3'})

        #  _the_q : ARG0 x, RSTR h, BODY h.
        # result of pogg_config.concretize("_the_q") should match golden_args
        golden_slots = {"ARG0": "x1", "RSTR": "h2", "BODY": "h3"}

        return give_EP, golden_slots


class CreateBaseSement:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_base_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide arguments to be passed into create_base_sement and the expected result; test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. _give_v_1
        2. _the_q
    """

    @staticmethod
    def case_give():
        # base SEMENT for _give_v1
        SEMENT_str = """[ TOP: h0
              INDEX: e1 [ TENSE: pres ]
              RELS: < [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ] >
              SLOTS: < ARG1: i2 ARG2: u3 ARG3: i4 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)
        return "_give_v_1", {"TENSE": "pres"},  gold_SEMENT

    @staticmethod
    def case_the():
        SEMENT_str = """[ TOP: h0
              INDEX: x1
              RELS: < [ _the_q LBL: h2 ARG0: x1 RSTR: h3 BODY: h4 ] >
              SLOTS: < ARG0: x1 RSTR: h3 BODY: h4 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)
        return "_the_q", {},  gold_SEMENT


class CreateCARGSement:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.create_CARG_SEMENT

    GENERAL DESCRIPTION OF TEST CASES:
        Provide arguments to be passed into create_CARG_SEMENT and the expected result; test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "Liz"
        2. "five""
    """

    @staticmethod
    def case_liz(semantic_algebra_test_dir):
        SEMENT_str = """[ TOP: h0
          INDEX: x1
          RELS: < [ named LBL: h0 ARG0: x1 CARG: "Liz" ] > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        return "named", "Liz",  gold_SEMENT

    @staticmethod
    def case_five(semantic_algebra_test_dir):
        SEMENT_str = """[ TOP: h0
          INDEX: i1
          RELS: < [ card LBL: h0 ARG0: i1 ARG1: u2 CARG: "5" ] >
          SLOTS: < ARG1: u2 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        return "card", "5",  gold_SEMENT


class OpNonScopalArgumentHook:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_argument_hook_slots

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_non_scopal_argument_hook_slots, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "tasty cookie"
        2. "extremely tasty"
    """

    @staticmethod
    def case_tasty_cookie(semantic_algebra_test_dir, sem_alg_obj):
        SEMENT_str = """[ TOP: h3
          INDEX: x4
          RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: u2 ]
                  [ _cookie_n_1 LBL: h3 ARG0: x4 ] >
          EQS: < u2 eq x4 h0 eq h3 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        # assumes create_base_SEMENT works
        tasty_sement = sem_alg_obj.create_base_SEMENT("_tasty_a_1")
        cookie_sement = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        return tasty_sement, cookie_sement, "ARG1", gold_SEMENT

    @staticmethod
    def case_extremely_tasty(semantic_algebra_test_dir, sem_alg_obj):
        SEMENT_str = """[ TOP: h3
          INDEX: e4
          RELS: < [ _extremely_x_deg LBL: h0 ARG0: e1 ARG1: u2 ]
                  [ _tasty_a_1 LBL: h3 ARG0: e4 ARG1: u5 ] >
          EQS: < u2 eq e4 h0 eq h3 >
          SLOTS: < ARG1: u5 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        # assumes create_base_SEMENT works
        extremely_sement = sem_alg_obj.create_base_SEMENT("_extremely_x_deg")
        tasty_sement = sem_alg_obj.create_base_SEMENT("_tasty_a_1")

        return extremely_sement, tasty_sement, "ARG1", gold_SEMENT


class OpNonScopalFunctorHook:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_functor_hook_slots

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_non_scopal_functor_hook_slots, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "eat the cookie"
    """

    @staticmethod
    def case_tasty_cookie(sem_alg_obj):
        gold_SEMENT_str = """[ TOP: h7
          INDEX: e8
          RELS: < [ _eat_v_1 LBL: h7 ARG0: e8 ARG1: i9 ARG2: i10 ]
                  [ _the_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                  [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
          EQS: < x1 eq x5 x5 eq i10 >
          SLOTS: < ARG1: i9 >
          HCONS: < h2 qeq h4 > ]"""
        gold_SEMENT = sementcodecs.decode(gold_SEMENT_str)

        the_cookie_SEMENT_str = """[ TOP: h6
          INDEX: x1
          RELS: < [ _the_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                  [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
          EQS: < x1 eq x5 >
          SLOTS: < BODY: h3 >
          HCONS: < h2 qeq h4 > ]"""
        the_cookie_sement = sementcodecs.decode(the_cookie_SEMENT_str)

        # assumes create_base_SEMENT works
        eat_sement = sem_alg_obj.create_base_SEMENT("_eat_v_1")

        return eat_sement, the_cookie_sement, "ARG2", gold_SEMENT


class OpScopalQuantifier:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_quantifier

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_scopal_quantifier and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "the cookie"
    """

    @staticmethod
    def case_the_cookie(sem_alg_obj):
        SEMENT_str = """[ TOP: h6
                  INDEX: x1
                  RELS: < [ _the_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                          [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
                  EQS: < x1 eq x5 >
                  SLOTS: < BODY: h3 >
                  HCONS: < h2 qeq h4 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        # assumes create_base_SEMENT works
        the_sement = sem_alg_obj.create_base_SEMENT("_the_q")
        cookie_sement = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        return the_sement, cookie_sement, gold_SEMENT


class OpScopalArgumentIndex:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_argument_index_slots

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_scopal_argument_index_slots, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "probably sleeps"
    """

    @staticmethod
    def case_probably_sleeps(sem_alg_obj):
        SEMENT_str = """[ TOP: h0
          INDEX: e4
          RELS: <
            [ _probable_a_1 LBL: h0 ARG0: e1 ARG1: u2 ]
            [ _sleep_v_1 LBL: h3 ARG0: e4 ARG1: i5 ] >
          HCONS: <  u2 qeq h3 >]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        # assumes create_base_SEMENT works
        probable_sement = sem_alg_obj.create_base_SEMENT("_probable_a_1")
        sleep_sement = sem_alg_obj.create_base_SEMENT("_sleep_v_1")

        return probable_sement, sleep_sement, "ARG1", gold_SEMENT


class OpScopalFunctorIndex:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_scopal_functor_index, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "believe cats sleep"
    """

    @staticmethod
    def case_believe_cats_sleep(sem_alg_obj):
        SEMENT_str = """[ TOP: h0
          INDEX: e1
          RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                  [ udef_q LBL: h5 ARG0: x6 RSTR: h7 BODY: h8 ]
                  [ _cat_n_1 LBL: h9 ARG0: x10 ]
                  [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: i13 ] >
          EQS: < x10 eq i13 x10 eq x6 >
          SLOTS: < ARG1: i2 ARG3: h4 >
          HCONS: < h7 qeq h9 u3 qeq h11 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        udef_cat_sleep_SEMENT_str = """[ TOP: h117
            INDEX: e118
            RELS: <
                [ udef_q LBL: h110 ARG0: x111 RSTR: h112 BODY: h113 ]
                [ _cat_n_1 LBL: h114 ARG0: x115 ]
                [ _sleep_v_1 LBL: h117 ARG0: e118 ARG1: x119 ]
            >
            EQS: < x111 eq x115 x111 eq x119 >
            SLOTS: < BODY: h113 >
            HCONS: < h112 qeq h114 > ]"""
        udef_cat_sleep_sement = sementcodecs.decode(udef_cat_sleep_SEMENT_str)

        # assumes create_base_SEMENT works
        believe_sement = sem_alg_obj.create_base_SEMENT("_believe_v_1")

        return believe_sement, udef_cat_sleep_sement, "ARG2", gold_SEMENT


class OpScopalFunctorIndexArgumentSlots:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_functor_index_argument_slots

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_scopal_functor_index_argument_slots, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "did not sleep"
    """

    @staticmethod
    def case_did_not_sleep(sem_alg_obj):
        SEMENT_str = """[ TOP: h0
              INDEX: e1
              RELS: <
                [ neg LBL: h0 ARG0: e1 ARG1: h2 ]
                [ _sleep_v_1 LBL: h3 ARG0: e4 ARG1: i5 ] >
              HCONS: <  h2 qeq h3 >
              SLOTS: < ARG1: i5 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        neg_synopsis = {
            'roles': [
                {'name': 'ARG0',
                 'value': 'e'},
                {'name': 'ARG1',
                 'value': 'h'},
            ]
        }

        # assumes create_base_SEMENT works
        neg_sement = sem_alg_obj.create_base_SEMENT("neg", None, neg_synopsis)
        sleep_sement = sem_alg_obj.create_base_SEMENT("_sleep_v_1")

        return neg_sement, sleep_sement, "ARG1", gold_SEMENT


class PrepareForGeneration:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.prepare_for_generation

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a SEMENT to be passed into prepare_for_generation, and a gold version that is already prepared for generation
        test should compare result of call with gold SEMENT that's been prepared
    """

    """
    SUCCESS CASES
        1. unquantified noun
        2. quantified noun 
        3. verb
        4. probably sleeps (the ARG1 of probably needs to be constrained to type "h")
        5. unquantified cardinal number 
        6. already has GTOP 
    """

    @staticmethod
    def case_unquantified_noun():
        SEMENT_str = """[ TOP: h10
            INDEX: e1
            RELS: <
                [ unknown LBL: h0 ARG0: e1 ARG: x4 ]
                [ def_udef_a_q LBL: h3 ARG0: x4 RSTR: h5 BODY: h6 ]
                [ _cookie_n_1 LBL: h7 ARG0: x4 ] >
            HCONS: < h5 qeq h7 h10 qeq h0 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        cookie_SEMENT_str = """[ TOP: h0
            INDEX: x1
            RELS: < [ _cookie_n_1 LBL: h0 ARG0: x1 ] > ]"""
        cookie_sement = sementcodecs.decode(cookie_SEMENT_str)

        return cookie_sement, gold_SEMENT

    @staticmethod
    def case_quantified_noun():
        SEMENT_str = """[ TOP: h10
            INDEX: e1
            RELS: <
                [ unknown LBL: h0 ARG0: e1 ARG: x4 ]
                [ def_udef_a_q LBL: h3 ARG0: x4 RSTR: h5 BODY: h6 ]
                [ _cookie_n_1 LBL: h7 ARG0: x4 ] >
            HCONS: < h5 qeq h7 h10 qeq h0 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        quant_cookie_SEMENT_str = """[ TOP: h6
            INDEX: x1
            RELS: <
                [ def_udef_a_Q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
            EQS: < x1 eq x5 >
            SLOTS: < BODY: h3 >
            HCONS: < h2 qeq h4 > ]"""
        quant_cookie_sement = sementcodecs.decode(quant_cookie_SEMENT_str)

        return quant_cookie_sement, gold_SEMENT

    @staticmethod
    def case_verb():
        SEMENT_str = """[ TOP: h0
            INDEX: e1
            RELS: < [ _eat_v_1 LBL: h2 ARG0: e1 ARG1: i2  ARG2: i3 ] >
            HCONS: < h0 qeq h2 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        eat_SEMENT_str = """[ TOP: h2
            INDEX: e1
            RELS: < [ _eat_v_1 LBL: h2 ARG0: e1 ARG1: i2  ARG2: i3 ] > ]"""
        eat_sement = sementcodecs.decode(eat_SEMENT_str)

        return eat_sement, gold_SEMENT

    @staticmethod
    def case_probably_sleeps():
        SEMENT_str = """[ TOP: h7
          INDEX: e4
          RELS: <
            [ _probable_a_1 LBL: h0 ARG0: e1 ARG1: h6 ]
            [ _sleep_v_1 LBL: h3 ARG0: e4 ARG1: i5 ] >
          HCONS: <  h6 qeq h3 h7 qeq h0 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        probably_sleeps_SEMENT_str = """[ TOP: h0
          INDEX: e4
          RELS: <
            [ _probable_a_1 LBL: h0 ARG0: e1 ARG1: u2 ]
            [ _sleep_v_1 LBL: u3 ARG0: e4 ARG1: i5 ] >
          HCONS: <  u2 qeq u3 > ]"""
        probably_sleeps_sement = sementcodecs.decode(probably_sleeps_SEMENT_str)

        return probably_sleeps_sement, gold_SEMENT

    @staticmethod
    def case_unquantified_number():
        SEMENT_str = """[ TOP: h10
                INDEX: e1
                RELS: <
                    [ unknown LBL: h0 ARG0: e1 ARG: x4 ]
                    [ number_q LBL: h3 ARG0: x4 RSTR: h5 BODY: h6 ]
                    [ card LBL: h7 ARG0: x4 CARG: "5" ] >
                HCONS: < h5 qeq h7 h10 qeq h0 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        number_SEMENT_str = """[ TOP: h0
                INDEX: x1
                RELS: < [ card LBL: h0 ARG0: x1 CARG: "5" ] > ]"""
        cookie_sement = sementcodecs.decode(number_SEMENT_str)

        return cookie_sement, gold_SEMENT

    @staticmethod
    def case_has_gtop():
        SEMENT_str = """[ TOP: h10
                    INDEX: e1
                    RELS: <
                        [ unknown LBL: h0 ARG0: e1 ARG: x4 ]
                        [ def_udef_a_q LBL: h3 ARG0: x4 RSTR: h5 BODY: h6 ]
                        [ _cookie_n_1 LBL: h7 ARG0: x4 ] >
                    HCONS: < h5 qeq h7 h10 qeq h0 > ]"""
        gold_SEMENT = sementcodecs.decode(SEMENT_str)

        return gold_SEMENT, gold_SEMENT
