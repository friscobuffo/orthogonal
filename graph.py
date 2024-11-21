class Graph:
    def __init__(self, numberOfNodes: int):
        self.adjacency_list: list = []
        for _ in range(numberOfNodes):
            self.adjacency_list.append([])
        self.matrix_graph = [[False for _ in range(numberOfNodes)] for _ in range(numberOfNodes)]

    def add_edge(self, node1: int, node2: int):
        neighbors1: list = self.adjacency_list[node1]
        neighbors2: list = self.adjacency_list[node2]
        neighbors1.append(node2)
        neighbors2.append(node1)
        self.matrix_graph[node1][node2] = True
        self.matrix_graph[node2][node1] = True

    def get_neighbors(self, node: int):
        return self.adjacency_list[node]
    
    def has_edge(self, node1: int, node2: int):
        return self.matrix_graph[node1][node2]
    
    def size(self):
        return len(self.adjacency_list)
    
    def __str__(self):
        return "\n".join([f"{i}: {neighbors}" for i, neighbors in enumerate(self.adjacency_list)])
    
    def find_all_cycles(self):
        def find_all_cycles_with_node(self, node, visited, path, cycles, visitedGlobal):
            visited[node] = True
            path.append(node)
            for neighbor in self.get_neighbors(node):
                if visitedGlobal[neighbor]: continue
                if len(path) > 1 and neighbor == path[-2]: continue
                if neighbor in path:
                    if neighbor == path[0]:
                        cycles.append(path[path.index(neighbor):])
                else:
                    find_all_cycles_with_node(self, neighbor, visited, path.copy(), cycles, visitedGlobal)
        visitedGlobal = [False] * self.size()
        cycles = []
        for node in range(self.size()):
            visited = [False] * self.size()
            find_all_cycles_with_node(self, node, visited, [], cycles, visitedGlobal)
            visitedGlobal[node] = True
        return cycles