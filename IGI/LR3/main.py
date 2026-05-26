"""
Main module for Laboratory Work No. 3
Version: 1.0
Developer: Pavel Finsky
Date: 2026-03-21
This module serves as the entry point for testing all functions
from the developed modules.
"""

import sys
from typing import Callable, Dict
import module_series
import module_sequence
import module_string_analysis
import module_text_analysis
import module_list_processing


def display_menu() -> None:
    """Display main menu"""
    print("\n" + "=" * 60)
    print("LABORATORY WORK No. 3 - VARIANT 24")
    print("=" * 60)
    print("1. Task 1 - Series Expansion: ln((x+1)/(x-1))")
    print("2. Task 2 - Sequence: Count numbers in range [5, 25]")
    print("3. Task 3 - String: Count whitespace and apostrophes")
    print("4. Task 4 - Text: Analyze text (words < 7, words ending with 'a', sort by length)")
    print("5. Task 5 - List: Min positive element and sum between first/last positive")
    print("0. Exit")
    print("=" * 60)


def main() -> None:
    """Main function to run the program"""
    
    # Dictionary mapping menu options to functions
    tasks: Dict[str, Callable] = {
        '1': module_series.task1_main,
        '2': module_sequence.SequenceProcessor().task2_main,
        '3': module_string_analysis.task3_main,
        '4': module_text_analysis.TextAnalyzer().task4_main,
        '5': module_list_processing.task5_main,
    }
    
    print("\n" + "=" * 70)
    print("LABORATORY WORK No. 3")
    print("Developer: Pavel Finsky")
    print("Version: 1.0")
    print("Date: 2026-03-21")
    print("=" * 70)
    
    while True:
        try:
            display_menu()
            choice = input("\nSelect task (0-5): ").strip()
            
            if choice == '0':
                print("\nThank you for using the program. Goodbye!")
                sys.exit(0)
            
            if choice in tasks:
                tasks[choice]()
            else:
                print("Invalid choice. Please select 0-5.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error in main: {e}")
            
            while True:
                cont = input("Continue using program? (y/n): ").strip().lower()
                if cont in ['y', 'yes']:
                    break
                elif cont in ['n', 'no']:
                    sys.exit(0)
                else:
                    print("Please enter 'y' or 'n'")


if __name__ == "__main__":
    main()