import unittest
from copy import deepcopy
from delphin import mrs
from pogg.semantic_composition.sement_util import SEMENT
import pogg.my_delphin.sementcodecs as sement


class TestCodecs(unittest.TestCase):

    def setUp(self):
        # Example sement that is mocked below
        self.gold_full_encoding = """
        [ TOP: h0
            INDEX: e1 [ e NUM: sg ]
            RELS: < [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13 ]
                [ _cookie_n_1 LBL: h6 ARG0: x7 ]
                [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ] >
            HCONS: < h12 qeq h6 >
            EQS: < x11 eq x7 x7 eq i2 >
            SLOTS: < ARG2: u3 ARG3: i4 > ]
        """

        self.gold_no_varprop_encoding = """
        [ TOP: h0
            INDEX: e1
            RELS: < [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13 ]
                [ _cookie_n_1 LBL: h6 ARG0: x7 ]
                [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ] >
            HCONS: < h12 qeq h6 >
            EQS: < x11 eq x7 x7 eq i2 >
            SLOTS: < ARG2: u3 ARG3: i4 > ]
        """

        # FIRST SEMENT
        self.top = 'h0'
        self.index = 'e1'

        self.a_ep = mrs.EP('_a_q', 'h10', {'ARG0': 'x11', 'RSTR': 'h12', 'BODY': 'h13'})
        self.cookie_ep = mrs.EP('_cookie_n_1', 'h6', {'ARG0': 'x7'})
        self.give_ep = mrs.EP('_give_v_1', 'h0', {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})
        self.rels_first = [self.a_ep, self.cookie_ep, self.give_ep]

        self.eqs = [('x11', 'x7'), ('x7', 'i2')]
        self.collapsed_eqs = [('x11', 'x7', 'i2')]
        self.slots = {'ARG2': 'u3', 'ARG3': 'i4'}
        self.hcons = [mrs.HCons.qeq('h12', 'h6')]

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        self.sement = SEMENT(self.top, self.index, self.rels_first, self.slots, self.eqs,
                             self.hcons)
        # set a variable property
        self.sement.variables['e1'] = {'NUM': 'sg'}

    def test__encode_eqs(self):
        gold_encoding = "EQS: < x11 eq x7 x7 eq i2 >"

        mock_eqs = sement._encode_eqs(self.sement.eqs)
        # comes as ['EQS: <', ... ], so join them into one string
        mock_eqs_joined = ' '.join(mock_eqs)
        self.assertEqual(gold_encoding, mock_eqs_joined)

    def test__encode_collapsed_eqs(self):
        gold_encoding = "EQS: < x11 eq x7 eq i2 >"

        mock_eqs = sement._encode_eqs(self.collapsed_eqs)
        # comes as ['EQS: <', ... ], so join them into one string
        mock_eqs_joined = ' '.join(mock_eqs)
        self.assertEqual(gold_encoding, mock_eqs_joined)

    def test__encode_eqs_no_eqs(self):
        self.assertEqual(None, sement._encode_eqs(None))

    def test__encode_slots(self):
        gold_encoding = "SLOTS: < ARG2: u3 ARG3: i4 >"

        mock_slots = sement._encode_slots(self.sement.slots)
        # comes as ['SLOTS: <', ... ], so join them into one string
        mock_slots_joined = ' '.join(mock_slots)
        self.assertEqual(gold_encoding, mock_slots_joined)

    def test__encode_eqs_no_slots(self):
        self.assertEqual(None, sement._encode_slots(None))

    def test__encode_sement(self):
        mock_full_encoding = sement._encode_sement(self.sement, properties=True, lnk=True, indent=True)
        self.assertEqual(self.gold_full_encoding.split(), mock_full_encoding.split())

    def test__encode(self):
        mock_full_encoding = sement._encode([self.sement], properties=True, lnk=True, indent=True)
        self.assertEqual(self.gold_full_encoding.split(), mock_full_encoding.split())

    def test_encode(self):
        mock_full_encoding = sement.encode(self.sement, properties=True, lnk=True, indent=True)
        self.assertEqual(self.gold_full_encoding.split(), mock_full_encoding.split())

    def test_encode_false_options(self):
        mock_full_encoding = sement.encode(self.sement, properties=False, lnk=False, indent=False)
        self.assertEqual(self.gold_no_varprop_encoding.split(), mock_full_encoding.split())

