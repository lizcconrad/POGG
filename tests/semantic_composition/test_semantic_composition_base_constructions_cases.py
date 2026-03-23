import os
from pytest_cases import case

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs


class BaseConstructions:
    """
        FUNCTIONS BEING TESTED:
            - pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.prenominal_adjective
            - pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.compound_noun
            - pogg.semantic_composition.composition_mixins.base_constructions.BaseConstructionsMixin.quantify


        GENERAL DESCRIPTION OF TEST CASES:
            Provide two SEMENTs to use for composition and the expected gold result SEMENT
            test compares result of calling function to gold SEMENT

            These tests assume that the tests from semantic_algebra
        """

    """
    CASES

        - prenominal_adjective
            1. "tasty cookie"
        - compound_noun 
            1. "sugar cookie"
        - quantify
            1. "the cookie"
    """

    @staticmethod
    @case(tags="prenominal_adjective")
    def case_tasty_cookie(sem_alg_obj):
        gold_sement_str = """[ TOP: h0
            INDEX: x2
            RELS: <
                [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x2 ]
                [ _cookie_n_1 LBL: h3 ARG0: x4 ]
            >
            EQS: < x2 eq x4 h0 eq h3 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        tasty = sem_alg_obj.create_base_SEMENT("_tasty_a_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return functor SEMENT first, then argument, then gold
        return tasty, cookie, gold_sement

    @staticmethod
    @case(tags="compound_noun")
    def case_sugar_cookie(sem_alg_obj):
        gold_sement_str = """[ TOP: h2
            INDEX: x11
            RELS: <
                [ _sugar_n_1 LBL: h0 ARG0: x1 ]
                [ compound LBL: h2 ARG0: e3 [ PROG: - ] ARG1: x4 ARG2: x5 ]
                [ udef_q LBL: h6 ARG0: x7 RSTR: h8 BODY: h9 ]
                [ _cookie_n_1 LBL: h10 ARG0: x11 ] >
            EQS: < x1 eq x7 x5 eq x1 x4 eq x11 h2 eq h10 >
            HCONS: < h8 qeq h0 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        sugar = sem_alg_obj.create_base_SEMENT("_sugar_n_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return head SEMENT first, then non head, then gold
        return cookie, sugar, gold_sement

    @staticmethod
    @case(tags="quantify")
    def case_the_cookie(sem_alg_obj):
        gold_sement_str = """[ TOP: h6
            INDEX: x1
            RELS: <
                [ _the_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                [ _cookie_n_1 LBL: h4 ARG0: x5 ]
            >
            SLOTS: < BODY: h3 >
            EQS: < x1 eq x5 >
            HCONS: < h2 qeq h4 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        the = sem_alg_obj.create_base_SEMENT("_the_q")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # functor, argument, gold
        return the, cookie, gold_sement