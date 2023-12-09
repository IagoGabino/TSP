import os
import subprocess
import tsplib95
import re
import csv
import time

# Configurações
diretorio_das_instancias = "./lib"  # Ajuste para o seu caminho correto
algoritmos = {1: "tatt", 2: "ctfds"}
tempo_limite = 1800  # 30 minutos em segundos
arquivo_de_log = "results_tsp.txt"

def extrair_numero(nome_arquivo):
    # Procura por números no nome do arquivo e retorna o primeiro que encontrar convertido para int
    numeros = re.findall(r'\d+', nome_arquivo)
    return int(numeros[0]) if numeros else -1

# Iniciar log
with open(arquivo_de_log, "w") as log_file:
    log_file.write("Instancia Algoritmo,Resultado,Tempo,Memoria,Qualidade\n")

# Armazena a menor dimensão que falhou para cada algoritmo
menor_dimensao_falha = {alg: float('inf') for alg in algoritmos.values()}

def executar_algoritmos_tsp():
    for nome_arquivo in sorted(os.listdir(diretorio_das_instancias), key=extrair_numero):
        if nome_arquivo.endswith(".tsp"):
            caminho_completo = os.path.join(diretorio_das_instancias, nome_arquivo)
            try:
                problema = tsplib95.load(caminho_completo)
                dimensao = problema.dimension
                print(f"Trabalhando na instância {nome_arquivo} de dimensão {dimensao}.")
            except Exception as e:
                print(f"Erro ao carregar o problema TSP do arquivo {nome_arquivo}: {e}")
                continue

            for alg_num, alg_nome in algoritmos.items():
                # Verifique se o algoritmo atual pode ser executado para esta dimensão
                if dimensao < menor_dimensao_falha[alg_nome]:
                    comando = ["python", "main.py", caminho_completo, str(alg_num)]
                    print(f"Começando a execução: {comando}")
                    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    try:
                        stdout, stderr = processo.communicate(timeout=tempo_limite)
                        resultado = stdout.decode('utf-8', 'ignore').strip()

                        if processo.returncode == 0 and resultado:
                            print(f"Resultado para {alg_nome}: {resultado}")
                            # RESULTADO = 696, 0.0035071372985839844, 57.25, 77.29885057471265%
                        else:
                            print(f"Erro ou timeout para {alg_nome} em {nome_arquivo}")
                            if dimensao < menor_dimensao_falha[alg_nome]:
                                menor_dimensao_falha[alg_nome] = dimensao
                    except subprocess.TimeoutExpired:
                        processo.kill()
                        stdout, stderr = processo.communicate()
                        resultado = "Timeout"
                        print(f"Timeout para {alg_nome} em {nome_arquivo}")
                        if dimensao < menor_dimensao_falha[alg_nome]:
                            menor_dimensao_falha[alg_nome] = dimensao
                    with open(arquivo_de_log, "a") as log_file:
                        log_file.write(f"{nome_arquivo}, {alg_nome}, {resultado}\n")
                else:
                    print(f"{alg_nome} não será executado na instância {nome_arquivo} pois excedeu o tempo em uma instância de dimensão menor.")

if __name__ == "__main__":
    start = time.time()

    executar_algoritmos_tsp()

    end = time.time()
    execution_time = end - start

    print("Tempo de execução dos testes:", execution_time)