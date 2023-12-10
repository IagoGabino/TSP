import os
import subprocess
import tsplib95
import re
import time

def extract_number_from_filename(filename):
    numbers  = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else -1

def runApproximation():
    instancesDir = "../lib"
    tspAlgorithms = {1: "tatt", 2: "ctfds"}
    timeLimit = 1800  # limit in seconds
    logFilename = "results_approx.txt"

    # Log file header
    with open(logFilename, "w") as file:
        file.write("Instancia,Algoritmo,Resultado,Tempo,Memoria,Qualidade\n")

    # Dictionary to store the dimension of the largest instance in which each algorithm failed
    # If the algorithm fails in a smaller instance, it will not be executed in larger instances
    failureDimension = {alg: float('inf') for alg in tspAlgorithms.values()}

    for filename in sorted(os.listdir(instancesDir), key=extract_number_from_filename):
        if filename.endswith(".tsp"):
            problemPath = os.path.join(instancesDir, filename)
            
            try:
                problem = tsplib95.load(problemPath)
                probDimension = problem.dimension

            except Exception as e:
                print(f"Error loading TSP problem from {filename}: {e}")
                continue

            for algId, algName in tspAlgorithms.items():
                if probDimension < failureDimension[algName]: # Check if the algorithm has already failed in a smaller instance
                    command = ["python", "approx.py", problemPath, str(algId)]
                    print(f"Starting execution of {algName} for instance {filename}")
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    try:
                        stdout, stderr = process.communicate(timeout=timeLimit)
                        result = stdout.decode('utf-8', 'ignore').strip() # get the result of the algorithm execution

                        if process.returncode == 0 and result:
                            print(f"Result for {algName}: {result}")
                        else:
                            print(f"Error or timeout for {algName} in {filename}")
                            if probDimension < failureDimension[algName]:
                                failureDimension[algName] = probDimension

                    except subprocess.TimeoutExpired:
                        process.kill()
                        stdout, stderr = process.communicate()
                        result = "Timeout"
                        print(f"Timeout for {algName} in {filename}")
                        if probDimension < failureDimension[algName]:
                            failureDimension[algName] = probDimension

                    with open(logFilename, "a") as file:
                        file.write(f"{filename}, {algName}, {result}\n")

                else:
                    print(f"{algName} will not be executed for instance {filename} due to exceeding time limit on a smaller instance.")

if __name__ == "__main__":
    start = time.time()

    runApproximation()

    end = time.time()
    executionTime = end - start

    print("Total testing execution time:", executionTime)