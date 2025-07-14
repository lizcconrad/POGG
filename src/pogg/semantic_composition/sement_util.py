# functions to help with constructing and comparing SEMENT structures
from copy import deepcopy
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
import tabulate

def group_equalities(equalities):
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
    eqs = equalities.copy()
    while eqs:
        # pop one eq off the list
        current_eq = eqs.pop()
        # convert to set from tuple
        current_eq = set(current_eq)
        # flag for whether a new group is needed
        need_new = True

        # which already created equality_sets are the eq members found in?
        sets_found_in = []
        for eq_set in equality_sets:
            # if there is an intersection (i.e. any member of the current_eq is in the new_set)
            if current_eq.intersection(eq_set):
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

        # TODO check the icons...???

        # update the variable dictionary to make sure only remaining variables are included
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
        SEMENT: the version of s1 with the EQS overwritten which was used in the actual check
        SEMENT: the version of s2 with the EQS overwritten which was used in the actual check
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
    # return isomorphism check
    return mrs_isomorphism and slots_equivalent


def create_variable_roles_dict(sement):
    """
    Given a SEMENT object, create a dictionary where each key is a variable in the SEMENT
    and the value is the set of semantic roles that variable fills

    Args:
        sement (SEMENT): the SEMENT object

    Returns:
        dict: resulting dictionary mapping variables to sets of semantic roles
    """

    # throw exception if EQs present, only SEMENTs that have had EQs overwritten already should go through this function
    if sement.eqs != None and len(sement.eqs) > 0:
        raise ValueError("SEMENT has uncollappsed EQs: {}, aborting".format(sement.eqs))

    # dict of variables but for storing semantic roles
    variable_roles = {}

    # add top
    variable_roles[sement.top] = {"TOP"}
    variable_roles[sement.index] = {"INDEX"}
    for rel in sement.rels:
        predicate = rel.predicate
        if rel.label in variable_roles:
            variable_roles[rel.label].add("{}.LBL".format(predicate))
        else:
            variable_roles[rel.label] = {"{}.LBL".format(predicate)}

        for arg in rel.args:
            if rel.args[arg] in variable_roles:
                variable_roles[rel.args[arg]].add("{}.{}".format(predicate, arg))
            else:
                variable_roles[rel.args[arg]] = {"{}.{}".format(predicate, arg)}

    # sort the role_sets alphabetically
    for var in variable_roles:
        variable_roles[var] = sorted(variable_roles[var])

    return variable_roles

def create_hcons_list(sement):
    """
    Create a list of HCons entries. Each entry includes the handles that are in the HCons relationship as well as
    the semantic roles those handles occupy to enable easier comparison of existing handle constraints across SEMENTs

    Args:
        sement (SEMENT): the SEMENT object

    Returns:
        list: a list of HCons entries
    """

    # throw exception if EQs present, only SEMENTs that have had EQs overwritten already should go through this function
    if sement.eqs != None and len(sement.eqs) > 0:
        raise ValueError("SEMENT has uncollappsed EQs: {}, aborting".format(sement.eqs))

    variable_roles_dict = create_variable_roles_dict(sement)

    # create a list of hcons labeled with their actual semantic role sets along with the handles themselves
    hcons_list = []

    for hcons in sement.hcons:
        hi_role_set = variable_roles_dict[hcons.hi]
        lo_role_set = variable_roles_dict[hcons.lo]
        hcons_entry = {
            "hi_role_set": hi_role_set,
            "lo_role_set": lo_role_set,
            "hi_var": hcons.hi,
            "lo_var": hcons.lo,
        }
        hcons_list.append(hcons_entry)
    return hcons_list

def find_var_eq_overlaps(gold_sement, actual_sement):
    """
    Produces three lists: overlap_eqs, gold_only_eqs, and actual_only_eqs. The goal is to compare semantic role
    equivalencies across two SEMENTs to detect differences when isomorphism checks fail.

    Each list contains dictionaries that detail sets of semantic roles that are filled by the same variable.
    e.g. {
        "eq_set": {"_a_q.ARG0", "_cat_n_1.ARG0", "_cozy_a_1.ARG1"}
        "gold_var": 'x1',
        "actual_var": 'x2'
    }

    If two SEMENts are isomorphic, the gold_only_eqs and actual_only_eqs lists will be empty, but when the SEMENTs are
    not isomorphic, the sets of semantic role equivalencies will not match so these lists will help pinpoint where
    the differences lie.

    Args:
        gold_sement (SEMENT): one of the SEMENTs being compared, nominally the "gold" one that the actual aims to match
        actual_sement (SEMENT): one of the SEMENTs being compared, nominally the one produced by the system

    Returns:
        list: list of overlapping semantic role equivalencies
        list: list of semantic role equivalencies only present in the gold_sement
        list: list of semantic role equivalencies only present in the actual_sement
    """

    overlap_eqs = []
    gold_eqs = []
    actual_eqs = []

    # throw exception if EQs present, only SEMENTs that have had EQs overwritten already should go through this function
    if (gold_sement.eqs != None and len(gold_sement.eqs) > 0):
        raise ValueError("Gold SEMENT has uncollappsed EQs: {}, aborting".format(gold_sement.eqs))
    if (actual_sement.eqs != None and len(actual_sement.eqs) > 0):
        raise ValueError("Actual SEMENT has uncollappsed EQs: {}, aborting".format(actual_sement.eqs))

    # make the variable_roles dicts
    gold_variable_roles = create_variable_roles_dict(gold_sement)
    actual_variable_roles = create_variable_roles_dict(actual_sement)

    for gold_var in gold_variable_roles:
        role_set = gold_variable_roles[gold_var]

        # check for regular variable equivalence overlap
        found_overlap = False
        for actual_var in actual_variable_roles:
            if actual_variable_roles[actual_var] == role_set:
                overlap_eq = {
                    "eq_set": role_set,
                    "gold_var": gold_var,
                    "actual_var": actual_var,
                }

                overlap_eqs.append(overlap_eq)
                found_overlap = True
                # delete from remaining actual_variable_roles if equivalence found
                del actual_variable_roles[actual_var]
                break
        if not found_overlap:
            gold_eq = {
                "eq_set": role_set,
                "gold_var": gold_var
            }
            gold_eqs.append(gold_eq)

    for actual_var in actual_variable_roles:
        actual_eq = {
            "eq_set": actual_variable_roles[actual_var],
            "actual_var": actual_var,
        }
        actual_eqs.append(actual_eq)

    # sort each eq_list
    # sort first by length of the eq_set then alphabetically by first item in eq_set
    # TODO: is making it negative insane ?!?! ... i don't see how to reverse the order for just One of the properties
    sorter = lambda eq_entry: (len(eq_entry["eq_set"]) * -1, eq_entry["eq_set"][0])
    sorted_overlap_eqs = sorted(overlap_eqs, key=sorter)
    sorted_gold_eqs = sorted(gold_eqs, key=sorter)
    sorted_actual_eqs = sorted(actual_eqs, key=sorter)

    return sorted_overlap_eqs, sorted_gold_eqs, sorted_actual_eqs

def find_hcons_overlaps(gold_sement, actual_sement):
    """
    Produces three lists: overlap_hcons, gold_only_hcons, and actual_only_hcons. The goal is to compare semantic role
    equivalencies across two SEMENTs to detect differences when isomorphism checks fail.

    Each list contains dictionaries that detail which handle constraints are present in which SEMENT.
    e.g. {
        "hi_role_set": {"_a_q.RSTR"},
        "lo_role_set": {"_cookie_n_1.LBL", "_tasty_a_1.LBL"},
        "hi_gold_var": "h0",
        "lo_gold_var": "h1",
        "hi_actual_var": "h00",
        "lo_actual_var": "h01",
    }

    If two SEMENts are isomorphic, the gold_only_hcons and actual_only_hcons lists will be empty, but when the SEMENTs are
    not isomorphic, the sets of handle constraints may not match so these lists will help pinpoint where any differences lie.

    Args:
        gold_sement (SEMENT): one of the SEMENTs being compared, nominally the "gold" one that the actual aims to match
        actual_sement (SEMENT): one of the SEMENTs being compared, nominally the one produced by the system

    Returns:
        list: list of overlapping handle constraints
        list: list of handle constraints only present in the gold_sement
        list: list of handle constraints only present in the actual_sement
    """

    # throw exception if EQs present, only SEMENTs that have had EQs overwritten already should go through this function
    if (gold_sement.eqs != None and len(gold_sement.eqs) > 0):
        raise ValueError("Gold SEMENT has uncollappsed EQs: {}, aborting".format(gold_sement.eqs))
    if (actual_sement.eqs != None and len(actual_sement.eqs) > 0):
        raise ValueError("Actual SEMENT has uncollappsed EQs: {}, aborting".format(actual_sement.eqs))

    gold_hcons_list = create_hcons_list(gold_sement)
    actual_hcons_list = create_hcons_list(actual_sement)

    overlap_hcons = []
    gold_hcons = []
    actual_hcons = []

    for gold_entry in gold_hcons_list:
        gold_hi = gold_entry["hi_role_set"]
        gold_lo = gold_entry["lo_role_set"]

        found_overlap = False
        to_remove = None
        for actual_entry in actual_hcons_list:
            actual_hi = actual_entry["hi_role_set"]
            actual_lo = actual_entry["lo_role_set"]

            if gold_hi == actual_hi and gold_lo == actual_lo:
                overlap_hcon = {
                    "hi_role_set": gold_hi,
                    "lo_role_set": gold_lo,
                    "gold_hi_var": gold_entry["hi_var"],
                    "gold_lo_var": gold_entry["lo_var"],
                    "actual_hi_var": actual_entry["hi_var"],
                    "actual_lo_var": actual_entry["lo_var"],

                }
                overlap_hcons.append(overlap_hcon)

                found_overlap = True
                to_remove = actual_entry
                break

        if not found_overlap:
            gold_hcon = {
                "hi_role_set": gold_hi,
                "lo_role_set": gold_lo,
                "gold_hi_var": gold_entry["hi_var"],
                "gold_lo_var": gold_entry["lo_var"],
            }
            gold_hcons.append(gold_hcon)
        else:
            actual_hcons_list.remove(to_remove)

    for actual_entry in actual_hcons_list:
        actual_hcon = {
            "hi_role_set": actual_entry["hi_role_set"],
            "lo_role_set": actual_entry["lo_role_set"],
            "actual_hi_var": actual_entry["hi_var"],
            "actual_lo_var": actual_entry["lo_var"],
        }
        actual_hcons.append(actual_hcon)

    # sort each eq_list
    # sort first by length of the hi_role_set, then lo_role_set, then then alphabetically by first item in hi_role_set
    # TODO: is making it negative insane ?!?! ... i don't see how to reverse the order for just One of the properties
    sorter = lambda hcon_entry: (len(hcon_entry["hi_role_set"]) * -1, len(hcon_entry["lo_role_set"]) * -1, hcon_entry["hi_role_set"][0])
    sorted_overlap_hcons = sorted(overlap_hcons, key=sorter)
    sorted_gold_hcons = sorted(gold_hcons, key=sorter)
    sorted_actual_hcons = sorted(actual_hcons, key=sorter)

    return sorted_overlap_hcons, sorted_gold_hcons, sorted_actual_hcons


def _build_overlap_eqs_table(overlap_eqs):
    """
    Make a table that displays which semantic role equivalence sets are present in two SEMENTs

    Args:
        overlap_eqs (list): list of semantic role equivalencies present in two SEMENTs

    Returns:
        str: table representation of overlapping semantic role equivalencies
    """

    overlap_eq_table = []
    overlap_eq_table_headers = ["Role Set", "Gold Var", "Actual Var"]
    for overlap_eq in overlap_eqs:
        overlap_eq_table.append([overlap_eq["eq_set"], overlap_eq["gold_var"], overlap_eq["actual_var"]])

    return tabulate.tabulate(overlap_eq_table, overlap_eq_table_headers)


def _build_nonoverlap_eqs_table(nonoverlap_eqs, table_type):
    """
    Make a table that displays which semantic role equivalence sets are only present in one SEMENT

    Args:
        nonoverlap_eqs (list): list of semantic role equivalencies present in one SEMENT
        table_type (str): type of table, either Gold or Actual

    Returns:
        str: table representation of nonoverlapping semantic role equivalencies
    """
    if table_type.lower() == "gold":
        type_header = "Gold Var"
        type_key = "gold_var"
    else:
        type_header = "Actual Var"
        type_key = "actual_var"

    # make table for overlap
    nonoverlap_eq_table = []
    nonoverlap_eq_table_headers = ["Role Set", type_header]
    for nonoverlap_eq in nonoverlap_eqs:
        nonoverlap_eq_table.append([nonoverlap_eq["eq_set"], nonoverlap_eq[type_key]])
    return tabulate.tabulate(nonoverlap_eq_table, nonoverlap_eq_table_headers)

def _build_overlap_hcons_table(overlap_hcons):
    """
    Make a table that displays which handle constraints are present in two SEMENTs

    Args:
        overlap_hcons (list): list of handle constraints present in two SEMENTs

    Returns:
        str: table representation of overlapping handle constraints
    """

    overlap_hcons_table = []
    overlap_hcons_table_headers = ["Hi Role Set", "Lo Role Set", "Gold QEQ", "Actual QEQ"]
    for overlap_hcon in overlap_hcons:
        hi_role_set = overlap_hcon["hi_role_set"]
        lo_role_set = overlap_hcon["lo_role_set"]
        gold_qeq = "{} qeq {}".format(overlap_hcon["gold_hi_var"], overlap_hcon["gold_lo_var"])
        actual_qeq = "{} qeq {}".format(overlap_hcon["actual_hi_var"], overlap_hcon["actual_lo_var"])
        overlap_hcons_table.append([hi_role_set, lo_role_set, gold_qeq, actual_qeq])
    return tabulate.tabulate(overlap_hcons_table, overlap_hcons_table_headers)


def _build_nonoverlap_hcons_table(nonoverlap_hcons, table_type):
    """
    Make a table that displays which handle constraints are only present in one SEMENT

    Args:
        nonoverlap_hcons (list): list of handle constraints present in one SEMENT
        table_type (str): type of table, either Gold or Actual

    Returns:
        str: table representation of nonoverlapping handle constraints
    """
    if table_type.lower() == "gold":
        type_header = "Gold QEQ"
        type_key_hi = "gold_hi_var"
        type_key_lo = "gold_lo_var"
    else:
        type_header = "Actual QEQ"
        type_key_hi = "actual_hi_var"
        type_key_lo = "actual_lo_var"

    # make table for nonoverlapping handle constraints
    nonoverlap_hcons_table = []
    nonoverlap_hcons_table_headers = ["Hi Role Set", "Lo Role Set", type_header]
    for nonoverlap_hcon in nonoverlap_hcons:
        hi_role_set = nonoverlap_hcon["hi_role_set"]
        lo_role_set = nonoverlap_hcon["lo_role_set"]
        nonoverlap_qeq = "{} qeq {}".format(nonoverlap_hcon[type_key_hi], nonoverlap_hcon[type_key_lo])
        nonoverlap_hcons_table.append([hi_role_set, lo_role_set, nonoverlap_qeq])

    return tabulate.tabulate(nonoverlap_hcons_table, nonoverlap_hcons_table_headers)

def build_isomorphism_report(gold_sement, actual_sement):
    """
    Print a report detailing which semantic role equivalencies and handle constraints are present in two SEMENTs.
    If two SEMENTs are not isomorphic, this can be used to pinpoint where the mismatch lies.

    Args:
        gold_sement (SEMENT): a SEMENT, nominally the gold one
        actual_sement (Sement): a SEMENT, nominally the one to compare to the gold

    Returns:
        str: the isomorphism report
    """

    # collapse EQs before starting
    gold_sement_collapsed = overwrite_eqs(gold_sement)
    actual_sement_collapsed = overwrite_eqs(actual_sement)

    report = ""

    overlap_eqs, gold_eqs, actual_eqs = find_var_eq_overlaps(gold_sement_collapsed, actual_sement_collapsed)
    overlap_hcons, gold_hcons, actual_hcons = find_hcons_overlaps(gold_sement_collapsed, actual_sement_collapsed)

    report += "SEMANTIC ROLE EQUIVALENCES\n"
    report += "================================\n"
    report += "OVERLAPPING\n"
    report += "{}\n\n".format(_build_overlap_eqs_table(overlap_eqs))
    report += "GOLD ONLY\n"
    report += "{}\n\n".format(_build_nonoverlap_eqs_table(gold_eqs, "gold"))
    report += "ACTUAL ONLY\n"
    report += "{}\n\n\n".format(_build_nonoverlap_eqs_table(actual_eqs, "actual"))

    report += "HANDLE CONSTRAINTS \n"
    report += "=====================\n"
    report += "OVERLAPPING\n"
    report += "{}\n\n".format(_build_overlap_hcons_table(overlap_hcons))
    report += "GOLD ONLY\n"
    report += "{}\n\n".format(_build_nonoverlap_hcons_table(gold_hcons, "gold"))
    report += "ACTUAL ONLY\n"
    report += "{}\n\n".format(_build_nonoverlap_hcons_table(actual_hcons, "actual"))

    return report




