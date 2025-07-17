import os
import unittest
import delphin
from pogg.pogg_config import POGGConfig
from pogg.my_delphin.my_delphin import SEMENT
import pogg.my_delphin.sementcodecs as sementcodecs
from pogg.semantic_composition import sement_util
import pogg.semantic_composition.semantic_algebra as semantic_algebra


class TestAlgebraFunctions(unittest.TestCase):
    """
    Tests functions included in the semantic algebra
    """
    def assertSEMENTIsomorphism(self, gold_sement, test_sement):
        isomorphism_results = sement_util.is_sement_isomorphic(gold_sement, test_sement)
        isomorphism_report = sement_util.build_isomorphism_report(gold_sement, test_sement)

        self.assertTrue(isomorphism_results,
                        "\nGold: {}\nActual: {}\nIsomorphism Report: {}".format(sementcodecs.encode(gold_sement, indent=True),
                                                        sementcodecs.encode(test_sement, indent=True), isomorphism_report))

    def decode_gold_sement_string(self, filename):
        return sementcodecs.decode(open(os.path.join(self.test_dir, filename)).read())

    def setUp(self):
        # create a POGGConfig object that points to a real grammar for testing functionality
        self.top_test_dir = os.getenv("TEST_WORKING_DIR")
        self.test_dir = os.path.join(self.top_test_dir, "test_data/semantic_composition/semantic_algebra")
        self.pogg_config = POGGConfig(os.path.join(self.top_test_dir, "test_data/test_config.yml"))
        # set variterator to start at 100 to avoid collision with gold SEMENTs
        self.pogg_config.var_labeler.varIt.set(100)


    def test__get_slots(self):
        # create an EP
        self.give_EP = delphin.mrs.EP("_give_v_1", "h0", {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})

        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_slots = {"ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}

        self.assertDictEqual(golden_slots, semantic_algebra._get_slots(self.give_EP))

    def test__get_slots_quantifier(self):
        # create an EP
        self.give_EP = delphin.mrs.EP("_the_q", "h0", {'ARG0': 'x1', 'RSTR': 'h2', 'BODY': 'h3'})

        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_slots = {"ARG0": "x1", "RSTR": "h2", "BODY": "h3"}

        self.assertDictEqual(golden_slots, semantic_algebra._get_slots(self.give_EP))

    def test_create_base_SEMENT_give(self):
        gold_give_sement = self.decode_gold_sement_string("give_base_sement.txt")

        test_give_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_give_v_1")
        self.assertSEMENTIsomorphism(gold_give_sement, test_give_sement)


    def test_create_base_SEMENT_the(self):
        gold_the_sement = self.decode_gold_sement_string("the_base_sement.txt")

        test_the_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_the_q")
        self.assertSEMENTIsomorphism(gold_the_sement, test_the_sement)

    def test_create_CARG_SEMENT_liz(self):
        gold_liz_sement = self.decode_gold_sement_string("liz_CARG_sement.txt")

        test_liz_sement = semantic_algebra.create_CARG_SEMENT(self.pogg_config, "named", "Liz")
        self.assertSEMENTIsomorphism(gold_liz_sement, test_liz_sement)

    def test_create_CARG_SEMENT_five(self):
        gold_five_sement = self.decode_gold_sement_string("five_CARG_sement.txt")

        test_five_sement = semantic_algebra.create_CARG_SEMENT(self.pogg_config, "card", "5")
        self.assertSEMENTIsomorphism(gold_five_sement, test_five_sement)

    def test_op_non_scopal_argument_hook_tasty_cookie(self):
        gold_tasty_cookie_sement = self.decode_gold_sement_string("tasty_cookie_sement.txt")

        # assumes create_base_SEMENT works
        tasty_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_tasty_a_1")
        cookie_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_cookie_n_1")

        test_tasty_cookie_sement = semantic_algebra.op_non_scopal_argument_hook(tasty_sement, cookie_sement, "ARG1")
        self.assertSEMENTIsomorphism(gold_tasty_cookie_sement, test_tasty_cookie_sement)

    def test_op_non_scopal_argument_hook_extremely_tasty(self):
        gold_extremely_tasty_sement = self.decode_gold_sement_string("extremely_tasty_sement.txt")

        # assumes create_base_SEMENT works
        extremely_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_extremely_x_deg")
        tasty_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_tasty_a_1")

        test_tasty_cookie_sement = semantic_algebra.op_non_scopal_argument_hook(extremely_sement, tasty_sement, "ARG1")
        self.assertSEMENTIsomorphism(gold_extremely_tasty_sement, test_tasty_cookie_sement)

    def test_op_non_scopal_functor_hook_eat_the_cookie(self):
        gold_eat_the_cookie_sement = self.decode_gold_sement_string("eat_the_cookie_sement.txt")

        # assumes create_base_SEMENT works
        eat_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_eat_v_1")
        the_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_the_q")
        cookie_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_cookie_n_1")
        # assumes op_scopal_quantifier works
        test_the_cookie_sement = semantic_algebra.op_scopal_quantifier(the_sement, cookie_sement)

        test_eat_the_cookie_sement = semantic_algebra.op_non_scopal_functor_hook(eat_sement, test_the_cookie_sement, "ARG2")
        self.assertSEMENTIsomorphism(gold_eat_the_cookie_sement, test_eat_the_cookie_sement)

    def test_op_scopal_quantifier_the_cookie(self):
        gold_the_cookie_sement = self.decode_gold_sement_string("the_cookie_sement.txt")

        # assumes create_base_SEMENT works
        the_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_the_q")
        cookie_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_cookie_n_1")

        test_the_cookie_sement = semantic_algebra.op_scopal_quantifier(the_sement, cookie_sement)
        self.assertSEMENTIsomorphism(gold_the_cookie_sement, test_the_cookie_sement)


    def test_op_scopal_argument_index_probably_sleeps(self):
        gold_probably_sleeps_sement = self.decode_gold_sement_string("probably_sleeps_sement.txt")

        # assumes create_base_SEMENT works
        probably_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_probable_a_1")
        sleep_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_sleep_v_1")

        test_probably_sleeps_sement = semantic_algebra.op_scopal_argument_index(probably_sement, sleep_sement, "ARG1")
        self.assertSEMENTIsomorphism(gold_probably_sleeps_sement, test_probably_sleeps_sement)


    def test_op_scopal_functor_index_believe_cats_sleep(self):
        gold_believe_cats_sleep_sement = self.decode_gold_sement_string("believe_cats_sleep_sement.txt")

        # assumes create_base_SEMENT works
        believe_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_believe_v_1")
        udef_q_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "udef_q")
        cat_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_cat_n_1")
        sleep_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_sleep_v_1")

        # assumes op_scopal_quantifier works
        udef_q_cat_sement = semantic_algebra.op_scopal_quantifier(udef_q_sement, cat_sement)
        # assumes op_non_scopal_functor_hook works
        udef_cat_sleep_sement = semantic_algebra.op_non_scopal_functor_hook(sleep_sement, udef_q_cat_sement, "ARG1")
        test_believe_cats_sleep_sement = semantic_algebra.op_scopal_functor_index(believe_sement, udef_cat_sleep_sement, "ARG2")
        self.assertSEMENTIsomorphism(gold_believe_cats_sleep_sement, test_believe_cats_sleep_sement)


    def test_prepare_for_generation_unquant_noun(self):
        gold_sement = self.decode_gold_sement_string("generatable_quant_cookie_sement.txt")

        cookie_sement = self.decode_gold_sement_string("unquantified_cookie_sement.txt")
        prepared_sement = semantic_algebra.prepare_for_generation(self.pogg_config, cookie_sement)

        self.assertSEMENTIsomorphism(gold_sement, prepared_sement)

    def test_prepare_for_generation_quant_noun(self):
        gold_sement = self.decode_gold_sement_string("generatable_quant_cookie_sement.txt")

        cookie_sement = self.decode_gold_sement_string("quantified_cookie_sement.txt")
        prepared_sement = semantic_algebra.prepare_for_generation(self.pogg_config, cookie_sement)

        self.assertSEMENTIsomorphism(gold_sement, prepared_sement)

    def test_prepare_for_generation_verb(self):
        gold_sement = self.decode_gold_sement_string("generatable_verb_sement.txt")

        eat_sement = self.decode_gold_sement_string("eat_sement.txt")
        prepared_sement = semantic_algebra.prepare_for_generation(self.pogg_config, eat_sement)

        self.assertSEMENTIsomorphism(gold_sement, prepared_sement)

    def test_prepare_for_generation_hi_hcon_type_constrain(self):
        gold_sement = self.decode_gold_sement_string("generatable_probably_sleeps_sement.txt")

        probably_sleeps_sement = self.decode_gold_sement_string("probably_sleeps_u_hcons_members_sement.txt")
        prepared_sement = semantic_algebra.prepare_for_generation(self.pogg_config, probably_sleeps_sement)

        self.assertSEMENTIsomorphism(gold_sement, prepared_sement)
        for hcon in prepared_sement.hcons:
            self.assertTrue(hcon.hi[0] == "h", "hi-handle not type h: {}".format(hcon.hi))
            self.assertTrue(hcon.lo[0] == "h", "lo-handle not type h: {}".format(hcon.lo))