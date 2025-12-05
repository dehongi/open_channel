"""
Flow analysis modules for open channel hydraulics.
"""

from .uniform import solve_discharge, solve_normal_depth
from .critical import calculate_froude, solve_critical_depth, solve_alternate_depths
from .gvf import direct_step_method, standard_step_method

__all__ = [
    "solve_discharge",
    "solve_normal_depth",
    "calculate_froude",
    "solve_critical_depth",
    "solve_alternate_depths",
    "direct_step_method",
    "standard_step_method",
]
