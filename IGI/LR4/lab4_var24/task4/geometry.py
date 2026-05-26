"""
Laboratory Work No. 4
Task 4: Geometric figures and inheritance
Variant 24
Version: 1.0
Developer: Pavel Finsky
Date: 01.05.2026
"""

from abc import ABC, abstractmethod
import math


class FigureColor:
    """Mixin class for figure color."""

    def __init__(self, color="black", *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(color, str) or not color.strip():
            color = "blue"

        self._color = color

    @property
    def color(self):
        """Get figure color."""
        return self._color

    @color.setter
    def color(self, value):
        """Set figure color."""

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "Color must be a non-empty string."
            )

        self._color = value


class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""

    _figure_count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GeometricFigure._figure_count += 1

    @abstractmethod
    def area(self):
        """Calculate figure area."""
        pass

    @classmethod
    def get_figure_name(cls):
        """Return class name."""
        return cls.__name__

    @staticmethod
    def get_total_figures():
        """Return total number of figures."""
        return GeometricFigure._figure_count


class IsoscelesTrapezoid(FigureColor, GeometricFigure):
    """Class representing an isosceles trapezoid."""

    FIGURE_NAME = "IsoscelesTrapezoid"

    def __init__(
        self,
        base_a: float,
        side_b: float,
        angle_y: float,
        color: str = "blue"
    ):

        # Validation
        if base_a <= 0:
            raise ValueError(
                "Base a must be positive."
            )

        if side_b <= 0:
            raise ValueError(
                "Side b must be positive."
            )

        if angle_y <= 0 or angle_y >= 90:
            raise ValueError(
                "Angle Y must be between 0 and 90 degrees."
            )

        # Correct super() usage
        super().__init__(color=color)

        self._base_a = base_a
        self._side_b = side_b
        self._angle_y = angle_y

        # Convert angle to radians
        angle_rad = math.radians(angle_y)

        # Geometry calculations
        self._height = (
            side_b * math.sin(angle_rad)
        )

        self._projection = (
            side_b * math.cos(angle_rad)
        )

        # Check trapezoid existence
        if base_a <= 2 * self._projection:
            raise ValueError(
                "Impossible trapezoid: "
                "lower base is too small."
            )

        self._base_c = (
            base_a - 2 * self._projection
        )

    @property
    def base_a(self):
        """Get lower base."""
        return self._base_a

    @property
    def side_b(self):
        """Get side length."""
        return self._side_b

    @property
    def angle_y(self):
        """Get angle."""
        return self._angle_y

    @property
    def height(self):
        """Get trapezoid height."""
        return self._height

    @property
    def projection(self):
        """Get side projection."""
        return self._projection

    @property
    def base_c(self):
        """Get upper base."""
        return self._base_c

    def area(self):
        """Calculate trapezoid area."""

        return (
            (self._base_a + self._base_c)
            * self._height
            / 2
        )

    def perimeter(self):
        """Calculate trapezoid perimeter."""

        return (
            self._base_a
            + self._base_c
            + 2 * self._side_b
        )

    def info(self):
        """Return formatted figure information."""

        return (
            "Figure: {}\n"
            "Color: {}\n"
            "Base a: {:.2f}\n"
            "Base c: {:.2f}\n"
            "Side b: {:.2f}\n"
            "Angle Y: {:.2f}\n"
            "Height: {:.2f}\n"
            "Projection: {:.2f}\n"
            "Area: {:.2f}\n"
            "Perimeter: {:.2f}"
        ).format(
            self.FIGURE_NAME,
            self.color,
            self._base_a,
            self._base_c,
            self._side_b,
            self._angle_y,
            self._height,
            self._projection,
            self.area(),
            self.perimeter()
        )

    def __str__(self):
        """String representation."""
        return self.info()

    def __repr__(self):
        """Official representation."""

        return (
            f"IsoscelesTrapezoid("
            f"base_a={self._base_a}, "
            f"side_b={self._side_b}, "
            f"angle_y={self._angle_y}, "
            f"color='{self.color}')"
        )

    def __eq__(self, other):
        """Compare figures by area."""

        if isinstance(other, IsoscelesTrapezoid):
            return abs(
                self.area() - other.area()
            ) < 1e-6

        return False

    def __lt__(self, other):
        """Compare figures by area."""

        if isinstance(other, GeometricFigure):
            return self.area() < other.area()

        return NotImplemented