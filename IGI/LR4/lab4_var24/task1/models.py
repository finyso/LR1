"""
Lab 4, Task 1, Variant 24
This module defines data models for students using classes, inheritance, and mixins.
Developer: Finsky Pavel
Date: 30.04.2026
Version: 1.0
"""
from dataclasses import dataclass
from typing import Optional

class ComparableMixin:
    """Mixin to provide comparison capabilities based on a dynamic attribute."""
    def __lt__(self, other):
        return self.get_comparable_key() < other.get_comparable_key()

    def __le__(self, other):
        return self.get_comparable_key() <= other.get_comparable_key()

    def __gt__(self, other):
        return self.get_comparable_key() > other.get_comparable_key()

class BasePerson:
    """Base class for a person with a surname."""
    _total_persons = 0 # Static attribute

    def __init__(self, surname: str):
        self._surname = surname
        BasePerson._total_persons += 1

    @property
    def surname(self):
        """Getter for surname."""
        return self._surname

    @surname.setter
    def surname(self, value: str):
        """Setter for surname with basic validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Surname cannot be empty.")
        self._surname = value

    @staticmethod
    def get_total_persons():
        """Static method to get the total number of persons created."""
        return BasePerson._total_persons

class Student(BasePerson, ComparableMixin):
    """Class representing a university applicant/student."""
    def __init__(self, surname: str, needs_dormitory: bool, work_experience: int,
                 education: str, language: str):
        super().__init__(surname)
        self._needs_dormitory = needs_dormitory
        self._work_experience = work_experience
        self._education = education
        self._language = language

    # Properties using property decorator
    @property
    def needs_dormitory(self):
        return self._needs_dormitory

    @property
    def work_experience(self):
        return self._work_experience

    @property
    def education(self):
        return self._education

    @property
    def language(self):
        return self._language

    # Magic methods for polymorphism
    def __str__(self):
        return f"Student: {self.surname}, Dormitory: {self.needs_dormitory}, Experience: {self.work_experience}y, Education: {self.education}, Language: {self.language}"

    def __repr__(self):
        return f"Student('{self.surname}', {self.needs_dormitory}, {self.work_experience}, '{self.education}', '{self.language}')"

    def get_comparable_key(self):
        """Returns the key used for comparison, required by ComparableMixin."""
        return self.surname