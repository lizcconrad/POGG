import unittest, unittest.mock
from copy import deepcopy
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
import pogg.semantic_composition.sement_util as sement_util


class TestSEMENTUtilFunctions(unittest.TestCase):
    """
    Tests functions included in the semantic algebra
    """
    # SETUP USING ACTUAL SEMENT CLASS
    # TODO: just do a decoding... but I don't have SEMENT decoding implemented yet :/
    def setUp(self):
        # FIRST SEMENT
        self.top_first = 'h0101'
        self.index_first = 'e1101'

        self.a_ep_first = mrs.EP('_a_q', 'h10', {'ARG0': 'x11', 'RSTR': 'h12', 'BODY': 'h13'})
        self.cookie_ep_first = mrs.EP('_cookie_n_1', 'h6', {'ARG0': 'x7'})
        self.give_ep_first = mrs.EP('_give_v_1', 'h0', {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})
        self.rels_first_first = [self.a_ep_first, self.cookie_ep_first, self.give_ep_first]

        self.eqs_first = [('x11', 'x7'), ('x7', 'i2'), ('h0101', 'h0'), ('e1', 'e1101')]
        self.slots_first = {'ARG2': 'u3', 'ARG3': 'i4'}
        self.hcons_first = [mrs.HCons.qeq('h12', 'h6')]

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        self.sement = SEMENT(self.top_first, self.index_first, self.rels_first_first, self.slots_first, self.eqs_first, self.hcons_first)
        # set a variable property
        self.sement.variables['e1'] = {'NUM': 'sg'}

        # SECOND SEMENT #
        self.top_second = 'h011'
        self.index_second = 'e111'

        self.a_ep_second = mrs.EP('_a_q', 'h1011', {'ARG0': 'x1111', 'RSTR': 'h1211', 'BODY': 'h1311'})
        self.cookie_ep_second = mrs.EP('_cookie_n_1', 'h611', {'ARG0': 'x711'})
        self.give_ep_second = mrs.EP('_give_v_1', 'h011', {'ARG0': 'e111', 'ARG1': 'i211', 'ARG2': 'u311', 'ARG3': 'i411'})
        self.rels_second = [self.cookie_ep_second, self.give_ep_second, self.a_ep_second]

        self.eqs_second = [('x1111', 'x711'), ('x711', 'i211')]
        self.slots_second = {'ARG2': 'u311', 'ARG3': 'i411'}
        self.hcons_second = [mrs.HCons.qeq('h1211', 'h611')]

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        self.second_sement = SEMENT(self.top_second, self.index_second, self.rels_second, self.slots_second, self.eqs_second, self.hcons_second)
        self.second_sement.variables['e111'] = {'NUM': 'sg'}

        # "a tasty cookie"
        self.tasty_ep = mrs.EP('_tasty_a_1', 'h20', {'ARG0': 'e21', 'ARG1': 'x22'})
        self.tasty_cookies_top = 'h6'
        self.tasty_cookies_index = 'x7'
        self.tasty_cookies_rels = [self.a_ep_first, self.cookie_ep_first, self.tasty_ep]
        self.tasty_cookies_eqs = [('x7', 'x22', 'x11'), ('h6', 'h20')]
        self.tasty_cookies_hcons = [mrs.HCons.qeq('h10', 'h6')]
        self.tasty_cookies_sement = SEMENT(self.tasty_cookies_top, self.tasty_cookies_index, self.tasty_cookies_rels,
                                           {}, self.tasty_cookies_eqs, self.tasty_cookies_hcons)


    # SETUP USING MOCK
    # def setUp(self):
    #     self.sement = unittest.mock.Mock()
    #
    #     # Example sement that is mocked below
    #     self.gold_full_encoding = """
    #     [ TOP: h0
    #         INDEX: e1
    #         RELS: < [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ]
    #             [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13 ]
    #             [ _cookie_n_1 LBL: h6 ARG0: x7 ] >
    #         HCONS: < h12 qeq h6 >
    #         EQS: < (x11,x7), (x7,i2) >
    #         SLOTS: < ARG2: u3, ARG3: i4 > ]
    #     """
    #
    #     # mock the EPs
    #     self.give = unittest.mock.Mock()
    #     self.give.args = {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'}
    #     self.give.id = 'e1'
    #     self.give.iv = 'e1'
    #     self.give.label = 'h0'
    #     self.give.predicate = '_give_v_1'
    #     self.give.type = 'e'
    #
    #     self.a = unittest.mock.Mock()
    #     self.a.args = {'ARG0': 'x11', 'RSTR': 'h12', 'BODY': 'h13'}
    #     self.a.id = 'x11'
    #     self.a.iv = 'x11'
    #     self.a.label = 'h10'
    #     self.a.predicate = '_a_q'
    #     self.a.type = 'x'
    #
    #     self.cookie = unittest.mock.Mock()
    #     self.cookie.args = {'ARG0': 'x7'}
    #     self.cookie.id = 'x7'
    #     self.cookie.iv = 'x7'
    #     self.cookie.label = 'h6'
    #     self.cookie.predicate = '_cookie_n_1'
    #     self.cookie.type = 'x'
    #
    #     self.sement.top = 'h0'
    #     self.sement.index = 'e1'
    #     self.sement.variables = {}
    #     self.sement.predications = [self.give, self.a, self.cookie]
    #     self.sement.rels = [self.give, self.a, self.cookie]
    #     self.sement.eqs = [(self.a.args['ARG0'], self.cookie.args['ARG0']),
    #                        (self.cookie.args['ARG0'], self.give.args['ARG1'])]
    #
    #     # make a mock hcons
    #     self.sement.hcons_obj.hi = self.a.args['RSTR']
    #     self.sement.hcons_obj.relation = "qeq"
    #     self.sement.hcons_obj.lo = self.cookie.label
    #     self.sement.hcons = [self.sement.hcons_obj]
    #
    #     self.sement.icons = []
    #
    #     # copy args and pop ARG1
    #     give_args = deepcopy(self.give.args)
    #     # delete the intrinsic arg, as it's not a slot
    #     del give_args['ARG0']
    #     # delete the hole that would be filled, in this case ARG1
    #     del give_args['ARG1']
    #     self.sement.slots = give_args

    def test_group_equalities(self):
        eqs = [("x1", "x2"), ("x3", "x4"), ("x1", "x4"), ("x5", "x6")]

        # result of grouping should equal this
        gold_groups = [{"x1", "x2", "x3", "x4"}, {"x5", "x6"}]

        grouped_eqs = sement_util.group_equalities(eqs)

        self.assertCountEqual(gold_groups, grouped_eqs)

    def test_get_most_specified_variable(self):
        vars = ["u1", "i2", "x3"]

        most_specified_var = sement_util.get_most_specified_variable(vars)

        # x3 is most specific
        self.assertEqual(most_specified_var, vars[2])

    def test_overwrite_eqs(self):
        new_sement = sement_util.overwrite_eqs(self.sement)

        # for the sement "give a cookie"
        # the following should all be the same if the overwrite worked:
        # a.ARG0 = cookie.ARG0 = give.ARG1

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_arg0 = r.args['ARG0']
            else:
                give_lbl = r.label
                give_arg0 = r.args['ARG0']
                give_arg1 = r.args['ARG1']


        # original equality check
        self.assertTrue(a_arg0 == cookie_arg0 == give_arg1)
        # make sure TOP is back to being the LBL of cookie
        self.assertTrue(new_sement.top == give_lbl)
        # make sure INDEX is back to being ARG0 of give
        self.assertTrue(new_sement.index == give_arg0)

    def test_overwrite_eqs2(self):
        # checks whether overwrite works when a member of a handle constraint are members of an eq
        # this case was unaccounted for above
        new_sement = sement_util.overwrite_eqs(self.tasty_cookies_sement)

        # for the sement "a tasty cookie"
        # the following should all be the same if the overwrite worked:
        # a.ARG0 = cookie.ARG0 = tasty.ARG1

        for r in new_sement.rels:
            if r.predicate == "_a_q":
                a_arg0 = r.args['ARG0']
            elif r.predicate == "_cookie_n_1":
                cookie_lbl = r.label
                cookie_arg0 = r.args['ARG0']
            else:
                tasty_lbl = r.label
                tasty_arg1 = r.args['ARG1']

        # original equality check
        self.assertTrue(a_arg0 == cookie_arg0 == tasty_arg1)
        # make sure TOP == cookie.lbl == tasty.lbl
        self.assertTrue(new_sement.top == cookie_lbl == tasty_lbl)



    def test_is_sement_isomorphic_true(self):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        self.assertTrue(sement_util.is_sement_isomorphic(self.sement, self.second_sement))


    def test_is_sement_isomorphic_false(self):
        # two SEMENTs for the VP "give a cookie"
        # identical other than the order of RELs and specific numbers for variable values
        # but also the TOP is incorrect in this one (refers to LBL of 'cookie' not 'give')
        # so they should not be isomorphic

        # change top
        self.second_sement.top = self.cookie_ep_second.label
        self.assertFalse(sement_util.is_sement_isomorphic(self.sement, self.second_sement))