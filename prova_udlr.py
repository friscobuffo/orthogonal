from example_graphs import get_example_graph
from gurobipy import GRB
from graph import Graph
import gurobipy as gp

# WARNING: Angles checking doesn't work if the find_all_cycles function finds the same cycle twice
# such as: [0,1,2,3] and [2,3,1,0]. 

angle_list = [(0, 2, 1), (2, 1, 3), (1, 3, 2), (3, 0, 0)] # (direction1, direction2, angle type)

def is_an_angle(model, cycle, variable_matrix, i, angle_matrix, direction1, direction2, angle, triggers):

        x = variable_matrix[cycle[i]][cycle[(i + 1) % len(cycle)]][direction1] 
        y = variable_matrix[cycle[(i + 1) % len(cycle)]][cycle[(i + 2) % len(cycle)]][direction2]

        trigger = model.addVar(vtype=GRB.BINARY, name=f"trigger_{i}_{cycle}")
        triggers.append(trigger)

        # the matrix of variables and angles are both updated according to the trigger
        model.addConstr((trigger == 1) >> (x + y >= 2))
        model.addConstr((trigger == 0) >> (x + y <= 1))

        model.addConstr((trigger == 1) >> (angle_matrix[cycle[(i + 1) % len(cycle)]][angle] == 1))
        model.addConstr((trigger == 0) >> (angle_matrix[cycle[(i + 1) % len(cycle)]][angle] == 0))
        
def check_angles(model, cycle, angle_list, variable_matrix, graph):
    
        # n x 4 matrix of tuples (left_up, right_up, left_down, right_down)
        angle_matrix = [[None for _ in range(4)] for _ in range(len(graph.adjacency_list))]
            
        for i in range(len(graph.adjacency_list)):
            angle_matrix[i][0] = model.addVar(vtype=GRB.BINARY, name=f"{i}_left_up")
            angle_matrix[i][1] = model.addVar(vtype=GRB.BINARY, name=f"{i}_right_up")
            angle_matrix[i][2] = model.addVar(vtype=GRB.BINARY, name=f"{i}_left_down")
            angle_matrix[i][3] = model.addVar(vtype=GRB.BINARY, name=f"{i}_right_down")
                
        triggers = []
        for i in range(len(cycle)):
            for angle in angle_list:
                is_an_angle(model, cycle, variable_matrix, i, angle_matrix, angle[0], angle[1], angle[2], triggers)
                model.addConstr(sum(angle_matrix[i][k] for k in range(4)) <= 1) 
                
        return angle_matrix, triggers
   
def check_sum_angles(model, cycle, angle_matrix):         
    model.addConstr(sum(angle_matrix[cycle[i]][0] for i in range(len(cycle))) >= 1)
    model.addConstr(sum(angle_matrix[cycle[i]][1] for i in range(len(cycle))) >= 1)
    model.addConstr(sum(angle_matrix[cycle[i]][2] for i in range(len(cycle))) >= 1)
    model.addConstr(sum(angle_matrix[cycle[i]][3] for i in range(len(cycle))) >= 1)
    
    model.addConstr(sum(angle_matrix[cycle[i]][2] for i in range(len(cycle))) == sum(angle_matrix[cycle[i]][1] for i in range(len(cycle)))) # left_down = right_up
    model.addConstr(sum(angle_matrix[cycle[i]][0] for i in range(len(cycle))) == sum(angle_matrix[cycle[i]][3] for i in range(len(cycle)))) # left_up = right_down


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
            if len(cycle) == 3: continue
            
            # check clockwise if there is at least one edge in each direction 
            # clockwise => variable_matrix[i][j] is checked, while variable_matrix[j][i] is not
            model.addConstr(sum(variable_matrix[cycle[i]][cycle[(i + 1) % len(cycle)]][0] for i in range(len(cycle))) >= 1) 
            model.addConstr(sum(variable_matrix[cycle[i]][cycle[(i + 1) % len(cycle)]][1] for i in range(len(cycle))) >= 1) 
            model.addConstr(sum(variable_matrix[cycle[i]][cycle[(i + 1) % len(cycle)]][2] for i in range(len(cycle))) >= 1) 
            model.addConstr(sum(variable_matrix[cycle[i]][cycle[(i + 1) % len(cycle)]][3] for i in range(len(cycle))) >= 1) 
            
            # angle_matrix, triggers = check_angles(model, cycle, angle_list, variable_matrix, g)
            # check_sum_angles(model, cycle, angle_matrix) 
            
        model.optimize()
        
        # for trigger in triggers:
        #     print(trigger.varName, trigger.X)
            
        # for cycle in g.find_all_cycles():
        #     for i in range(len(cycle)):
        #                 print(f"node {i} = {angle_matrix[i][0].x}, {angle_matrix[i][1].x}, {angle_matrix[i][2].x}, {angle_matrix[i][3].x}")
            
        # for i in range(len(g.adjacency_list)):
        #     for j in g.get_neighbors(i):
        #         # if(i < j):
        #             print(f"{i}_{j} = {variable_matrix[i][j][0].x}, {variable_matrix[i][j][1].x}, {variable_matrix[i][j][2].x}, {variable_matrix[i][j][3].x}")
        
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
        graph = get_example_graph(7)
        print(check_graph_udlr(graph))
