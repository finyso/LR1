"""
Lab 4, Task 1: Working with files, classes, serializers.
Variant 24: University applicants data processing.
"""
from .models import Student, BasePerson, ComparableMixin
from .service import (
    save_to_csv,
    load_from_csv,
    save_to_pickle,
    load_from_pickle,
    analyze_data,
    find_student_by_surname,
    INITIAL_DATA,
    CSV_FILE,
    PICKLE_FILE,
)