import csv
import os
from functools import reduce
from math import gcd
import pandas as pd
import numpy as np
import plotly.express as px
import json
from datetime import timedelta
from .classes import Tarefa, Evento, Resultado

def edf(tarefas, output_file_path):
  # print(tarefas)
  # print('aciona edf')

  # Cria uma matriz, com orientação baseada no índice
  tasks = pd.DataFrame(tarefas)
  tasks['deadline'] = tasks['Periodo']
  tasks['current_capacity'] = tasks['Custo']
  tasks['current_deadline'] = tasks['deadline']

  # Lista para armazenar os resultados
  results = []

  for i in range(np.lcm.reduce(tasks.Periodo)):
    # Consulta "tasks" que já foram completadas
    left_tasks = tasks[tasks['current_capacity'] > 0]

    if len(left_tasks) > 0:
        # Encontra "task" com "deadline" mais próximo
        top_task = left_tasks.sort_values('current_deadline').index[0]

        # Decrementa o "capacity" da "task" atual
        tasks.loc[top_task, 'current_capacity'] -= 1

        if 0 < i and results[-1]['task'] == top_task and results[-1]['end'] == i:
          # Caso a "task" atual é mesma que a anterior, atuliza "end" e "length"
          results[-1].update(
            {
              'end': i+1,
              'length': results[-1]['length'] + 1
            }
          )
        else:
          # Caso não adicionar uma "task" na results
          results += [
            {
              'task': f"T{top_task+1}",
              'start': i,
              'end': i+1, 
              'length': 1
            }
          ]

    # Atualiza the "capacity" e o "deadline"
    arrived = tasks[(i + 1) % tasks['Periodo'] == 0].index
    tasks.loc[arrived, 'current_capacity'] = tasks.loc[arrived, 'Custo']
    tasks.loc[arrived, 'current_deadline'] = tasks.loc[arrived, 'deadline'] + i + 2

  # print(results)

  # Converte a lista de dicionários para um DataFrame
  results_df = pd.DataFrame(results)
  
  # Define a função to_date
  def to_date(days):
      start_date = pd.to_datetime("2024-01-01")
      return start_date + timedelta(days=days)

  results_df['start'] = results_df['start'].apply(to_date)
  results_df['end'] = results_df['end'].apply(to_date)

  fig = px.timeline(results_df, 
                    x_start="start",
                    x_end="end", 
                    y="task",
                    color="task")

  fig.layout.xaxis.tickformat = '%j'

  # Exibe o gráfico
  fig.show()
