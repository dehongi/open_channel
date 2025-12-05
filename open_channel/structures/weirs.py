"""
Weir discharge calculations.

Weirs are overflow structures used for flow measurement and control.
"""

import math


def rectangular_weir_discharge(Cd: float, L: float, H: float) -> float:
    """
    Calculate discharge over a rectangular (sharp-crested) weir.

    Q = Cd * L * H^(3/2)

    The standard value of Cd depends on the weir configuration:
    - Sharp-crested: Cd ≈ 1.84 (SI) or 3.33 (English)
    - Broad-crested: Cd ≈ 1.7 (SI) or 3.09 (English)

    Args:
        Cd: Discharge coefficient (includes sqrt(2g) factor).
        L: Weir crest length (m or ft).
        H: Head over the weir crest (m or ft).

    Returns:
        float: Discharge Q (m³/s or ft³/s).

    Raises:
        ValueError: If inputs are not positive.

    Examples:
        >>> # Sharp-crested rectangular weir, SI units
        >>> Q = rectangular_weir_discharge(Cd=1.84, L=2.0, H=0.5)
        >>> print(f"{Q:.3f} m³/s")  # ~1.301 m³/s
    """
    if Cd <= 0:
        raise ValueError(f"Discharge coefficient must be positive. Got: {Cd}")
    if L <= 0:
        raise ValueError(f"Weir length must be positive. Got: {L}")
    if H <= 0:
        raise ValueError(f"Head must be positive. Got: {H}")

    Q = Cd * L * H ** (3 / 2)
    return Q


def vnotch_weir_discharge(Cd: float, theta: float, H: float) -> float:
    """
    Calculate discharge over a V-notch (triangular) weir.

    Q = Cd * tan(θ/2) * H^(5/2)

    The standard value of Cd depends on the notch angle:
    - For 90° V-notch: Cd ≈ 1.38 (SI) or 2.50 (English)

    Args:
        Cd: Discharge coefficient (includes sqrt(2g)/5 factors).
        theta: Notch angle in radians (e.g., π/2 for 90° notch).
        H: Head over the weir vertex (m or ft).

    Returns:
        float: Discharge Q (m³/s or ft³/s).

    Raises:
        ValueError: If inputs are not valid.

    Examples:
        >>> import math
        >>> # 90-degree V-notch weir, SI units
        >>> Q = vnotch_weir_discharge(Cd=1.38, theta=math.pi/2, H=0.3)
        >>> print(f"{Q:.4f} m³/s")
    """
    if Cd <= 0:
        raise ValueError(f"Discharge coefficient must be positive. Got: {Cd}")
    if theta <= 0 or theta > math.pi:
        raise ValueError(
            f"Notch angle must be between 0 and π radians. Got: {theta}"
        )
    if H <= 0:
        raise ValueError(f"Head must be positive. Got: {H}")

    Q = Cd * math.tan(theta / 2) * H ** (5 / 2)
    return Q
