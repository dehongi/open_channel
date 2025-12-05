"""
Trapezoidal channel geometry.
"""

import math
from .base import Channel


class TrapezoidalChannel(Channel):
    """
    Trapezoidal open channel cross-section.

    A trapezoidal channel has sloped side walls and a flat bottom.

    Attributes:
        b: Bottom width (m or ft).
        z: Side slope (z horizontal : 1 vertical).

    Formulas:
        - Area: A = (b + z*y) * y
        - Wetted Perimeter: P = b + 2y * sqrt(1 + z²)
        - Top Width: T = b + 2zy
    """

    def __init__(self, b: float, z: float) -> None:
        """
        Initialize a trapezoidal channel.

        Args:
            b: Bottom width (m or ft). Must be positive.
            z: Side slope (z horizontal : 1 vertical). Must be non-negative.

        Raises:
            ValueError: If bottom width is not positive or side slope is negative.
        """
        if b <= 0:
            raise ValueError(f"Bottom width must be positive. Got: {b}")
        if z < 0:
            raise ValueError(f"Side slope must be non-negative. Got: {z}")
        self.b = b
        self.z = z

    def __repr__(self) -> str:
        return f"TrapezoidalChannel(b={self.b}, z={self.z})"

    def area(self, y: float) -> float:
        """
        Calculate cross-sectional flow area: A = (b + z*y) * y.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Flow area (m² or ft²).
        """
        self._validate_depth(y)
        return (self.b + self.z * y) * y

    def wetted_perimeter(self, y: float) -> float:
        """
        Calculate wetted perimeter: P = b + 2y * sqrt(1 + z²).

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Wetted perimeter (m or ft).
        """
        self._validate_depth(y)
        return self.b + 2 * y * math.sqrt(1 + self.z**2)

    def top_width(self, y: float) -> float:
        """
        Calculate top width: T = b + 2zy.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Top width (m or ft).
        """
        self._validate_depth(y)
        return self.b + 2 * self.z * y
