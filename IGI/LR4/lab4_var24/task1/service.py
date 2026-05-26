"""
Lab 4, Task 1, Variant 24
Service module for file operations (CSV and Pickle) and data analysis.
Developer: Finsky Pavel
Date: 30.04.2026
Version: 1.0
"""
import csv
import pickle
import os
from typing import List
from .models import Student

# Initial data
INITIAL_DATA = [
    Student("Ivanov", True, 0, "school", "English"),
    Student("Petrov", False, 3, "technicum", "German"),
    Student("Sidorova", True, 1, "school", "French"),
    Student("Smirnov", False, 5, "technicum", "English"),
    Student("Kuznetsova", True, 2, "school", "English"),
    Student("Popov", False, 4, "school", "German"),
]

CSV_FILE = "students.csv"
PICKLE_FILE = "students.pkl"

def save_to_csv(students: List[Student], filename: str = CSV_FILE):
    """Saves list of Student objects to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["surname", "needs_dormitory", "work_experience", "education", "language"])
        for s in students:
            writer.writerow([s.surname, s.needs_dormitory, s.work_experience, s.education, s.language])
    print(f"Данные сохранены в {filename}")

def load_from_csv(filename: str = CSV_FILE) -> List[Student]:
    """Loads Student objects from a CSV file."""
    students = []
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(Student(
                surname=row['surname'],
                needs_dormitory=row['needs_dormitory'] == 'True',
                work_experience=int(row['work_experience']),
                education=row['education'],
                language=row['language']
            ))
    return students

def save_to_pickle(students: List[Student], filename: str = PICKLE_FILE):
    """Serializes the list of Student objects to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(students, f)
    print(f"Данные сохранены в {filename}")

def load_from_pickle(filename: str = PICKLE_FILE) -> List[Student]:
    """Deserializes Student objects from a pickle file."""
    students = []
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return []
    with open(filename, 'rb') as f:
        students = pickle.load(f)
    return students

def analyze_data(students: List[Student]):
    """Performs analysis according to variant 24."""
    # a) How many need a dormitory
    dorm_needed = sum(1 for s in students if s.needs_dormitory)
    print(f"a) Количество нуждающихся в общежитии: {dorm_needed}")

    # b) List of students with > 2 years work experience
    exp_students = [s for s in students if s.work_experience > 2]
    print(f"b) Студенты со стажем более 2 лет: {', '.join(s.surname for s in exp_students) if exp_students else 'Нет'}")

    # c) List of students who finished technical school
    technicum_students = [s for s in students if s.education.lower() == 'technicum']
    print(f"c) Окончившие техникум: {', '.join(s.surname for s in technicum_students) if technicum_students else 'Нет'}")

    # d) Language groups
    language_groups = {}
    for s in students:
        lang = s.language
        if lang not in language_groups:
            language_groups[lang] = []
        language_groups[lang].append(s.surname)
    print("d) Языковые группы:")
    for lang, surnames in language_groups.items():
        print(f"   {lang}: {', '.join(surnames)}")

def find_student_by_surname(students: List[Student], surname: str):
    """Finds and prints a student by surname."""
    for s in students:
        if s.surname.lower() == surname.lower():
            print(s)
            return
    print(f"Студент с фамилией '{surname}' не найден.")