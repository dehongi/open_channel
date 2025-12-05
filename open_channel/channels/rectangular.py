"""
Rectangular channel geometry.
"""

from .base import Channel


class RectangularChannel(Channel):
    """
    Rectangular open channel cross-section.

    A rectangular channel has vertical walls and a flat bottom.

    Attributes:
        b: Bottom width (m or ft).

    Formulas:
        - Area: A = b * y
        - Wetted Perimeter: P = b + 2y
        - Top Width: T = b
    """

    def __init__(self, b: float) -> None:
        """
        Initialize a rectangular channel.

        Args:
            b: Bottom width (m or ft). Must be positive.

        Raises:
            ValueError: If bottom width is not positive.
        """
        if b <= 0:
            raise ValueError(f"Bottom width must be positive. Got: {b}")
        self.b = b

    def __repr__(self) -> str:
        return f"RectangularChannel(b={self.b})"

    def area(self, y: float) -> float:
        """
        Calculate cross-sectional flow area: A = b * y.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Flow area (m² or ft²).
        """
        self._validate_depth(y)
        return self.b * y

    def wetted_perimeter(self, y: float) -> float:
        """
        Calculate wetted perimeter: P = b + 2y.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Wetted perimeter (m or ft).
        """
        self._validate_depth(y)
        return self.b + 2 * y

    def top_width(self, y: float) -> float:
        """
        Calculate top width: T = b.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Top width (m or ft).
        """
        self._validate_depth(y)
        return self.b
