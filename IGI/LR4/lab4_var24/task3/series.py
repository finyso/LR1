"""
Laboratory Work No. 4
Task 3: Series expansion and statistical analysis
Variant 24
Version: 1.0
Developer: Pavel Finsky
Date: 30.04.2026
"""

import math
import numpy as np
from statistics import multimode


class LnSeries:
    """
    Class for calculating the series expansion of ln(1-x).

    Formula:
    ln(1-x) = -(x + x^2/2 + x^3/3 + ...)

    Valid only for |x| < 1.
    """

    def __init__(self, x: float, n_terms: int = 10):
        """Initialize the series object."""

        if abs(x) >= 1:
            raise ValueError("|x| must be less than 1.")

        if n_terms <= 0:
            raise ValueError("Number of terms must be positive.")

        self.x = x
        self.n_terms = n_terms
        self._results = []

    @property
    def x(self):
        """Getter for x."""
        return self._x

    @x.setter
    def x(self, value):
        """Setter for x with validation."""

        if abs(value) >= 1:
            raise ValueError("|x| must be less than 1.")

        self._x = value

    def compute_series(self):
        """Calculate series values."""

        self._results = []
        partial_sum = 0.0

        for n in range(1, self.n_terms + 1):
            term = -(self.x ** n) / n
            partial_sum += term

            self._results.append({
                "n": n,
                "term": term,
                "partial_sum": partial_sum
            })

        return self._results

    def math_value(self):
        """Calculate exact value using math module."""

        return math.log(1 - self.x)

    def statistics(self):
        """Calculate statistical characteristics."""

        if not self._results:
            self.compute_series()

        terms = np.array([r["term"] for r in self._results])

        mean = np.mean(terms)
        median = np.median(terms)
        variance = np.var(terms)
        std_dev = np.std(terms)

        # Mode for floating-point values
        rounded_terms = [round(value, 6) for value in terms]
        mode_values = multimode(rounded_terms)

        return {
            "mean": mean,
            "median": median,
            "variance": variance,
            "std_dev": std_dev,
            "mode": mode_values
        }