from graph import Graph
from gurobipy import Model, GRB
import gurobipy as gp
from shape_builder import Shape

def _has_node_a_right_neighbor(graph: Graph, node, shape):
    for neighbor in graph.get_neighbors(node):
        if shape[(node, neighbor)] == "right":
            return neighbor
    return None

def _has_node_a_left_neighbor(graph: Graph, node, shape):
    for neighbor in graph.get_neighbors(node):
        if shape[(node, neighbor)] == "left":
            return neighbor
    return None

def _has_node_an_up_neighbor(graph: Graph, node, shape):
    for neighbor in graph.get_neighbors(node):
        if shape[(node, neighbor)] == "up":
            return neighbor
    return None

def _has_node_a_down_neighbor(graph: Graph, node, shape):
    for neighbor in graph.get_neighbors(node):
        if shape[(node, neighbor)] == "down":
            return neighbor
    return None

BIG_M = 500

def _initialize_nodes_variables(model: Model, graph: Graph):
    nodes_x_variables = []
    nodes_y_variables = []
    for node in range(graph.size()):
        nodes_x_variables.append(model.addVar(name=f"x_{node}", vtype=GRB.CONTINUOUS))
        nodes_y_variables.append(model.addVar(name=f"y_{node}", vtype=GRB.CONTINUOUS))
    return nodes_x_variables, nodes_y_variables

def _constraints_positive_coordinates(model: Model, graph: Graph, nodes_x_variables, nodes_y_variables):
    for node in range(graph.size()):
        model.addConstr(nodes_x_variables[node] >= 0)
        model.addConstr(nodes_y_variables[node] >= 0)

def _constraints_nodes_inside_horizontal_edge(graph: Graph, model: Model, left, right, nodes_x_variables, nodes_y_variables, can_node_be_skipped):
    left_x_var = nodes_x_variables[left]
    left_y_var = nodes_y_variables[left]
    right_x_var = nodes_x_variables[right]
    for other_node in range(len(graph)):
        if other_node == left or other_node == right: continue
        if can_node_be_skipped[other_node]: continue
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

        model.addConstr(left_y_var - other_node_y_var >= 1 - BIG_M*(1-aux1))
        model.addConstr(other_node_y_var - left_y_var >= 1 - BIG_M*(1-aux2))
        model.addConstr(left_x_var - other_node_x_var >= 1 - BIG_M*(1-aux3))
        model.addConstr(other_node_x_var - right_x_var >= 1 - BIG_M*(1-aux4))
        model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)

def _expand_edge(graph: Graph, smaller_node, bigger_node, bigger_direction_function, smaller_direction_function, shape, is_edge_already_computed, can_node_be_skipped):
    while (True): # get the most right/up node
        bigger_node_neighbor = bigger_direction_function(graph, bigger_node, shape)
        if bigger_node_neighbor is None: break
        can_node_be_skipped[bigger_node] = True
        for n in graph.get_neighbors(bigger_node):
            can_node_be_skipped[n] = True
        is_edge_already_computed[bigger_node][bigger_node_neighbor] = True
        is_edge_already_computed[bigger_node_neighbor][bigger_node] = True
        bigger_node = bigger_node_neighbor
    while (True): # get the most left/down node
        smaller_node_neighbor = smaller_direction_function(graph, smaller_node, shape)
        if smaller_node_neighbor is None: break
        can_node_be_skipped[smaller_node] = True
        for n in graph.get_neighbors(smaller_node):
            can_node_be_skipped[n] = True
        is_edge_already_computed[smaller_node][smaller_node_neighbor] = True
        is_edge_already_computed[smaller_node_neighbor][smaller_node] = True
        smaller_node = smaller_node_neighbor
    return smaller_node, bigger_node

def _constraints_nodes_inside_edges(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape: Shape):
    is_edge_already_computed = [[False for _ in range(len(graph))] for _ in range(len(graph))]
    for node in range(len(graph)):
        for neighbor in graph.get_neighbors(node):
            if is_edge_already_computed[node][neighbor]: continue
            if is_edge_already_computed[neighbor][node]: continue
            is_edge_already_computed[node][neighbor] = True
            is_edge_already_computed[neighbor][node] = True
            can_node_be_skipped = [False for _ in range(len(graph))]
            for n in graph.get_neighbors(node):
                can_node_be_skipped[n] = True
            for n in graph.get_neighbors(neighbor):
                can_node_be_skipped[n] = True
            if shape.is_horizontal(node, neighbor):
                if shape.is_left(node, neighbor):
                    left, right = neighbor, node
                else:
                    left, right = node, neighbor
                left, right = _expand_edge(graph, left, right, _has_node_a_right_neighbor, _has_node_a_left_neighbor, shape, is_edge_already_computed, can_node_be_skipped)
                _constraints_nodes_inside_horizontal_edge(graph, model, left, right, nodes_x_variables, nodes_y_variables, can_node_be_skipped)
            else:
                if shape.is_up(node, neighbor):
                    down, up = node, neighbor
                else:
                    down, up = neighbor, node
                down, up = _expand_edge(graph, down, up, _has_node_an_up_neighbor, _has_node_a_down_neighbor, shape, is_edge_already_computed, can_node_be_skipped)                    
                _constraints_nodes_inside_horizontal_edge(graph, model, down, up, nodes_y_variables, nodes_x_variables, can_node_be_skipped)

def _constraints_from_edges_directions(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape: Shape):
    for node in range(graph.size()):
        for neighbor in graph.get_neighbors(node):
            if (neighbor > node): continue
            if shape.is_vertical(node, neighbor):
                model.addConstr(nodes_x_variables[node] == nodes_x_variables[neighbor])
                if shape.is_up(node, neighbor):
                    model.addConstr(nodes_y_variables[node] +1 <= nodes_y_variables[neighbor])
                else:
                    model.addConstr(nodes_y_variables[node] >= nodes_y_variables[neighbor] + 1)
            elif shape.is_horizontal(node, neighbor):
                model.addConstr(nodes_y_variables[node] == nodes_y_variables[neighbor])
                if shape.is_left(node, neighbor):
                    model.addConstr(nodes_x_variables[node] >= nodes_x_variables[neighbor] + 1)
                else:
                    model.addConstr(nodes_x_variables[node] + 1 <= nodes_x_variables[neighbor])
            else:
                assert False

def _constraints_for_no_nodes_overlapping(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape):
    for node in range(graph.size()):
        node_x = nodes_x_variables[node]
        node_y = nodes_y_variables[node]
        for other_node in range(node):
            if (other_node > node): continue
            if (node, other_node) in shape: continue
            aux1 = model.addVar(vtype=GRB.BINARY)
            aux2 = model.addVar(vtype=GRB.BINARY)
            aux3 = model.addVar(vtype=GRB.BINARY)
            aux4 = model.addVar(vtype=GRB.BINARY)
            other_node_x = nodes_x_variables[other_node]
            other_node_y = nodes_y_variables[other_node]
            model.addConstr(node_x-other_node_x >= 1 - BIG_M*(1-aux1))
            model.addConstr(node_y-other_node_y >= 1 - BIG_M*(1-aux2))
            model.addConstr(other_node_x-node_x >= 1 - BIG_M*(1-aux3))
            model.addConstr(other_node_y-node_y >= 1 - BIG_M*(1-aux4))
            model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)
    
from time import perf_counter

def shape_to_nodes_positions(graph: Graph, shape: Shape):
    gp.setParam('OutputFlag', 0) # suppresses the prints of gurobi
    model = Model("my_model")
    nodes_x_variables, nodes_y_variables = _initialize_nodes_variables(model, graph)
    timer_start = perf_counter()
    _constraints_positive_coordinates(model, graph, nodes_x_variables, nodes_y_variables)
    _constraints_from_edges_directions(graph, model, nodes_x_variables, nodes_y_variables, shape)
    _constraints_for_no_nodes_overlapping(graph, model, nodes_x_variables, nodes_y_variables, shape)
    _constraints_nodes_inside_edges(graph, model, nodes_x_variables, nodes_y_variables, shape)
    print(f"Gurobi constraints generation time: {perf_counter() - timer_start}")
    model.setObjective(sum(nodes_x_variables) + sum(nodes_y_variables), GRB.MINIMIZE)
    timer_start = perf_counter()
    model.optimize()
    print(f"Gurobi solving time: {perf_counter() - timer_start}")
    if model.status == GRB.OPTIMAL:
        nodes_positions = dict()
        for node in range(graph.size()):
            nodes_positions[node] = (nodes_x_variables[node].x, nodes_y_variables[node].x)
        return nodes_positions