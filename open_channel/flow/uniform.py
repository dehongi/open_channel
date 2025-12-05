"""
Uniform flow calculations using Manning's equation.

Manning's Equation: Q = (k/n) * A * R^(2/3) * S^(1/2)
Where:
    k = 1.0 (SI) or 1.486 (English)
    n = Manning's roughness coefficient
    A = Cross-sectional area
    R = Hydraulic radius
    S = Channel bed slope
"""

from typing import Union
from scipy.optimize import brentq

from ..channels.base import Channel
from ..config import UnitSystem, get_constants


def solve_discharge(
    channel: Channel,
    y: float,
    n: float,
    s: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
) -> float:
    """
    Calculate discharge using Manning's equation.

    Q = (k/n) * A * R^(2/3) * S^(1/2)

    Args:
        channel: Channel geometry object.
        y: Water depth (m or ft).
        n: Manning's roughness coefficient.
        s: Channel bed slope (dimensionless).
        unit_system: Unit system (SI or English).

    Returns:
        float: Discharge Q (m³/s or ft³/s).

    Raises:
        ValueError: If inputs are not positive.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> Q = solve_discharge(channel, y=1.0, n=0.015, s=0.001)
        >>> print(f"{Q:.3f}")  # Output: ~5.312 m³/s
    """
    if n <= 0:
        raise ValueError(f"Manning's n must be positive. Got: {n}")
    if s <= 0:
        raise ValueError(f"Slope must be positive. Got: {s}")

    constants = get_constants(unit_system)
    k = constants.k

    A = channel.area(y)
    R = channel.hydraulic_radius(y)

    Q = (k / n) * A * (R ** (2 / 3)) * (s ** 0.5)
    return Q


def solve_normal_depth(
    channel: Channel,
    Q: float,
    n: float,
    s: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
    y_min: float = 0.001,
    y_max: float = 100.0,
) -> float:
    """
    Solve for normal depth using Manning's equation.

    Uses Brent's method to find y where Q_calc(y) - Q_target = 0.

    Args:
        channel: Channel geometry object.
        Q: Target discharge (m³/s or ft³/s).
        n: Manning's roughness coefficient.
        s: Channel bed slope (dimensionless).
        unit_system: Unit system (SI or English).
        y_min: Minimum depth for solver bracket (default: 0.001).
        y_max: Maximum depth for solver bracket (default: 100.0).

    Returns:
        float: Normal depth y_n (m or ft).

    Raises:
        ValueError: If inputs are not positive or solution cannot be found.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> y_n = solve_normal_depth(channel, Q=10.0, n=0.015, s=0.001)
        >>> print(f"{y_n:.3f}")  # Normal depth in meters
    """
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")
    if n <= 0:
        raise ValueError(f"Manning's n must be positive. Got: {n}")
    if s <= 0:
        raise ValueError(f"Slope must be positive. Got: {s}")

    def residual(y: float) -> float:
        """Residual function: Q_calc - Q_target."""
        Q_calc = solve_discharge(channel, y, n, s, unit_system)
        return Q_calc - Q

    # Use Brent's method to find the root
    try:
        y_n = brentq(residual, y_min, y_max)
        return y_n
    except ValueError as e:
        raise ValueError(
            f"Could not find normal depth in range [{y_min}, {y_max}]. "
            f"Try adjusting the search bounds. Original error: {e}"
        )
