from graph import Graph

def filter_cycles(all_cycles, length):
     return [cycle for cycle in all_cycles if len(cycle) == length]

def intersection(cycle1, cycle2):
    intersec = [node for node in cycle1 if node in cycle2]
    return intersec

def check_loops(all_cycles: list[list]):
        for cycle in all_cycles:
            if len(cycle) == 3: 
                print("3 loop found")
                return False
            
        four_cycles = filter_cycles(all_cycles, 4)
        five_cycles = filter_cycles(all_cycles, 5)
        five_cycles += four_cycles
        # check each cycle made of four edges with cycles made of four or five edges
        for cycle1 in four_cycles:
            for cycle2 in five_cycles:
                if cycle1 != cycle2:
                    intersec = intersection(cycle1, cycle2)
                    if len(intersec) == 3:
                        print('Intersection found', intersec)
                        return False

        # check three cycles made of four edges at a time 
        # for cycle1 in four_cycles:
        #     for cycle2 in four_cycles:
        #         if cycle1 != cycle2:
        #             intersec = intersection(cycle1, cycle2)
        #             if len(intersec) == 2:
        #                 for cycle3 in four_cycles:
        #                     if cycle1 != cycle3 and cycle2  != cycle3:
        #                         intersec1 = intersection(cycle1, cycle3)
        #                         intersec1 += intersection(cycle2, cycle3)
        #                         if len(intersec1) == 3:                        
        #                             print('Intersection found', intersec)
        #                             return False
                                    
        return True

if __name__ == "__main__":
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(0, 4)
    graph.add_edge(0, 5)
    graph.add_edge(6, 5)
    graph.add_edge(6, 2)
    all_cycles = graph.find_all_cycles()
    print("All cycles:", all_cycles)
    print("Result:", check_loops(all_cycles))
