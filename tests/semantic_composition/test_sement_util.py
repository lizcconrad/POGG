import pytest
import re
from pytest_cases import parametrize_with_cases
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_sement_util_cases import *


class TestSEMENTUtilFunctions:
    """
    Tests POGGSEMENTUtil functions
    """

    @staticmethod
    @parametrize_with_cases("sement, property_name, property_value, gold_changed_var", cases=AddIntrinsicVariableProperty)
    def test_add_intrinsic_variable_property(sement, property_name, property_value, gold_changed_var):
        POGGSEMENTUtil.add_intrinsic_variable_property(sement, property_name, property_value)
        assert sement.variables[gold_changed_var][property_name] == property_value

    @staticmethod
    @parametrize_with_cases("sement, gold_key_rel_pred", cases=GetKeyRel, has_tag="success")
    def test_get_key_rel(sement, gold_key_rel_pred):
        key_rel = POGGSEMENTUtil.get_key_rel(sement)
        assert key_rel.predicate == gold_key_rel_pred

    @staticmethod
    @parametrize_with_cases("sement", cases=GetKeyRel, has_tag="failure")
    def test_get_key_rel_no_key_rel(sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.get_key_rel(sement)

    @staticmethod
    @parametrize_with_cases("sement", cases=DuplicateSement)
    def test_duplicate_sement(sement):
        duplicate_sement = POGGSEMENTUtil.duplicate_sement(sement)

        assert sement == duplicate_sement, "Duplicated SEMENT does not match original"
        # assert Object ids are different
        assert id(sement.rels) != id(duplicate_sement.rels), "IDs for RELS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy"
        assert id(sement.slots) != id(duplicate_sement.slots), "IDs for SLOTS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy"
        assert id(sement.eqs) != id(duplicate_sement.eqs), "IDs for EQs list on both original and duplicate SEMENT match, indicating pass by reference and not a copy"
        assert id(sement.hcons) != id(duplicate_sement.hcons), "IDs for HCONS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy"
        assert id(sement.icons) != id(duplicate_sement.icons), "IDs for ICONS list on both original and duplicate SEMENT match, indicating pass by reference and not a copy"

    @staticmethod
    @parametrize_with_cases("eqs, gold_eqs", cases=GroupEqualities)
    def test_group_equalities(eqs, gold_eqs):
        grouped_eqs = POGGSEMENTUtil.group_equalities(eqs)

        assert len(grouped_eqs) == len(gold_eqs)

        for grouped_eq in grouped_eqs:
            assert grouped_eq in gold_eqs

    @staticmethod
    @parametrize_with_cases("vars, gold_most_specified", cases=GetMostSpecifiedVariable)
    def test_get_most_specified_variable_with_list(vars, gold_most_specified):
        most_specified_var = POGGSEMENTUtil.get_most_specified_variable(vars)
        assert most_specified_var == gold_most_specified


    @staticmethod
    @parametrize_with_cases("eqs_list", cases=OverwriteEqs, has_tag="eqs")
    def test_overwrite_eqs(eqs_list):
        for item in eqs_list:
            set_item = set(item)
            assert len(set_item) == 1, "Not all vars are equal: {}".format(item)

    @staticmethod
    @parametrize_with_cases("hcons, gold_hcons", cases=OverwriteEqs, has_tag="hcons")
    def test_overwrite_eqs_hcons(hcons, gold_hcons):
        assert hcons == gold_hcons

    @staticmethod
    @parametrize_with_cases("icons, gold_icons", cases=OverwriteEqs, has_tag="icons")
    def test_overwrite_eqs_icons(icons, gold_icons):
        assert icons == gold_icons

    @staticmethod
    @parametrize_with_cases("original_sement, new_sement", cases=OverwriteEqs, has_tag="empty")
    def test_overwrite_eqs_empty(original_sement, new_sement):
        assert original_sement == new_sement

    @staticmethod
    @parametrize_with_cases("pre_rewrite_eqs, post_rewrite_eqs", cases=OverwriteEqs, has_tag="preservation")
    def test_overwrite_eqs_preservation(pre_rewrite_eqs, post_rewrite_eqs):
        assert pre_rewrite_eqs == post_rewrite_eqs


    @staticmethod
    @parametrize_with_cases("sement", cases=CheckIfQuantified, has_tag="true")
    def test_check_is_quantified_true(sement):
        assert POGGSEMENTUtil.check_if_quantified(sement)

    @staticmethod
    @parametrize_with_cases("sement", cases=CheckIfQuantified, has_tag="false")
    def test_check_is_quantified_false(sement):
        assert not POGGSEMENTUtil.check_if_quantified(sement)


    @staticmethod
    @parametrize_with_cases("sement1, sement2, result", cases=IsSementIsomorphic)
    def test_is_sement_isomorphic(sement1, sement2, result):
        assert POGGSEMENTUtil.is_sement_isomorphic(sement1, sement2) == result


    @staticmethod
    @parametrize_with_cases("sement, gold_roles_dict", cases=CreateVariableRolesDict, has_tag="success")
    def test_create_variable_roles_dict(sement, gold_roles_dict):
        sement_roles_dict = POGGSEMENTUtil.create_variable_roles_dict(sement)
        assert sement_roles_dict == gold_roles_dict

    @staticmethod
    @parametrize_with_cases("sement", cases=CreateVariableRolesDict, has_tag="failure")
    def test_create_variable_roles_dict_error(sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.create_variable_roles_dict(sement)

    @staticmethod
    @parametrize_with_cases("sement, gold_hcons_list", cases=CreateHConsList, has_tag="success")
    def test_create_hcons_list(sement, gold_hcons_list):
        hcons_list = POGGSEMENTUtil.create_hcons_list(sement)
        assert hcons_list == gold_hcons_list

    @staticmethod
    @parametrize_with_cases("sement", cases=CreateHConsList, has_tag="failure")
    def test_create_hcons_list_error(sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.create_hcons_list(sement)

    @staticmethod
    @parametrize_with_cases("sement, gold_icons_list", cases=CreateIConsList, has_tag="success")
    def test_create_icons_list(sement, gold_icons_list):
        icons_list = POGGSEMENTUtil.create_icons_list(sement)
        assert icons_list == gold_icons_list

    @staticmethod
    @parametrize_with_cases("sement", cases=CreateIConsList, has_tag="failure")
    def test_create_icons_list_error(sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.create_icons_list(sement)

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement, gold_overlap_slots, gold_gold_slots, gold_actual_slots",
                            cases=FindSlotOverlaps, has_tag="success")
    def test_find_slot_overlaps(gold_sement, actual_sement, gold_overlap_slots, gold_gold_slots, gold_actual_slots):
        test_overlap_slots, test_gold_slots, test_actual_slots = POGGSEMENTUtil.find_slot_overlaps(gold_sement, actual_sement)

        assert gold_overlap_slots == test_overlap_slots
        assert gold_gold_slots == test_gold_slots
        assert gold_actual_slots == test_actual_slots

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement", cases=FindSlotOverlaps, has_tag="failure")
    def test_find_slot_overlaps_error(gold_sement, actual_sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.find_slot_overlaps(gold_sement, actual_sement)

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement, gold_overlap_eqs, gold_prop_diff_eqs, gold_gold_eqs, gold_actual_eqs",
                            cases=FindVarEqOverlaps, has_tag="success")
    def test_find_eqs_overlaps(gold_sement, actual_sement, gold_overlap_eqs,
                               gold_prop_diff_eqs, gold_gold_eqs, gold_actual_eqs):
        test_overlap_eqs, test_prop_diffs, test_gold_eqs, test_actual_eqs = POGGSEMENTUtil.find_var_eq_overlaps(gold_sement, actual_sement)

        assert gold_overlap_eqs == test_overlap_eqs
        assert gold_prop_diff_eqs == test_prop_diffs
        assert gold_gold_eqs == test_gold_eqs
        assert gold_actual_eqs == test_actual_eqs

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement", cases=FindVarEqOverlaps, has_tag="failure")
    def test_find_eqs_overlaps_error(gold_sement, actual_sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.find_var_eq_overlaps(gold_sement, actual_sement)

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement, gold_overlap_hcons, gold_gold_hcons, gold_actual_hcons",
                            cases=FindHConsOverlaps, has_tag="success")
    def test_find_hcons_overlaps(gold_sement, actual_sement, gold_overlap_hcons, gold_gold_hcons, gold_actual_hcons):
        test_overlap_hcons, test_gold_hcons, test_actual_hcons = POGGSEMENTUtil.find_hcons_overlaps(gold_sement, actual_sement)

        assert gold_overlap_hcons == test_overlap_hcons
        assert gold_gold_hcons == test_gold_hcons
        assert gold_actual_hcons == test_actual_hcons

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement", cases=FindHConsOverlaps, has_tag="failure")
    def test_find_hcons_overlaps_error(gold_sement, actual_sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.find_hcons_overlaps(gold_sement, actual_sement)

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement, gold_overlap_icons, gold_gold_icons, gold_actual_icons",
                            cases=FindIConsOverlaps, has_tag="success")
    def test_find_icons_overlaps(gold_sement, actual_sement, gold_overlap_icons, gold_gold_icons, gold_actual_icons):
        test_overlap_icons, test_gold_icons, test_actual_icons = POGGSEMENTUtil.find_icons_overlaps(gold_sement,
                                                                                                    actual_sement)

        assert gold_overlap_icons == test_overlap_icons
        assert gold_gold_icons == test_gold_icons
        assert gold_actual_icons == test_actual_icons

    @staticmethod
    @parametrize_with_cases("gold_sement, actual_sement", cases=FindIConsOverlaps, has_tag="failure")
    def test_find_icons_overlaps_error(gold_sement, actual_sement):
        with pytest.raises(ValueError):
            POGGSEMENTUtil.find_icons_overlaps(gold_sement, actual_sement)

    @staticmethod
    @parametrize_with_cases("gold_table, actual_table", cases=BuildTable)
    def test_build_table(gold_table, actual_table):
        gold_chars = [c for c in gold_table if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in actual_table if re.match(r'[^\s=-]', c)]
        assert gold_chars == test_chars


    @staticmethod
    @parametrize_with_cases("sement1, sement2, gold_report", cases=BuildIsomorphismReport)
    def test_build_isomorphism_report(sement1, sement2, gold_report):
        test_report = POGGSEMENTUtil.build_isomorphism_report(sement1, sement2)

        gold_chars = [c for c in gold_report if re.match(r'[^\s=-]', c)]
        test_chars = [c for c in test_report if re.match(r'[^\s=-]', c)]
        assert gold_chars == test_chars, test_report