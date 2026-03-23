from pytest_cases import fixture
from copy import deepcopy
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
import pogg.my_delphin.sementcodecs as sementcodecs


class TestCodecs:

    @fixture(scope="class")
    def gold_full_encoding(self):
        return """
        [ TOP: h0
            INDEX: e1 [ e NUM: sg ]
            RELS: < [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13 ]
                [ _cookie_n_1 LBL: h6 ARG0: x7 ]
                [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ] >
            HCONS: < h12 qeq h6 >
            EQS: < x11 eq x7 x7 eq i2 >
            SLOTS: < ARG2: u3 ARG3: i4 > ]
        """

    @fixture(scope="class")
    def gold_no_varprop_encoding(self):
        return """
        [ TOP: h0
            INDEX: e1
            RELS: < [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13 ]
                [ _cookie_n_1 LBL: h6 ARG0: x7 ]
                [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ] >
            HCONS: < h12 qeq h6 >
            EQS: < x11 eq x7 x7 eq i2 >
            SLOTS: < ARG2: u3 ARG3: i4 > ]
        """

    @fixture(scope="class")
    def eqs(self):
        return [('x11', 'x7'), ('x7', 'i2')]

    @ fixture(scope="class")
    def collapsed_eqs(self):
        return [('x11', 'x7', 'i2')]

    @fixture(scope="class")
    def slots(self):
        return {'ARG2': 'u3', 'ARG3': 'i4'}

    @fixture(scope="class")
    def sement(self, eqs, slots):
        top = 'h0'
        index = 'e1'

        a_ep = mrs.EP('_a_q', 'h10', {'ARG0': 'x11', 'RSTR': 'h12', 'BODY': 'h13'})
        cookie_ep = mrs.EP('_cookie_n_1', 'h6', {'ARG0': 'x7'})
        give_ep = mrs.EP('_give_v_1', 'h0', {'ARG0': 'e1', 'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'})
        rels_first = [a_ep, cookie_ep, give_ep]

        hcons = [mrs.HCons.qeq('h12', 'h6')]

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        # slots and eqs called from fixtures
        sement = SEMENT(top, index, rels_first, slots, eqs, hcons)
        # set a variable property
        sement.variables['e1'] = {'NUM': 'sg'}

        return sement

    def test__encode_eqs(self, eqs):
        gold_encoding = "EQS: < x11 eq x7 x7 eq i2 >"

        test_eqs = sementcodecs._encode_eqs(eqs)
        # comes as ['EQS: <', ... ], so join them into one string
        test_eqs_joined = ' '.join(test_eqs)
        assert gold_encoding == test_eqs_joined

    def test__encode_collapsed_eqs(self, collapsed_eqs):
        gold_encoding = "EQS: < x11 eq x7 eq i2 >"

        test_eqs = sementcodecs._encode_eqs(collapsed_eqs)
        # comes as ['EQS: <', ... ], so join them into one string
        test_eqs_joined = ' '.join(test_eqs)
        assert gold_encoding == test_eqs_joined

    def test__encode_eqs_no_eqs(self):
        assert None == sementcodecs._encode_eqs(None)

    def test__encode_slots(self, slots):
        gold_encoding = "SLOTS: < ARG2: u3 ARG3: i4 >"

        test_slots = sementcodecs._encode_slots(slots)
        # comes as ['SLOTS: <', ... ], so join them into one string
        test_slots_joined = ' '.join(test_slots)
        assert gold_encoding == test_slots_joined

    def test__encode_eqs_no_slots(self):
        assert None == sementcodecs._encode_slots(None)

    def test__encode_sement(self, gold_full_encoding, sement):
        test_full_encoding = sementcodecs._encode_sement(sement, properties=True, lnk=True, indent=True)
        assert gold_full_encoding.split() == test_full_encoding.split()

    def test__encode(self, gold_full_encoding, sement):
        test_full_encoding = sementcodecs._encode([sement], properties=True, lnk=True, indent=True)
        assert gold_full_encoding.split() == test_full_encoding.split()

    def test_encode(self, gold_full_encoding, sement):
        test_full_encoding = sementcodecs.encode(sement, properties=True, lnk=True, indent=True)
        assert gold_full_encoding.split() == test_full_encoding.split()

    def test_encode_false_options(self, gold_no_varprop_encoding, sement):
        test_full_encoding = sementcodecs.encode(sement, properties=False, lnk=False, indent=False)
        assert gold_no_varprop_encoding.split() == test_full_encoding.split()

