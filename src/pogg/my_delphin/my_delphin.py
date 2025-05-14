# modified versions of pydelphin elements that may be submitted for a PR later
# taken from the _mrs.py file to test my subclass
from typing import Optional, Iterable, Mapping, Dict

import delphin.semi
from delphin.lnk import Lnk
# end from _mrs.py

from copy import deepcopy
from delphin import mrs

# import codecs stuff
from delphin.codecs import simplemrs


class SEMENT(mrs.MRS):
    """
    A SEMENT (Semantic Element) is formally very similar to an MRS (Minimal Recursion Semantics) structure.
    However, an MRS is typically understood to be a "complete" structure which will not participate in further semantic composition.
    A SEMENT, on the other hand, is like a version of an MRS with additional machinery to enable composition.
    In order to facilitate this, a SEMENT has everything that an MRS does plus
        (1) a list of "slots" (semantic arguments available to be filled, such as the SLEEPER (ARG1) for the verb 'sleep')
        (2) a running list of equalities between variables which will be collapsed when composition is complete
            e.g. if there is a 'cat' relation whose intrinsic variable is x1 and there is a 'sleep' relation whose ARG1 (the 'sleeper') is x2,
            if we want to say the cat is the entity that is sleeping, we add x1=x2 to the list of variable equalities
            and then when composition is complete one of those variables is chosen as the "representative" (say, x1)
            and every instance of x1 or x2 is set to be x1 for the final structure

    The formal differences between an MRS and a SEMENT are included below.

    An MRS is a tuple of the form <HOOK, RELS, HCONS> where...
        ... Hook is a tuple of the form <GTOP, IND, XARG> where ...
            ... GTOP -- top handle
            ... IND -- index
            ... XARG is ... ? used to deal with raising/control constructions
        ... RELS is a bag of EPs <LBL, REL, ARGS, SC-ARGS>
            ... LBL -- handle which is the label of the eP
            ... REL -- relation (i.e. predicate)
            ... ARGS -- list of zero or more ordinary variable arguments
            ... SC-ARGS -- list of zero or more handles corresponding to scopal arguments
                Note: In PyDelphin ARGS and SC-ARGS list is collapsed into one
        ... HCONS is a bag of handle constraints

    A SEMENT is a tuple of the form <HOOK, SLOTS, RELS, EQS, HCONS> where ...
        ... HOOK is a tuple of the form <TOP, IND, XARG> (same as above, but the TOP is not global because composition is incomplete)
        ... SLOTS is the list of slots, two-layer deep dict labeled per predicate in RELS list
        ... RELS is the list of EPs
        ... EQS is a list of equalities between variables
        ... HCONS is a bag of handle constraints
    """

    # TODO: rels, hcons, and icons are of type mrs.EP, mrs.HCons, and mrs.ICons ...
    #  should just be EP, HCons, and ICons but this isn't in the real file yet
    def __init__(self,
                 top: Optional[str] = None,
                 index: Optional[str] = None,
                 rels: Optional[Iterable[mrs.EP]] = None,
                 slots: Optional[Mapping[str, Mapping[str, str]]] = None,
                 eqs: Optional[Iterable[set[str, ...]]] = None,
                 hcons: Optional[Iterable[mrs.HCons]] = None,
                 icons: Optional[Iterable[mrs.ICons]] = None,
                 variables: Optional[Mapping[str, Mapping[str, str]]] = None,
                 lnk: Optional[Lnk] = None,
                 surface=None,
                 identifier=None):
        super().__init__(top, index, rels, hcons, icons, variables, lnk, surface, identifier)

        self.slots = slots
        self.eqs = eqs


### Encoding ###
def _encode_eqs(eqs):
    # e.g. [(x1, x2), (x3, x4, x5)]
    tokens = None
    if eqs:
        tokens = ['({})'.format(','.join(eq)) for eq in eqs]
        tokens = ['EQS: <'] + [', '.join(tokens)] + ['>']
    return tokens

def _encode_slots(slots):
    tokens = None
    if slots:
        tokens = ['{}: {}'.format(slot, slots[slot]) for slot in slots]
        tokens = ['SLOTS: <'] + [', '.join(tokens)] + ['>']
    return tokens


def _encode_sement(s, properties=True, lnk=True, indent=False):
    delim = '\n  ' if indent else ' '
    if properties:
        varprops = dict(s.variables)
    else:
        varprops = {}
    parts = [
        simplemrs._encode_surface_info(s, lnk),
        simplemrs._encode_hook(s, varprops, indent),
        simplemrs._encode_rels(s.rels, varprops, lnk, indent),
        simplemrs._encode_hcons(s.hcons),
        simplemrs._encode_icons(s.icons, varprops),
        _encode_eqs(s.eqs),
        _encode_slots(s.slots)
    ]
    return '[ {} ]'.format(
        delim.join(
            ' '.join(tokens) for tokens in parts if tokens))

def _encode(ms, properties, lnk, indent):
    if indent is None or indent is False:
        indent = False  # normalize None to False
        delim = ' '
    else:
        indent = True  # normalize integers to True
        delim = '\n'
    return delim.join(_encode_sement(m, properties, lnk, indent) for m in ms)

def encode(s, properties=True, lnk=True, indent=False):
    """
    Serialize a SEMENT object to a string.

    Args:
        s: a SEMENT object
        properties (bool): if `False`, suppress variable properties
        lnk: if `False`, suppress surface alignments and strings
        indent (bool, int): if `True` or an integer value, add
            newlines and indentation
    Returns:
        a serialization of the SEMENT object
    """
    return _encode([s], properties, lnk, indent)


