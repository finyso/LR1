"""
Module for sequence processing
Laboratory Work No. 3, Task 2 - Variant 24
Developer: Pavel Finsky
Date: 2026-03-21
"""

from typing import List, Optional, Any, Iterator
from functools import wraps


def validate_number(func):
    """Decorator for number validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Error: Please enter a valid integer")
            return None
    return wrapper


def number_generator() -> Iterator[int]:
    """
    Generator function that yields numbers from user input
    Uses yield to return values one by one
    """
    while True:
        try:
            num = int(input("Enter number: "))
            if num == 0:
                break
            yield num
        except ValueError:
            print("Error: Please enter a valid integer")


class SequenceProcessor:
    """Class for processing integer sequences"""
    
    def __init__(self):
        self.numbers: List[int] = []
        self.sequence_data: List[int] = []
    
    @validate_number
    def get_integer_input(self, prompt: str) -> Optional[int]:
        """
        Get integer input from user
        
        Args:
            prompt: message to display
            
        Returns:
            integer value or None if invalid
        """
        value = int(input(prompt))
        return value
    
    def init_from_generator(self) -> List[int]:
        """
        Initialize sequence using generator with yield
        """
        result = []
        print("\n--- Using GENERATOR (yield) for initialization ---")
        for num in number_generator():
            result.append(num)
        return result
    
    def task2_main(self) -> None:
        """
        Main function for Task 2 - Count numbers in range [5, 25]
        Condition: input numbers until 0 is entered
        """
        print("\n" + "=" * 60)
        print("TASK 2: Sequence Analysis")
        print("Count numbers in the range from 5 to 25 (inclusive)")
        print("Enter numbers one by one (enter 0 to finish)")
        print("=" * 60)
        
        while True:
            try:
                print("\nChoose initialization method:")
                print("1. Using GENERATOR (yield)")
                print("2. Using regular user input")
                
                choice = input("\nSelect method (1/2): ").strip()
                
                if choice == '1':
                    self.sequence_data = self.init_from_generator()
                else:
                    self.sequence_data = []
                    print("\nEnter numbers (0 to stop):")
                    while True:
                        num = self.get_integer_input("Number: ")
                        if num is None:
                            continue
                        if num == 0:
                            break
                        self.sequence_data.append(num)
                
                if not self.sequence_data:
                    print("No numbers entered")
                    continue
                
                count_in_range = sum(1 for num in self.sequence_data if 5 <= num <= 25)
                
                print("\n" + "-" * 40)
                print("Results:")
                print(f"Entered numbers: {self.sequence_data}")
                print(f"Count of numbers in range [5, 25]: {count_in_range}")
                print("-" * 40)
                
            except Exception as e:
                print(f"Unexpected Error: {e}")
            
            while True:
                repeat = input("\nDo you want to analyze another sequence? (y/n): ").strip().lower()
                if repeat in ['y', 'yes']:
                    break
                elif repeat in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' or 'n'")