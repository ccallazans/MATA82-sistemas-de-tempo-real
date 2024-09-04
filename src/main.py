import os
import argparse
from reader import read_csv
from algorithms.rate_monotonic import rate_monotonic

def main():
    parser = argparse.ArgumentParser(description="Escolha o algoritmo de escalonamento e forneça o arquivo CSV de entrada.")
    parser.add_argument("file", type=str, help="Caminho para o arquivo CSV de entrada")
    parser.add_argument("algorithm", type=str, choices=['rm', 'edf'], help="Algoritmo de escalonamento: 'rm' para Rate Monotonic, 'edf' para Earliest Deadline First")
    
    args = parser.parse_args()
    
    file_path = os.path.join(os.path.dirname(__file__), '../data/entrada/', args.file)
    algorithm = args.algorithm
    
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado.")
        return
    
    tasks = read_csv(file_path)
    

    if algorithm == 'rm':
        print("Rate monotonic")
        rate_monotonic(tasks)

if __name__ == "__main__":
    main()