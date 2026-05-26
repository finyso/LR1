"""
Lab 4, Task 4, Variant 24
Rendering functions for drawing isosceles trapezoid using matplotlib.
Developer: Finsky Pavel
Date: 01.05.2026
Version: 1.0
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_trapezoid(trapezoid_instance, text="", filename="figure.png"):
    """
    Draws the isosceles trapezoid and saves to file.

    The trapezoid is drawn with:
    - Bottom base a horizontally centered
    - Top base c centered above
    - Height h
    - Filled with specified color
    - Labeled with user text
    """
    a = trapezoid_instance.base_a      # Bottom base
    c = trapezoid_instance.base_c      # Top base
    h = trapezoid_instance.height      # Height
    color = trapezoid_instance.color   # Color

    # Calculate vertex coordinates
    # Bottom base centered at y=0
    x_bottom_left = -a / 2
    x_bottom_right = a / 2
    y_bottom = 0

    # Top base centered at y=h
    x_top_left = -c / 2
    x_top_right = c / 2
    y_top = h

    # Trapezoid vertices (counterclockwise starting from bottom-left)
    vertices = [
        (x_bottom_left, y_bottom),
        (x_bottom_right, y_bottom),
        (x_top_right, y_top),
        (x_top_left, y_top)
    ]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the trapezoid as a filled polygon
    trapezoid_patch = patches.Polygon(
        vertices,
        closed=True,
        fill=True,
        facecolor=color,
        edgecolor='black',
        linewidth=2,
        alpha=0.7,
        label=trapezoid_instance.FIGURE_NAME
    )
    ax.add_patch(trapezoid_patch)

    # Add dimension labels
    # Base a dimension
    ax.annotate(
        f'a = {a:.2f}',
        xy=(0, y_bottom),
        xytext=(0, y_bottom - h * 0.15),
        ha='center', va='top',
        fontsize=10
    )

    # Base c dimension
    ax.annotate(
        f'c = {c:.2f}',
        xy=(0, y_top),
        xytext=(0, y_top + h * 0.05),
        ha='center', va='bottom',
        fontsize=10
    )

    # Side b dimension (left side)
    mid_left_x = (x_bottom_left + x_top_left) / 2
    mid_left_y = (y_bottom + y_top) / 2
    ax.annotate(
        f'b = {trapezoid_instance.side_b:.2f}',
        xy=(mid_left_x, mid_left_y),
        xytext=(mid_left_x - a * 0.15, mid_left_y),
        ha='right', va='center',
        fontsize=10,
        arrowprops=dict(arrowstyle='->', color='black')
    )

    # Height dimension
    ax.annotate(
        f'h = {h:.2f}',
        xy=(x_bottom_right + a * 0.05, y_bottom),
        xytext=(x_bottom_right + a * 0.1, h / 2),
        ha='left', va='center',
        fontsize=10,
    )

    # Angle Y label
    ax.annotate(
        f'Y = {trapezoid_instance.angle_y:.2f}°',
        xy=(x_bottom_left + trapezoid_instance.projection * 0.3, y_bottom + h * 0.1),
        ha='left', va='bottom',
        fontsize=10,
        color='black'
    )

    # User text in the center of the trapezoid
    if text:
        ax.text(
            0, h / 2, text,
            ha='center', va='center',
            fontsize=14,
            fontweight='bold',
            color='white' if color not in ['white', 'yellow', 'cyan', 'lime'] else 'black',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.3)
        )

    # Set axes limits and aspect ratio
    margin = max(a, c, h) * 0.3
    ax.set_xlim(-a / 2 - margin, a / 2 + margin)
    ax.set_ylim(-margin, h + margin)
    ax.set_aspect('equal', 'box')

    # Add grid and title
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(
        "Trapezoid\n",
        fontsize=12
    )
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Add legend
    ax.legend(loc='upper right')

    # Save and show
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()
    plt.close()
    print(f"Figure saved to {filename}")