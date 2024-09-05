class Tarefa:
    def __init__(self, id, custo, periodo):
        self.id = id
        self.custo = custo
        self.periodo = periodo
        self.prioridade = periodo  # No RMS, quanto menor o período, maior a prioridade

class Evento:
    def __init__(self, tempo, tipo, tarefa_id):
        self.tempo = tempo
        self.tipo = tipo  # 'release', 'start', 'finish', 'preempt'
        self.tarefa_id = tarefa_id