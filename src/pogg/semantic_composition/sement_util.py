# functions to help with constructing and comparing SEMENT structures
from copy import deepcopy
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT


def group_equalities(eqs):
    """
    Group equalities from a list of EQs into lists as opposed to individual equalities
    That is, if x1=x2 and x2=x3 create a set (x1, x2, x3) such that they're in an equality "group"

    Args:
        eqs (list): list of variable equalities (e.g. (x1, x2))

    Returns:
        list of sets: list of sets of equalities
    """

    """
    Example list of EQs prior to overwrite algorithm: ((x1, x2), (x3, x4), (x1, x4), (x5, x6))
    
    Assume sets have already been created from the first two equalities, i.e. (x1, x2) and (x3, x4)
    
    Algorithm proceeds as follows:
        1. pop  eq off the list -- (x1, x4)
        2. look through the already created sets to see if either member of the equality is found in existing sets
            (x1, x2) -- yes, x1 is a member
            (x3, x4) -- yes, x4 is a member 
        3. Add all the sets that contained either member of the current eq 
        4. Remove those sets from the list and create a new set that is the union of all those sets
        
    If none of the sets in the list had either of the eq members, create a new set and add it to the list to be checked 
    against for future eqs 
    
    Result from this example: ({x1, x2, x3, x4}, {x5, x6})
    """

    equality_sets = []
    # as long as there are eqs still not covered
    while eqs:
        # pop one eq off the list
        current_eq = eqs.pop()
        # flag for whether a new group is needed
        need_new = True

        # which already created equality_sets are the eq members found in?
        sets_found_in = []
        for eq_set in equality_sets:
            # if either member is in the new_set, update the set so that it's the union of both
            if current_eq[0] in eq_set or current_eq[1] in eq_set:
                # append eq_set to the list of sets the
                sets_found_in.append(eq_set)
                # and therefore we don't need to create a new set because we found a candidate group
                need_new = False

        # if need_new is True, start a new group
        if need_new:
            equality_sets.append(set(current_eq))
        # else, unionize all sets it was found in and pop extras from equality_sets
        else:
            updated_equality_set = set()
            # update the set
            for s in sets_found_in:
                updated_equality_set.update(s)
                equality_sets.remove(s)
            updated_equality_set.update(current_eq)
            equality_sets.append(updated_equality_set)

    return equality_sets


def get_most_specified_variable(eq_vars):
    """
    Get the most "specific" variable to serve as the representative for the EQ set
    That is, a variable of type x is more specific than one of type i, according to the ERG hierarchy

    Hierarchy:
    u -- unspecific
    i -- subtype of u, underspecified between e and x
    p -- suptype of u, underspecified between h and x
    e -- suptype of i, eventualities (e.g. intrinsic variable of a verb)
    x -- subtype of i and p, instance (e.g. intrinsic variable of a noun)
    h -- subtype of p, handle used for scopal composition

    Args:
        eq_vars (list): list of variables that are equivalent

    Returns:
        str: return the most specific variable from the list
    """
    # this isn't going to check for incompatibilities, I'm assuming those have been handled already
    types = {
        'u': 0,
        'i': 1,
        'p': 1,
        'e': 2,
        'x': 2,
        'h': 2
    }

    most_spec_var = eq_vars[0]
    for var in eq_vars:
        # type is the first char in the string
        # if the type of the current var is more specific than the already chosen one,
        # update the chosen one
        if types[var[0]] > types[most_spec_var[0]]:
            most_spec_var = var
    return most_spec_var


def overwrite_eqs(sement):
    """
    Create a new SEMENT where any variables that are members of an EQ have been overwritten to one representative value

    Args:
        sement (SEMENT): SEMENT structure with unresolved variable equalities

    Returns:
        SEMENT: new SEMENT with resolved variable equalities (i.e. if x1=x2 then all instances of x2 are overwritten to be x1)
    """

    # will be progressively collecting a new list of EPs, HCONS, and EQs, so start with those from the given SEMENT
    current_SEMENT = sement
    current_top = current_SEMENT.top
    current_index = current_SEMENT.index
    current_eps = current_SEMENT.rels
    current_variables = current_SEMENT.variables
    current_hcons = current_SEMENT.hcons
    # group the equalities so if x1=x2 and x2=x3 there's a list of [x1, x2, x3] with all variables that are equivalent
    grouped_eqs = group_equalities(current_SEMENT.eqs)

    for eq in grouped_eqs:
        # need to get the most specific variable of the set
        chosen_var = get_most_specified_variable(list(eq))

        # check the top
        if current_SEMENT.top in eq:
            current_top = chosen_var
        # else:
            # current_top = current_SEMENT.top

        # check the index
        if current_SEMENT.index in eq:
            current_index = chosen_var
        # else:
            # current_index = current_SEMENT.index

        # check the rels
        new_eps = []
        for r in current_eps:
            if r.label in eq:
                new_r_label = chosen_var
            else:
                new_r_label = r.label
            new_r_args = {}
            for arg in r.args:
                if r.args[arg] in eq:
                    new_r_args[arg] = chosen_var
                else:
                    new_r_args[arg] = r.args[arg]
            new_eps.append(mrs.EP(r.predicate, new_r_label, new_r_args))


        # update the EP list with the current ones
        current_eps = new_eps

        # update the variable dictionary
        new_variables = {}
        for var in current_variables:
            if var in eq:
                new_variables[chosen_var] = {}
                # update the new property dictionary with properties from every var in the eq group
                for e in eq:
                    new_variables[chosen_var].update(current_variables[e])
            else:
                new_variables[var] = current_variables[var]
        current_variables = new_variables

        # check the hcons...
        new_hcons = []
        for hcon in current_hcons:
            # is there any chance that the hi of an hcon will be one member of an eq
            # and the lo could be another member of the eq? so both need to be checked/changed?
            # idk but i'm scared so

            # hcon.hi should never be a memeber of an eq, so this condition is not necessary
            # if hcon.hi in eq:
            #     new_hi = chosen_var
            # else:
            #     new_hi = hcon.hi

            if hcon.lo in eq:
                new_lo = chosen_var
            else:
                new_lo = hcon.lo
            new_hcons.append(mrs.HCons(hcon.hi, 'qeq', new_lo))

        current_hcons = new_hcons

        # check the icons...???

    # build new overwritten SEMENT
    # eqs list is gone now
    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    return SEMENT(current_top, current_index, current_eps, current_SEMENT.slots, None, current_hcons, None, current_variables)



# per delphinqa communication
def is_sement_isomorphic(s1: SEMENT, s2: SEMENT) -> bool:
    """
    Check whether two SEMENTs are isomorphic
    i.e. The SEMENTs have the same directed graph structure, but might not be literally identical.
    For example, the EPs in the RELS list may be in different orders.

    Args:
        s1 (SEMENT): first SEMENT
        s2 (SEMENT): second SEMENT

    Returns:
        bool: whether the two SEMENTs are isomorphic
    """

    # overwrite EQs in both SEMENTs for ease of checking isomorphism
    s1_ovrwrit = overwrite_eqs(s1)
    s2_ovrwrit = overwrite_eqs(s2)

    # deepcopy broken right now
    # s1_copy = deepcopy(s1_eq_overwritten)  # don't modify the original
    # s2_copy = deepcopy(s2_eq_overwritten)

    # recreate copies by hand ...
    # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
    s1_copy = SEMENT(s1_ovrwrit.top, s1_ovrwrit.index, s1_ovrwrit.rels, s1_ovrwrit.slots,
                     s1_ovrwrit.eqs, s1_ovrwrit.hcons, s1_ovrwrit.icons, s1_ovrwrit.variables,
                     s1_ovrwrit.lnk, s1_ovrwrit.surface, s1_ovrwrit.identifier)
    s2_copy = SEMENT(s2_ovrwrit.top, s2_ovrwrit.index, s2_ovrwrit.rels, s2_ovrwrit.slots,
                     s2_ovrwrit.eqs, s2_ovrwrit.hcons, s2_ovrwrit.icons, s2_ovrwrit.variables,
                     s2_ovrwrit.lnk, s2_ovrwrit.surface, s2_ovrwrit.identifier)


    # add *top* as a variable
    s1_copy.variables["*top*"] = None
    s2_copy.variables["*top*"] = None

    s1_copy.hcons.append(mrs.HCons.qeq("*top*", s1_copy.top))
    s2_copy.hcons.append(mrs.HCons.qeq("*top*", s2_copy.top))


    mrs_isomorphism = mrs.is_isomorphic(s1_copy, s2_copy)
    # check that both SEMENTs have the same slot keys (not vals tho)
    slots_equivalent = s1_copy.slots.keys() == s2_copy.slots.keys()
    return mrs_isomorphism and slots_equivalent

