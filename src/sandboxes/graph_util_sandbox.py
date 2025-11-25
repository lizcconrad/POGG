import os
import json
import networkx as nx
from pogg.data_handling.graph_util import POGGGraphUtil

data_dir = "../../tests/test_data/data_handling"

graph_json = json.load(open(os.path.join(data_dir, "small_red_car.json")))
test_graph = POGGGraphUtil.build_graph(graph_json)

POGGGraphUtil.write_graph_to_dot(test_graph, os.path.join(data_dir, "small_red_car_written_dot.dot"))
POGGGraphUtil.write_graph_to_png(test_graph, os.path.join(data_dir, "small_red_car.png"))
POGGGraphUtil.write_graph_to_svg(test_graph, os.path.join(data_dir, "small_red_car.svg"))