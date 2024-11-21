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
    graph.add_edge(3, 5)
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

def get_example_graph(n):
    if n==1:
        return graph1()
    if n==2:
        return graph2()
    if n==3:
        return graph3()
    if n==4:
        return graph4()
    if n==5:
        return graph5()
    return None