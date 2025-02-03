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

    # given an undirected graph (in which each edge is represented twice, in both directions), it computes a cycle basis
    # (i.e., a set of cycles such that each cycle of the graph can be expressed as a linear combination of the cycles in the basis)
    def compute_cycle_basis(self):
        def dfs_cycle_basis(node, parent, visited, stack, cycles):
            visited[node] = True
            stack.append(node)
            for neighbor in self.get_neighbors(node):
                if neighbor == parent:
                    continue
                if not visited[neighbor]:
                    dfs_cycle_basis(neighbor, node, visited, stack, cycles)
                elif neighbor in stack:
                    cycle = stack[stack.index(neighbor):]
                    cycles.append(cycle)
            stack.pop()

        visited = [False] * self.size()
        cycles = []
        for node in range(self.size()):
            if not visited[node]:
                dfs_cycle_basis(node, -1, visited, [], cycles)
        return cycles
    
    def compute_2_cycles_covering(self):
        all_cycles = self.find_all_cycles()
        all_cycles.sort(key=lambda cycle: len(cycle)) # SEEMS TO BE MANDATORY
        cycles_covering = []
        edges_cycles_count = dict()
        edges_left = set()
        for node in range(self.size()):
            for neighbor in self.get_neighbors(node):
                if node < neighbor:
                    edges_cycles_count[(node, neighbor)] = 0
                    edges_left.add((node, neighbor))
        for cycle in all_cycles:
            is_cycle_useful = False
            for i in range(len(cycle)):
                node1 = cycle[i]
                node2 = cycle[(i + 1) % len(cycle)]
                if node1 > node2:
                    node1, node2 = node2, node1
                edges_cycles_count[(node1, node2)] += 1
                if (node1, node2) in edges_left:
                    is_cycle_useful = True
                if edges_cycles_count[(node1, node2)] == 2:
                    edges_left.discard((node1, node2))
            if is_cycle_useful:
                cycles_covering.append(cycle)
            if not edges_left:
                break
        return cycles_covering
    
    def compute_cycle_basis_tree(self, tree_root = 0):
        spanning = SpanningTree(self, tree_root)
        print(spanning)
        cycles = []
        for node in range(self.size()):
            for neighbor in self.get_neighbors(node):
                if node > neighbor: continue
                if not spanning.is_edge_in_tree(node, neighbor):
                    common_ancestor = spanning.compute_common_ancestor(node, neighbor)
                    path1 = spanning.get_path(node)
                    path2 = spanning.get_path(neighbor)
                    path1.reverse()
                    path2.reverse()
                    while path1[-1] != common_ancestor:
                        path1.pop()
                    while path2[-1] != common_ancestor:
                        path2.pop()
                    path1.reverse()
                    path1.extend(path2)
                    path1.pop()
                    cycles.append(path1)
        return cycles                    

from queue import Queue

class SpanningTree:
    def __init__(self, graph: Graph, root: int):
        self.graph = graph
        self.root = root
        self.parent = [None] * graph.size()
        self.depth = [None] * graph.size()
        self.children = dict()
        self.build_tree([False] * graph.size())
    def build_tree(self, is_visited):
        self.parent[self.root] = -1
        self.depth[self.root] = 0
        is_visited[self.root] = True
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            for neighbor in self.graph.get_neighbors(node):
                if not is_visited[neighbor]:
                    is_visited[neighbor] = True
                    self.parent[neighbor] = node
                    self.depth[neighbor] = self.depth[node] + 1
                    if node not in self.children:
                        self.children[node] = []
                    self.children[node].append(neighbor)
                    q.put(neighbor)
    def get_parent(self, node):
        return self.parent[node]
    def get_depth(self, node):
        return self.depth[node]
    def get_children(self, node):
        return self.children[node] if node in self.children else []
    def get_root(self):
        return self.root
    def get_graph(self):
        return self.graph
    def compute_common_ancestor(self, node1, node2):
        while self.get_depth(node1) > self.get_depth(node2):
            node1 = self.get_parent(node1)
        while self.get_depth(node2) > self.get_depth(node1):
            node2 = self.get_parent(node2)
        while node1 != node2:
            node1 = self.get_parent(node1)
            node2 = self.get_parent(node2)
        return node1
    def get_path(self, node):
        path = []
        while node != -1:
            path.append(node)
            node = self.parent[node]
        return path[::-1]
    def is_edge_in_tree(self, node1, node2):
        return self.parent[node1] == node2 or self.parent[node2] == node1
    def __str__(self):
        return "\n".join([f"{i}: {self.parent[i]}" for i in range(self.graph.size())])