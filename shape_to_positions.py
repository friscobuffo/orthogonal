from graph import Graph
from gurobipy import Model, GRB
import gurobipy as gp

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

def _is_edge_horizontal(node, neighbor, shape):
    return shape[(node, neighbor)] == "left" or shape[(node, neighbor)] == "right"

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

        model.addConstr(left_y_var - other_node_y_var >= 0.5 - BIG_M*(1-aux1))
        model.addConstr(other_node_y_var - left_y_var >= 0.5 - BIG_M*(1-aux2))
        model.addConstr(left_x_var - other_node_x_var >= 0.5 - BIG_M*(1-aux3))
        model.addConstr(other_node_x_var - right_x_var >= 0.5 - BIG_M*(1-aux4))
        model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)

def _constraints_nodes_inside_edges(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape):
    is_edge_already_computed = [[False for _ in range(len(graph))] for _ in range(len(graph))]
    for node in range(len(graph)):
        for neighbor in graph.get_neighbors(node):
            if is_edge_already_computed[node][neighbor]: continue
            if is_edge_already_computed[neighbor][node]: continue
            is_edge_already_computed[node][neighbor] = True
            is_edge_already_computed[neighbor][node] = True
            if _is_edge_horizontal(node, neighbor, shape):
                is_node_in_between = [False for _ in range(len(graph))] # nodes that are in between the left and right nodes
                is_node_neighbor = [False for _ in range(len(graph))] # nodes that are neighbors of left, right and in between nodes
                for n in graph.get_neighbors(node):
                    is_node_neighbor[n] = True
                for n in graph.get_neighbors(neighbor):
                    is_node_neighbor[n] = True
                if shape[(node, neighbor)] == "left":
                    left, right = neighbor, node
                else:
                    left, right = node, neighbor
                while (True): # get the most right node
                    right_neighbor = _has_node_a_right_neighbor(graph, right, shape)
                    if right_neighbor is None: break
                    is_node_in_between[right] = True
                    for n in graph.get_neighbors(right):
                        is_node_neighbor[n] = True
                    is_edge_already_computed[right][right_neighbor] = True
                    is_edge_already_computed[right_neighbor][right] = True
                    right = right_neighbor
                while (True): # get the most left node
                    left_neighbor = _has_node_a_left_neighbor(graph, left, shape)
                    if left_neighbor is None: break
                    is_node_in_between[left] = True
                    for n in graph.get_neighbors(left):
                        is_node_neighbor[n] = True
                    is_edge_already_computed[left][left_neighbor] = True
                    is_edge_already_computed[left_neighbor][left] = True
                    left = left_neighbor
                can_node_be_skipped = [False for _ in range(len(graph))]
                for n in range(len(graph)):
                    if is_node_in_between[n] or is_node_neighbor[n]:
                        can_node_be_skipped[n] = True
                        continue
                _constraints_nodes_inside_horizontal_edge(graph, model, left, right, nodes_x_variables, nodes_y_variables, can_node_be_skipped)
            else:
                is_node_in_between = [False for _ in range(len(graph))] # nodes that are in between the left and right nodes
                is_node_neighbor = [False for _ in range(len(graph))] # nodes that are neighbors of left, right and in between nodes
                for n in graph.get_neighbors(node):
                    is_node_neighbor[n] = True
                for n in graph.get_neighbors(neighbor):
                    is_node_neighbor[n] = True
                if shape[(node, neighbor)] == "up":
                    down, up = node, neighbor
                else:
                    down, up = neighbor, node
                while (True): # get the most up node
                    up_neighbor = _has_node_an_up_neighbor(graph, up, shape)
                    if up_neighbor is None: break
                    is_node_in_between[up] = True
                    for n in graph.get_neighbors(up):
                        is_node_neighbor[n] = True
                    is_edge_already_computed[up][up_neighbor] = True
                    is_edge_already_computed[up_neighbor][up] = True
                    up = up_neighbor
                while (True): # get the most down node
                    down_neighbor = _has_node_a_down_neighbor(graph, down, shape)
                    if down_neighbor is None: break
                    is_node_in_between[down] = True
                    for n in graph.get_neighbors(down):
                        is_node_neighbor[n] = True
                    is_edge_already_computed[down][down_neighbor] = True
                    is_edge_already_computed[down_neighbor][down] = True
                    down = down_neighbor
                can_node_be_skipped = [False for _ in range(len(graph))]
                for n in range(len(graph)):
                    if is_node_in_between[n] or is_node_neighbor[n]:
                        can_node_be_skipped[n] = True
                        continue
                _constraints_nodes_inside_horizontal_edge(graph, model, down, up, nodes_y_variables, nodes_x_variables, can_node_be_skipped)

def _constraints_from_edges_directions(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables, shape):
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

def _constraints_for_no_nodes_overlapping(graph: Graph, model: Model, nodes_x_variables, nodes_y_variables):
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
            model.addConstr(node_x-other_node_x >= 1 - BIG_M*(1-aux1))
            model.addConstr(node_y-other_node_y >= 1 - BIG_M*(1-aux2))
            model.addConstr(other_node_x-node_x >= 1 - BIG_M*(1-aux3))
            model.addConstr(other_node_y-node_y >= 1 - BIG_M*(1-aux4))
            model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)
            # model.addConstr((nodes_x_variables[node] - nodes_x_variables[other_node])**2 + (nodes_y_variables[node] - nodes_y_variables[other_node])**2 >= 1)
    
def shape_to_nodes_positions(graph: Graph, shape: dict):
    gp.setParam('OutputFlag', 0) # suppresses the prints of gurobi
    model = Model("my_model")
    nodes_x_variables, nodes_y_variables = _initialize_nodes_variables(model, graph)
    _constraints_positive_coordinates(model, graph, nodes_x_variables, nodes_y_variables)
    _constraints_from_edges_directions(graph, model, nodes_x_variables, nodes_y_variables, shape)
    _constraints_for_no_nodes_overlapping(graph, model, nodes_x_variables, nodes_y_variables)
    _constraints_nodes_inside_edges(graph, model, nodes_x_variables, nodes_y_variables, shape)
    model.setObjective(sum(nodes_x_variables) + sum(nodes_y_variables), GRB.MINIMIZE)
    model.optimize()
    if model.status == GRB.OPTIMAL:
        nodes_positions = dict()
        for node in range(graph.size()):
            nodes_positions[node] = (nodes_x_variables[node].x, nodes_y_variables[node].x)
        return nodes_positions