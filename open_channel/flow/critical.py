"""
Critical flow and energy calculations.

Critical flow occurs when the Froude number equals 1, representing
the transition between subcritical and supercritical flow regimes.
"""

import math
from typing import Tuple, Union
from scipy.optimize import brentq

from ..channels.base import Channel
from ..config import UnitSystem, get_constants


def calculate_froude(
    channel: Channel,
    y: float,
    Q: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
) -> float:
    """
    Calculate the Froude number.

    Fr = V / sqrt(g * Dh)

    Where:
        V = Q / A (flow velocity)
        Dh = A / T (hydraulic depth)

    Args:
        channel: Channel geometry object.
        y: Water depth (m or ft).
        Q: Discharge (m³/s or ft³/s).
        unit_system: Unit system (SI or English).

    Returns:
        float: Froude number (dimensionless).
            Fr < 1: Subcritical flow
            Fr = 1: Critical flow
            Fr > 1: Supercritical flow

    Raises:
        ValueError: If inputs are not positive.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> Fr = calculate_froude(channel, y=1.0, Q=10.0)
    """
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")

    constants = get_constants(unit_system)
    g = constants.g

    A = channel.area(y)
    Dh = channel.hydraulic_depth(y)
    V = Q / A

    Fr = V / math.sqrt(g * Dh)
    return Fr


def solve_critical_depth(
    channel: Channel,
    Q: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
    y_min: float = 0.001,
    y_max: float = 100.0,
) -> float:
    """
    Solve for critical depth where Froude number equals 1.

    At critical depth: Q²T / (gA³) = 1

    Args:
        channel: Channel geometry object.
        Q: Discharge (m³/s or ft³/s).
        unit_system: Unit system (SI or English).
        y_min: Minimum depth for solver bracket (default: 0.001).
        y_max: Maximum depth for solver bracket (default: 100.0).

    Returns:
        float: Critical depth y_c (m or ft).

    Raises:
        ValueError: If inputs are not positive or solution cannot be found.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> y_c = solve_critical_depth(channel, Q=10.0)
    """
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")

    constants = get_constants(unit_system)
    g = constants.g

    def residual(y: float) -> float:
        """Residual function: 1 - Q²T / (gA³)."""
        A = channel.area(y)
        T = channel.top_width(y)
        return 1 - (Q**2 * T) / (g * A**3)

    try:
        y_c = brentq(residual, y_min, y_max)
        return y_c
    except ValueError as e:
        raise ValueError(
            f"Could not find critical depth in range [{y_min}, {y_max}]. "
            f"Try adjusting the search bounds. Original error: {e}"
        )


def _specific_energy(channel: Channel, y: float, Q: float, g: float) -> float:
    """
    Calculate specific energy: E = y + V²/(2g) = y + Q²/(2gA²).

    Args:
        channel: Channel geometry object.
        y: Water depth (m or ft).
        Q: Discharge (m³/s or ft³/s).
        g: Gravitational acceleration.

    Returns:
        float: Specific energy (m or ft).
    """
    A = channel.area(y)
    return y + (Q**2) / (2 * g * A**2)


def solve_alternate_depths(
    channel: Channel,
    E: float,
    Q: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
    y_min: float = 0.001,
    y_max: float = 100.0,
) -> Tuple[float, float]:
    """
    Find the two alternate depths (subcritical and supercritical) for given specific energy.

    For a given specific energy E and discharge Q, there are typically two
    possible depths: a subcritical depth (larger, slower flow) and a
    supercritical depth (smaller, faster flow).

    Args:
        channel: Channel geometry object.
        E: Specific energy (m or ft).
        Q: Discharge (m³/s or ft³/s).
        unit_system: Unit system (SI or English).
        y_min: Minimum depth for solver bracket (default: 0.001).
        y_max: Maximum depth for solver bracket (default: 100.0).

    Returns:
        Tuple[float, float]: (y_supercritical, y_subcritical) - the two alternate depths.

    Raises:
        ValueError: If inputs are not valid or solutions cannot be found.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> y_sup, y_sub = solve_alternate_depths(channel, E=2.0, Q=10.0)
    """
    if E <= 0:
        raise ValueError(f"Specific energy must be positive. Got: {E}")
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")

    constants = get_constants(unit_system)
    g = constants.g

    # First find critical depth to split the search range
    y_c = solve_critical_depth(channel, Q, unit_system, y_min, y_max)

    def residual(y: float) -> float:
        """Residual function: E_calc - E_target."""
        return _specific_energy(channel, y, Q, g) - E

    # Find supercritical depth (y < y_c)
    try:
        y_supercritical = brentq(residual, y_min, y_c * 0.999)
    except ValueError:
        raise ValueError(
            f"Could not find supercritical depth. Specific energy {E} may be "
            f"less than minimum specific energy at critical depth."
        )

    # Find subcritical depth (y > y_c)
    try:
        y_subcritical = brentq(residual, y_c * 1.001, y_max)
    except ValueError:
        raise ValueError(
            f"Could not find subcritical depth in range [{y_c}, {y_max}]. "
            f"Try increasing y_max."
        )

    return y_supercritical, y_subcritical
