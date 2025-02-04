from graph import Graph
from shape_builder import Shape

class EquivalenceClasses:
    def __init__(self, shape: Shape):
        self._shape : Shape = shape
        graph: Graph = shape.get_original_graph()
        self._nodes_classes_x = [-1 for _ in range(graph.size())]
        self._nodes_classes_y = [-1 for _ in range(graph.size())]
        self._next_class = 0
        is_edge_visited = [[False for _ in range(graph.size())] for _ in range(graph.size())]
        for i in range(graph.size()):
            for j in graph.get_neighbors(i):
                if is_edge_visited[i][j]: continue
                is_edge_visited[i][j] = True
                is_edge_visited[j][i] = True
                new_class = self._next_class
                self._next_class += 1
                if shape.is_horizontal(i, j):
                    self._nodes_classes_y[i] = new_class
                    self._nodes_classes_y[j] = new_class
                    if shape.is_left(i, j):
                        left, right = j, i
                    else:
                        left, right = i, j
                    left, right = self._expand_edge_horizontally(left, right, is_edge_visited, new_class)
                elif shape.is_vertical(i, j):
                    self._nodes_classes_x[i] = new_class
                    self._nodes_classes_x[j] = new_class
                    if shape.is_down(i, j):
                        down, up = j, i
                    else:
                        down, up = i, j
                    down, up = self._expand_edge_vertically(down, up, is_edge_visited, new_class)
                else: assert False
        self._class_to_nodes_x = dict()
        self._class_to_nodes_y = dict()
        for i,elem in enumerate(self._nodes_classes_x):
            if elem not in self._class_to_nodes_x:
                self._class_to_nodes_x[elem] = []
            self._class_to_nodes_x[elem].append(i)
        for i,elem in enumerate(self._nodes_classes_y):
            if elem not in self._class_to_nodes_y:
                self._class_to_nodes_y[elem] = []
            self._class_to_nodes_y[elem].append(i)
        if -1 in self._class_to_nodes_x:
            for node in self._class_to_nodes_x[-1]:
                self._nodes_classes_x[node] = self._next_class
                self._class_to_nodes_x[self._next_class] = [node]
                self._next_class += 1
            self._class_to_nodes_x.pop(-1)
        if -1 in self._class_to_nodes_y:
            for node in self._class_to_nodes_y[-1]:
                self._nodes_classes_y[node] = self._next_class
                self._class_to_nodes_y[self._next_class] = [node]
                self._next_class += 1
            self._class_to_nodes_y.pop(-1)
    def _edge_expanding_function(self, node, direction_function, is_edge_visited, new_class, belonging_class):
        starting_node = node
        visited_nodes = {node}
        while (True):
            neighbor = direction_function(node)
            if neighbor is None: break
            belonging_class[neighbor] = new_class
            is_edge_visited[node][neighbor] = True
            is_edge_visited[neighbor][node] = True
            node = neighbor
            if node in visited_nodes:
                error = f"Edge expanding function loops while expanding node: {starting_node}\ndirection of expansion name: {direction_function.__name__}"
                raise Exception(error)
            visited_nodes.add(node)
        return node
    def _keep_expanding_right(self, node, is_edge_visited, new_class):
        return self._edge_expanding_function(node, self._shape.has_node_a_right_neighbor, is_edge_visited, new_class, self._nodes_classes_y)
    def _keep_expanding_left(self, node, is_edge_visited, new_class):
        return self._edge_expanding_function(node, self._shape.has_node_a_left_neighbor, is_edge_visited, new_class, self._nodes_classes_y)
    def _keep_expanding_up(self, node, is_edge_visited, new_class):
        return self._edge_expanding_function(node, self._shape.has_node_an_up_neighbor, is_edge_visited, new_class, self._nodes_classes_x)
    def _keep_expanding_down(self, node, is_edge_visited, new_class):
        return self._edge_expanding_function(node, self._shape.has_node_a_down_neighbor, is_edge_visited, new_class, self._nodes_classes_x)
    def _expand_edge_horizontally(self, left, right, is_edge_visited, new_class):
        left = self._keep_expanding_left(left, is_edge_visited, new_class)
        right = self._keep_expanding_right(right, is_edge_visited, new_class)
        return (left, right)
    def _expand_edge_vertically(self, down, up, is_edge_visited, new_class):
        down = self._keep_expanding_down(down, is_edge_visited, new_class)
        up = self._keep_expanding_up(up, is_edge_visited, new_class)
        return (down, up)
    def __str__(self):
        s = f"Nodes classes x: {self._nodes_classes_x}\nNodes classes y: {self._nodes_classes_y}\n"
        s += f"Class to nodes x: {self._class_to_nodes_x}\nClass to nodes y: {self._class_to_nodes_y}\n"
        return s
    def get_original_shape(self):
        return self._shape
    def get_node_class_x(self, node):
        return self._nodes_classes_x[node]
    def get_node_class_y(self, node):
        return self._nodes_classes_y[node]
    def get_classes_list_x(self):
        return self._class_to_nodes_x.keys()
    def get_classes_list_y(self):
        return self._class_to_nodes_y.keys()
    def get_nodes_of_class_x(self, class_x):
        return self._class_to_nodes_x.get(class_x, [])
    def get_nodes_of_class_y(self, class_y):
        return self._class_to_nodes_y.get(class_y, [])