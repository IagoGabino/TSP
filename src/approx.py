import tsplib95
import sys
from threading import Timer
from memory_profiler import memory_usage
from opt import get_optimal_distance
from tatt import twiceAround
from ctfds import christofides

def load_tsp_problem(file_path):
    problem = tsplib95.load(file_path)
    graph = problem.get_graph()
    return graph

def timeout_handler():
    print("Limit exceeded. Exiting...")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python approx.py <file_path> <algorithm>")
        print("<algorithm> = 1 (TATT) or 2 (CTFDS)")
        sys.exit(1)

    file_path = sys.argv[1]
    algorithm = int(sys.argv[2])

    graph = load_tsp_problem(file_path)

    # Timer 30 minutes
    timer = Timer(1800, timeout_handler)
    timer.start()

    # Algorithm execution
    peak_memory = 0
    weight = 0
    path = []
    try:
        if algorithm == 1:
            mem_usage, retval = memory_usage((twiceAround, (graph,)), retval=True, max_usage=True)
            peak_memory = mem_usage
            weight, path, execution_time = retval
        elif algorithm == 2:
            mem_usage, retval = memory_usage((christofides, (graph,)), retval=True, max_usage=True)
            peak_memory = mem_usage
            weight, path, execution_time = retval
        else:
            print("Algoritmo não reconhecido.")
            sys.exit(1)
    finally:
        timer.cancel()

    # Calculating quality from optimal distance
    optimal_distance = get_optimal_distance(file_path)
    quality = 0
    if weight > 0:
        quality = optimal_distance / weight

    # Output
    print(f"{weight}, {execution_time}, {peak_memory}, {quality*100}%")

if __name__ == "__main__":
    main()