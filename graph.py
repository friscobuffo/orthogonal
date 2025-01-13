class Graph:
    def __init__(self, numberOfNodes: int):
        self.adjacency_list: dict = dict()
        self.edges: set = set()
        self.nodes_color = []
        for i in range(numberOfNodes):
            self.adjacency_list[i] = []
            self.nodes_color.append("red")

    def add_edge(self, node1: int, node2: int):
        neighbors1: list = self.adjacency_list[node1]
        neighbors2: list = self.adjacency_list[node2]
        neighbors1.append(node2)
        neighbors2.append(node1)
        self.edges.add((node1, node2))
        self.edges.add((node2, node1))

    def get_neighbors(self, node: int):
        return self.adjacency_list[node]
    
    def has_edge(self, node1: int, node2: int):
        return (node1, node2) in self.edges
    
    def size(self):
        return len(self.adjacency_list)
    
    def __str__(self):
        return "\n".join([f"{i}: {neighbors}" for i, neighbors in enumerate(self.adjacency_list)])
    
    def find_all_cycles(self):
        def find_all_cycles_with_node(self: Graph, node, visited, path, cycles, visitedGlobal):
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
    
    def __len__(self):
        return self.size()
    
    def remove_edge(self, node1: int, node2: int):
        if node2 in self.adjacency_list[node1]:
            self.adjacency_list[node1].remove(node2)
        if node1 in self.adjacency_list[node2]:
            self.adjacency_list[node2].remove(node1)
        self.edges.discard((node1, node2))
        self.edges.discard((node2, node1))
    
    def add_node(self):
        self.adjacency_list[self.size()] = []
        self.nodes_color.append("green")