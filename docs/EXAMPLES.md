# Practical Engineering Examples

This document provides detailed walk-throughs of the practical examples found in the `examples/` directory. Each example solves a common civil engineering hydraulics problem.

## Table of Contents
1. [Trapezoidal Channel Design](#1-trapezoidal-channel-design)
2. [Backwater Curve Analysis (M1 Profile)](#2-backwater-curve-analysis-m1-profile)
3. [Hydraulic Jump in a Stilling Basin](#3-hydraulic-jump-in-a-stilling-basin)
4. [Storm Drain Capacity (English Units)](#4-storm-drain-capacity-english-units)

---

## 1. Trapezoidal Channel Design
**File:** `examples/01_channel_design.py`

### Problem Statement
An unlined earth channel ($n = 0.022$) must be designed to carry a discharge of $25\text{ m}^3\text{/s}$ on a slope of 0.0005. The side slopes are fixed at 2:1 (H:V). To prevent overflow and maintain safety, the maximum water depth must not exceed 2.5 meters. We need to find the minimum bottom width $b$.

### Implementation
We use an iterative approach, starting from a small width and increasing it until the calculated normal depth $y_n$ falls below our 2.5m limit.

```python
from open_channel import TrapezoidalChannel, solve_normal_depth

# ... (iteration loop)
channel = TrapezoidalChannel(b=b, z=2.0)
y_n = solve_normal_depth(channel, Q=25.0, n=0.022, s=0.0005)
```

### Analysis of Results
```text
Width (m)  Normal Depth (m)     Status    
1.0        2.890                Too Deep  
1.5        2.777                Too Deep  
2.0        2.670                Too Deep  
2.5        2.569                Too Deep  
3.0        2.474                OK        
```
The solution shows that a **3.0m bottom width** is required. At this width, the Froude number is 0.329, indicating stable subcritical flow.

---

## 2. Backwater Curve Analysis (M1 Profile)
**File:** `examples/02_backwater_curve.py`

### Problem Statement
A rectangular river channel ($b=50\text{m}$, $Q=200\text{ m}^3\text{/s}$, $n=0.03$, $S_0=0.0004$) is obstructed by a dam. The dam raises the water level to 8.0m at the dam face. We want to determine the water surface profile upstream and find how far the "backwater effect" extends.

### Implementation
This is a **Gradually Varied Flow (GVF)** problem. Since $y_{dam} > y_n > y_c$, this is an **M1 profile**. We use the `standard_step_method` to calculate depths at 500m intervals moving upstream (negative direction).

```python
next_y = standard_step_method(
    channel,
    x_start=current_x,
    y_start=current_y,
    x_target=next_x, # x_start - 500
    Q=200.0, n=0.03, s0=0.0004
)
```

### Analysis of Results
The calculation shows that the backwater effect is significant for over 20 kilometers upstream.
- **Normal Depth:** 3.069 m
- **Start Depth:** 8.000 m
- **Normal depth reached at:** ~21.5 km upstream.

---

## 3. Hydraulic Jump in a Stilling Basin
**File:** `examples/03_hydraulic_jump.py`

### Problem Statement
A spillway at a dam discharges $50\text{ m}^3\text{/s}$ into a 6m wide rectangular stilling basin. The water enters at a high velocity of 12 m/s. We need to analyze the hydraulic jump that will form to dissipate energy.

### Implementation
We use the Belanger equation (implemented in `solve_conjugate_depth`) to find the sequent depth and energy loss.

```python
from open_channel import solve_conjugate_depth, calculate_froude

y1 = Q / (v1 * width) # 0.694 m
Fr1 = calculate_froude(channel, y=y1, Q=Q) # 4.598
y2, delta_E = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
```

### Analysis of Results
- **Upstream Froude Number:** 4.60 (Steady Jump)
- **Conjugate Depth ($y_2$):** 4.18 m
- **Energy Dissipation:** 45.4%
- **Efficiency:** 54.6%

The analysis tells engineers that the stilling basin walls must be at least 4.2m high (plus freeboard) to contain the jump, and that nearly half of the flow energy is successfully dissipated by the turbulence of the jump.

---

## 4. Storm Drain Capacity (English Units)
**File:** `examples/04_storm_drain.py`

### Problem Statement
A 48-inch (4.0 ft) concrete storm drain is assessed for its capacity. We use the Standard English unit system ($g = 32.2$, $k = 1.486$).

### Implementation
We utilize the `UnitSystem.ENGLISH` flag in our calculations.

```python
from open_channel import CircularChannel, UnitSystem, solve_discharge

channel = CircularChannel(D=4.0)
Q_full = solve_discharge(channel, y=3.99, n=0.013, s=0.005, unit_system=UnitSystem.ENGLISH)
```

### Analysis of Results
- **Full Capacity:** 102.26 cfs
- **Half-full Discharge:** 50.79 cfs
- **Normal Depth for 30 cfs:** 1.49 ft (37% of diameter)

Note that in circular pipes, the "half-full" discharge is not exactly half of the "full" discharge because the hydraulic radius changes non-linearly with depth. This example shows the half-full discharge is roughly 49.7% of the capacity.
