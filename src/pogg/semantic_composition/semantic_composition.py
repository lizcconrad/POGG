"""
The base_constructions module contains classes that help in creating SEMENTs from scratch as well as performing composition on existing SEMENTs.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/base_constructions_usage.ipynb)
"""


from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.composition_mixins.single_word_constructions import SingleWordConstructionsMixin
from pogg.semantic_composition.composition_mixins.base_constructions import BaseConstructionsMixin

class SemanticComposition(SingleWordConstructionsMixin, BaseConstructionsMixin):
    """
    The SemanticComposition class inherits from the various Mixin classes that contain semantic composition functions.

    No matter how many Mixin classes there are covering different kinds of composition functions,
    the `SemanticComposition` class can inherit from all of them and serve as the one-stop shop for performing composition.

    All functions from the base Mixins can be accessed as instance methods on a `SemanticComposition` object.
    """
    def __init__(self, semantic_algebra: SemanticAlgebra):
        """
        Initialize the `SemanticComposition` object

        Each parameter may also be accessed as an instance attribute

        **Parameters / Instance Attributes**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `semantic_algebra` | `SemanticAlgebra` | SemanticAlgebra object that contains functions that perform semantic composition directly |
        """
        self.semantic_algebra = semantic_algebra

