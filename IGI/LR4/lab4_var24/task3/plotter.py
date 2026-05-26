"""
Laboratory Work No. 4
Task 3: Plotting series approximation
Variant 24
Version: 1.0
Developer: Pavel Finsky
Date: 30.04.2026
"""

import matplotlib.pyplot as plt


def plot_series_vs_math(series_instance, filename="series_plot.png"):
    """Plot series approximation and exact math function."""

    results = series_instance.compute_series()

    x_value = series_instance.x

    n_values = [0] + [r["n"] for r in results]
    sum_values = [0] + [r["partial_sum"] for r in results]

    math_value = series_instance.math_value()
    math_values = [math_value] * len(n_values)

    plt.figure(figsize=(10, 6))

    # Series graph
    plt.plot(
        n_values,
        sum_values,
        marker='o',
        label='Series F(x)'
    )

    # Exact math function
    plt.plot(
        n_values,
        math_values,
        linestyle='--',
        label='math.log(1-x)'
    )

    plt.xlabel('Number of terms (n)')
    plt.ylabel('Function value')

    plt.title(
        f'Series approximation of ln(1-x), x = {x_value}'
    )

    plt.grid(True)
    plt.legend()

    # Annotation (required by assignment)
    plt.annotate(
        f'Exact value = {math_value:.5f}',
        xy=(n_values[-1], math_value),
        xytext=(n_values[-1] - 2, math_value + 0.2),
        arrowprops=dict(arrowstyle='->')
    )

    plt.savefig(filename)
    plt.close()

    print(f'Graph saved to {filename}')