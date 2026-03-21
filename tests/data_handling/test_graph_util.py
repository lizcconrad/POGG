import os
import tempfile
import pytest
import json
import networkx as nx
from pytest_cases import parametrize_with_cases

from pogg.data_handling.graph_util import POGGGraphUtil

# import test case classes
# use the dot to specify that the module should be imported from the same path as *this* module
from .test_graph_util_cases import *


def all_attr_match(x1, x2):
    if len(x1.keys()) != len(x2.keys()):
        return False

    for attr in x1.keys():
        if attr in x2.keys():
            if x1[attr] != x2[attr]:
                return False
        else:
            return False
    return True

def assertGraphIsomorphism(gold_graph, test_graph):
    nm = all_attr_match
    em = all_attr_match
    assert nx.is_isomorphic(gold_graph, test_graph, node_match=nm, edge_match=em)


class TestGraphUtil:
    @staticmethod
    @parametrize_with_cases("json_graph, gold_nx_graph", cases=BuildGraph)
    def test_build_graph(json_graph, gold_nx_graph):
        pogg_nx_graph = POGGGraphUtil.build_graph(json_graph)
        assertGraphIsomorphism(gold_nx_graph, pogg_nx_graph)


    ## FIND ROOT TESTS ##
    @staticmethod
    @parametrize_with_cases("nx_graph, gold_root", cases=FindRoot, has_tag="success")
    def test_find_root(nx_graph, gold_root):
        assert POGGGraphUtil.find_root(nx_graph) == gold_root

    @staticmethod
    @parametrize_with_cases("nx_graph", cases=FindRoot, has_tag="failure")
    def test_find_root_failure(nx_graph):
        with pytest.raises(ValueError):
            POGGGraphUtil.find_root(nx_graph)


    ## I/O TESTS ##
    @staticmethod
    @parametrize_with_cases("graph_file", cases=ReadFromDot)
    def test_read_from_dot(graph_file):
        graph = POGGGraphUtil.read_graph_from_dot(graph_file)
        assert isinstance(graph, nx.DiGraph)

    @staticmethod
    @parametrize_with_cases("nx_graph", cases=WriteTo)
    def test_write_to_dot(nx_graph):
        # only tests that a dot file was written, does not test the contents of the tile
        # fxn just calls the write_to_dot from NetworkX anyway
        # so the contents are the responsibility of that package
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "write_to_dot.dot")

            POGGGraphUtil.write_graph_to_dot(nx_graph, out_file)
            assert os.path.isfile(out_file)

    @staticmethod
    @parametrize_with_cases("nx_graph", cases=WriteTo)
    def test_write_to_png(nx_graph):
        # only tests that a png file was written, does not test the contents of the tile
        # fxn just calls the write_to_png from NetworkX anyway
        # so the contents are the responsibility of that package
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "write_to_png.png")

            POGGGraphUtil.write_graph_to_png(nx_graph, out_file)
            assert os.path.isfile(out_file)

    @staticmethod
    @parametrize_with_cases("nx_graph", cases=WriteTo)
    def test_write_to_svg(nx_graph):
        # only tests that a svg file was written, does not test the contents of the tile
        # fxn just calls the write_to_svg from NetworkX anyway
        # so the contents are the responsibility of that package
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "write_to_svg.svg")

            POGGGraphUtil.write_graph_to_svg(nx_graph, out_file)
            assert os.path.isfile(out_file)

    @staticmethod
    @parametrize_with_cases("nx_graph, gold_json", cases=WriteToJSON)
    def test_write_to_json(nx_graph, gold_json):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "write_to_json.json")

            POGGGraphUtil.write_graph_to_json(nx_graph, out_file)

            assert json.load(open(out_file)) == gold_json




