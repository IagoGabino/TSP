import time
import networkx as nx
import tsplib95
from memory_profiler import memory_usage

def christofides(graph):
    start = time.time()

    # minimum spanning tree
    MST = nx.minimum_spanning_tree(graph)

    # find nodes with odd degree in MST
    degrees = nx.degree(MST)
    oddNodes = [x[0] for x in degrees if degrees[x[0]] % 2 == 1]

    # create subgraph of odd degree nodes
    oddNodesSubgraph = nx.subgraph(graph, oddNodes)

    # find minimum weight matching
    matching = list(nx.min_weight_matching(oddNodesSubgraph, maxcardinality=True))

    # combine MST and matching
    MSTMultiGraph = nx.MultiGraph(MST)
    for edge in matching:
        MSTMultiGraph.add_edge(edge[0], edge[1], weight=graph[edge[0]][edge[1]]['weight'])

    # find Eulerian circuit
    eulerian_circuit = list(nx.eulerian_circuit(MSTMultiGraph, source=1))
   
    visited = set()
    hamiltonian_cycle = []
    total_weight = 0

    for u, v in eulerian_circuit:
        if u not in visited:
            hamiltonian_cycle.append(u)
            visited.add(u)
            if len(hamiltonian_cycle) > 1:
                total_weight += graph[hamiltonian_cycle[-2]][u]['weight']

    # Fechando o ciclo e adicionando o peso da última aresta
    hamiltonian_cycle.append(hamiltonian_cycle[0])
    total_weight += graph[hamiltonian_cycle[-2]][hamiltonian_cycle[-1]]['weight']

    end = time.time()
    execution_time = end - start

    return total_weight, hamiltonian_cycle, execution_time

# tests
if __name__ == "__main__":
    problem = tsplib95.load('lib/p654.tsp')
    graph = problem.get_graph()
    # mem_usage, retval= memory_usage((christofides, (graph,)), retval=True, max_usage=True)
    # peak_memory = mem_usage
    weight, path, execution_time = christofides(graph)
    print("Peso total:", weight)
    print("Caminho:", path)
    print("Tempo de execução:", execution_time)