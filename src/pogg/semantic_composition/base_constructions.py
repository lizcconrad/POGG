"""
The base_constructions module contains classes that help in creating SEMENTs from scratch as well as performing composition on existing SEMENTs

[See usage examples here](project:/usage_nbs/pogg/semantic_composition/base_constructions_usage.ipynb)
"""

from pogg.my_delphin.my_delphin import SEMENT
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra

class SingleWordConstructionsMixin:
    """
    The `SingleWordConstructionsMixin` contains functions for creating "starter" SEMENTs
    (typically containing only one predicate and roughly map to one English word) from scratch
    """
    def basic(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Wrapper around semantic_algebra.create_base_SEMENT. Used in fallback cases where part-of-speech guessing fails.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


    def adjective(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just an adjective EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


    def determiner(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a determiner EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'IND': '+'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


    def named_entity(self, name: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT for a named entity, e.g. a person ("Liz")

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `name` | `str` | | | `'Liz'` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'PERS': '3'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT("named", name, intrinsic_variable_properties)


    def noun(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a noun EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


    def preposition(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a preposition EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_in_p_loc` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


    def pronoun(self, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT for a pronoun.
        If values for PER and NUM (and GEND for third person) are not specified in the intrinsic_variable_properties dictionary,
        it will be ambiguous between all values.

        ```{info} Possible variables and values for a pronoun's intrinsic variable
        :collapsible:
        | Variable | Values |
        | -------- | ------ |
        | `'PERS'` | `'1'`, `'2'`, `'3'` |
        | `'NUM'` | `'sg'`, `'pl'` |
        | `'GEND'` | `'m'`, `'f'`, `'n'` |
        ```

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `intrinsic_variable_properties` | `dict` of `str:str` | `None` | optional dictionary of properties of the intrinsic variable | `{'PER': '3', 'NUM': 'sg', 'GEND': 'f'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        pron_EP = self.semantic_algebra.create_base_SEMENT("pron", intrinsic_variable_properties)
        pronoun_q_EP = self.determiner("pronoun_q")

        # scopal composition between pronoun quantifier and the pron EP
        return self.semantic_algebra.op_scopal_quantifier(pronoun_q_EP, pron_EP)


    def quantifier(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a quantifier EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_eat_v_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'TENSE': 'pres'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)



    def verb(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a verb EP in it.
        This is just a wrapper around create_base_SEMENT but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_eat_v_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'TENSE': 'pres'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)


class BaseConstructionsMixin:
    """
    The `BaseConstructionsMixin` contains functions for creating "starter" SEMENTs
    (typically containing only one predicate and roughly map to one English word) from scratch
    """
    def prenominal_adjective(self, adjective_sement: SEMENT, nominal_sement: SEMENT) -> SEMENT:
        """
        Performs composition with an adjective SEMENT and a nominal SEMENT
        e.g. "tasty cookie" or "tasty cookie in the oven"

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `adjective_sement` | `SEMENT` | SEMENT object for the adjective |
        | `nominal_sement` | `SEMENT` | SEMENT object for the noun (plus potential adjuncts) that the adjective modifies |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT composed of an adjective and the elements it modifies |
        """

        return self.semantic_algebra.op_non_scopal_argument_hook(adjective_sement, nominal_sement, "ARG1")

    def compound_noun(self, head_noun_sement: SEMENT, non_head_noun_sement: SEMENT) -> SEMENT:
        udef_q = self.quantifier("udef_q")
        compound = self.basic("compound")
        udef_non_head_noun = self.quantify(udef_q, non_head_noun_sement)

        # plug ARG2 of compound (non_head)
        arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook(compound, udef_non_head_noun, "ARG2")
        # plug ARG1 of compound (head)
        arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook(arg2_plugged, head_noun_sement, "ARG1")

        return arg1_plugged


    def prepositional_relationship(self, preposition_predicate: str, figure_sement: SEMENT, ground_sement: SEMENT) -> SEMENT:
        pass

    def relative_direction(self, direction_predicate: str, figure_sement: SEMENT, ground_sement: SEMENT) -> SEMENT:
        pass

    def possessive(self, possessor_sement: SEMENT, possessed_sement: SEMENT) -> SEMENT:
        pass

    def quantify(self, quantifier_sement: SEMENT, quantified_sement: SEMENT) -> SEMENT:
        return self.semantic_algebra.op_scopal_quantifier(quantifier_sement, quantified_sement)


class SemanticComposition(SingleWordConstructionsMixin, BaseConstructionsMixin):
    """
    A SingleWordConstructions object contains functions for creating "single word" SEMENTs (e.g. noun)

    These functions create SEMENTs "from scratch" that can be later used as semantic functors or arguments for further composition
    """
    def __init__(self, semantic_algebra: SemanticAlgebra):
        """
        Initialize the `SemanticAlgebra` object

        Each parameter may also be accessed as an instance attribute

        **Parameters / Instance Attributes**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `semantic_algebra` | `SemanticAlgebra` | SemanticAlgebra object that contains functions that perform semantic composition directly |
        """
        self.semantic_algebra = semantic_algebra

