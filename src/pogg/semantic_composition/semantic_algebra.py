# Contains the MRS algebra
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
import pogg.semantic_composition.sement_util as sement_util


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
        # include all semantic arguments except the intrinsic variable (usually ARG0) or CARG
        # EXCEPT for quantifiers, where ARG0 is also a slot
        if (ep.args[arg] != ep.iv and arg != "CARG") or ep.predicate.endswith("_q"):
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
    # send in empty lists for eqs, hcons, and icons for ease of composition
    return SEMENT(ltop, ep.args['ARG0'], [ep], _get_slots(ep), [], [], [], {ep.args['ARG0']: intrinsic_variable_properties})


def create_CARG_SEMENT(pogg_config, predicate, carg_value, intrinsic_variable_properties={}):
    """
    Make a base case SEMENT for an EP with a CARG argument (e.g. named, with a CARG value of "Liz")

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        predicate (str): ERG predicate label
        carg_value (str): Value for the CARG argument
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
    # add CARG as an argument and set the value
    ep.args['CARG'] = carg_value


    # create SEMENT with one EP on the RELS list
    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    # send in empty lists for eqs, hcons, and icons for ease of composition
    return SEMENT(lbl, ep.args['ARG0'], [ep], _get_slots(ep), [], [], [], {ep.args['ARG0']: intrinsic_variable_properties})


def op_non_scopal_argument_hook(functor, argument, slot_label):
    """
    Perform non-scopal composition on two SEMENTs. The hook (i.e. the LTOP and INDEX) of the resulting SEMENT comes from the argument.
    Typically used when the functor is a modifier (e.g. "tasty cookie")

    Args:
        functor (SEMENT): SEMENT object for the functor
        argument (SEMENT): SEMENT object for the argument
        slot_label (str): label for the semantic argument slot in the functor that the argument is plugging (e.g. ARG1)

    Returns:
        SEMENT: newly created SEMENT resulting from composition
    """

    # FUNC = semantic functor
    # ARG = semantic argument
    # SLOT = hole to be filled on the functor by composition
    # RES = SEMENT resulting from composition

    # RES.TOP = ARG.TOP (note TOP serves as LTOP for SEMENTs)
    # RES.INDEX = ARG.INDEX
    # RES.RELS = FUNC.RELS + ARG.RELS
    # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.TOP = ARG.TOP) + (FUNC.SLOTS.slot_label = ARG.INDEX)
    # ... (1) identify LTOPs and (2) add EQ between plugged ARG and ARG's INDEX
    # RES.SLOTS = ARG.SLOTS
    # ... take the slots from whichever SEMENT is contributing the HOOK

    # RES.HCONS = FUNC.HCONS + ARG.HCONS
    # RES.ICONS = FUNC.HCONS + ARG.HCONS

    result_top = argument.top
    result_index = argument.index

    result_rels = functor.rels + argument.rels

    result_eqs = functor.eqs + argument.eqs
    # identify (L)TOPs
    result_eqs.append((functor.top, argument.top))
    # add EQ between FUNC.SLOTS.slot_label and ARG.INDEX
    result_eqs.append((functor.slots[slot_label], argument.index))

    result_slots = argument.slots.copy()

    result_hcons = functor.hcons + argument.hcons

    result_icons = functor.icons + argument.icons

    result_variables = {}
    result_variables.update(functor.variables)
    result_variables.update(argument.variables)

    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)


def op_non_scopal_functor_hook(functor, argument, slot_label):
    """
    Perform non-scopal composition on two SEMENTs. The hook of the resulting SEMENT comes from the functor.
    Typically used when the argument is a complement (e.g. "give a cookie") or preposition ("in the park")

    Args:
        functor (SEMENT): SEMENT object for the functor
        argument (SEMENT): SEMENT object for the argument
        slot_label (str): label for the semantic argument slot in the functor that the argument is plugging (e.g. ARG1)

    Returns:
        SEMENT: newly created SEMENT resulting from composition
    """

    # FUNC = semantic functor
    # ARG = semantic argument
    # SLOT = hole to be filled on the functor by composition
    # RES = SEMENT resulting from composition

    # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
    # RES.INDEX = FUNC.INDEX
    # RES.RELS = FUNC.RELS + ARG.RELS
    # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.TOP = ARG.TOP) + (FUNC.SLOTS.slot_label = ARG.INDEX)
    # ... (1) identify LTOPs and (2) add EQ between plugged ARG and ARG's INDEX
    # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
    # ... take the slots from whichever SEMENT is contributing the HOOK

    # RES.HCONS = FUNC.HCONS + ARG.HCONS
    # RES.ICONS = FUNC.ICONS + ARG.ICONS

    result_top = functor.top
    result_index = functor.index

    result_rels = functor.rels + argument.rels

    result_eqs = functor.eqs + argument.eqs
    # identify (L)TOPs
    result_eqs.append((functor.top, argument.top))
    # add EQ between FUNC.SLOTS.slot_label and ARG.INDEX
    result_eqs.append((functor.slots[slot_label], argument.index))

    result_slots = functor.slots.copy()
    # delete the slot that's been plugged
    del result_slots[slot_label]

    result_hcons = functor.hcons + argument.hcons

    result_icons = functor.icons + argument.icons

    result_variables = {}
    result_variables.update(functor.variables)
    result_variables.update(argument.variables)

    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)


def op_scopal_argument_index(functor, argument, slot_label):
    """
    Perform scopal composition where the INDEX comes from the argument, but the LTOP comes from the functor.
    Used when the argument is a scopal modifier (e.g. "probably sleeps").

    Args:
        functor (SEMENT): SEMENT object for the functor
        argument (SEMENT): SEMENT object for the argument
        slot_label (str): label for the semantic argument slot in the functor that the argument is plugging (e.g. ARG1)

    Returns:
        SEMENT: newly created SEMENT resulting from composition
    """

    # FUNC = semantic functor
    # ARG = semantic argument
    # SLOT = hole to be filled on the functor by composition
    # RES = SEMENT resulting from composition

    # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
    # RES.INDEX = ARG.INDEX
    # RES.RELS = FUNC.RELS + ARG.RELS
    # RES.EQS = FUNC.EQS + ARG.EQS
    # ... no new EQs here just a QEQ in HCONS
    # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
    # ... take the slots from whichever SEMENT is contributing the HOOK

    # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.slot_label =q ARG.TOP
    # RES.ICONS = FUNC.ICONS + ARG.ICONS

    result_top = functor.top
    result_index = argument.index

    result_rels = functor.rels + argument.rels

    result_eqs = functor.eqs + argument.eqs

    result_slots = functor.slots.copy()
    # delete the slot that's been plugged
    del result_slots[slot_label]

    result_hcons = functor.hcons + argument.hcons
    result_hcons.append(mrs.HCons(functor.slots[slot_label], "qeq", argument.top))

    result_icons = functor.icons + argument.icons

    result_variables = {}
    result_variables.update(functor.variables)
    result_variables.update(argument.variables)

    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

def op_scopal_functor_index(functor, argument, slot_label):
    """
    Perform scopal composition where the INDEX comes from the functor (as does the LTOP, but this is true for all versions of scopal composition).
    Used when the argument is a complement (e.g. "believes it's raining").

    Args:
        functor (SEMENT): SEMENT object for the functor
        argument (SEMENT): SEMENT object for the argument
        slot_label (str): label for the semantic argument slot in the functor that the argument is plugging (e.g. ARG1)

    Returns:
        SEMENT: newly created SEMENT resulting from composition
    """

    # FUNC = semantic functor
    # ARG = semantic argument
    # SLOT = hole to be filled on the functor by composition
    # RES = SEMENT resulting from composition

    # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
    # RES.INDEX = FUNC.INDEX
    # RES.RELS = FUNC.RELS + ARG.RELS
    # RES.EQS = FUNC.EQS + ARG.EQS
    # ... no new EQs here just a QEQ in HCONS
    # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
    # ... take the slots from whichever SEMENT is contributing the HOOK

    # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.slot_label =q ARG.TOP
    # RES.ICONS = FUNC.ICONS + ARG.ICONS

    result_top = functor.top
    result_index = functor.index

    result_rels = functor.rels + argument.rels

    result_eqs = functor.eqs + argument.eqs

    result_slots = functor.slots.copy()
    # delete the slot that's been plugged
    del result_slots[slot_label]

    result_hcons = functor.hcons + argument.hcons
    result_hcons.append(mrs.HCons(functor.slots[slot_label], "qeq", argument.top))

    result_icons = functor.icons + argument.icons

    result_variables = {}
    result_variables.update(functor.variables)
    result_variables.update(argument.variables)

    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)


def op_scopal_quantifier(functor, argument):
    """
    Perform scopal composition between a quantifier SEMENT and a quantified SEMENT (e.g. "the cookie").
    This involves the plugging of two slots (ARG0 directly, RSTR with a qeq) thus warranting a separate function.

    Args:
        functor (SEMENT): SEMENT object for the functor
        argument (SEMENT): SEMENT object for the argument

    Returns:
        SEMENT: newly created SEMENT resulting from composition
    """

    # FUNC = semantic functor
    # ARG = semantic argument
    # SLOT = hole to be filled on the functor by composition
    # RES = SEMENT resulting from composition

    # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
    # RES.INDEX = FUNC.INDEX
    # RES.RELS = FUNC.RELS + ARG.RELS
    # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.SLOTS.ARG0 = ARG.INDEX)
    # ... add EQ between ARG0 and INDEX of thing being quantified
    # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
    # ... take the slots from whichever SEMENT is contributing the HOOK

    # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.RSTR =q ARG.TOP
    # RES.ICONS = FUNC.ICONS + ARG.ICONS

    result_top = functor.top
    result_index = functor.index

    result_rels = functor.rels + argument.rels

    result_eqs = functor.eqs + argument.eqs
    result_eqs.append((functor.slots["ARG0"], argument.index))

    result_slots = functor.slots.copy()
    # delete the slot that's been plugged
    del result_slots["ARG0"]

    result_hcons = functor.hcons + argument.hcons
    result_hcons.append(mrs.HCons(functor.slots["RSTR"], "qeq", argument.top))
    del result_slots["RSTR"]

    result_icons = functor.icons + argument.icons

    result_variables = {}
    result_variables.update(functor.variables)
    result_variables.update(argument.variables)

    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)


def prepare_for_generation(pogg_config, sement):
    """
    Prepare the given SEMENT for generation. This involves...
    (1) Checking if the INDEX is of type e
        If not...
        (a) check if given SEMENT is quantified, and wrap in generic quantifier if not
        (b) wrap in "unknown" event
    (2) Creating a new GTOP handle and set it to be QEQ to the SEMENT's previous LTOP
    (3) Overwriting all EQs to one representative value
    (4) Constrain all hi-handles in QEQ relationships to be of type h

    Args:
        pogg_config (POGGConfig): POGGConfig object that contains information about the SEMI and variable labeler
        sement (SEMENT): SEMENT to prepare to be sent to the ERG for generation
    """

    # duplicate sement to avoid editing the original
    unprepared_sement = sement_util.duplicate_sement(sement)


    if sement.index[0] != "e":
        # check if quantified, wrap in one if not
        if not sement_util.check_if_quantified(unprepared_sement):
            quant_sement = create_base_SEMENT(pogg_config, "def_udef_a_q")
            quantified_sement = op_scopal_quantifier(quant_sement, unprepared_sement)
        else:
            quantified_sement = sement

        # wrap in "unknown" event
        unknown_sement = create_base_SEMENT(pogg_config, "unknown")
        e_type_sement = op_non_scopal_functor_hook(unknown_sement, quantified_sement, "ARG")
    else:
        e_type_sement = unprepared_sement

    # wrap with GTOP
    gtop = pogg_config.var_labeler.get_var_name("h")
    new_hcon = mrs.HCons(gtop, "qeq", e_type_sement.top)

    # change top and add hcon
    e_type_sement.top = gtop
    e_type_sement.hcons.append(new_hcon)

    # go through all handle constraints, if any variable is not of type h, add another EQ
    # e.g. if the hi argument in an hcon is u1 then add < u1 eq h2 >
    # then when EQs are overwritten the most specific one, h2, is chosen
    for hcon in e_type_sement.hcons:
        if hcon.hi[0] != "h":
            new_h = pogg_config.var_labeler.get_var_name("h")
            e_type_sement.eqs.append((new_h, hcon.hi))
            e_type_sement.variables[new_h] = {}
        if hcon.lo[0] != "h":
            new_h = pogg_config.var_labeler.get_var_name("h")
            e_type_sement.eqs.append((new_h, hcon.lo))
            e_type_sement.variables[new_h] = {}

    final_sement = sement_util.overwrite_eqs(e_type_sement)
    return final_sement




