"""
Triangular channel geometry.
"""

import math
from .base import Channel


class TriangularChannel(Channel):
    """
    Triangular open channel cross-section.

    A triangular channel has sloped side walls meeting at a point (no bottom width).

    Attributes:
        z: Side slope (z horizontal : 1 vertical).

    Formulas:
        - Area: A = z * y²
        - Wetted Perimeter: P = 2y * sqrt(1 + z²)
        - Top Width: T = 2zy
    """

    def __init__(self, z: float) -> None:
        """
        Initialize a triangular channel.

        Args:
            z: Side slope (z horizontal : 1 vertical). Must be positive.

        Raises:
            ValueError: If side slope is not positive.
        """
        if z <= 0:
            raise ValueError(f"Side slope must be positive. Got: {z}")
        self.z = z

    def __repr__(self) -> str:
        return f"TriangularChannel(z={self.z})"

    def area(self, y: float) -> float:
        """
        Calculate cross-sectional flow area: A = z * y².

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Flow area (m² or ft²).
        """
        self._validate_depth(y)
        return self.z * y**2

    def wetted_perimeter(self, y: float) -> float:
        """
        Calculate wetted perimeter: P = 2y * sqrt(1 + z²).

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Wetted perimeter (m or ft).
        """
        self._validate_depth(y)
        return 2 * y * math.sqrt(1 + self.z**2)

    def top_width(self, y: float) -> float:
        """
        Calculate top width: T = 2zy.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Top width (m or ft).
        """
        self._validate_depth(y)
        return 2 * self.z * y
