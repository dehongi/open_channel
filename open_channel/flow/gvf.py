"""
Gradually Varied Flow (GVF) calculations.

GVF occurs when water surface profiles change gradually along the channel.
The governing equation is: dy/dx = (S0 - Sf) / (1 - Fr²)

Where:
    S0 = Channel bed slope
    Sf = Friction slope = n²Q² / (A²R^(4/3))
    Fr = Froude number
"""

from typing import Union
from scipy.optimize import brentq

from ..channels.base import Channel
from ..config import UnitSystem, get_constants
from .critical import calculate_froude


def _friction_slope(
    channel: Channel,
    y: float,
    Q: float,
    n: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
) -> float:
    """
    Calculate friction slope using Manning's equation.

    Sf = n²Q² / (k²A²R^(4/3))

    Args:
        channel: Channel geometry object.
        y: Water depth (m or ft).
        Q: Discharge (m³/s or ft³/s).
        n: Manning's roughness coefficient.
        unit_system: Unit system (SI or English).

    Returns:
        float: Friction slope (dimensionless).
    """
    constants = get_constants(unit_system)
    k = constants.k

    A = channel.area(y)
    R = channel.hydraulic_radius(y)

    Sf = (n**2 * Q**2) / (k**2 * A**2 * R ** (4 / 3))
    return Sf


def _specific_energy(
    channel: Channel,
    y: float,
    Q: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
) -> float:
    """
    Calculate specific energy: E = y + V²/(2g).

    Args:
        channel: Channel geometry object.
        y: Water depth (m or ft).
        Q: Discharge (m³/s or ft³/s).
        unit_system: Unit system (SI or English).

    Returns:
        float: Specific energy (m or ft).
    """
    constants = get_constants(unit_system)
    g = constants.g

    A = channel.area(y)
    V = Q / A
    return y + V**2 / (2 * g)


def direct_step_method(
    channel: Channel,
    y1: float,
    y2: float,
    Q: float,
    n: float,
    s0: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
) -> float:
    """
    Calculate distance between two known depths using Direct Step Method.

    This method is suitable for prismatic (uniform) channels where the
    channel properties don't change along the length.

    The method uses the energy equation:
    Δx = (E2 - E1) / (S0 - Sf_avg)

    Args:
        channel: Channel geometry object.
        y1: Upstream water depth (m or ft).
        y2: Downstream water depth (m or ft).
        Q: Discharge (m³/s or ft³/s).
        n: Manning's roughness coefficient.
        s0: Channel bed slope (dimensionless).
        unit_system: Unit system (SI or English).

    Returns:
        float: Distance Δx between the two depths (m or ft).
            Positive value indicates downstream direction.
            Negative value indicates upstream direction.

    Raises:
        ValueError: If inputs are not positive.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> dx = direct_step_method(channel, y1=1.0, y2=1.2, Q=10.0, n=0.015, s0=0.001)
    """
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")
    if n <= 0:
        raise ValueError(f"Manning's n must be positive. Got: {n}")
    if s0 <= 0:
        raise ValueError(f"Bed slope must be positive. Got: {s0}")

    # Calculate specific energy at both sections
    E1 = _specific_energy(channel, y1, Q, unit_system)
    E2 = _specific_energy(channel, y2, Q, unit_system)

    # Calculate friction slope at both sections and average
    Sf1 = _friction_slope(channel, y1, Q, n, unit_system)
    Sf2 = _friction_slope(channel, y2, Q, n, unit_system)
    Sf_avg = (Sf1 + Sf2) / 2

    # Calculate distance
    delta_x = (E2 - E1) / (s0 - Sf_avg)

    return delta_x


def standard_step_method(
    channel: Channel,
    x_start: float,
    y_start: float,
    x_target: float,
    Q: float,
    n: float,
    s0: float,
    unit_system: Union[UnitSystem, str] = UnitSystem.SI,
    y_min: float = 0.001,
    y_max: float = 100.0,
    tol: float = 1e-6,
) -> float:
    """
    Calculate depth at target station using Standard Step Method.

    This method finds the water depth at a target location given a starting
    condition. It iteratively solves the energy equation to balance energy
    between the two stations.

    Energy equation: E1 + S0*Δx = E2 + Sf_avg*Δx

    Args:
        channel: Channel geometry object.
        x_start: Starting station (m or ft).
        y_start: Water depth at starting station (m or ft).
        x_target: Target station (m or ft).
        Q: Discharge (m³/s or ft³/s).
        n: Manning's roughness coefficient.
        s0: Channel bed slope (dimensionless).
        unit_system: Unit system (SI or English).
        y_min: Minimum depth for solver bracket (default: 0.001).
        y_max: Maximum depth for solver bracket (default: 100.0).
        tol: Solver tolerance (default: 1e-6).

    Returns:
        float: Water depth at target station (m or ft).

    Raises:
        ValueError: If inputs are not valid or solution cannot be found.

    Examples:
        >>> from open_channel.channels import RectangularChannel
        >>> channel = RectangularChannel(b=3.0)
        >>> y2 = standard_step_method(
        ...     channel, x_start=0, y_start=1.0, x_target=100,
        ...     Q=10.0, n=0.015, s0=0.001
        ... )
    """
    if Q <= 0:
        raise ValueError(f"Discharge must be positive. Got: {Q}")
    if n <= 0:
        raise ValueError(f"Manning's n must be positive. Got: {n}")
    if s0 <= 0:
        raise ValueError(f"Bed slope must be positive. Got: {s0}")

    delta_x = x_target - x_start

    # Edge case: if target is at same position, return starting depth
    if delta_x == 0:
        return y_start

    # Calculate energy and friction slope at starting section
    E1 = _specific_energy(channel, y_start, Q, unit_system)
    Sf1 = _friction_slope(channel, y_start, Q, n, unit_system)

    def residual(y2: float) -> float:
        """
        Residual function for energy balance.

        Energy equation: E1 + S0*Δx = E2 + Sf_avg*Δx
        Rearranged: E1 + (S0 - Sf_avg)*Δx - E2 = 0
        """
        E2 = _specific_energy(channel, y2, Q, unit_system)
        Sf2 = _friction_slope(channel, y2, Q, n, unit_system)
        Sf_avg = (Sf1 + Sf2) / 2

        return E1 + (s0 - Sf_avg) * delta_x - E2

    try:
        y_target = brentq(residual, y_min, y_max, xtol=tol)
        return y_target
    except ValueError as e:
        raise ValueError(
            f"Could not find depth at target station in range [{y_min}, {y_max}]. "
            f"The flow conditions may not be valid. Original error: {e}"
        )
