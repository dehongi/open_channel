"""
Circular channel geometry.
"""

import math
from .base import Channel


class CircularChannel(Channel):
    """
    Circular open channel cross-section (partially filled pipe).

    A circular channel is typically a pipe flowing partially full.

    Attributes:
        D: Diameter (m or ft).

    Formulas (using θ = 2*arccos(1 - 2y/D)):
        - Area: A = (D²/8) * (θ - sin(θ))
        - Wetted Perimeter: P = (1/2) * θ * D
        - Top Width: T = D * sin(θ/2)
    """

    def __init__(self, D: float) -> None:
        """
        Initialize a circular channel.

        Args:
            D: Diameter (m or ft). Must be positive.

        Raises:
            ValueError: If diameter is not positive.
        """
        if D <= 0:
            raise ValueError(f"Diameter must be positive. Got: {D}")
        self.D = D

    def __repr__(self) -> str:
        return f"CircularChannel(D={self.D})"

    def _calculate_theta(self, y: float) -> float:
        """
        Calculate the central angle θ for a given water depth.

        θ = 2 * arccos(1 - 2y/D)

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Central angle θ in radians.

        Raises:
            ValueError: If depth exceeds diameter.
        """
        if y > self.D:
            raise ValueError(
                f"Water depth ({y}) cannot exceed diameter ({self.D})."
            )
        
        # Clamp the argument to [-1, 1] to handle floating point precision
        arg = 1 - 2 * y / self.D
        arg = max(-1, min(1, arg))
        return 2 * math.acos(arg)

    def area(self, y: float) -> float:
        """
        Calculate cross-sectional flow area: A = (D²/8) * (θ - sin(θ)).

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Flow area (m² or ft²).
        """
        self._validate_depth(y)
        theta = self._calculate_theta(y)
        return (self.D**2 / 8) * (theta - math.sin(theta))

    def wetted_perimeter(self, y: float) -> float:
        """
        Calculate wetted perimeter: P = (1/2) * θ * D.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Wetted perimeter (m or ft).
        """
        self._validate_depth(y)
        theta = self._calculate_theta(y)
        return 0.5 * theta * self.D

    def top_width(self, y: float) -> float:
        """
        Calculate top width: T = D * sin(θ/2).

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Top width (m or ft).
        """
        self._validate_depth(y)
        theta = self._calculate_theta(y)
        return self.D * math.sin(theta / 2)
