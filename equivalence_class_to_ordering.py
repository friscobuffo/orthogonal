from shape_to_equivalence_class import EquivalenceClasses
from shape_builder import Shape
from graph import Graph

class PartialOrdering:
    def __init__(self, equivalence_classes: EquivalenceClasses):
        shape : Shape = equivalence_classes.get_original_shape()
        graph : Graph = shape.get_original_graph()
        self._partial_ordering_x = dict()
        self._partial_ordering_y = dict()
        self._equivalence_classes = equivalence_classes
        for node in range(graph.size()):
            for neighbor in graph.get_neighbors(node):
                if shape.is_horizontal(node, neighbor):
                    node_class_x = equivalence_classes.get_node_class_x(node)
                    neighbor_class_x = equivalence_classes.get_node_class_x(neighbor)
                    if node_class_x == -1 or neighbor_class_x == -1: continue
                    if shape.is_left(node, neighbor):
                        self._partial_ordering_x[(neighbor_class_x, node_class_x)] = "<"
                    elif shape.is_right(node, neighbor):
                        self._partial_ordering_x[(node_class_x, neighbor_class_x)] = "<"
                    else: assert False
                elif shape.is_vertical(node, neighbor):
                    node_class_y = equivalence_classes.get_node_class_y(node)
                    neighbor_class_y = equivalence_classes.get_node_class_y(neighbor)
                    if node_class_y == -1 or neighbor_class_y == -1: continue
                    if shape.is_down(node, neighbor):
                        self._partial_ordering_y[(neighbor_class_y, node_class_y)] = "<"
                    elif shape.is_up(node, neighbor):
                        self._partial_ordering_y[(node_class_y, neighbor_class_y)] = "<"
                    else: assert False
    def __str__(self):
        return f"Partial ordering x: {self._partial_ordering_x}\nPartial ordering y:{self._partial_ordering_y}\n"
    def get_relation_between_x_classes(self, class1, class2):
        return self._partial_ordering_x.get((class1, class2), None)
    def get_relation_between_y_classes(self, class1, class2):
        return self._partial_ordering_y.get((class1, class2), None)
    def get_equiv_classes(self) -> EquivalenceClasses:
        return self._equivalence_classes
    def get_relationships_x(self):
        return self._partial_ordering_x
    def get_relationships_y(self):
        return self._partial_ordering_y

from collections import deque

class TotalOrdering:
    def __init__(self, partial_ordering: PartialOrdering):
        self._partial_ordering = partial_ordering
        self._total_ordering_x = self._build_total_ordering(self._partial_ordering.get_relationships_x())
        self._total_ordering_y = self._build_total_ordering(self._partial_ordering.get_relationships_y())
        self._equivalence_classes = partial_ordering.get_equiv_classes()
    def _build_total_ordering(self, relationships: dict):
        dag = dict()
        for class1, class2 in relationships.keys():
            if class1 not in dag:
                dag[class1] = []
            if class2 not in dag:
                dag[class2] = []
            dag[class1].append(class2)
        in_degree = dict()
        for node in dag:
            if node not in in_degree:
                in_degree[node] = 0
            for neighbor in dag[node]:
                if neighbor not in in_degree:
                    in_degree[neighbor] = 0
                in_degree[neighbor] += 1
        queue = deque([node for node in dag if in_degree[node] == 0])
        order = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in dag[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        if len(order) != len(dag):
            raise ValueError("Cycle detected, no valid topological ordering exists.")
        return order
    def get_equiv_classes(self) -> EquivalenceClasses:
        return self._equivalence_classes
    def get_ordering_x(self):
        return self._total_ordering_x
    def get_ordering_y(self):
        return self._total_ordering_y
    def __str__(self):
        return f"Total ordering x: {self._total_ordering_x}\nTotal ordering y:{self._total_ordering_y}\n"