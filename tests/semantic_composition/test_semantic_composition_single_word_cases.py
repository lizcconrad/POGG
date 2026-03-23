import os
from pytest_cases import case

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs


class SingleWordConstructions:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.basic
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.adjective
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.determiner
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.named_entity
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.noun
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.preposition
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.pronoun
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.quantifier
        - pogg.semantic_composition.composition_mixins.single_word_constructions.SingleWordConstructionsMixin.verb

    GENERAL DESCRIPTION OF TEST CASES:
        Provide arguments for single word construction functions and the gold SEMENT
        test compares result of calling function to gold SEMENT

    """

    """
    CASES
        - manual_synopsis
            1. "neg"
            2. "neg" (w/ var props)
        - basic
            1. "cookie"
            2. "cookie" (w/ var props)
        - adjective 
            1. "tasty"
            2. "tasty" (w/ var props)
        - determiner
            1. "the"
            2. "the" (w/ var props)
        - named entity
            1. "Liz"
            2. "Liz" (w/ var props)
        - noun
            1. "cookie"
            2. "cookie" (w/ var props)
        - pronoun
            1. "she" (i.e. 3rd sg f)
        - quantifier
            1. "the"
            2. "the" (w/ var props)
        - verb
            1. "eat"
            2. "eat" (w/ var props)
    """

    @staticmethod
    @case(tags="manual_synopsis")
    def case_manual():
        neg_synopsis = {
            'roles': [
                {'name': 'ARG0',
                 'value': 'e'},
                {'name': 'ARG1',
                 'value': 'h'},
            ]
        }

        gold_sement_str = """[ TOP: h0
            INDEX: e1
            RELS: < [ neg LBL: h0 ARG0: e1 ARG1: h2 ] >
            SLOTS: < ARG1: h2 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "neg", None, neg_synopsis, gold_sement

    @staticmethod
    @case(tags="manual_synopsis")
    def case_manual_w_props():
        neg_synopsis = {
            'roles': [
                {'name': 'ARG0',
                 'value': 'e'},
                {'name': 'ARG1',
                 'value': 'h'},
            ]
        }

        gold_sement_str = """[ TOP: h0
            INDEX: e1 [ TENSE: tensed ]
            RELS: < [ neg LBL: h0 ARG0: e1 ARG1: h2 ] > 
            SLOTS: < ARG1: h2 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "neg", {"TENSE": "tensed"}, neg_synopsis, gold_sement

    @staticmethod
    @case(tags=["basic", "noun"])
    def case_cookie():
        gold_sement_str = """[  TOP: h2
            INDEX: x1
            RELS: < [ _cookie_n_1 LBL: h2 ARG0: x1 ] > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_cookie_n_1", None, gold_sement

    @staticmethod
    @case(tags=["basic", "noun"])
    def case_cookie_w_props():
        gold_sement_str = """[  TOP: h2
            INDEX: x1 [ x NUM: sg ]
            RELS: < [ _cookie_n_1 LBL: h2 ARG0: x1 ] > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_cookie_n_1", {"NUM": "sg"}, gold_sement

    @staticmethod
    @case(tags="adjective")
    def case_tasty():
        gold_sement_str = """[ TOP: h5
          INDEX: e3
          RELS: < [ _tasty_a_1 LBL: h5 ARG0: e3 ARG1: u4 ] >
          SLOTS: < ARG1: u4 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_tasty_a_1", None, gold_sement

    @staticmethod
    @case(tags="adjective")
    def case_tasty_w_props():
        gold_sement_str = """[ TOP: h5
          INDEX: e3 [ MOOD: indicative ]
          RELS: < [ _tasty_a_1 LBL: h5 ARG0: e3 ARG1: u4 ] >
          SLOTS: < ARG1: u4 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_tasty_a_1", {"MOOD": "indicative"}, gold_sement

    @staticmethod
    @case(tags="comparative_adjective")
    def case_tastier():
        gold_sement_str = """[ TOP: h0
                  INDEX: e2
                  RELS: <
                    [ more_comp LBL: h0 ARG0: i1 ARG1: e2 ARG2: u3]
                    [ _tasty_a_1 LBL: h0 ARG0: e2 ARG1: u6 ] >
                  SLOTS: < ARG1: u6 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_tasty_a_1", None, gold_sement

    @staticmethod
    @case(tags="comparative_adjective")
    def case_tastier_w_props():
        gold_sement_str = """[ TOP: h0
                  INDEX: e2 [ MOOD: indicative ]
                  RELS: <
                    [ more_comp LBL: h0 ARG0: i1 ARG1: e2 ARG2: u3]
                    [ _tasty_a_1 LBL: h0 ARG0: e2 ARG1: u6 ] >
                  SLOTS: < ARG1: u6 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_tasty_a_1", {"MOOD": "indicative"}, gold_sement

    @staticmethod
    @case(tags=["determiner", "quantifier"])
    def case_the():
        gold_sement_str = """[ TOP: h0
            INDEX: x1
            RELS: < [ _the_q LBL: h2 ARG0: x1 RSTR: h3 BODY: h4 ] >
            SLOTS: < ARG0: x1 RSTR: h3 BODY: h4 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_the_q", None, gold_sement

    @staticmethod
    @case(tags=["determiner", "quantifier"])
    def case_the_w_props():
        gold_sement_str = """[ TOP: h0
            INDEX: x1 [ IND: + ]
            RELS: < [ _the_q LBL: h2 ARG0: x1 RSTR: h3 BODY: h4 ] >
            SLOTS: < ARG0: x1 RSTR: h3 BODY: h4 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "_the_q", {"IND": "+"}, gold_sement

    @staticmethod
    @case(tags="number")
    def case_five():
        gold_sement_str = """[ TOP: h12
            INDEX: e11
            RELS: < [ card LBL: h12 ARG0: e11 ARG1: u13 CARG: "5" ] >
            SLOTS: < ARG1: u13 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "5", None, gold_sement

    @staticmethod
    @case(tags="number")
    def case_five_w_props():
        gold_sement_str = """[ TOP: h12
                INDEX: e11 [ TENSE: untensed ]
                RELS: < [ card LBL: h12 ARG0: e11 ARG1: u13 CARG: "5" ] > 
                SLOTS: < ARG1: u13 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "5", {"TENSE": "untensed"}, gold_sement

    @staticmethod
    @case(tags="preposition")
    def case_in():
        gold_sement_str = """[ TOP: h6
                  INDEX: e3
                  RELS: < [ _in_p_loc LBL: h6 ARG0: e3 ARG1: u4 ARG2: u5 ] >
                  SLOTS: < ARG1: u4 ARG2: u5 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        return "_in_p_loc", None, gold_sement

    @staticmethod
    @case(tags="preposition")
    def case_in_w_props():
        gold_sement_str = """[ TOP: h6
          INDEX: e3 [ MOOD: indicative ]
          RELS: < [ _in_p_loc LBL: h6 ARG0: e3 ARG1: u4 ARG2: u5 ] >
          SLOTS: < ARG1: u4 ARG2: u5 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        return "_in_p_loc", {"MOOD": "indicative"}, gold_sement

    @staticmethod
    @case(tags="pronoun")
    def case_pronoun():
        gold_sement_str = """[ TOP: h23
          INDEX: x19
          RELS: < [ pronoun_q LBL: h22 ARG0: x19 RSTR: h20 BODY: h21 ]
                  [ pron LBL: h18 ARG0: x17 ] >
          HCONS: < h20 qeq h18 >
          EQS: < x19 eq x17 >
          SLOTS: < BODY: h21 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return None, gold_sement

    @staticmethod
    @case(tags="pronoun")
    def case_pronoun_w_props():
        gold_sement_str = """[ TOP: h23
          INDEX: x19
          RELS: < [ pronoun_q LBL: h22 ARG0: x19 RSTR: h20 BODY: h21 ]
                  [ pron LBL: h18 ARG0: x17 [ x PERS: 3 NUM: sg GEND: f ] ] >
          HCONS: < h20 qeq h18 >
          EQS: < x19 eq x17 >
          SLOTS: < BODY: h21 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return {"NUM": "sg", "PERS": "3", "GEND": "f"}, gold_sement

    @staticmethod
    @case(tags="proper_noun")
    def case_liz():
        gold_sement_str = """[ TOP: h12
             INDEX: x11
             RELS: < [ named LBL: h12 ARG0: x11 CARG: "Liz" ] > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "Liz", None, gold_sement

    @staticmethod
    @case(tags="proper_noun")
    def case_liz_w_props():
        gold_sement_str = """[ TOP: h12
             INDEX: x11 [ PERS: 3 ]
             RELS: < [ named LBL: h12 ARG0: x11 CARG: "Liz" ] > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)
        return "Liz", {"PERS": "3"}, gold_sement

    @staticmethod
    @case(tags="verb")
    def case_eat():
        gold_sement_str = """[ TOP: h0
            INDEX: e1
            RELS: < [ _eat_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: i3 ] >
            SLOTS: < ARG1: i2 ARG2: i3 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        return "_eat_v_1", None, gold_sement

    @staticmethod
    @case(tags="verb")
    def case_eat_w_props():
        gold_sement_str = """[ TOP: h0
                    INDEX: e1 [ TENSE: pres ]
                    RELS: < [ _eat_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: i3 ] >
                    SLOTS: < ARG1: i2 ARG2: i3 > ]"""
        gold_sement = sementcodecs.decode(gold_sement_str)

        return "_eat_v_1", {"TENSE": "pres"}, gold_sement


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
    def case_tasty_cookie(base_constructions_test_dir, sem_alg_obj):
        gold_sement_str = os.path.join(base_constructions_test_dir, "tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        tasty = sem_alg_obj.create_base_SEMENT("_tasty_a_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return functor SEMENT first, then argument, then gold
        return tasty, cookie, gold_sement

    @staticmethod
    @case(tags="compound_noun")
    def case_sugar_cookie(base_constructions_test_dir, sem_alg_obj):
        gold_sement_str = os.path.join(base_constructions_test_dir, "sugar_cookie_sement.txt")
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        sugar = sem_alg_obj.create_base_SEMENT("_sugar_n_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return head SEMENT first, then non head, then gold
        return cookie, sugar, gold_sement

    @staticmethod
    @case(tags="quantify")
    def case_the_cookie(base_constructions_test_dir, sem_alg_obj):
        gold_sement_str = os.path.join(base_constructions_test_dir, "the_cookie_sement.txt")
        gold_sement = sementcodecs.decode(gold_sement_str)

        # assume semantic algebra works
        the = sem_alg_obj.create_base_SEMENT("_the_q")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # functor, argument, gold
        return the, cookie, gold_sement