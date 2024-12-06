from graph import Graph
from gurobipy import Model, GRB
import gurobipy as gp

def initialize_nodes_variables(model: Model, graph: Graph):
    nodes_x_variables = []
    nodes_y_variables = []
    for node in range(graph.size()):
        nodes_x_variables.append(model.addVar(name=f"x_{node}", vtype=GRB.CONTINUOUS))
        nodes_y_variables.append(model.addVar(name=f"y_{node}", vtype=GRB.CONTINUOUS))
    return nodes_x_variables, nodes_y_variables

def constraints_positive_coordinates(model: Model, graph: Graph, nodes_x_variables, nodes_y_variables):
    for node in range(graph.size()):
        model.addConstr(nodes_x_variables[node] >= 0)
        model.addConstr(nodes_y_variables[node] >= 0)

def is_edge_horizontal(node, neighbor, shape):
    return shape[(node, neighbor)] == "left" or shape[(node, neighbor)] == "right"

def constraints_nodes_inside_horizontal_edge(graph: Graph, model: Model, shape, node, neighbor, node_x_var, node_y_var,
                                             neighbor_x_var, neighbor_y_var, nodes_x_variables, nodes_y_variables):
    direction = shape[(node, neighbor)]
    M = 1000
    if direction == "left":
        node, neighbor = neighbor, node
        node_x_var, node_y_var, neighbor_x_var, neighbor_y_var = neighbor_x_var, neighbor_y_var, node_x_var, node_y_var
    for other_node in range(len(graph)):
        if other_node == node or other_node == neighbor: continue
        other_node_x_var = nodes_x_variables[other_node]
        other_node_y_var = nodes_y_variables[other_node]
        aux1 = model.addVar(vtype=GRB.BINARY)
        aux2 = model.addVar(vtype=GRB.BINARY)
        aux3 = model.addVar(vtype=GRB.BINARY)
        aux4 = model.addVar(vtype=GRB.BINARY)

        # (a_y == o_y) >> (o_x < a_x) or (o_x > b_x)
        # (a_y != o_y) or [(o_x < a_x) or (o_x > b_x)]
        # (a_y != o_y) or (o_x < a_x) or (o_x > b_x)
        # (a_y > o_y) or (a_y < o_y) or (o_x < a_x) or (o_x > b_x)

        model.addConstr(node_y_var - other_node_y_var >= 0.1 - M*(1-aux1))
        model.addConstr(other_node_y_var - node_y_var >= 0.1 - M*(1-aux2))
        model.addConstr(node_x_var - other_node_x_var >= 0.1 - M*(1-aux3))
        model.addConstr(other_node_x_var - neighbor_x_var >= 0.1 - M*(1-aux4))
        model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)

def constraints_nodes_inside_vertical_edge(graph: Graph, model: Model, shape, node, neighbor, node_x_var, node_y_var,
                                             neighbor_x_var, neighbor_y_var, nodes_x_variables, nodes_y_variables):
    direction = shape[(node, neighbor)]
    M = 1000
    if direction == "down":
        node, neighbor = neighbor, node
        node_x_var, node_y_var, neighbor_x_var, neighbor_y_var = neighbor_x_var, neighbor_y_var, node_x_var, node_y_var
    for other_node in range(len(graph)):
        if other_node == node or other_node == neighbor: continue
        other_node_x_var = nodes_x_variables[other_node]
        other_node_y_var = nodes_y_variables[other_node]
        aux1 = model.addVar(vtype=GRB.BINARY)
        aux2 = model.addVar(vtype=GRB.BINARY)
        aux3 = model.addVar(vtype=GRB.BINARY)
        aux4 = model.addVar(vtype=GRB.BINARY)

        # (a_x == o_x) >> (o_y < a_y) or (o_y > b_y)
        # (a_x != o_x) or [(o_y < a_y) or (o_y > b_y)]
        # (a_x != o_x) or (o_y < a_y) or (o_y > b_y)
        # (a_x > o_x) or (a_x < o_x) or (o_y < a_y) or (o_y > b_y)

        model.addConstr(node_x_var - other_node_x_var >= 0.1 - M*(1-aux1))
        model.addConstr(other_node_x_var - node_x_var >= 0.1 - M*(1-aux2))
        model.addConstr(node_y_var - other_node_y_var >= 0.1 - M*(1-aux3))
        model.addConstr(other_node_y_var - neighbor_y_var >= 0.1 - M*(1-aux4))
        model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)  

def constraints_nodes_inside_edges(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape):
    for node in range(len(graph)):
        node_x_var = nodes_x_variables[node]
        node_y_var = nodes_y_variables[node]
        for neighbor in graph.get_neighbors(node):
            if (neighbor > node): continue
            neighbor_x_var = nodes_x_variables[neighbor]
            neighbor_y_var = nodes_y_variables[neighbor]
            if is_edge_horizontal(node, neighbor, shape):
                function_to_call = constraints_nodes_inside_horizontal_edge
            else:
                function_to_call = constraints_nodes_inside_vertical_edge
            function_to_call(graph, model, shape, node, neighbor, node_x_var, node_y_var, neighbor_x_var, neighbor_y_var,
                             nodes_x_variables, nodes_y_variables)

def constraints_from_edges_directions(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape):
    for node in range(graph.size()):
        for neighbor in graph.get_neighbors(node):
            if (neighbor > node): continue
            direction = shape[(node, neighbor)]
            if direction == "up" or direction == "down":
                model.addConstr(nodes_x_variables[node] == nodes_x_variables[neighbor])
                if direction == "up":
                    model.addConstr(nodes_y_variables[node] +1 <= nodes_y_variables[neighbor])
                else:
                    model.addConstr(nodes_y_variables[node] >= nodes_y_variables[neighbor] + 1)
            elif direction == "left" or direction == "right":
                model.addConstr(nodes_y_variables[node] == nodes_y_variables[neighbor])
                if direction == "left":
                    model.addConstr(nodes_x_variables[node] >= nodes_x_variables[neighbor] + 1)
                else:
                    model.addConstr(nodes_x_variables[node] + 1 <= nodes_x_variables[neighbor])
            else:
                assert False

def constraints_for_no_nodes_overlapping(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables):
    for node in range(graph.size()):
        node_x = nodes_x_variables[node]
        node_y = nodes_y_variables[node]
        for other_node in range(node):
            if (other_node > node): continue
            aux1 = model.addVar(vtype=GRB.BINARY)
            aux2 = model.addVar(vtype=GRB.BINARY)
            aux3 = model.addVar(vtype=GRB.BINARY)
            aux4 = model.addVar(vtype=GRB.BINARY)
            other_node_x = nodes_x_variables[other_node]
            other_node_y = nodes_y_variables[other_node]
            M = 1000
            model.addConstr(node_x-other_node_x >= 0.1 - M*(1-aux1))
            model.addConstr(node_y-other_node_y <= 0.1 + M*(1-aux2))
            model.addConstr(other_node_x-node_x >= 0.1 - M*(1-aux3))
            model.addConstr(other_node_y-node_y <= 0.1 + M*(1-aux4))
            model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)
            # model.addConstr((nodes_x_variables[node] - nodes_x_variables[other_node])**2 + (nodes_y_variables[node] - nodes_y_variables[other_node])**2 >= 1)
    
def shape_to_nodes_positions(graph: Graph, shape: dict):
    gp.setParam('OutputFlag', 0) # suppresses the prints of gurobi
    model = Model("my_model")
    nodes_x_variables, nodes_y_variables = initialize_nodes_variables(model, graph)
    constraints_positive_coordinates(model, graph, nodes_x_variables, nodes_y_variables)
    constraints_from_edges_directions(graph, model, nodes_x_variables, nodes_y_variables, shape)
    constraints_for_no_nodes_overlapping(graph, model, nodes_x_variables, nodes_y_variables)
    constraints_nodes_inside_edges(graph, model, nodes_x_variables, nodes_y_variables, shape)
    model.setObjective(sum(nodes_x_variables) + sum(nodes_y_variables), GRB.MINIMIZE)
    model.optimize()
    if model.status == GRB.OPTIMAL:
        nodes_positions = dict()
        for node in range(graph.size()):
            nodes_positions[node] = (nodes_x_variables[node].x, nodes_y_variables[node].x)
        return nodes_positions