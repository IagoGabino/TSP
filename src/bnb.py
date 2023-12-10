from heapq import heappush, heappop
import tsplib95
import time
import memory_profiler

# class Node to store information of search tree
class Node:
    def __init__(self, path, bound):
        self.path = path  # current path
        self.bound = bound  # lower bound of the path

    def __lt__(self, other):
        return self.bound < other.bound  # compare function for priority queue
    
def calculate_bound(path, adj):
    N = len(adj)
    lower_bound = 0

    # verify if the path contains non-existent edges
    for i in range(len(path) - 1):
        if adj[path[i]][path[i + 1]] == 0:
            return float('inf')  # return infinity if an edge does not exist
        lower_bound += adj[path[i]][path[i + 1]]

    # add the smallest costs of edges for unvisited nodes
    for i in range(N):
        if i not in path:
            min_edge = sorted(adj[i])[1] if len(adj[i]) > 1 else float('inf')
            if min_edge == float('inf'):
                return float('inf')  # return infinity if an edge does not exist
            lower_bound += min_edge

    return lower_bound

# function to expand nodes in heap and choose next node with least lower bound
def best_first_search(adj, start=0):
    N = len(adj)
    pq = []

    # add initial node to the priority queue
    initial_path = [start]
    initial_bound = calculate_bound(initial_path, adj)
    heappush(pq, Node(initial_path, initial_bound))

    best_cost = float('inf')
    best_path = []

    while pq:
        node = heappop(pq)

        # verify if this node can lead to a better solution
        if node.bound < best_cost:
            last_vertex = node.path[-1]

            # expand adjacent nodes
            for i in range(N):
                if i not in node.path:
                    new_path = node.path + [i]
                    if len(new_path) < N:
                        # calculate new lower bound
                        new_bound = calculate_bound(new_path, adj)
                        if new_bound < best_cost:
                            heappush(pq, Node(new_path, new_bound))
                    else:
                        # add the initial vertex to complete the cycle
                        new_path.append(start)
                        if all(adj[new_path[i]][new_path[i + 1]] > 0 for i in range(N)):
                            new_cost = sum(adj[new_path[i]][new_path[i + 1]] for i in range(N))
                            if new_cost < best_cost:
                                best_cost = new_cost
                                best_path = new_path

    return best_cost, best_path

def convert_to_matrix(graph):
    # Obtém o número de nós do grafo
    N = graph.dimension

    # Inicializa a matriz de adjacência com infinito em todas as posições
    maxsize = float('inf')
    adj_matrix = [[0 if i == j else maxsize for i in range(N)] for j in range(N)]

    # Preenche a matriz de adjacência com os pesos das arestas
    for i in range(N):
        for j in range(i + 1, N):
            distance = graph.get_weight(i + 1, j + 1)
            
            # Preenche a matriz de adjacência com a distância calculada
            adj_matrix[i][j] = distance
            adj_matrix[j][i] = distance

    return adj_matrix

def branch_and_bound(graph):
    start = time.time()

    adj_matrix = convert_to_matrix(graph)
    cost, path = best_first_search(adj_matrix)

    end = time.time()
    execution_time = end - start

    adjusted_path = [p + 1 for p in path]

    return cost, adjusted_path, execution_time

# tests
if __name__ == "__main__":
    # test
    files = ['test10.tsp', 'test15.tsp']
    folder = '../test_bnb'

    # header
    with open('results_bnb.txt', 'w') as f:
        f.write('Instancia, Custo, Tempo, Memoria\n')

    for file in files:
        print('Testing', file)
        graph = tsplib95.load(f'{folder}/{file}')
        cost, path, execution_time = branch_and_bound(graph)
        mem_usage, retval = memory_profiler.memory_usage((branch_and_bound, (graph,)), retval=True, max_usage=True)
        peak_memory = mem_usage
        cost, path, execution_time = retval
        cost, path, execution_time = branch_and_bound(graph)

        # peak_memory = memory_profiler.memory_usage()[0]

        # save to results_bnb.txt
        with open('results_bnb.txt', 'a') as f:
            f.write(f'{file}, {cost}, {execution_time}, {peak_memory}\n')
            f.write(f'{path}\n')

        