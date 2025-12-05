"""
Abstract base class for channel geometry.
"""

from abc import ABC, abstractmethod


class Channel(ABC):
    """
    Abstract base class for open channel cross-sections.

    All channel subclasses must implement methods to calculate:
    - Cross-sectional flow area
    - Wetted perimeter
    - Top width at free surface

    The base class provides concrete implementations for:
    - Hydraulic radius (R = A / P)
    - Hydraulic depth (Dh = A / T)
    """

    def _validate_depth(self, y: float) -> None:
        """
        Validate that water depth is positive.

        Args:
            y: Water depth (m or ft).

        Raises:
            ValueError: If depth is not positive.
        """
        if y <= 0:
            raise ValueError(f"Water depth must be positive. Got: {y}")

    @abstractmethod
    def area(self, y: float) -> float:
        """
        Calculate cross-sectional flow area.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Flow area (m² or ft²).
        """
        pass

    @abstractmethod
    def wetted_perimeter(self, y: float) -> float:
        """
        Calculate wetted perimeter.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Wetted perimeter length (m or ft).
        """
        pass

    @abstractmethod
    def top_width(self, y: float) -> float:
        """
        Calculate top width at free surface.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Top width (m or ft).
        """
        pass

    def hydraulic_radius(self, y: float) -> float:
        """
        Calculate hydraulic radius: R = A / P.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Hydraulic radius (m or ft).
        """
        self._validate_depth(y)
        A = self.area(y)
        P = self.wetted_perimeter(y)
        return A / P

    def hydraulic_depth(self, y: float) -> float:
        """
        Calculate hydraulic depth: Dh = A / T.

        Args:
            y: Water depth (m or ft).

        Returns:
            float: Hydraulic depth (m or ft).
        """
        self._validate_depth(y)
        A = self.area(y)
        T = self.top_width(y)
        return A / T
