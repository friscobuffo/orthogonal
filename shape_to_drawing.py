from graph import Graph
from gurobipy import Model, GRB
import gurobipy as gp

def shape_to_nodes_positions(graph: Graph, shape: dict):
    gp.setParam('OutputFlag', 0) # suppresses the prints of gurobi
    model = Model("my_model")
    nodes_x_variables = []
    nodes_y_variables = []
    for node in range(graph.size()):
        nodes_x_variables.append(model.addVar(name=f"x_{node}", vtype=GRB.CONTINUOUS))
        model.addConstr(nodes_x_variables[node] >= 0)
        nodes_y_variables.append(model.addVar(name=f"y_{node}", vtype=GRB.CONTINUOUS))
        model.addConstr(nodes_y_variables[node] >= 0)
    # constraints of edges directions
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
    # constraints to avoid overlapping of nodes
    for node in range(graph.size()):
        for other_node in range(node):
            if (other_node > node): continue
            aux1 = model.addVar(vtype=GRB.BINARY)
            aux2 = model.addVar(vtype=GRB.BINARY)
            aux3 = model.addVar(vtype=GRB.BINARY)
            aux4 = model.addVar(vtype=GRB.BINARY)
            node_x = nodes_x_variables[node]
            other_node_x = nodes_x_variables[other_node]
            node_y = nodes_y_variables[node]
            other_node_y = nodes_y_variables[other_node]
            M = 1000
            model.addConstr(node_x-other_node_x >= 0.001 - M*(1-aux1))
            model.addConstr(node_y-other_node_y <= 0.001 + M*(1-aux2))
            model.addConstr(other_node_x-node_x >= 0.001 - M*(1-aux3))
            model.addConstr(other_node_y-node_y <= 0.001 + M*(1-aux4))
            model.addConstr(aux1 + aux2 + aux3 + aux4 >= 1)
            # model.addConstr((nodes_x_variables[node] - nodes_x_variables[other_node])**2 + (nodes_y_variables[node] - nodes_y_variables[other_node])**2 >= 1)
    # constraints to avoid nodes between edges (TODO)

    # objective function to minimize values of positions
    model.setObjective(sum(nodes_x_variables) + sum(nodes_y_variables), GRB.MINIMIZE)
    # optimize
    model.optimize()
    if model.status == GRB.OPTIMAL:
        nodes_positions = dict()
        for node in range(graph.size()):
            nodes_positions[node] = (nodes_x_variables[node].x, nodes_y_variables[node].x)
        return nodes_positions