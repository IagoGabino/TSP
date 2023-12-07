from heapq import heappush, heappop

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
            min_edge = min(adj[i][j] if adj[i][j] > 0 else float('inf') for j in range(N) if j != i)
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
    # tsplib95 to adjacency matrix
    maxsize = float('inf')
    N = graph.number_of_nodes()
    adj_matrix = [[0 if i == j else maxsize for i in range(N)] for j in range(N)]
    for i, j, data in graph.edges(data=True):
        # tsp instances start with node 1, so we need to subtract 1 from each node
        adj_matrix[i-1][j-1] = data['weight'] 
        adj_matrix[j-1][i-1] = data['weight']
    return adj_matrix

def branch_and_bound(graph):
    adj_matrix = convert_to_matrix(graph)
    return best_first_search(adj_matrix)

# tests
if __name__ == "__main__":
    import tsplib95
    problem = tsplib95.load('lib/eil51.tsp')
    graph = problem.get_graph()
    weight, path = branch_and_bound(graph)
    print("Peso total:", weight)
    print("Caminho:", path)