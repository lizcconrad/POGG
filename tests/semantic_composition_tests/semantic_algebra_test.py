import unittest
import delphin
from pogg.pogg_config import POGGConfig
from pogg.my_delphin.my_delphin import SEMENT
from pogg.semantic_composition import sement_util
import pogg.semantic_composition.semantic_algebra as semantic_algebra


class TestAlgebraFunctions(unittest.TestCase):
    """
    Tests functions included in the semantic algebra
    """
    def setUp(self):
        # self.gold_give_ep.predicate = "_give_v_1"
        # self.gold_give_ep.label = "h0"
        # self.gold_give_ep.args = {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'}
        # self.gold_give_sement.top = "h0"
        # self.gold_give_sement.index = "e1"
        # self.gold_give_sement.rels = [self.gold_give_ep]
        # self.gold_give_sement.eqs = None
        # self.gold_give_sement.slots = {"ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}
        # self.gold_give_sement.variables = {'h0': {}, 'e1': {}, 'i2': {}, 'u3': {}, 'i4': {}}

        # create a POGGConfig object that points to a real grammar for testing functionality
        # path for running tests in pycharm using "Current File" configuration
        # self.pogg_config = POGGConfig("../test_data/test_config.yml")
        # path for running tests using hatch
        self.pogg_config = POGGConfig("tests/test_data/test_config.yml")



        # gold base SEMENT for 'give' (assumes SEMENT init fxn works properly)
        self.gold_give_EP = delphin.mrs.EP("_give_v_1", "h0", {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})
        self.gold_give_sement = SEMENT("h0", "e1", [self.gold_give_EP], {'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})

        # gold base SEMENT for 'the'
        # self.gold_the_EP =


    def test__get_slots(self):
        # create an EP
        self.give_EP = delphin.mrs.EP("_give_v_1", "h0", {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})

        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_slots = {"ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}

        self.assertDictEqual(golden_slots, semantic_algebra._get_slots(self.give_EP))

    def test_create_base_SEMENT(self):
        test_give_sement = semantic_algebra.create_base_SEMENT(self.pogg_config, "_give_v_1")
        self.assertTrue(sement_util.is_sement_isomorphic(self.gold_give_sement, test_give_sement),
                        "create_base_SEMENT for '_give_v_1' is not isomorphic to gold SEMENT for '_give_v_1'")



