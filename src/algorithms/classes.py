class Tarefa:
    def __init__(self, id, custo, periodo):
        self.id = id
        self.custo = custo
        self.periodo = periodo
        self.prioridade = periodo  # No RMS, quanto menor o período, maior a prioridade

    def __repr__(self):
        return f"Tarefa(id={self.id}, custo={self.custo}, periodo={self.periodo}, prioridade={self.prioridade})"

class Evento:
    def __init__(self, tempo, tipo, tarefa_id):
        self.tempo = tempo
        self.tipo = tipo  # 'release', 'start', 'finish', 'preempt'
        self.tarefa_id = tarefa_id

    def __repr__(self):
        return f"Evento(tempo={self.tempo}, tipo={self.tipo}, tarefa_id={self.tarefa_id})"

class Resultado:
    def __init__(self, id, inicio, fim):
        self.id = id
        self.inicio = inicio 
        self.fim = fim

    def __repr__(self):
        return f"Resultado(id={self.id}, inicio={self.inicio}, fim={self.fim})"