# def is_edge_in_cycle(cycle, node1, node2):
#     if node1 not in cycle or node2 not in cycle:
#         return False
#     index1 = cycle.index(node1)
#     index2 = cycle.index(node2)
#     return (index1 + 1) % len(cycle) == index2 or (index2 + 1) % len(cycle) == index1

# def find_common_path_in_cycles(cycle1, cycle2):
#     position = None
#     for i in range(len(cycle1)):
#         if cycle1[i] not in cycle2:
#             position = i
#     if position is None:
#         return find_common_path_in_cycles(cycle2, cycle1)
#     while cycle1[position] not in cycle2:
#         position = (position + 1) % len(cycle1)
#     path = []
#     while cycle1[position] in cycle2:
#         path.append(cycle1[position])
#         position = (position + 1) % len(cycle1)
#     return path

# def add_cycles(cycle1: list, cycle2: list):
#     path_in_common = find_common_path_in_cycles(cycle1, cycle2)
#     print("found common path:", path_in_common)
#     if len(path_in_common) == 0: raise Exception("No common edge")
#     if len(path_in_common) == 1: raise Exception("Only common node")
#     position = cycle1.index(path_in_common[0])
#     if cycle1[(position+1) % len(cycle1)] == path_in_common[1]:
#         cycle1.reverse()
#         position = cycle1.index(path_in_common[0])
#     result = []
#     while True:
#         result.append(cycle1[position])
#         if cycle1[position] == path_in_common[-1]:
#             break
#         position = (position+1) % len(cycle1)
#     path_in_common.reverse()
#     position = cycle2.index(path_in_common[0])
#     if cycle2[(position+1) % len(cycle2)] == path_in_common[1]:
#         cycle2.reverse()
#         position = cycle2.index(path_in_common[0])
#     position = (position+1)%len(cycle2)
#     while True:
#         if cycle2[position] == path_in_common[-1]:
#             break
#         result.append(cycle2[position])
#         position = (position+1) % len(cycle2)
#     return result

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
        return "\n".join([f"{node}: {self.adjacency_list[node]}" for node in range(self.size())])

    def find_all_cycles(self):
        def find_all_cycles_with_node(node, path: list):
            path.append(node)
            for neighbor in self.get_neighbors(node):
                if visited_global[neighbor]: continue
                if len(path) > 1 and neighbor == path[-2]: continue
                if neighbor in path:
                    if neighbor == path[0]:
                        cycles.append(path[path.index(neighbor):])
                else:
                    find_all_cycles_with_node(neighbor, path.copy())
        visited_global = [False] * self.size()
        cycles = []
        for node in range(self.size()):
            find_all_cycles_with_node(node, [])
            visited_global[node] = True
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
    
    def compute_cycle_basis(self, tree_root = 0):
        spanning = SpanningTree(self, tree_root)
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
    
    def get_edges(self):
        return self.edges
    
    def _cycles_sum(self, cycles):
        keep_edge = dict()
        for cycle in cycles:
            for i in range(len(cycle)):
                edge = (cycle[i], cycle[(i+1)%len(cycle)])
                reversed_edge = (cycle[(i+1)%len(cycle)], cycle[i])
                if edge not in keep_edge:
                    keep_edge[edge] = True
                    keep_edge[reversed_edge] = True
                    starting_node = edge[0]
                else:
                    keep_edge[edge] = not keep_edge[edge]
                    keep_edge[reversed_edge] = not keep_edge[reversed_edge]
                    if keep_edge[edge]:
                        starting_node = edge[0]
        result = []
        def dfs(node, path: list):
            path.append(node)
            for neighbor in self.get_neighbors(node):
                if not keep_edge.get((node, neighbor), False): continue
                keep_edge[(node, neighbor)] = False
                keep_edge[(neighbor, node)] = False
                dfs(neighbor, path)
        dfs(starting_node, result)
        result.pop()
        return result

    def compute_cycle_basis_plus(self, tree_root = 0):
        basis = self.compute_cycle_basis(tree_root)
        extra_cycle = self._cycles_sum(basis)
        return basis + [extra_cycle]

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