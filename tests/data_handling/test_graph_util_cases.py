import os
import json
import networkx as nx
from pytest_cases import case

class BuildGraph:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_util.POGGGraphUtil.build_graph

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a path to a graph in JSON format, a gold graph, and compare the result of build_graph to the gold
    """

    """
    SUCCESS CASES
        1. one graph JSON that covers all build_graph branches...
            - node with 'node_properties'
            - node without 'node_properties'
            - node with 'lexicon_key'
            - node without 'lexicon_key'
            - edge with parent node not already in nodes (so it has to be added)
            - edge with child node not already in nodes (so it has to be added)
            - edge with 'edge_properties'
            - edge without 'edge_properties'
            - edge with 'lexicon_key'
            - edge without 'lexicon_key'
    """

    @staticmethod
    def case_full_coverage_graph(data_handling_test_dir):
        json_graph_file = os.path.join(data_handling_test_dir, "full_build_graph_coverage.json")
        gold_graph_dot_file = os.path.join(data_handling_test_dir, "full_build_graph_coverage.dot")

        json_graph = json.load(open(json_graph_file))
        gold_nx_graph = nx.nx_pydot.read_dot(gold_graph_dot_file)

        return json_graph, gold_nx_graph


class FindRoot:
    """
    FUNCTION BEING TESTED:
        - pogg.data_handling.graph_util.POGGGraphUtil.find_root

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a NetworkX directed graph, the expected result of find_root (which is a tuple of values: the node ID and its properties), and compare result to expected root
    """

    """
    SUCCESS CASES
        1. root is marked with node property
        2. root is not marked, found using topological sort 
        3. root is not marked and graph has a cycle, topological sort can't be used so find node with in-degree 0 
        4. no root found, but no exception raised, root is None 
        
    FAILURE CASES
        1. more than one node marked as root, raise ValueError 
        2. more than one node with in-degree 0, raise ValueError
    """

    @staticmethod
    @case(tags="success")
    def case_root_marked(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "full_build_graph_coverage.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        gold_root = ('idCar1', {'lexicon_key': 'idCar', 'node_type': 'entity', 'root': 'root'})

        return nx_graph, gold_root

    @staticmethod
    @case(tags="success")
    def case_root_not_marked(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "small_red_car_no_root.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        gold_root = ('idCar1', {'lexicon_key': 'idCar', 'node_type': 'entity'})

        return nx_graph, gold_root

    @staticmethod
    @case(tags="success")
    def case_root_not_marked_extra_newline(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "small_red_car_no_root_extra_newline.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        gold_root = ('idCar1', {'lexicon_key': 'idCar', 'node_type': 'entity'})

        return nx_graph, gold_root

    @staticmethod
    @case(tags="success")
    def case_rooted_graph_with_cycle(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "rooted_graph_with_cycle.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        gold_root = ('idCar1', {'lexicon_key': 'idCar', 'node_type': 'entity'})

        return nx_graph, gold_root

    @staticmethod
    @case(tags="success")
    def case_no_root_candidate(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "no_root_candidate.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        return nx_graph, None

    @staticmethod
    @case(tags="failure")
    def case_double_root_marked(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "double_root_failure.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        return nx_graph

    @staticmethod
    @case(tags="failure")
    def case_double_root_with_cycle(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "double_rooted_graph_with_cycle.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)

        return nx_graph



class ReadFromDot:
    @staticmethod
    def case_dot_file(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "full_build_graph_coverage.dot")
        return graph_file

class WriteTo:
    @staticmethod
    def case_graph(data_handling_test_dir):
        graph_file = os.path.join(data_handling_test_dir, "full_build_graph_coverage.dot")
        nx_graph = nx.nx_pydot.read_dot(graph_file)
        return nx_graph