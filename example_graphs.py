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
    return None

def all_example_graphs_indexes():
    return range(1,9)