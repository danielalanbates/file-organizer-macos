# make an app that sorts my mac's files by size

import csv
from collections import Counter
from typing import List, Dict

def read_employees(file_path: str) -> List[Dict[str, str]]:
    \"\"\"Read employees from CSV and return a list of dicts.\"\"\"
    csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
    employees = []
    try:
        with open(file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f, dialect='empDialect')
            for row in reader:
                employees.append(dict(row))
    except FileNotFoundError:
        print(f\"File not found: {file_path}\")
    except OSError as e:
        print(f\"Error opening file {file_path}: {e}\")
    return employees

def process_data(employee_list: List[Dict[str, str]]) -> Dict[str, int]:
    \"\"\"Return a count of employees per department.\"\"\"
    departments = [e.get('Department', '').strip() for e in employee_list if e.get('Department')]
    return dict(Counter(departments))

if __name__ == '__main__':
    path = '/Users/daniel/Documents/Code/10_25/Employees.csv'
    employees = read_employees(path)
    dept_counts = process_data(employees)
    print(dept_counts)