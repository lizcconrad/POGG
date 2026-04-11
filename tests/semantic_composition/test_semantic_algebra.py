from pytest_cases import fixture, parametrize_with_cases
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_semantic_algebra_cases import *


class TestAlgebraFunctions:
    """
    Tests functions included in the semantic algebra
    """

    @staticmethod
    @parametrize_with_cases("ep, gold_slots", cases=GetSlots)
    def test__get_slots(ep, gold_slots, sem_alg_obj):
        test_slots = sem_alg_obj._get_slots(ep)
        assert test_slots == gold_slots

    @staticmethod
    @parametrize_with_cases("predicate, var_props, gold_sement", cases=CreateBaseSement)
    def test_create_base_SEMENT(predicate, var_props, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.create_base_SEMENT(predicate, var_props)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("predicate, carg_val, gold_sement", cases=CreateCARGSement)
    def test_create_CARG_SEMENT(predicate, carg_val, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.create_CARG_SEMENT(predicate, carg_val)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, slot_label, gold_sement", cases=OpNonScopalArgumentHook)
    def test_op_non_scopal_argument_hook_slots(functor, argument, slot_label, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_non_scopal_argument_hook_slots_slots(functor, argument, slot_label)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, slot_label, gold_sement", cases=OpNonScopalFunctorHook)
    def test_op_non_scopal_functor_hook_slots(functor, argument, slot_label, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_non_scopal_functor_hook_slots_slots(functor, argument, slot_label)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, gold_sement", cases=OpScopalQuantifier)
    def test_op_scopal_quantifier(functor, argument, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_scopal_quantifier(functor, argument)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, slot_label, gold_sement", cases=OpScopalArgumentIndex)
    def test_op_scopal_argument_index_slots(functor, argument, slot_label, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_scopal_argument_index_slots_slots(functor, argument, slot_label)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, slot_label, gold_sement", cases=OpScopalFunctorIndex)
    def test_op_scopal_functor_index_slots(functor, argument, slot_label, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_scopal_functor_index_slots(functor, argument, slot_label)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("functor, argument, slot_label, gold_sement", cases=OpScopalFunctorIndexArgumentSlots)
    def test_op_scopal_functor_index_argument_slots(functor, argument, slot_label, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.op_scopal_functor_index_argument_slots(functor, argument, slot_label)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(
            gold_sement, test_sement)

    @staticmethod
    @parametrize_with_cases("unprepared_sement, gold_sement", cases=PrepareForGeneration)
    def test_prepare_for_generation(unprepared_sement, gold_sement, sem_alg_obj):
        test_sement = sem_alg_obj.prepare_for_generation(unprepared_sement)
        assert POGGSEMENTUtil.is_sement_isomorphic(gold_sement, test_sement), POGGSEMENTUtil.build_isomorphism_report(gold_sement, test_sement)
