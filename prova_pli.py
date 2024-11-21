from gurobipy import Model, GRB
from graph import Graph

def check_graph_pli(graph: Graph, print_solution=False):
    model = Model("my_model")
    variables = [[None for _ in range(graph.size())] for _ in range(graph.size())]
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            if (i < j):
                variables[i][j] = model.addVar(name=f"x_{i}_{j}", vtype=GRB.BINARY)
                variables[j][i] = variables[i][j]
    cycles = graph.find_all_cycles()
    for cycle in cycles:
        if len(cycle) == 3: continue
        for i in range(len(cycle)):
            model.addConstr(sum(variables[cycle[j % len(cycle)]][cycle[(j + 1) % len(cycle)]] for j in range(i, i+len(cycle)-2)) >= 1)
            model.addConstr(sum(variables[cycle[j % len(cycle)]][cycle[(j + 1) % len(cycle)]] for j in range(i, i+len(cycle)-2)) <= len(cycle)-3)
    for i in range(graph.size()):
        if len(graph.get_neighbors(i)) == 3:
            model.addConstr(sum(variables[i][j] for j in graph.get_neighbors(i)) >= 1)
            model.addConstr(sum(variables[i][j] for j in graph.get_neighbors(i)) <= 2)
        if len(graph.get_neighbors(i)) == 4:
            model.addConstr(sum(variables[i][j] for j in graph.get_neighbors(i)) == 2)
    model.optimize()
    if model.status == GRB.OPTIMAL:
        if print_solution:
            print("Solution found.")
            for i in range(graph.size()):
                for j in graph.get_neighbors(i):
                    if (i < j):
                        print(f"x_{i}_{j} = {variables[i][j].x}")
        return True
    else:
        if print_solution:
            print("No solution found.")
        return False