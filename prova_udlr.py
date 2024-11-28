from example_graphs import get_example_graph
from gurobipy import GRB
from graph import Graph
import gurobipy as gp

def check_graph_udlr(g: Graph):
        model = gp.Model("m1")
        
        # n x n matrix of tuples (l, r, u, d)
        variable_matrix: list[list] = [[None for _ in range(len(g.adjacency_list))] for _ in range(len(g.adjacency_list))]
        
        for i in range(len(g.adjacency_list)):
            for j in g.get_neighbors(i):
                if(i < j):
                    l = model.addVar(vtype=GRB.BINARY, name=f"{i}_{j}_left")
                    r = model.addVar(vtype=GRB.BINARY, name=f"{i}_{j}_right") 
                    u = model.addVar(vtype=GRB.BINARY, name=f"{i}_{j}_up") 
                    d = model.addVar(vtype=GRB.BINARY, name=f"{i}_{j}_down") 
                    
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
            model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][0] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][2] for i in range(len(cycle))) >= 2) # at least one left-up angle
            model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][0] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][3] for i in range(len(cycle))) >= 2)
            model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][1] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][3] for i in range(len(cycle))) >= 2)
            model.addConstr(sum(variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[i]][1] + variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][2] for i in range(len(cycle))) >= 2)
            
            sum_0101 = sum(variable_matrix[i][j][1] + variable_matrix[j][i][3] for i in range(len(g.adjacency_list)) for j in g.get_neighbors(i))
            sum_1010 = sum(variable_matrix[i][j][0] + variable_matrix[j][i][2] for i in range(len(g.adjacency_list)) for j in g.get_neighbors(i))
            sum_1001 = sum(variable_matrix[i][j][0] + variable_matrix[j][i][3] for i in range(len(g.adjacency_list)) for j in g.get_neighbors(i))
            sum_0110 = sum(variable_matrix[i][j][1] + variable_matrix[j][i][2] for i in range(len(g.adjacency_list)) for j in g.get_neighbors(i))
               
            model.addConstr(sum_0101 == sum_1010) # right-down angles == left-up angles
            model.addConstr(sum_1001 == sum_0110)
            
        model.optimize()
    
        if model.status == GRB.OPTIMAL:
                print("Solution found.")
                for var in model.getVars():
                    if var.X > 0:   
                        print('%s %g' % (var.VarName, var.X))
                return True
        else:
                print("No solution found.")
                return False

if __name__ == "__main__":
    # for i in range(1, 7):
    #     graph = get_example_graph(i)
    #     print(check_graph_udlr(graph))
        graph = get_example_graph(6)
        print(check_graph_udlr(graph))
