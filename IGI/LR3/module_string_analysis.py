"""
Module for string analysis
Laboratory Work No. 3, Task 3 - Variant 24
Developer: Pavel Finsky
Date: 2026-03-21
"""

from typing import Dict, Tuple, Any
from functools import wraps


def validate_string(func):
    """Decorator for string validation"""
    @wraps(func)
    def wrapper(s: str, *args, **kwargs) -> Any:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")
        return func(s, *args, **kwargs)
    return wrapper


@validate_string
def count_whitespace_and_apostrophes(text: str) -> Tuple[int, int]:
    """
    Count whitespace characters and apostrophes in a string
    
    Args:
        text: input string
        
    Returns:
        Tuple containing (whitespace_count, apostrophe_count)
    """
    whitespace_count = 0
    apostrophe_count = 0
    
    for char in text:
        if char.isspace():
            whitespace_count += 1
        elif char == "'" or char == '"':
            apostrophe_count += 1
    
    return whitespace_count, apostrophe_count


def task3_main() -> None:
    """
    Main function for Task 3 - Count whitespace characters and apostrophes
    """
    print("\n" + "=" * 60)
    print("TASK 3: String Analysis")
    print("Count whitespace characters and apostrophes")
    print("=" * 60)
    
    while True:
        try:
            text = input("\nEnter a string: ")
            
            if not text:
                print("Input cannot be empty")
                continue
            
            whitespace_count, apostrophe_count = count_whitespace_and_apostrophes(text)
            
            print("\n" + "-" * 40)
            print("Analysis Results:")
            print(f"Original string: \"{text}\"")
            print(f"Length: {len(text)} characters")
            print(f"Whitespace characters: {whitespace_count}")
            print(f"Apostrophe/quotation marks: {apostrophe_count}")
            print(f"Other characters: {len(text) - whitespace_count - apostrophe_count}")
            print("-" * 40)
            
        except Exception as e:
            print(f"Unexpected Error: {e}")
        
        while True:
            repeat = input("\nDo you want to analyze another string? (y/n): ").strip().lower()
            if repeat in ['y', 'yes']:
                break
            elif repeat in ['n', 'no']:
                return
            else:
                print("Please enter 'y' or 'n'")