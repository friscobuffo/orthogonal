from shape_builder import build_shape
from example_graphs import all_example_graphs_indexes, get_example_graph, generate_random_graph
from shape_to_positions import shape_to_nodes_positions_gurobi
from position_to_drawing import nodes_positions_to_drawing
from graph import Graph

from ordering_to_positions import shape_to_positions_ordering

from time import sleep
import sys

def make_orthogonal_draw(graph: Graph, draw_to_screen: bool):
    print("building shape...")
    cycles = graph.find_all_cycles()
    print("number of used cycles:", len(cycles))
    shape = build_shape(graph, cycles)
    if shape:
        print("shape built")
        try:
            print("building positions with equivalence classes")
            nodes_positions_eq_classes = shape_to_positions_ordering(shape)
            if draw_to_screen:
                nodes_positions_to_drawing(graph, nodes_positions_eq_classes, "Orthogonal Drawing with Equivalence Classes")
        except Exception as e:
            print("Error:")
            print("graph:\n", graph)
            print("shape:\n", shape)
            print("Error:", e)
        print("finished...\n\n\n")        

if __name__ == "__main__":
    args = set(sys.argv[1:])
    draw = "draw" in args
    if "all" in args:
        for i in all_example_graphs_indexes():
            graph = get_example_graph(i)
            make_orthogonal_draw(graph, draw)
            sleep(.5)
    if "random" in args:
        while True:
            graph = generate_random_graph(14, 22)
            make_orthogonal_draw(graph, draw)
            if input("Press enter to continue, or q to quit: ") == "q":
                break