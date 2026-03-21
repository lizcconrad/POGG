import os
from delphin import mrs
from pytest_cases import case, fixture

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
    @case(tags=["basic", "noun"])
    def case_cookie(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_cookie_n_1", None, gold_sement

    @staticmethod
    @case(tags=["basic", "noun"])
    def case_cookie_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "cookie_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_cookie_n_1", {"NUM": "sg"}, gold_sement

    @staticmethod
    @case(tags="adjective")
    def case_tasty(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "tasty_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_tasty_a_1", None, gold_sement

    @staticmethod
    @case(tags="adjective")
    def case_tasty_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "tasty_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_tasty_a_1", {"MOOD": "indicative"}, gold_sement

    @staticmethod
    @case(tags=["determiner", "quantifier"])
    def case_the(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "the_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_the_q", None, gold_sement

    @staticmethod
    @case(tags=["determiner", "quantifier"])
    def case_the_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "the_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_the_q", {"IND": "+"}, gold_sement

    @staticmethod
    @case(tags="named_entity")
    def case_liz(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "liz_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "Liz", None, gold_sement

    @staticmethod
    @case(tags="named_entity")
    def case_liz_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "liz_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "Liz", {"PERS": "3"}, gold_sement

    @staticmethod
    @case(tags="preposition")
    def case_in(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "in_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_in_p_loc", None, gold_sement

    @staticmethod
    @case(tags="preposition")
    def case_in_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "in_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_in_p_loc", {"MOOD": "indicative"}, gold_sement

    @staticmethod
    @case(tags="pronoun")
    def case_pronoun(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "generic_pronoun_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return None, gold_sement

    @staticmethod
    @case(tags="pronoun")
    def case_pronoun_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "3_sg_f_pronoun_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return {"NUM": "sg", "PERS": "3", "GEND": "f"}, gold_sement

    @staticmethod
    @case(tags="verb")
    def case_eat(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "eat_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_eat_v_1", None, gold_sement

    @staticmethod
    @case(tags="verb")
    def case_eat_w_props(base_constructions_test_dir):
        gold_sement_file = os.path.join(base_constructions_test_dir, "eat_sement_w_var_props.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

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
        gold_sement_file = os.path.join(base_constructions_test_dir, "tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assume semantic algebra works
        tasty = sem_alg_obj.create_base_SEMENT("_tasty_a_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return functor SEMENT first, then argument, then gold
        return tasty, cookie, gold_sement

    @staticmethod
    @case(tags="compound_noun")
    def case_sugar_cookie(base_constructions_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(base_constructions_test_dir, "sugar_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assume semantic algebra works
        sugar = sem_alg_obj.create_base_SEMENT("_sugar_n_1")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # return head SEMENT first, then non head, then gold
        return cookie, sugar, gold_sement

    @staticmethod
    @case(tags="quantify")
    def case_the_cookie(base_constructions_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(base_constructions_test_dir, "the_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assume semantic algebra works
        the = sem_alg_obj.create_base_SEMENT("_the_q")
        cookie = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        # functor, argument, gold
        return the, cookie, gold_sement