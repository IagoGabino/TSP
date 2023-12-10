import time
import networkx as nx
import tsplib95
from memory_profiler import memory_usage

def twiceAround(graph):
    start = time.time()
    # minimum spanning tree
    minSpanTree = nx.minimum_spanning_tree(graph)

    # pre-order depth-first search
    startNode = list(minSpanTree.nodes)[0]
    dfsPath = list(nx.dfs_preorder_nodes(minSpanTree, startNode))

    # hamiltonian cycle from MST
    hamiltonianPath = []
    visited = set()
    for node in dfsPath:
        if node not in visited:
            visited.add(node)
            hamiltonianPath.append(node)
    hamiltonianPath.append(hamiltonianPath[0])  # back to start

    # calculate total weight
    totalWeight = sum(graph[hamiltonianPath[i]][hamiltonianPath[i+1]]['weight'] for i in range(len(hamiltonianPath) - 1))

    end = time.time()
    executionTime = end - start

    return totalWeight, hamiltonianPath, executionTime

# tests
if __name__ == "__main__":
    problem = tsplib95.load('lib/eil51.tsp')
    graph = problem.get_graph()
    mem_usage, retval= memory_usage((twiceAround, (graph,)), retval=True, max_usage=True)
    peak_memory = mem_usage
    weight, path, executionTime = retval
    print("Peso total:", weight)
    print("Caminho:", path)
    print("Tempo de execução:", executionTime)