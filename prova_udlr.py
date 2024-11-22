import gurobipy as gp
from gurobipy import GRB
from graph import Graph

if __name__ == "__main__":
    g = Graph(6)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 5)
    g.add_edge(4, 5) 
    
    print(g.adjacency_list)
    
    model = gp.Model("m1")
    
    # n x n matrix of tuples (l, r, u, d)
    variable_matrix: list[list] = [[None for _ in range(len(g.adjacency_list))] for _ in range(len(g.adjacency_list))]
    
    for i in range(len(g.adjacency_list)):
        for j in g.get_neighbors(i):
            if(i < j):
                l = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}l")
                r = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}r") 
                u = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}u") 
                d = model.addVar(vtype=GRB.BINARY, name=f"{i}{j}d") 
                
                variable_matrix[i][j] = l, r, u, d
                variable_matrix[j][i] = r, l, d, u                
                
    for i in range(len(g.adjacency_list)):
        # a node can't have two edges with the same direction
        model.addConstr(sum(variable_matrix[i][j][0] for j in g.get_neighbors(i)) <= 1) 
        model.addConstr(sum(variable_matrix[i][j][1] for j in g.get_neighbors(i)) <= 1) 
        model.addConstr(sum(variable_matrix[i][j][2] for j in g.get_neighbors(i)) <= 1) 
        model.addConstr(sum(variable_matrix[i][j][3] for j in g.get_neighbors(i)) <= 1) 
        
        for j in g.get_neighbors(i):
            # an edge between nodes i and j can only have one direction
            model.addConstr(sum(variable_matrix[i][j][k] for k in range(4)) == 1) 
    
    for cycle in g.find_all_cycles():
        for i in range(len(cycle)):
            fst = cycle[i]
            snd = cycle[(i + 1) % len(cycle)]
            trd = cycle[(i + 2) % len(cycle)]
            
            print(fst, snd, trd)
            
        # 1010
        model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][0] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][2]  for i in range(len(cycle))) >= 2)
        # 1001
        model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][0] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][3] for i in range(len(cycle)))  >= 2)
        # 0101
        model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][1] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][3] for i in range(len(cycle))) >= 2)
        # 0110
        model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][1] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][2] for i in range(len(cycle))) >= 2)
            

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
        