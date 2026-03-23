from pytest_cases import fixture, parametrize_with_cases
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_semantic_composition_single_word_cases import *
from .test_semantic_composition_base_constructions_cases import *


class TestSingleWordConstructions:
    """
    Tests functions that produce single word constructions from the SemanticComposition class
    """

    @staticmethod
    @parametrize_with_cases("predicate, var_props, synopsis, gold_SEMENT", cases=SingleWordConstructions, has_tag="manual_synopsis")
    def test_manual_synopsis(predicate, var_props, synopsis, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.manual_synopsis(predicate, synopsis, var_props)

        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="basic")
    def test_basic(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.basic(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="adjective")
    def test_adjective(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.adjective(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="comparative_adjective")
    def test_comparative_adjective(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.comparative_adjective(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="determiner")
    def test_determiner(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.determiner(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="noun")
    def test_noun(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.noun(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("digit, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="number")
    def test_number(digit, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.number(digit, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="preposition")
    def test_preposition(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.preposition(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="pronoun")
    def test_pronoun(var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.pronoun(var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("name, var_props, gold_SEMENT", cases=SingleWordConstructions,
                            has_tag="proper_noun")
    def test_proper_noun(name, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.proper_noun(name, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT,
                                                   test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="quantifier")
    def test_quantifier(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.quantifier(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_SEMENT", cases=SingleWordConstructions, has_tag="verb")
    def test_verb(predicate, var_props, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.verb(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)


class TestBaseConstructions:
    """
    Tests functions that perform semantic composition between two SEMENTs from the SemanticComposition class
    """

    @staticmethod
    @parametrize_with_cases("functor_SEMENT, argument_SEMENT, gold_SEMENT", cases=BaseConstructions,
                            has_tag="prenominal_adjective")
    def test_prenominal_adjective(functor_SEMENT, argument_SEMENT, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.prenominal_adjective(functor_SEMENT, argument_SEMENT)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("head_noun_sement, non_head_noun_sement, gold_SEMENT", cases=BaseConstructions,
                            has_tag="compound_noun")
    def test_compound_noun(head_noun_sement, non_head_noun_sement, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.compound_noun(head_noun_sement, non_head_noun_sement)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)

    @staticmethod
    @parametrize_with_cases("quantifier_sement, quantified_sement, gold_SEMENT", cases=BaseConstructions,
                            has_tag="quantify")
    def test_quantify(quantifier_sement, quantified_sement, gold_SEMENT, sem_comp_obj):
        test_sement = sem_comp_obj.quantify(quantifier_sement, quantified_sement)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_SEMENT, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_SEMENT, test_sement)


