from pogg.pogg_config import POGGConfig
import semantic_algebra
import sement_util

def basic(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Wrapper around semantic_algebra.create_base_SEMENT. Used in fallback cases where part-of-speech guessing fails.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """
    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


def adjective(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Creates a SEMENT with just a adjective EP in it.
    This is just a wrapper around create_base_SEMENt but is more transparently named for users.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """
    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


def determiner(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Creates a SEMENT with just a determiner EP in it.
    This is just a wrapper around create_base_SEMENt but is more transparently named for users.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """
    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


def named_entity(pogg_config, name, intrinsic_variable_properties={}):
    """
    Creates a SEMENT for a named entity, e.g. a person ("Liz")

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        name (str): the name of the entity
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}
    """

    return semantic_algebra.create_CARG_SEMENT(pogg_config, "named", name, intrinsic_variable_properties)


def noun(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Creates a SEMENT with just a noun EP in it.
    This is just a wrapper around create_base_SEMENt but is more transparently named for users.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """
    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


def preposition(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Creates a SEMENT with just a preposition EP in it.
    This is just a wrapper around create_base_SEMENt but is more transparently named for users.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """

    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


def pronoun(pogg_config, intrinsic_variable_properties={}):
    """Creates a SEMENT for a pronoun.
    If values for PER and NUM are not specific in the intrinsic_variable_properties dictionary it will be ambiguous between all values.

    Args:
        pogg_config: (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        intrinsic_variable_properties (dict of str: str): Specifies PER and NUM values for the pronoun, e.g. {'PER':
    """


def verb(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Creates a SEMENT with just a verb EP in it.
    This is just a wrapper around create_base_SEMENt but is more transparently named for users.

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT
    """

    return semantic_algebra.create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties)


