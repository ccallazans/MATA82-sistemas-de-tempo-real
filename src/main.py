import os
import argparse
from reader import read_csv
from algorithms.rate_monotonic import rate_monotonic
from algorithms.edf import edf
from gantt import criar_grafico_gantt

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
        output_file_name = os.path.splitext(args.file)[0] + "-saida.csv"
        output_file_path = os.path.join(os.path.dirname(__file__), '../data/saida/', output_file_name)
        resultado, tarefas, eventos = rate_monotonic(tasks, output_file_path)
        # print(resultado)
        # print(tarefas)
        # print(eventos)
        criar_grafico_gantt(resultado, tarefas, eventos)
    if algorithm == 'edf':
        output_file_name = os.path.splitext(args.file)[0] + "-saida.csv"
        output_file_path = os.path.join(os.path.dirname(__file__), '../data/saida/', output_file_name)
        # resultado, tarefas, eventos = edf(tasks, output_file_path)
        # print(resultado)
        # print(tarefas)
        # print(eventos)
        # criar_grafico_gantt(resultado, tarefas, eventos)
        edf(tasks, output_file_path)

if __name__ == "__main__":
    main()