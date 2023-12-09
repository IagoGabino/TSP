import tsplib95
import sys
from threading import Timer
from tatt import twiceAround
from memory_profiler import memory_usage
from opt import get_optimal_distance
from ctfds import christofides

def load_tsp_problem(file_path):
    # Carrega o problema TSP
    problem = tsplib95.load(file_path)

    # Converte para um grafo do NetworkX para facilitar a manipulação
    graph = problem.get_graph()

    return graph

def timeout_handler():
    print("Tempo limite excedido (30 minutos). Execução abortada.")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py [caminho_para_o_arquivo.tsp] [algoritmo]")
        print("Algoritmos disponíveis: 1 (TATT), 2 (CTFDS)")
        sys.exit(1)

    file_path = sys.argv[1]
    algorithm = int(sys.argv[2])

    graph = load_tsp_problem(file_path)

    # Define um temporizador para 30 minutos
    timer = Timer(1800, timeout_handler)
    timer.start()

    # Executa o algoritmo
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
            pass
        else:
            print("Algoritmo não reconhecido.")
            sys.exit(1)
    finally:
        timer.cancel()

    # Qualidade da solução
    optimal_distance = get_optimal_distance(file_path)
    quality = 0
    if weight > 0:
        quality = optimal_distance / weight

    # tudo em uma linha em sequencia
    print(f"{weight}, {execution_time}, {peak_memory}, {quality*100}%")

if __name__ == "__main__":
    main()