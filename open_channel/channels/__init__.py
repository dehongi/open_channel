"""
Channel geometry classes for open channel hydraulics.
"""

from .base import Channel
from .rectangular import RectangularChannel
from .trapezoidal import TrapezoidalChannel
from .triangular import TriangularChannel
from .circular import CircularChannel

__all__ = [
    "Channel",
    "RectangularChannel",
    "TrapezoidalChannel",
    "TriangularChannel",
    "CircularChannel",
]
