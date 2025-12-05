"""
Hydraulic jump calculations.

A hydraulic jump is a rapid transition from supercritical to subcritical flow,
accompanied by significant energy dissipation.
"""

import math
from typing import Tuple

from ..channels.base import Channel
from ..channels.rectangular import RectangularChannel


def solve_conjugate_depth(
    channel: Channel,
    y1: float,
    Fr1: float,
) -> Tuple[float, float]:
    """
    Calculate conjugate (sequent) depth and energy loss in a hydraulic jump.

    For a rectangular channel, the conjugate depth relationship is:
    y2 = (y1/2) * (sqrt(1 + 8*Fr1²) - 1)

    Energy loss: ΔE = (y2 - y1)³ / (4*y1*y2)

    Args:
        channel: Channel geometry object (must be rectangular for exact solution).
        y1: Upstream depth (supercritical) (m or ft).
        Fr1: Upstream Froude number (must be > 1 for hydraulic jump).

    Returns:
        Tuple[float, float]: (y2, delta_E)
            y2: Downstream conjugate depth (subcritical) (m or ft).
            delta_E: Energy loss in the jump (m or ft).

    Raises:
        ValueError: If inputs are not valid.
        TypeError: If channel is not rectangular.

    Notes:
        The hydraulic jump formula used is exact only for rectangular channels.
        For non-rectangular channels, consider using momentum equation methods.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> y2, delta_E = solve_conjugate_depth(channel, y1=0.5, Fr1=3.0)
        >>> print(f"Conjugate depth: {y2:.3f} m")
        >>> print(f"Energy loss: {delta_E:.3f} m")
    """
    if not isinstance(channel, RectangularChannel):
        raise TypeError(
            "Hydraulic jump calculation is only implemented for rectangular channels. "
            f"Got: {type(channel).__name__}"
        )
    
    if y1 <= 0:
        raise ValueError(f"Upstream depth must be positive. Got: {y1}")
    
    if Fr1 <= 1:
        raise ValueError(
            f"Upstream Froude number must be greater than 1 for a hydraulic jump. "
            f"Got: {Fr1}"
        )

    # Conjugate depth formula for rectangular channels
    # y2/y1 = (1/2) * (sqrt(1 + 8*Fr1²) - 1)
    y2 = (y1 / 2) * (math.sqrt(1 + 8 * Fr1**2) - 1)

    # Energy loss in the jump
    # ΔE = (y2 - y1)³ / (4*y1*y2)
    delta_E = (y2 - y1) ** 3 / (4 * y1 * y2)

    return y2, delta_E
