from graph import Graph

def graph1():
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(1, 6)
    graph.add_edge(6, 7)
    graph.add_edge(3, 7)
    return graph

def graph2():
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(1, 6)
    graph.add_edge(6, 5)
    return graph

def graph3():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(0, 4)
    graph.add_edge(0, 2)
    return graph

def graph4():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(0, 4)
    graph.add_edge(0, 5)
    graph.add_edge(5, 2)
    return graph

def graph5():
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)

    graph.add_edge(0, 4)
    graph.add_edge(1, 5)
    graph.add_edge(4, 5)

    graph.add_edge(0, 6)
    graph.add_edge(1, 7)
    graph.add_edge(6, 7)

    return graph

def graph6():
    graph = Graph(17)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(1, 6)
    graph.add_edge(6, 7)
    graph.add_edge(3, 7)
    
    graph.add_edge(0, 8)
    graph.add_edge(8, 9)
    graph.add_edge(10, 9)
    graph.add_edge(10, 2)
    graph.add_edge(10, 11)
    graph.add_edge(12, 11)
    graph.add_edge(12, 13)
    graph.add_edge(16, 13)
    graph.add_edge(16, 15)
    graph.add_edge(16, 8)
    graph.add_edge(14, 15)
    graph.add_edge(14, 13)
    return graph

def graph7():
    graph = Graph(10)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)

    graph.add_edge(0, 4)
    graph.add_edge(1, 5)
    graph.add_edge(4, 5)


    graph.add_edge(0, 6)
    graph.add_edge(1, 7)


    graph.add_edge(6, 8)
    graph.add_edge(7, 9)
    graph.add_edge(8, 9)

    return graph

def graph8():
    graph = Graph(40)
    graph.add_edge(12, 11)
    graph.add_edge(10, 11)
    graph.add_edge(9, 10)
    graph.add_edge(8, 9)
    graph.add_edge(32, 33)
    graph.add_edge(13, 22)
    graph.add_edge(23, 24)
    graph.add_edge(35, 21)
    graph.add_edge(21, 36)
    graph.add_edge(0, 30)
    graph.add_edge(30, 14)
    graph.add_edge(21, 25)
    graph.add_edge(25, 7)
    graph.add_edge(15, 27)
    graph.add_edge(1, 16)
    graph.add_edge(16, 29)
    graph.add_edge(28, 31)
    graph.add_edge(31, 6)
    graph.add_edge(37, 20)
    graph.add_edge(20, 38)
    graph.add_edge(17, 18)
    graph.add_edge(19, 39)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(26, 34)

    graph.add_edge(34, 33)
    graph.add_edge(32, 10)
    graph.add_edge(12, 0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(13, 30)
    graph.add_edge(16, 17)
    graph.add_edge(14, 15)
    graph.add_edge(15, 29)
    graph.add_edge(11, 22)
    graph.add_edge(22, 35)
    graph.add_edge(37, 18)
    graph.add_edge(18, 3)
    graph.add_edge(9, 23)
    graph.add_edge(23, 36)
    graph.add_edge(38, 19)
    graph.add_edge(19, 4)
    graph.add_edge(21, 27)
    graph.add_edge(27, 28)
    graph.add_edge(24, 25)
    graph.add_edge(31, 39)
    graph.add_edge(7, 8)
    graph.add_edge(7, 6)
    graph.add_edge(5, 6)
    graph.add_edge(32, 26)


    graph.add_edge(20, 34)

    return graph

def graph9():
    graph = Graph(10)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(7, 8)
    graph.add_edge(8, 9)
    return graph

def graph10():
    graph = Graph(12)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(1, 6)
    graph.add_edge(6, 11)
    graph.add_edge(11, 7)
    graph.add_edge(3, 7)
    
    graph.add_edge(0, 8)
    graph.add_edge(8, 9)
    graph.add_edge(10, 9)
    graph.add_edge(10, 2)
    return graph

def graph11():
    graph = Graph(36)
    graph.add_edge(12, 11) 
    graph.add_edge(10, 11)
    graph.add_edge(9, 10)
    graph.add_edge(8, 9)
    graph.add_edge(32, 33)
    graph.add_edge(13, 22) 
    graph.add_edge(23, 24)
    graph.add_edge(35, 21)
    graph.add_edge(0, 30) 
    graph.add_edge(30, 14)
    graph.add_edge(21, 25)
    graph.add_edge(25, 7)
    graph.add_edge(15, 27)
    graph.add_edge(1, 16)
    graph.add_edge(16, 29)
    graph.add_edge(28, 31)
    graph.add_edge(31, 6)
    graph.add_edge(17, 18)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(26, 34)

    graph.add_edge(34, 33)
    graph.add_edge(32, 10)
    graph.add_edge(12, 0) 
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(13, 30) 
    graph.add_edge(16, 17)
    graph.add_edge(14, 15)
    graph.add_edge(15, 29)
    graph.add_edge(11, 22) 
    graph.add_edge(22, 35)
    graph.add_edge(18, 3)
    graph.add_edge(9, 23)
    graph.add_edge(19, 4)
    graph.add_edge(21, 27)
    graph.add_edge(27, 28)
    graph.add_edge(24, 25)
    graph.add_edge(7, 8)
    graph.add_edge(7, 6)
    graph.add_edge(5, 6)
    graph.add_edge(32, 26)

    graph.add_edge(20, 34)

    return graph

def graph12():
    graph = Graph(12)
    graph.add_edge(0, 1)
    graph.add_edge(0, 6)
    graph.add_edge(2, 1)
    graph.add_edge(2, 3)
    graph.add_edge(5, 1)
    graph.add_edge(5, 6)
    graph.add_edge(4, 3)
    graph.add_edge(7, 8)
    graph.add_edge(9, 6)
    graph.add_edge(9, 7)

    graph.add_edge(5, 10)
    graph.add_edge(10, 4)

    graph.add_edge(4, 11)
    graph.add_edge(8, 11)
     
    return graph

def get_example_graph(n):
    if n == 1:
        return graph1()
    if n == 2:
        return graph2()
    if n == 3:
        return graph3()
    if n == 4:
        return graph4()
    if n == 5:
        return graph5()
    if n == 6:
        return graph6()
    if n == 7:
        return graph7()
    if n == 8:
        return graph8()
    if n == 9:
        return graph9()
    if n == 10:
        return graph10()
    if n == 11:
        return graph11()
    if n == 12:
        return graph12()
    return None

def all_example_graphs_indexes():
    return range(1, 13)

def generate_random_graph_tree(number_of_nodes: int):
    import random
    graph = Graph(number_of_nodes)
    nodes = list(range(number_of_nodes))
    random.shuffle(nodes)
    tree = [nodes[0]]
    for i in range(1, number_of_nodes):
        node = nodes[i]
        random.shuffle(tree)
        while (len(graph.get_neighbors(tree[0])) >= 4):
            random.shuffle(tree)
        parent = tree[0]
        graph.add_edge(node, parent)
        tree.append(node)
    return graph

# makes a random graph with n nodes
# the graph is connected, fist a random tree is created and then the remaining edges are added
# each node cannot have more than 4 neighbors
def generate_random_graph(number_of_nodes: int, number_of_edges: int):
    import random
    graph = Graph(number_of_nodes)
    nodes = list(range(number_of_nodes))
    random.shuffle(nodes)
    tree = [nodes[0]]
    for i in range(1, number_of_nodes):
        node = nodes[i]
        random.shuffle(tree)
        while (len(graph.get_neighbors(tree[0])) >= 4):
            random.shuffle(tree)
        parent = tree[0]
        graph.add_edge(node, parent)
        tree.append(node)
    edges_left_to_add = number_of_edges - number_of_nodes + 1
    while edges_left_to_add > 0:
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)
        while (node2 in graph.get_neighbors(node1)):
            node2 = random.choice(nodes)
        if node1 != node2 and len(graph.get_neighbors(node1)) < 4 and len(graph.get_neighbors(node2)) < 4:
            graph.add_edge(node1, node2)
            edges_left_to_add -= 1
    return graph