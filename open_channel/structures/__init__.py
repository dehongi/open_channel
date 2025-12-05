"""
Hydraulic structures calculations.
"""

from .hydraulic_jump import solve_conjugate_depth
from .weirs import rectangular_weir_discharge, vnotch_weir_discharge

__all__ = [
    "solve_conjugate_depth",
    "rectangular_weir_discharge",
    "vnotch_weir_discharge",
]
