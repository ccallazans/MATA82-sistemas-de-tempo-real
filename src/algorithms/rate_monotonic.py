import csv
import os
from functools import reduce
from math import gcd
from .classes import Tarefa, Evento, Resultado

def rate_monotonic(tasks, output_file_path):
    # Ordenar as tarefas pelo período (menor período primeiro)
    tasks = sorted(tasks, key=lambda x: x['Periodo'])

    tarefas = []
    for index, task in enumerate(tasks):
        tarefa = Tarefa(id=int(task['Task'][1]), custo=task['Custo'], periodo=task['Periodo'])
        tarefa.prioridade = index
        tarefas.append(tarefa)
    
    # Encontrar o maior período para definir o tempo total de simulação
    hyper_period = reduce(lambda x, y: lcm(x, y), [task['Periodo'] for task in tasks])
    
    # Inicializar o estado das tarefas
    task_state = {task['Task']: {'Custo': task['Custo'], 'Periodo': task['Periodo'], 'Execution': 0, 'Deadline': task['Periodo']} for task in tasks}
    
    # Lista para armazenar os resultados
    results = []
    header = ['Tempo'] + sorted([task['Task'] for task in tasks], key=lambda x: int(x[1:]))
    results.append(header)

    deadline_error = []
    # Simulação do tempo
    for time in range(hyper_period):
        # Escolher a tarefa a ser executada com base no Rate Monotonic
        task_to_run = None
        for task in tasks:
            if task_state[task['Task']]['Execution'] < task_state[task['Task']]['Custo'] and time >= task_state[task['Task']]['Deadline'] - task_state[task['Task']]['Periodo']:
                task_to_run = task
                break
        
        # Executar a tarefa escolhida
        executing_task = task_to_run['Task'] if task_to_run else None
        if executing_task:
            task_state[executing_task]['Execution'] += 1
        
        # Registrar o estado atual das tarefas
        current_state = [time]
        for task in sorted(tasks, key=lambda x: int(x['Task'][1:])):
            if task['Task'] == executing_task:
                current_state.append('X')
            else:
                current_state.append('')
        
        results.append(current_state)
        
        # Atualizar o estado das tarefas após execução
        for task in tasks:
            if time + 1 == task_state[task['Task']]['Deadline']:
                if task_state[task['Task']]['Execution'] < task_state[task['Task']]['Custo'] and task_state[task['Task']]['Execution'] > 0:
                    deadline_error.append({task['Task']: time})
                    print(f"Task {task['Task']} falhou o seu deadline em {time}")
                task_state[task['Task']]['Execution'] = 0
                task_state[task['Task']]['Deadline'] += task_state[task['Task']]['Periodo']
    
    # Escrever os resultados no arquivo de saída
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)


    resultados = coletar_resultados(output_file_path)
    eventos = coletar_eventos(output_file_path)
    os.remove(output_file_path)
    return resultados, tarefas, eventos


def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def coletar_eventos(file_path):
    eventos = []
    start_flags = {} 
    finish_flags = {}

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        for header in headers[1:]:
            start_flags[header] = False
            finish_flags[header] = None
        
        for row in csv_reader:
            tempo = int(row[0])
            for idx, cell in enumerate(row[1:], start=1):
                tarefa_id = idx
                header = headers[idx]

                if tempo == 0:
                    eventos.append(Evento(tempo, 'release', tarefa_id))

                if cell == 'X':
                    if not start_flags[header]:
                        eventos.append(Evento(tempo, 'start', tarefa_id))
                        start_flags[header] = True
                    finish_flags[header] = tempo

    for header, last_finish in finish_flags.items():
        if last_finish is not None:
            tarefa_id = int(header[1:]) 
            eventos.append(Evento(last_finish+1, 'finish', tarefa_id))
    
    return eventos

def coletar_resultados(file_path):
    resultados = []
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        
        column_data = {int(col[1:]): [] for col in header[1:]}
        
        for row in csv_reader:
            for i, col in enumerate(header[1:], start=1):
                column_data[int(col[1:])].append((int(row[0]), row[i]))
        
        for col, data in column_data.items():
            id = col
            inicio, fim = None, None
            in_sequence = False
            
            for tempo, val in data:
                if val == 'X' and not in_sequence:
                    inicio = tempo
                    in_sequence = True
                elif val != 'X' and in_sequence:
                    fim = tempo
                    resultados.append(Resultado(id, inicio, fim))
                    in_sequence = False
            
            if in_sequence:
                fim = data[-1][0]
                resultados.append(Resultado(id, inicio, fim))
    
    return resultados