# Contains the MRS algebra
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
from pogg.pogg_config import POGGConfig


def _get_slots(ep):
    """
    Get the slots contributed by a particular EP to send into a SEMENT
    slots dict looks like ...
    {
        'pred_label': {'ARG1': 'x0', 'ARG2': 'x1'}
    }

    Args:
        ep (delphin.mrs.EP): EP (elementary predicate) object to get slots from


    Returns:
        dict: dict of slots contributed by the EP
    """
    slots = {}
    for arg in ep.args:
        if ep.args[arg] != ep.iv:
            slots[arg] = ep.args[arg]
    return slots


def create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties={}):
    """
    Make the base case SEMENT, i.e. a SEMENT with only one EP in the RELS list before any composition has occurred

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        intrinsic_variable_properties (dict of str: str): optional dictionary of properties of the intrinsic variable, e.g. {'NUM': 'sg'}

    Returns:
        SEMENT: newly created SEMENT with one EP in the RELS list
    """

    # get semantic arguments for given predicate
    args = pogg_config.concretize(predicate)
    # create EP
    # create a handle that will serve as the LBL for the EP
    lbl = pogg_config.var_labeler.get_var_name('h')
    ep = mrs.EP(predicate, lbl, args)


    # if the predicate ends in "_q" it's a quantifier, so a new handle needs to be created to serve as the LTOP
    # otherwise, use the LBL as LTOP
    if predicate.endswith("_q"):
        ltop = pogg_config.var_labeler.get_var_name('h')
    else:
        ltop = lbl

    # create SEMENT with one EP on the RELS list
    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(ltop, ep.args['ARG0'], [ep], _get_slots(ep), None, None, None, {ep.args['ARG0']: intrinsic_variable_properties})

