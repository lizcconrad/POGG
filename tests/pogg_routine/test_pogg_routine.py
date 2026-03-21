import pytest
from pytest_cases import parametrize_with_cases
from pogg.pogg_routine import POGG

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_pogg_cases import *


class TestPOGG:
    """
    Tests POGG class
    """
    @staticmethod
    def test_init(module_pogg_config, dataset_config_file):
        pogg_routine =