import pytest
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT

class TestSEMENT:
    """
    Tests the SEMENT class.
    """

    @pytest.fixture(scope="class")
    def sement_args(self):
        top = "h10"
        index = "e7"
        rels = [
            mrs.EP("_the_q", "h0", {"ARG0": "x1", "RSTR": "h2", "BODY": "h3"}),
            mrs.EP("_baker_n_1", "h4", {"ARG0": "x5"}),
            mrs.EP("_bake_v_cause", "h6", {"ARG0": "e7", "ARG1": "x8", "ARG2": "x9"})
        ]
        slots = {"ARG1": "x8"}
        eqs = [("x1", "x5"), ("x8", "x5")]
        hcons = [
            mrs.HCons("h2", "qeq", "h4"),
            mrs.HCons("h10", "qeq", "h6"),
        ]
        return {
            "top": top,
            "index": index,
            "rels": rels,
            "slots": slots,
            "eqs": eqs,
            "hcons": hcons,
        }

    @pytest.fixture(scope="class")
    def sement(self, sement_args):
        # make a SEMENT object to assert all fields were set correctly
        # SEMENT is for "the baker bakes" with a slot open for what is being baked
        top = sement_args["top"]
        index = sement_args["index"]
        rels = sement_args["rels"]
        slots = sement_args["slots"]
        eqs = sement_args["eqs"]
        hcons = sement_args["hcons"]
        return SEMENT(top, index, rels, slots, eqs, hcons)


    def test_SEMENT_object(self):
        # assert whether sement object is of the correct type
        sement = SEMENT()
        assert isinstance(sement, SEMENT), "object not of type SEMENT"


    def test_SEMENT_top(self, sement, sement_args):
        # test top got set correctly
        assert sement.top == sement_args["top"]

    def test_SEMENT_index(self, sement, sement_args):
        # test index got set correctly
        assert sement.index == sement_args["index"]

    def test_SEMENT_rels(self, sement, sement_args):
        # test rels got set correctly
        assert sement.rels == sement_args["rels"]

    def test_SEMENT_eqs(self, sement, sement_args):
        # test eqs got set correctly
        assert sement.eqs == sement_args["eqs"]

    def test_SEMENT_hcons(self, sement, sement_args):
        # test hcons got set correctly
        assert sement.hcons == sement_args["hcons"]
