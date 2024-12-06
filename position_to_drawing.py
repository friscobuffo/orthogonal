from graph import Graph
import matplotlib.pyplot as plt

def nodes_positions_to_drawing(graph: Graph, nodes_positions: dict):
    # draw nodes
    for node in range(graph.size()):
        plt.plot(nodes_positions[node][0], nodes_positions[node][1], 'ro')
    # draw edges
    for node in range(graph.size()):
        for neighbor in graph.get_neighbors(node):
            if neighbor > node:
                plt.plot([nodes_positions[node][0], nodes_positions[neighbor][0]], [nodes_positions[node][1], nodes_positions[neighbor][1]], 'b-')
    plt.show()