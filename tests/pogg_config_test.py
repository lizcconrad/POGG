import unittest
from tempfile import NamedTemporaryFile
import delphin
from pogg.pogg_config import _VarIterator, _VarLabeler, POGGConfig


class Test_VarIterator(unittest.TestCase):
    """
    Tests the VarIterator class.
    """

    def setUp(self):
        self.var_iterator = _VarIterator()

    def test__VarIterator_object(self):
        # assert whether var_iterator object is of the correct type
        self.assertIsInstance(self.var_iterator, _VarIterator,
                              "object not of type VarIterator")

    def test__VarIterator_iter(self):
        # assert whether __iter__ returns the VarIterator object
        self.assertIsInstance(self.var_iterator.__iter__(), _VarIterator,
                              "object not of type VarIterator")

    def test__VarIterator_next(self):
        # assert that the increment occurred correctly
        self.assertEqual(next(self.var_iterator), 1)

    def test__VarIterator_set(self):
        # assert that the iterator's new value is set correctly
        self.var_iterator.set(2)
        self.assertEqual(self.var_iterator.count, 2)

    def test__VarIterator_reset(self):
        # assert that the iterator was reset
        self.var_iterator.reset()
        self.assertEqual(self.var_iterator.count, 0)


class TestVarLabeler(unittest.TestCase):
    """
    Tests the VarLabeler class.
    """

    def setUp(self):
        self.var_labeler = _VarLabeler()

    def test__VarLabeler_object(self):
        # assert whether var_iterator object is of the correct type
        self.assertIsInstance(self.var_labeler, _VarLabeler,
                              "object not of type _VarLabeler")

    def test__VarLabeler_next_variable(self):
        # assert that the labeler produces the correct next variable name
        self.assertEqual(self.var_labeler.get_var_name("x"), "x1")

    def test__VarLabeler_multiple(self):
        # increment the labeler multiple times and check each one
        for i in range(1, 11):
            self.assertEqual(self.var_labeler.get_var_name("x"), "x" + str(i))

    def test__VarLabeler_reset(self):
        # increment the labeler a few times and check it
        for i in range(1, 4):
            self.assertEqual(self.var_labeler.get_var_name("x"), "x" + str(i))

        # reset and check that it was reset correctly
        self.var_labeler.reset_labeler()
        self.assertEqual(self.var_labeler.get_var_name("x"), "x1")


class TestPOGGConfig(unittest.TestCase):
    """
    Tests the POGGConfig class.
    """

    def setUp(self):
        # make temporary files
        self.temp_config = NamedTemporaryFile(suffix=".yml")
        self.temp_grammar = NamedTemporaryFile(suffix=".dat")
        self.temp_semi = NamedTemporaryFile(suffix=".smi")

        # write config information
        with open(self.temp_config.name, "w") as f:
            f.write("grammar_location: {}\n".format(self.temp_grammar.name))
            f.write("SEMI: {}\n".format(self.temp_semi.name))

        # make mock POGGConfig, for testing object initialization
        self.config_mock = POGGConfig(self.temp_config.name)

        # create a POGGConfig object that points to a real grammar for testing functionality
        # path for running tests in pycharm using "Current File" configuration
        # self.pogg_config = POGGConfig("test_data/test_config.yml")
        # path for running tests using hatch
        self.pogg_config = POGGConfig("tests/test_data/test_config.yml")


    ### OBJECT INITIALIZATION TESTS ###
    def test_POGGConfig_grammar_location(self):
        # assert whether grammar_location matches the provided location
        self.assertEqual(self.config_mock.grammar_location, self.temp_grammar.name,
                         """POGGConfig object's 'grammar_location' attribute does not match provided location:
                         POGGConfig object (config.grammar_location): {}
                         Provided location (temp_grammar.name): {}""".format(self.config_mock.grammar_location, self.temp_grammar.name))


    def test_POGGConfig_SEMI_location(self):
        # assert whether SEMI_location matches the provided config
        self.assertEqual(self.config_mock.SEMI_location, self.temp_semi.name,
                         """POGGConfig object's 'SEMI_location' attribute does not match provided location:
                         POGGConfig object (config.SEMI_location): {}
                         Provided location (temp_semi.name): {}""".format(self.config_mock.SEMI_location, self.temp_semi.name))

    def test_POGGConfig_SEMI_object(self):
        # assert whether SEMI_location matches the provided config
        self.assertIsInstance(self.config_mock.SEMI, delphin.semi.SemI,
                              "POGGConfig object's SEMI is not of type delphin.semi.SemI")

    def test_POGGConfig_VarLabeler_object(self):
        # assert whether SEMI_location matches the provided config
        self.assertIsInstance(self.config_mock.var_labeler, _VarLabeler,
                              "POGGConfig object's VarLabeler is not of type VarLabeler")


    # test whether exceptions are raised appropriately
    def test_POGGConfig_missing_grammar_location(self):
        # create temporary file with missing information
        # make temporary files
        self.temp_config_incomplete = NamedTemporaryFile(suffix=".yml")
        # write dummy information
        with open(self.temp_config_incomplete.name, "w") as f:
            f.write("dummy_key: {}\n".format("dummy_value"))

        # assert that KeyError is raised when the provided config file doesn't have grammar_location as a key
        self.assertRaises(KeyError, POGGConfig, self.temp_config_incomplete.name)

    def test_POGGConfig_missing_SEMI(self):
        # create temporary file with missing information
        # make temporary files
        self.temp_config_incomplete = NamedTemporaryFile(suffix=".yml")
        # write dummy grammar_location so that passes but then when we get to SEMI check it fails
        with open(self.temp_config_incomplete.name, "w") as f:
            f.write("grammar_location: {}\n".format("dummy_value"))

        # assert that KeyError is raised when the provided config file doesn't have SEMI as a key
        self.assertRaises(KeyError, POGGConfig, self.temp_config_incomplete.name)



    ### OBJECT FUNCTION TESTS ###
    def test_POGGConfig_concretize(self):
        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_args = {"ARG0": "e1", "ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}

        self.assertDictEqual(golden_args, self.pogg_config.concretize("_give_v_1"))

    def test_POGGConfig_concretize_no_synopsis(self):
        # assert that KeyError is raised when the provided config file doesn't have grammar_location as a key
        self.assertRaises(KeyError, self.pogg_config.concretize, "not_a_real_predicate_label")


if __name__ == '__main__':
    unittest.main()