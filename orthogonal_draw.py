from shape_builder import build_shape
from example_graphs import all_example_graphs_indexes, get_example_graph
from shape_to_positions import shape_to_nodes_positions
from position_to_drawing import nodes_positions_to_drawing
from graph import Graph

def make_orthogonal_draw(graph: Graph):
    print("building shape...")
    shape = build_shape(graph)
    if shape:
        print("shape built")
        print("building positions")
        nodes_positions = shape_to_nodes_positions(graph, shape)
        print("positions built")
        if nodes_positions:
            nodes_positions_to_drawing(graph, nodes_positions)
        else:
            print("ERROR: admissible shape but drawing not found")
        print("finished...\n\n\n\n")

if __name__ == "__main__":
    for i in all_example_graphs_indexes():
        graph = get_example_graph(i)
        make_orthogonal_draw(graph)
        input("press enter key to continue...")