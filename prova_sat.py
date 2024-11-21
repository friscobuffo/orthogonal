from pysat.solvers import Minisat22
import itertools
from graph import Graph

def check_graph_sat(graph: Graph, print_solution=False):
    variables = [[0 for _ in range(graph.size())] for _ in range(graph.size())]
    next_var = 1
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            if (i < j):
                variables[i][j] = next_var
                variables[j][i] = next_var
                next_var += 1
    cycles = graph.find_all_cycles()
    with Minisat22() as solver:
        for cycle in cycles:
            if len(cycle) == 3: continue
            for i in range(len(cycle)):
                clause1 = [variables[cycle[j % len(cycle)]][cycle[(j + 1) % len(cycle)]] for j in range(i, i+len(cycle)-2)]
                clause2 = [-variables[cycle[j % len(cycle)]][cycle[(j + 1) % len(cycle)]] for j in range(i, i+len(cycle)-2)]
                solver.add_clause(clause1)
                solver.add_clause(clause2)
        for i in range(graph.size()):
            if len(graph.get_neighbors(i)) == 3:
                solver.add_clause([variables[i][j] for j in graph.get_neighbors(i)])
                solver.add_clause([-variables[i][j] for j in graph.get_neighbors(i)])
            if len(graph.get_neighbors(i)) == 4:
                for triple in itertools.combinations(graph.get_neighbors(i), 3):
                    solver.add_clause([variables[i][j] for j in triple])
                    solver.add_clause([-variables[i][j] for j in triple])
        if solver.solve():
            if print_solution:
                print("SATISFIABLE")
                print("Model:", solver.get_model())
            return True
        else:
            if print_solution:
                print("UNSATISFIABLE")
            return False