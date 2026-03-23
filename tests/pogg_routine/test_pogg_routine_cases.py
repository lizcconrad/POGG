import os
import shutil
import yaml
from pytest_cases import case
from pogg.pogg_routine import POGG
import networkx as nx

# assume sementcodecs works
import pogg.my_delphin.sementcodecs as sementcodecs

"""
NOTE: FIXTURES COME FROM THE fixtures.py FILE IN THE SAME DIRECTORY AS THIS FILE
Each "case" in this file will modify things where needed and return necessary information for the tests
"""


class RunPOGGDataToTextAlgorithm:
    """
    FUNCTION BEING TESTED:
        - pogg.pogg_routine.POGG.run_POGG_data_to_text_algorithm

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a POGG object, expected location for eval results, and a location for the gold evaluation data and compare the gold evaluation data to the result
    """

    """
    SUCCESS CASES
        1. sample dataset  

    FAILURE CASES
        2. try storing evaluation report without running conversion algorithm
    """

    @staticmethod
    @case(tags='success')
    def case_sample_dataset(pogg_config_file, dataset_config_file, pogg_routine_test_dir):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        dataset_yaml_info = yaml.load(open(dataset_config_file), Loader=yaml.FullLoader)
        result_eval_dir = os.path.join(dataset_yaml_info['data_dir'], dataset_yaml_info['data_chunk'], dataset_yaml_info['evaluation_dir'], "single_runs")

        # delete result eval if it exists
        for root, dirs, files in os.walk(result_eval_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

        gold_eval_dir = os.path.join(pogg_routine_test_dir, "gold_evaluation", "single_runs")
        return pogg_obj, result_eval_dir, gold_eval_dir

    @staticmethod
    @case(tags='failure')
    def case_sample_dataset_no_run(pogg_config_file, dataset_config_file):
        # try to store evaluation without running anything
        pogg_obj = POGG(pogg_config_file, dataset_config_file)
        return pogg_obj

class RunPOGGDatatToTextAlgorithmOnSingleGraph:
    """
    FUNCTION BEING TESTED:
        - pogg.pogg_routine.POGG.run_POGG_data_to_text_algorithm_on_single_graph

    GENERAL DESCRIPTION OF TEST CASES:
        Provide a POGG object, a graph name, potentially a graph object, and a dictionary of gold properties to check against
    """

    """
    SUCCESS CASES
        1. graph JSON
        2. NetworkX DiGraph
        3. NetworkX DiGraph, no gold results file
        4. No graph obj
        5. Graph doesn't generate SEMENT

    FAILURE CASES
        2. No graph obj, bad name provided
    """

    @staticmethod
    @case(tags='success')
    def case_simple_graph_json(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        graph_name = "vanilla_cake"
        graph_json = {
            "nodes": {
                "cake": {
                    "lexicon_key": "cake",
                    "node_properties": {
                        "node_type": "entity"
                    }
                },
                "vanilla": {
                    "lexicon_key": "vanilla",
                    "node_properties": {
                        "node_type": "property"
                    }
                }
            },
            "edges": [
                {
                    "edge_name": "flavor",
                    "parent_node": "cake",
                    "child_node": "vanilla",
                    "lexicon_key": "flavor",
                    "edge_properties": {
                        "edge_type": "property"
                    }
                }
            ]
        }

        gen_string = """[ TOP: h2                                                                   
           INDEX: x1                                                                 
           RELS: < [ compound LBL: h13 ARG0: e10 [ e PROG: - ] ARG1: u11 ARG2: u12 ] 
                   [ udef_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]                     
                   [ _vanilla_n_1 LBL: h4 ARG0: x3 ]                                 
                   [ _cake_n_1 LBL: h2 ARG0: x1 ] >                                  
           HCONS: < h6 qeq h4 >                                                      
           EQS: < x5 eq x3 h13 eq h9 u12 eq x5 h13 eq h2 u11 eq x1 > ]               
        """

        # doesn't test all properties but good enough
        gold_properties = {
            "node_count": 2,
            "nodes_covered": 2,
            "nodes_included": 2,
            "node_coverage": 1.0,
            "node_inclusion": 1.0,
            "edge_count": 1,
            "edges_covered": 1,
            "edges_included": 1,
            "edge_coverage": 1.0,
            "edge_inclusion": 1.0,
            "gold_output_generation_coverage": 1.0,
            "generated_SEMENT": sementcodecs.decode(gen_string)

        }

        return pogg_obj, graph_name, graph_json, gold_properties

    @staticmethod
    @case(tags='success')
    def case_simple_graph_nx_obj(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        graph_name = "vanilla_cake"

        gen_string = """[ TOP: h2                                                                   
                   INDEX: x1                                                                 
                   RELS: < [ compound LBL: h13 ARG0: e10 [ e PROG: - ] ARG1: u11 ARG2: u12 ] 
                           [ udef_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]                     
                           [ _vanilla_n_1 LBL: h4 ARG0: x3 ]                                 
                           [ _cake_n_1 LBL: h2 ARG0: x1 ] >                                  
                   HCONS: < h6 qeq h4 >                                                      
                   EQS: < x5 eq x3 h13 eq h9 u12 eq x5 h13 eq h2 u11 eq x1 > ]               
                """

        graph = nx.DiGraph()
        graph.add_node("vanilla", lexicon_key="vanilla")
        graph.add_node("cake", lexicon_key="cake")
        graph.add_edge("cake", "vanilla", label="flavor", lexicon_key="flavor")

        # doesn't test all properties but good enough
        gold_properties = {
            "node_count": 2,
            "nodes_covered": 2,
            "nodes_included": 2,
            "node_coverage": 1.0,
            "node_inclusion": 1.0,
            "edge_count": 1,
            "edges_covered": 1,
            "edges_included": 1,
            "edge_coverage": 1.0,
            "edge_inclusion": 1.0,
            "gold_output_generation_coverage": 1.0,
            "generated_SEMENT": sementcodecs.decode(gen_string)

        }

        return pogg_obj, graph_name, graph, gold_properties

    @staticmethod
    @case(tags='success')
    def case_simple_graph_no_gold_file(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        graph_name = "bad_name"

        gen_string = """[ TOP: h2                                                                   
                       INDEX: x1                                                                 
                       RELS: < [ compound LBL: h13 ARG0: e10 [ e PROG: - ] ARG1: u11 ARG2: u12 ] 
                               [ udef_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]                     
                               [ _vanilla_n_1 LBL: h4 ARG0: x3 ]                                 
                               [ _cake_n_1 LBL: h2 ARG0: x1 ] >                                  
                       HCONS: < h6 qeq h4 >                                                      
                       EQS: < x5 eq x3 h13 eq h9 u12 eq x5 h13 eq h2 u11 eq x1 > ]               
                    """

        graph = nx.DiGraph()
        graph.add_node("vanilla", lexicon_key="vanilla")
        graph.add_node("cake", lexicon_key="cake")
        graph.add_edge("cake", "vanilla", label="flavor", lexicon_key="flavor")

        # doesn't test all properties but good enough
        gold_properties = {
            "node_count": 2,
            "nodes_covered": 2,
            "nodes_included": 2,
            "node_coverage": 1.0,
            "node_inclusion": 1.0,
            "edge_count": 1,
            "edges_covered": 1,
            "edges_included": 1,
            "edge_coverage": 1.0,
            "edge_inclusion": 1.0,
            "gold_output_generation_coverage": 0.0,
            "generated_SEMENT": sementcodecs.decode(gen_string)

        }

        return pogg_obj, graph_name, graph, gold_properties

    @staticmethod
    @case(tags='success')
    def case_simple_graph_no_obj(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        graph_name = "vanilla_cake"

        gen_string = """[ TOP: h2                                                                   
               INDEX: x1                                                                 
               RELS: < [ compound LBL: h13 ARG0: e10 [ e PROG: - ] ARG1: u11 ARG2: u12 ] 
                       [ udef_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]                     
                       [ _vanilla_n_1 LBL: h4 ARG0: x3 ]                                 
                       [ _cake_n_1 LBL: h2 ARG0: x1 ] >                                  
               HCONS: < h6 qeq h4 >                                                      
               EQS: < x5 eq x3 h13 eq h9 u12 eq x5 h13 eq h2 u11 eq x1 > ]               
            """

        # doesn't test all properties but good enough
        gold_properties = {
            "node_count": 2,
            "nodes_covered": 2,
            "nodes_included": 2,
            "node_coverage": 1.0,
            "node_inclusion": 1.0,
            "edge_count": 1,
            "edges_covered": 1,
            "edges_included": 1,
            "edge_coverage": 1.0,
            "edge_inclusion": 1.0,
            "gold_output_generation_coverage": 1.0,
            "generated_SEMENT": sementcodecs.decode(gen_string)

        }

        return pogg_obj, graph_name, None, gold_properties

    @staticmethod
    @case(tags='success')
    def case_simple_graph_no_sement(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)

        graph_name = "none"

        graph = nx.DiGraph()
        graph.add_node("tee", lexicon_key="hee")

        # doesn't test all properties but good enough
        gold_properties = {
            "node_count": 1,
            "nodes_covered": 0,
            "nodes_included": 0,
            "node_coverage": 0.0,
            "node_inclusion": 0.0,
            "edge_count": 0,
            "edges_covered": 0,
            "edges_included": 0,
            "edge_coverage": 0.0,
            "edge_inclusion": 0.0,
            "gold_output_generation_coverage": 0.0,
            "generated_SEMENT": None

        }

        return pogg_obj, graph_name, graph, gold_properties

    @staticmethod
    @case(tags='failure')
    def case_fake_graph(pogg_config_file, dataset_config_file):
        pogg_obj = POGG(pogg_config_file, dataset_config_file)
        return pogg_obj, "fake"