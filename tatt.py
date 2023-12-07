import time
import networkx as nx
import tsplib95
from memory_profiler import memory_usage

def twiceAround(graph):
    start = time.time()
    # minimum spanning tree
    MST = nx.minimum_spanning_tree(graph)

    # pre-order depth-first search
    start_node = list(MST.nodes)[0]
    path = list(nx.dfs_preorder_nodes(MST, start_node))

    # hamiltonian cycle from MST
    hamiltonian_cycle = []
    visited = set()
    for node in path:
        if node not in visited:
            visited.add(node)
            hamiltonian_cycle.append(node)
    hamiltonian_cycle.append(hamiltonian_cycle[0])  # back to start

    # calculate total weight
    total_weight = sum(graph[hamiltonian_cycle[i]][hamiltonian_cycle[i+1]]['weight'] for i in range(len(hamiltonian_cycle) - 1))

    end = time.time()
    execution_time = end - start

    return total_weight, hamiltonian_cycle, execution_time

# tests
if __name__ == "__main__":
    problem = tsplib95.load('lib/eil51.tsp')
    graph = problem.get_graph()
    mem_usage, retval= memory_usage((twiceAround, (graph,)), retval=True, max_usage=True)
    peak_memory = mem_usage
    weight, path, execution_time = retval
    print("Peso total:", weight)
    print("Caminho:", path)
    print("Tempo de execução:", execution_time)