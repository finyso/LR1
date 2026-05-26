"""
Module for series expansion calculations
Laboratory Work No. 3, Task 1 - Variant 24
Developer: Pavel Finsky
Date: 2026-03-21
"""

import math
from typing import Tuple, Callable, Optional, Any
from functools import wraps
import sys


def validate_input(func: Callable) -> Callable:
    """Decorator for input validation"""
    @wraps(func)
    def wrapper(x: float, eps: float, *args, **kwargs) -> Any:
        if eps <= 0 or eps > 1:
            raise ValueError("Accuracy eps must be in (0, 1]")
        if not isinstance(x, (int, float)):
            raise TypeError("Argument x must be a number")
        return func(x, eps, *args, **kwargs)
    return wrapper


@validate_input
def ln_series(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int]:
    """
    Calculate ln((x+1)/(x-1)) using series expansion:
    ln((x+1)/(x-1)) = 2 * sum(1/((2n+1)*x^(2n+1))) for n=0 to infinity, |x| > 1
    
    Args:
        x: argument (must satisfy |x| > 1)
        eps: required accuracy
        max_iter: maximum number of iterations (default 500)
        
    Returns:
        Tuple containing (series_sum, number_of_terms)
        
    Raises:
        ValueError: if |x| <= 1 or eps is invalid
        RuntimeError: if series does not converge within max_iter
    """
    if abs(x) <= 1:
        raise ValueError("For ln((x+1)/(x-1)) series, |x| must be > 1")
    if eps <= 0:
        raise ValueError("Accuracy eps must be positive")
    
    series_sum = 0.0
    term = 0.0
    n = 0
    
    while n < max_iter:
        term = 1.0 / ((2 * n + 1) * (x ** (2 * n + 1)))
        series_sum += term
        if n > 0 and abs(term) < eps:
            break
        n += 1
    
    if n == max_iter and abs(term) >= eps:
        raise RuntimeError(f"Series did not converge within {max_iter} iterations")
    
    return 2 * series_sum, n + 1


def calculate_math_value(x: float) -> float:
    """Calculate the exact value using math module"""
    return math.log((x + 1) / (x - 1))


def print_result_table(x: float, eps: float, series_value: float, 
                       math_value: float, n: int) -> None:
    """
    Print results in table format
    
    Args:
        x: argument value
        eps: required accuracy
        series_value: value calculated by series
        math_value: value calculated by math module
        n: number of summed terms
    """
    print("\n" + "=" * 80)
    print("TASK 1: Series Expansion Calculation")
    print("Function: ln((x+1)/(x-1)) = 2 * sum(1/((2n+1)*x^(2n+1)))")
    print("=" * 80)
    print(f"{'x':>10} | {'F(x) (series)':>15} | {'Math F(x)':>15} | {'eps':>12} | {'n':>8}")
    print("-" * 80)
    print(f"{x:>10.6f} | {series_value:>15.10f} | {math_value:>15.10f} | {eps:>12.2e} | {n:>8d}")
    print("=" * 80)


def task1_main() -> None:
    """
    Main function for Task 1 with user interaction
    """
    print("\n" + "=" * 60)
    print("TASK 1: Series Expansion")
    print("Function: ln((x+1)/(x-1))")
    print("Condition: |x| > 1")
    print("=" * 60)
    
    while True:
        try:
            x_input = input("\nEnter argument x (|x| > 1): ").strip()
            if not x_input:
                print("Input cannot be empty")
                continue
                
            x = float(x_input)
            
            if abs(x) <= 1:
                print("Error: |x| must be greater than 1")
                continue
            
            eps_input = input("Enter accuracy eps (0 < eps <= 1): ").strip()
            if not eps_input:
                print("Input cannot be empty")
                continue
                
            eps = float(eps_input)
            
            if eps <= 0 or eps > 1:
                print("Error: eps must be in (0, 1]")
                continue
            
            series_value, n = ln_series(x, eps)
            math_value = calculate_math_value(x)
            print_result_table(x, eps, series_value, math_value, n)
            
        except ValueError as e:
            print(f"Value Error: {e}")
        except RuntimeError as e:
            print(f"Runtime Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        
        while True:
            repeat = input("\nDo you want to calculate again? (y/n): ").strip().lower()
            if repeat in ['y', 'yes']:
                break
            elif repeat in ['n', 'no']:
                return
            else:
                print("Please enter 'y' or 'n'")