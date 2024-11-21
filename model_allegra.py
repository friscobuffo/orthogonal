import gurobipy as gp
from gurobipy import GRB
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
        if len(g.adjacency_list[i]) == 4:
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) == 4)
        if(len(g.adjacency_list[i]) == 3):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) <= 4)
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) >= 2) 
        if(len(g.adjacency_list[i]) == 2):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) <= 3)
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) >= 1)
        if(len(g.adjacency_list[i]) == 1):
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) <= 2)
            model.addConstr(sum(variable_matrix[i][j][0] + variable_matrix[i][j][1] for j in g.adjacency_list[i]) >= 0)
            
    model.optimize()
    
    for var in model.getVars():
        print('%s %g' % (var.VarName, var.X))
        