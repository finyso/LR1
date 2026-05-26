"""
Module for list processing
Laboratory Work No. 3, Task 5 - Variant 24
Developer: Pavel Finsky
Date: 2026-03-21
"""

from typing import List, Tuple, Optional, Union, Any
from functools import wraps
import random


def validate_list(func):
    """Decorator for list validation"""
    @wraps(func)
    def wrapper(lst: List[float], *args, **kwargs) -> Any:
        if not isinstance(lst, list):
            raise TypeError("Input must be a list")
        if not lst:
            raise ValueError("List cannot be empty")
        return func(lst, *args, **kwargs)
    return wrapper


def input_list_manually() -> List[float]:
    """
    Get list elements from user input
    
    Returns:
        list of floats entered by user
    """
    result = []
    print("\nEnter list elements (one per line). Enter empty line to finish:")
    
    while True:
        try:
            value = input(f"Element {len(result) + 1}: ").strip()
            if not value:
                break
            result.append(float(value))
        except ValueError:
            print("Error: Please enter a valid number")
            continue
    
    return result


def generate_random_list(size: int, min_val: float = -100, max_val: float = 100) -> List[float]:
    """
    Generate a list of random floats
    
    Args:
        size: number of elements
        min_val: minimum value
        max_val: maximum value
        
    Returns:
        list of random floats
    """
    return [random.uniform(min_val, max_val) for _ in range(size)]


@validate_list
def find_min_positive_element(lst: List[float]) -> Optional[float]:
    """
    Find the minimum positive element in the list
    
    Args:
        lst: input list
        
    Returns:
        minimum positive element, or None if no positive elements exist
    """
    positive_elements = [x for x in lst if x > 0]
    return min(positive_elements) if positive_elements else None


@validate_list
def sum_between_first_and_last_positive(lst: List[float]) -> float:
    """
    Calculate sum of elements between first and last positive elements
    
    Args:
        lst: input list
        
    Returns:
        sum of elements between first and last positive elements
    """
    positive_indices = [i for i, x in enumerate(lst) if x > 0]
    
    if len(positive_indices) < 2:
        return 0.0
    
    first_pos = positive_indices[0]
    last_pos = positive_indices[-1]
    
    if abs(last_pos - first_pos) <= 1:
        return 0.0
    
    return sum(lst[first_pos + 1:last_pos])


def print_list_info(lst: List[float], title: str = "List") -> None:
    """
    Print list information
    
    Args:
        lst: list to print
        title: title for printing
    """
    print(f"\n{title}:")
    print("-" * 60)
    
    # Print first 20 elements if list is long
    if len(lst) > 20:
        print(f"First 20 elements: {[round(x, 4) for x in lst[:20]]}")
        print(f"... and {len(lst) - 20} more elements")
    else:
        print(f"All elements: {[round(x, 4) for x in lst]}")
    
    print(f"Number of elements: {len(lst)}")
    
    min_pos = find_min_positive_element(lst)
    if min_pos is not None:
        print(f"Minimum positive element: {min_pos:.6f}")
    else:
        print("No positive elements in the list")
    
    sum_between = sum_between_first_and_last_positive(lst)
    print(f"Sum of elements between first and last positive: {sum_between:.6f}")


def task5_main() -> None:
    """
    Main function for Task 5 - Variant 24:
    Find minimum positive element and sum of elements between
    first and last positive elements
    """
    print("\n" + "=" * 60)
    print("TASK 5: List Processing")
    print("Variant 24 Conditions:")
    print("1. Find minimum positive element")
    print("2. Find sum of elements between first and last positive elements")
    print("=" * 60)
    
    while True:
        try:
            print("\nList initialization options:")
            print("1. Manual input")
            print("2. Random generation")
            print("3. Use default example")
            
            choice = input("\nSelect option (1/2/3): ").strip()
            
            if choice == '1':
                lst = input_list_manually()
                if not lst:
                    print("List cannot be empty")
                    continue
                    
            elif choice == '2':
                try:
                    size = int(input("Enter list size: "))
                    if size <= 0:
                        print("Size must be positive")
                        continue
                    min_val = float(input("Enter minimum value (default -100): ") or "-100")
                    max_val = float(input("Enter maximum value (default 100): ") or "100")
                    lst = generate_random_list(size, min_val, max_val)
                except ValueError as e:
                    print(f"Invalid input: {e}")
                    continue
                    
            elif choice == '3':
                lst = [-5.5, 2.3, -1.2, 7.8, -3.4, 4.5, -2.1, 1.2, -6.7, 3.3]
                print("Using default list: [-5.5, 2.3, -1.2, 7.8, -3.4, 4.5, -2.1, 1.2, -6.7, 3.3]")
            else:
                print("Invalid choice")
                continue
            
            # Perform analysis
            print_list_info(lst, "Analyzed List")
            
            # Additional details
            print("\nAdditional details:")
            positive_indices = [i for i, x in enumerate(lst) if x > 0]
            if positive_indices:
                print(f"First positive element at index {positive_indices[0]}: {lst[positive_indices[0]]:.6f}")
                if len(positive_indices) >= 2:
                    print(f"Last positive element at index {positive_indices[-1]}: {lst[positive_indices[-1]]:.6f}")
                    elements_between = lst[positive_indices[0] + 1:positive_indices[-1]]
                    if elements_between:
                        print(f"Elements between: {[round(x, 4) for x in elements_between]}")
                    else:
                        print("No elements between first and last positive elements")
            else:
                print("No positive elements found in the list")
                
        except Exception as e:
            print(f"Unexpected Error: {e}")
        
        while True:
            repeat = input("\nDo you want to process another list? (y/n): ").strip().lower()
            if repeat in ['y', 'yes']:
                break
            elif repeat in ['n', 'no']:
                return
            else:
                print("Please enter 'y' or 'n'")