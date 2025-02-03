from equivalence_class_to_ordering import PartialOrdering, TotalOrdering
from shape_to_equivalence_class import EquivalenceClasses
from shape_builder import Shape

def ordering_to_positions(ordering: TotalOrdering) -> dict:
    equivalence_classes : EquivalenceClasses = ordering.get_equiv_classes()
    nodes_positions = dict()
    current_position = 0
    for class_x in ordering.get_ordering_x():
        for node in equivalence_classes.get_nodes_of_class_x(class_x):
            if node not in nodes_positions:
                nodes_positions[node] = (0, 0)
            nodes_positions[node] = (current_position, 0)
        current_position += 1
    current_position = 0
    for class_y in ordering.get_ordering_y():
        for node in equivalence_classes.get_nodes_of_class_y(class_y):
            if node not in nodes_positions:
                nodes_positions[node] = (0, 0)
            nodes_positions[node] = (nodes_positions[node][0], current_position)
        current_position += 1
    return nodes_positions

from time import perf_counter

def shape_to_positions_ordering(shape: Shape) -> dict:
    start = perf_counter()
    equivalence_classes = EquivalenceClasses(shape)
    partial_ordering = PartialOrdering(equivalence_classes)
    total_ordering = TotalOrdering(partial_ordering)
    positions = ordering_to_positions(total_ordering)
    end = perf_counter()
    print(f"Positions computing total time (Eq class): {end-start}")
    return positions