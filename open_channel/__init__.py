"""
Open Channel Hydraulics Library

A modular Python library for solving open channel hydraulics problems including:
- Channel geometry calculations
- Uniform flow (Manning's equation)
- Critical flow analysis
- Gradually varied flow profiles
- Hydraulic structures (jumps, weirs)
"""

from .config import UnitSystem, get_constants
from .channels import (
    Channel,
    RectangularChannel,
    TrapezoidalChannel,
    TriangularChannel,
    CircularChannel,
)
from .flow.uniform import solve_discharge, solve_normal_depth
from .flow.critical import calculate_froude, solve_critical_depth, solve_alternate_depths
from .flow.gvf import direct_step_method, standard_step_method
from .structures.hydraulic_jump import solve_conjugate_depth
from .structures.weirs import rectangular_weir_discharge, vnotch_weir_discharge

__all__ = [
    # Config
    "UnitSystem",
    "get_constants",
    # Channels
    "Channel",
    "RectangularChannel",
    "TrapezoidalChannel",
    "TriangularChannel",
    "CircularChannel",
    # Uniform Flow
    "solve_discharge",
    "solve_normal_depth",
    # Critical Flow
    "calculate_froude",
    "solve_critical_depth",
    "solve_alternate_depths",
    # GVF
    "direct_step_method",
    "standard_step_method",
    # Structures
    "solve_conjugate_depth",
    "rectangular_weir_discharge",
    "vnotch_weir_discharge",
]

__version__ = "1.0.0"
