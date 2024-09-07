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
  # Cria uma matriz, com orientação baseada no índice
  tasks = pd.DataFrame(tarefas)
  tasks['Deadline'] = tasks['Periodo']
  tasks['Custo_Atual'] = tasks['Custo']
  tasks['Deadline_Atual'] = tasks['Deadline']

  # Lista para armazenar os resultados
  results = []

  for i in range(np.lcm.reduce(tasks.Periodo)):
    left_tasks = tasks[tasks['Custo_Atual'] > 0]

    if len(left_tasks) > 0:
        # Encontra "task" com "deadline" mais próximo
        top_task = left_tasks.sort_values('Deadline_Atual').index[0]

        # Decrementa o "capacity" da "task" atual
        tasks.loc[top_task, 'Custo_Atual'] -= 1

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
    tasks.loc[arrived, 'Custo_Atual'] = tasks.loc[arrived, 'Custo']
    tasks.loc[arrived, 'Deadline_Atual'] = tasks.loc[arrived, 'Deadline'] + i + 2

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
