def rate_monotonic(tasks):
    tasks.sort(key=lambda x: x['Periodo'])
    for task in tasks:
         print(f"Task {task['Task']} Custo {task['Custo']} Periodo {task['Periodo']}")
