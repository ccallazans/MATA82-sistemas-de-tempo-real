import csv

def read_csv(file_path):
    tasks = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task = {
                'Task': int(row['Task']),
                'Custo': int(row['Custo']),
                'Periodo': int(row['Periodo'])
            }
            tasks.append(task)
    return tasks
