from prova_pli import check_graph_pli
from prova_sat import check_graph_sat
from example_graphs import get_example_graph
from time import perf_counter

total_time_pli = 0.0
total_time_sat = 0.0
for i in range(1,6):
    graph = get_example_graph(i)
    start = perf_counter()
    print(check_graph_pli(graph))
    total_time_pli += (perf_counter() - start)
    start = perf_counter()
    print(check_graph_sat(graph))
    total_time_sat += (perf_counter() - start)
    print()
print(total_time_pli)
print(total_time_sat)
