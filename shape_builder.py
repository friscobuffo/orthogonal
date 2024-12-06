from pysat.solvers import Minisat22
from graph import Graph

def _initialize_variables(graph: Graph):
    is_edge_up_variable = [[-1 for _ in range(graph.size())] for _ in range(graph.size())]
    is_edge_down_variable = [[-1 for _ in range(graph.size())] for _ in range(graph.size())]
    is_edge_left_variable = [[-1 for _ in range(graph.size())] for _ in range(graph.size())]
    is_edge_right_variable = [[-1 for _ in range(graph.size())] for _ in range(graph.size())]
    next_var = 1
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            is_edge_up_variable[i][j] = next_var
            next_var += 1
            is_edge_down_variable[i][j] = next_var
            next_var += 1
            is_edge_left_variable[i][j] = next_var
            next_var += 1
            is_edge_right_variable[i][j] = next_var
            next_var += 1
    return is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable

def _get_variables(variables, i, j):
    assert variables[i][j] != -1
    return variables[i][j]

# each edge can only be in one direction
def _add_constraints_one_direction_per_edge(graph: Graph, solver: Minisat22, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable):
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            up = _get_variables(is_edge_up_variable, i, j)
            down = _get_variables(is_edge_down_variable, i, j)
            right = _get_variables(is_edge_right_variable, i, j)
            left = _get_variables(is_edge_left_variable, i, j)
            # at least one is true
            solver.add_clause([up, down, right, left])
            # at most one is true (at least three are false)
            # for every possible pair, at least one is false
            solver.add_clause([-up, -down])
            solver.add_clause([-up, -right])
            solver.add_clause([-up, -left])
            solver.add_clause([-down, -right])
            solver.add_clause([-down, -left])
            solver.add_clause([-left, -right])

# if edge i,j is up, edge j,i is down (etc)
def _add_constraints_opposite_edges(graph: Graph, solver: Minisat22, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable):
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            if (i > j):
                continue
            up = _get_variables(is_edge_up_variable, i, j)
            down = _get_variables(is_edge_down_variable, i, j)
            right = _get_variables(is_edge_right_variable, i, j)
            left = _get_variables(is_edge_left_variable, i, j)
            opposite_up = _get_variables(is_edge_up_variable, j, i)
            opposite_down = _get_variables(is_edge_down_variable, j, i)
            opposite_right = _get_variables(is_edge_right_variable, j, i)
            opposite_left = _get_variables(is_edge_left_variable, j, i)
            # if up is true, opposite edge down is true (and viceversa)
            solver.add_clause([-up, opposite_down])
            solver.add_clause([-opposite_down, up])
            # if down is true, opposite edge up is true (and viceversa)
            solver.add_clause([-down, opposite_up])
            solver.add_clause([-opposite_up, down])
            # if right is true, opposite edge left is true (and viceversa)
            solver.add_clause([-right, opposite_left])
            solver.add_clause([-opposite_left, right])
            # if left is true, opposite edge right is true (and viceversa)
            solver.add_clause([-left, opposite_right])
            solver.add_clause([-opposite_right, left])

def _one_edge_per_direction_clauses(graph: Graph, solver: Minisat22, is_edge_direction, node):
    if len(graph.get_neighbors(node)) == 4:
        direction0 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[0])
        direction1 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[1])
        direction2 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[2])
        direction3 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[3])
        solver.add_clause([direction0, direction1, direction2, direction3]) # at least one is true
    if len(graph.get_neighbors(node)) == 3:
        direction0 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[0])
        direction1 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[1])
        direction2 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[2])
        # at most one is true (at least 2 are false)
        solver.add_clause([-direction0, -direction1])
        solver.add_clause([-direction0, -direction2])
        solver.add_clause([-direction1, -direction2])
    if len(graph.get_neighbors(node)) == 2:
        direction0 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[0])
        direction1 = _get_variables(is_edge_direction, node, graph.get_neighbors(node)[1])
        # at most one is true (at least 1 is false)
        solver.add_clause([-direction0, -direction1])

def _add_nodes_constraints(graph: Graph, solver: Minisat22, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable):
    for node in range(graph.size()):
        # at most one up edge
        _one_edge_per_direction_clauses(graph, solver, is_edge_up_variable, node)
        # at most one down edge
        _one_edge_per_direction_clauses(graph, solver, is_edge_down_variable, node)
        # at most one right edge
        _one_edge_per_direction_clauses(graph, solver, is_edge_right_variable, node)
        # at most one left edge
        _one_edge_per_direction_clauses(graph, solver, is_edge_left_variable, node)

def _add_cycles_constraints(cycles, solver: Minisat22, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable):
    for cycle in cycles:
        assert len(cycle) > 3
        at_least_one_down = [is_edge_down_variable[cycle[i]][cycle[(i + 1) % len(cycle)]] for i in range(len(cycle))]
        at_least_one_up = [is_edge_up_variable[cycle[i]][cycle[(i + 1) % len(cycle)]] for i in range(len(cycle))]
        at_least_one_right = [is_edge_right_variable[cycle[i]][cycle[(i + 1) % len(cycle)]] for i in range(len(cycle))]
        at_least_one_left = [is_edge_left_variable[cycle[i]][cycle[(i + 1) % len(cycle)]] for i in range(len(cycle))]
        solver.add_clause(at_least_one_down)
        solver.add_clause(at_least_one_up)
        solver.add_clause(at_least_one_right)
        solver.add_clause(at_least_one_left)

def _model_solution_to_shape(graph: Graph, solution, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable):
    variable_values = dict()
    for i in range(len(solution)):
        var = solution[i]
        if var > 0:
            variable_values[var] = True
        else:
            variable_values[-var] = False
    shape = dict()
    for i in range(graph.size()):
        for j in graph.get_neighbors(i):
            up = _get_variables(is_edge_up_variable, i, j)
            down = _get_variables(is_edge_down_variable, i, j)
            right = _get_variables(is_edge_right_variable, i, j)
            left = _get_variables(is_edge_left_variable, i, j)
            assert variable_values[up] + variable_values[down] + variable_values[right] + variable_values[left] == 1
            if variable_values[up]:
                shape[(i, j)] = "up"
            elif variable_values[down]:
                shape[(i, j)] = "down"
            elif variable_values[right]:
                shape[(i, j)] = "right"
            elif variable_values[left]:
                shape[(i, j)] = "left"
            else: assert False
    return shape

def build_shape(graph: Graph):
    is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable = _initialize_variables(graph)
    cycles = graph.find_all_cycles()
    with Minisat22() as solver:
        _add_constraints_one_direction_per_edge(graph, solver, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable)
        _add_constraints_opposite_edges(graph, solver, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable)
        _add_nodes_constraints(graph, solver, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable)
        _add_cycles_constraints(cycles, solver, is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable)
        if solver.solve():
            return _model_solution_to_shape(graph, solver.get_model(), is_edge_up_variable, is_edge_down_variable, is_edge_right_variable, is_edge_left_variable)
