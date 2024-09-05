import matplotlib.pyplot as plt
import numpy as np
from algorithms.classes import Tarefa, Evento, Resultado

def criar_grafico_gantt(resultado, tarefas, eventos):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    cores = plt.cm.get_cmap('Set3')(np.linspace(0, 1, len(tarefas)))

    # Gráfico de Gantt
    for i, tarefa in enumerate(tarefas):
        execucoes = [r for r in resultado if r.id == tarefa.id]
        for execucao in execucoes:
            ax1.broken_barh([(execucao.inicio, execucao.fim - execucao.inicio)], (i, 0.9), facecolors=cores[i])
            if execucao.fim - execucao.inicio > 0.5:  # Apenas exibe o texto se houver espaço suficiente
                ax1.text(execucao.inicio + (execucao.fim - execucao.inicio)/2, i + 0.5, f'T{execucao.id}', ha='center', va='center')

    ax1.set_ylim(0, len(tarefas))
    ax1.set_yticks(range(len(tarefas)))
    ax1.set_yticklabels([f'T{t.id} (C={t.custo},P={t.periodo})' for t in tarefas])
    ax1.set_title('Escalonamento Rate Monotonic - Gráfico de Gantt')
    ax1.grid(True)

    # Gráfico de Eventos com tempos exatos
    eventos_por_tarefa = {tarefa.id: [] for tarefa in tarefas}
    for evento in eventos:
        eventos_por_tarefa[evento.tarefa_id].append(evento)

    for i, (tarefa_id, eventos_tarefa) in enumerate(eventos_por_tarefa.items()):
        for evento in eventos_tarefa:
            if evento.tipo == 'release':
                marker = 'v'
                color = 'g'
            elif evento.tipo == 'start':
                marker = '^'
                color = 'b'
            elif evento.tipo == 'finish':
                marker = 'o'
                color = 'r'
            elif evento.tipo == 'preempt':
                marker = 'X'
                color = 'm'
            ax2.scatter(evento.tempo, i, marker=marker, color=color, s=50)
            
            # Adiciona o tempo exato do evento
            ax2.annotate(f'{evento.tempo}', (evento.tempo, i), 
                         xytext=(0, 10), textcoords='offset points',
                         ha='center', va='bottom', fontsize=8, rotation=45)

    ax2.set_ylim(-0.5, len(tarefas) - 0.5)
    ax2.set_yticks(range(len(tarefas)))
    ax2.set_yticklabels([f'T{t.id}' for t in tarefas])
    ax2.set_xlabel('Tempo')
    ax2.set_title('Eventos de Escalonamento com Tempos Exatos')
    ax2.grid(True)

    # Legenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='v', color='w', label='Release', markerfacecolor='g', markersize=10),
        Line2D([0], [0], marker='^', color='w', label='Início', markerfacecolor='b', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Fim', markerfacecolor='r', markersize=10),
        Line2D([0], [0], marker='X', color='w', label='Preempção', markerfacecolor='m', markersize=10)
    ]
    ax2.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)

    plt.tight_layout()
    plt.show()
