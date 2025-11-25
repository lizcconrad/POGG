import os
from delphin import mrs

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
    def case_give(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "give_base_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_give_v_1", {"TENSE": "pres"},  gold_sement

    @staticmethod
    def case_the(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "the_base_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "_the_q", {},  gold_sement


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
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "liz_CARG_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "named", "Liz",  gold_sement

    @staticmethod
    def case_five(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "five_CARG_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        return "card", "5",  gold_sement

class OpNonScopalArgumentHook:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_argument_hook

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_non_scopal_argument_hook, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "tasty cookie"
        2. "extremely tasty"
    """

    @staticmethod
    def case_tasty_cookie(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "tasty_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assumes create_base_SEMENT works
        tasty_sement = sem_alg_obj.create_base_SEMENT("_tasty_a_1")
        cookie_sement = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        return tasty_sement, cookie_sement, "ARG1", gold_sement

    @staticmethod
    def case_extremely_tasty(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "extremely_tasty_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assumes create_base_SEMENT works
        extremely_sement = sem_alg_obj.create_base_SEMENT("_extremely_x_deg")
        tasty_sement = sem_alg_obj.create_base_SEMENT("_tasty_a_1")

        return extremely_sement, tasty_sement, "ARG1", gold_sement


class OpNonScopalFunctorHook:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_non_scopal_functor_hook

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_non_scopal_functor_hook, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "eat the cookie"
    """

    @staticmethod
    def case_tasty_cookie(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "eat_the_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        the_cookie_sement_file = os.path.join(semantic_algebra_test_dir, "the_cookie_sement.txt")
        the_cookie_sement = sementcodecs.decode(open(the_cookie_sement_file).read())

        # assumes create_base_SEMENT works
        eat_sement = sem_alg_obj.create_base_SEMENT("_eat_v_1")

        return eat_sement, the_cookie_sement, "ARG2", gold_sement

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
        2. "extremely tasty"
    """

    @staticmethod
    def case_the_cookie(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "the_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assumes create_base_SEMENT works
        the_sement = sem_alg_obj.create_base_SEMENT("_the_q")
        cookie_sement = sem_alg_obj.create_base_SEMENT("_cookie_n_1")

        return the_sement, cookie_sement, gold_sement

class OpScopalArgumentIndex:
    """
    FUNCTIONS BEING TESTED:
        - pogg.semantic_composition.semantic_algebra.SemanticAlgebra.op_scopal_argument_index

    GENERAL DESCRIPTION OF TEST CASES:
        Provide two SEMENTs to be passed into op_scopal_argument_index, the slot to be plugged, and the expected result
        test should compare result of call with expected result
    """

    """
    SUCCESS CASES
        1. "probably sleeps"
    """

    @staticmethod
    def case_probably_sleeps(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "probably_sleeps_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        # assumes create_base_SEMENT works
        probable_sement = sem_alg_obj.create_base_SEMENT("_probable_a_1")
        sleep_sement = sem_alg_obj.create_base_SEMENT("_sleep_v_1")

        return probable_sement, sleep_sement, "ARG1", gold_sement

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
        1. "probably sleeps"
    """

    @staticmethod
    def case_probably_sleeps(semantic_algebra_test_dir, sem_alg_obj):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "believe_cats_sleep_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        udef_cat_sleep_sement_file = os.path.join(semantic_algebra_test_dir, "udef_cat_sleep_sement.txt")
        udef_cat_sleep_sement = sementcodecs.decode(open(udef_cat_sleep_sement_file).read())

        # assumes create_base_SEMENT works
        believe_sement = sem_alg_obj.create_base_SEMENT("_believe_v_1")

        return believe_sement, udef_cat_sleep_sement, "ARG2", gold_sement


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
    """

    @staticmethod
    def case_unquantified_noun(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "generatable_quant_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        cookie_sement_file = os.path.join(semantic_algebra_test_dir, "unquantified_cookie_sement.txt")
        cookie_sement = sementcodecs.decode(open(cookie_sement_file).read())

        return cookie_sement, gold_sement

    @staticmethod
    def case_quantified_noun(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "generatable_quant_cookie_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        quant_cookie_sement_file = os.path.join(semantic_algebra_test_dir, "quantified_cookie_sement.txt")
        quant_cookie_sement = sementcodecs.decode(open(quant_cookie_sement_file).read())

        return quant_cookie_sement, gold_sement

    @staticmethod
    def case_verb(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "generatable_verb_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        eat_sement_file = os.path.join(semantic_algebra_test_dir, "eat_sement.txt")
        eat_sement = sementcodecs.decode(open(eat_sement_file).read())

        return eat_sement, gold_sement

    @staticmethod
    def case_probably_sleeps(semantic_algebra_test_dir):
        gold_sement_file = os.path.join(semantic_algebra_test_dir, "generatable_probably_sleeps_sement.txt")
        gold_sement = sementcodecs.decode(open(gold_sement_file).read())

        probably_sleeps_sement_file = os.path.join(semantic_algebra_test_dir, "probably_sleeps_u_hcons_members_sement.txt")
        probably_sleeps_sement = sementcodecs.decode(open(probably_sleeps_sement_file).read())

        return probably_sleeps_sement, gold_sement


