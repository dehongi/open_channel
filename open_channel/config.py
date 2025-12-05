"""
Unit system configuration for Open Channel Hydraulics.

Provides constants for SI and English unit systems.
"""

from enum import Enum
from typing import NamedTuple


class UnitSystem(Enum):
    """Unit system options for hydraulic calculations."""
    SI = "SI"
    ENGLISH = "English"


class HydraulicConstants(NamedTuple):
    """Container for hydraulic constants based on unit system."""
    g: float  # Gravitational acceleration (m/s² or ft/s²)
    k: float  # Manning's equation conversion factor


# Constants for each unit system
_CONSTANTS = {
    UnitSystem.SI: HydraulicConstants(g=9.81, k=1.0),
    UnitSystem.ENGLISH: HydraulicConstants(g=32.2, k=1.486),
}


def get_constants(unit_system: UnitSystem = UnitSystem.SI) -> HydraulicConstants:
    """
    Get hydraulic constants for the specified unit system.

    Args:
        unit_system: The unit system to use (SI or English).

    Returns:
        HydraulicConstants: Named tuple with g and k values.

    Raises:
        ValueError: If an invalid unit system is provided.

    Examples:
        >>> constants = get_constants(UnitSystem.SI)
        >>> constants.g
        9.81
        >>> constants.k
        1.0
    """
    if isinstance(unit_system, str):
        try:
            unit_system = UnitSystem(unit_system)
        except ValueError:
            raise ValueError(
                f"Invalid unit system: '{unit_system}'. Use 'SI' or 'English'."
            )
    
    if unit_system not in _CONSTANTS:
        raise ValueError(
            f"Invalid unit system: {unit_system}. Use UnitSystem.SI or UnitSystem.ENGLISH."
        )
    
    return _CONSTANTS[unit_system]
