import csv

def read_csv(file_path):
    tasks = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for index, row in enumerate(csv_reader, start=1):
            task = {
                'Task': f'T{index}',
                'Custo': int(row['Custo']),
                'Periodo': int(row['Periodo'])
            }
            tasks.append(task)
    return tasks
