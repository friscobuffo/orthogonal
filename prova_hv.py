import gurobipy as gp # type: ignore
from gurobipy import GRB # type: ignore
from graph import Graph

if __name__ == "__main__":
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(0, 3)
    print(g.adjacency_list)
    
    # legenda
    # 00 destra
    # 11 sinistra
    # 01 sotto 
    # 10 sopra
 
    model = gp.Model("m1")
    
    # n x n matrix of tuples (h, v)
    variable_matrix: list[list] = [[None for _ in range(len(g.adjacency_list))] for _ in range(len(g.adjacency_list))]
    
    for i in range(len(g.adjacency_list)):
        for j in g.get_neighbors(i):
            if(i < j):
                h = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}h")
                v = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}v") 
                # not_h = model.addVar(vtype=GRB.BINARY, name=f"{j}{i}h")
                # not_v = model.addVar(vtype=GRB.BINARY, name=f"{j}{i}v")
                
                # model.addConstr(not_h == 1 - h)
                # model.addConstr(not_v == 1 - v)
                
                variable_matrix[i][j] = h, v
                variable_matrix[j][i] = h, v
                # variable_matrix[j][i] = not_h, not_v
                
    for i in range(len(g.adjacency_list)):
        if(len(g.get_neighbors(i)) == 3):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.get_neighbors(i)) >= 2, name="three_neighbors") 
        if(len(g.get_neighbors(i)) == 2):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.get_neighbors(i)) <= 3, name="two_neighbors_1")
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.get_neighbors(i)) >= 1, name="two_neighbors_2")
        if(len(g.get_neighbors(i)) == 1):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.get_neighbors(i)) <= 2,  name="one_neighbor_1")
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.get_neighbors(i)) >= 0,  name="one_neighbor_2")
        
        model.addConstr(sum(variable_matrix[i][j][0] for j in g.get_neighbors(i)) <= 2) 
        model.addConstr(sum(variable_matrix[i][j][1] for j in g.get_neighbors(i)) <= 2)    
            
    angles: list[tuple[int, int, int, int]] =  [(0,1,0,0), (1,1,0,1), (1,0,1,1), (0,0,1,0)]
  
    # for cycle in g.find_all_cycles():
    # for cycle in [[0, 1, 2, 3]]:
    #     variable_list = []
        
    #     for angle in angles:
    #         x = model.addVar(vtype=GRB.BINARY, name=f"x_{cycle}_{angle}")
    #         y = model.addVar(vtype=GRB.BINARY, name=f"y_{cycle}_{angle}")
    #         z = model.addVar(vtype=GRB.BINARY, name=f"z_{cycle}_{angle}")
    #         w = model.addVar(vtype=GRB.BINARY, name=f"w_{cycle}_{angle}")
    #         variable_list.append((x, y, z, w))
        
    #     for i in range(len(cycle)):
    #         first = cycle[i]
    #         second = cycle[(i + 1) % len(cycle)]
    #         third = cycle[(i + 2) % len(cycle)]
    
    #         for angle, var in zip(angles, variable_list):
    #             model.addConstr((variable_matrix[first][second][0] == angle[0]) >> (var[0] == 1))
    #             model.addConstr((variable_matrix[first][second][0] == 1 - angle[0]) >> (var[0] == 0))
                
    #             model.addConstr((variable_matrix[first][second][1] == angle[1]) >> (var[1] == 1))
    #             model.addConstr((variable_matrix[first][second][1] == 1 - angle[1]) >> (var[1] == 0))
                
    #             model.addConstr((variable_matrix[second][third][0] == angle[2]) >> (var[2] == 1))
    #             model.addConstr((variable_matrix[second][third][0] == 1 - angle[2]) >> (var[2] == 0))
                
    #             model.addConstr((variable_matrix[second][third][1] == angle[3]) >> (var[3] == 1))
    #             model.addConstr((variable_matrix[second][third][1] == 1 - angle[3]) >> (var[3] == 0))
                
    #     for var in variable_list:
    #         model.addConstr(var[0] + var[1] + var[2] + var[3] == 4)
            
    model.optimize()
    
    if model.Status == GRB.INFEASIBLE:
        print("Model is infeasible")
        model.computeIIS()
        model.write("model.ilp")
        for constr in model.getConstrs():
            if constr.IISConstr:
                print(f"Infeasible constraint: {constr.ConstrName}")

    
    for var in model.getVars():
        print('%s %g' % (var.VarName, var.X))
        