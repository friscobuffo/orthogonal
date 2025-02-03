from shape_builder import build_shape
from example_graphs import all_example_graphs_indexes, get_example_graph
from shape_to_positions import shape_to_nodes_positions_gurobi
from position_to_drawing import nodes_positions_to_drawing
from graph import Graph

from ordering_to_positions import shape_to_positions_ordering

from time import sleep

def make_orthogonal_draw(graph: Graph, draw_to_screen: bool):
    print("building shape...")
    shape = build_shape(graph)
    if shape:
        print("shape built")

        # print("building positions with gurobi")
        # nodes_positions_gurobi = shape_to_nodes_positions_gurobi(graph, shape)
        # if draw_to_screen:
        #     nodes_positions_to_drawing(graph, nodes_positions_gurobi, "Orthogonal Drawing with Gurobi")

        print("building positions with equivalence classes")
        nodes_positions_eq_classes = shape_to_positions_ordering(shape)
        if draw_to_screen:
            nodes_positions_to_drawing(graph, nodes_positions_eq_classes, "Orthogonal Drawing with Equivalence Classes")

        print("finished...\n\n\n\n")

if __name__ == "__main__":
    for i in all_example_graphs_indexes():
        graph = get_example_graph(i)
        make_orthogonal_draw(graph, True)
        sleep(.5)