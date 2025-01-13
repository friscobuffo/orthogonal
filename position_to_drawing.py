from graph import Graph

# import matplotlib.pyplot as plt

# def nodes_positions_to_drawing(graph: Graph, nodes_positions: dict):
#     # draw nodes
#     for node in range(graph.size()):
#         plt.plot(nodes_positions[node][0], nodes_positions[node][1], 'o', color=graph.nodes_color[node], markersize=8)
#         plt.text(nodes_positions[node][0], nodes_positions[node][1], str(node), fontsize=15, ha='right')
#     # draw edges
#     for node in range(graph.size()):
#         for neighbor in graph.get_neighbors(node):
#             if neighbor > node:
#                 plt.plot([nodes_positions[node][0], nodes_positions[neighbor][0]], [nodes_positions[node][1], nodes_positions[neighbor][1]], 'b-')
#     plt.title("Orthogonal Drawing")
#     plt.show()

import plotly.graph_objects as go

def nodes_positions_to_drawing(graph: Graph, nodes_positions: dict):
    fig = go.Figure()
    # draw edges
    for node in range(graph.size()):
        for neighbor in graph.get_neighbors(node):
            if neighbor > node:
                x_coords = [nodes_positions[node][0], nodes_positions[neighbor][0]]
                y_coords = [nodes_positions[node][1], nodes_positions[neighbor][1]]
                fig.add_trace(go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode='lines',
                    line=dict(color='blue', width=5),
                    name=f'Edge {node}-{neighbor}',
                    showlegend=False
                ))
    # draw nodes
    for node in range(graph.size()):
        x, y = nodes_positions[node]
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            text=str(node),
            textposition='top right',
            marker=dict(color=graph.nodes_color[node], size=20),
            name=f'Node {node}'
        ))
    fig.update_layout(
        title='Orthogonal Drawing',
        xaxis=dict(title='X-axis', showgrid=False, zeroline=False),
        yaxis=dict(title='Y-axis', showgrid=False, zeroline=False),
        showlegend=False,
        template='plotly_white'
    )
    fig.show()