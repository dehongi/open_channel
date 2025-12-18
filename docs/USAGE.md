# Usage Documentation

> 💡 Looking for practical engineering applications? Check out the **[Detailed Engineering Examples](EXAMPLES.md)**.


## Table of Contents

1. [Unit Systems](#unit-systems)
2. [Channel Geometry](#channel-geometry)
3. [Uniform Flow](#uniform-flow)
4. [Critical Flow](#critical-flow)
5. [Gradually Varied Flow](#gradually-varied-flow)
6. [Hydraulic Structures](#hydraulic-structures)

---

## Unit Systems

The library supports both SI and English unit systems.

```python
from open_channel import UnitSystem, get_constants

# Get constants for SI units (default)
si = get_constants(UnitSystem.SI)
print(f"g = {si.g} m/s², k = {si.k}")  # g=9.81, k=1.0

# Get constants for English units
eng = get_constants(UnitSystem.ENGLISH)
print(f"g = {eng.g} ft/s², k = {eng.k}")  # g=32.2, k=1.486
```

---

## Channel Geometry

### Rectangular Channel

```python
from open_channel import RectangularChannel

# Create a 3m wide rectangular channel
channel = RectangularChannel(b=3.0)

# Calculate properties at 1m depth
y = 1.0
print(f"Area: {channel.area(y)} m²")                    # 3.0
print(f"Wetted Perimeter: {channel.wetted_perimeter(y)} m")  # 5.0
print(f"Hydraulic Radius: {channel.hydraulic_radius(y)} m")  # 0.6
print(f"Top Width: {channel.top_width(y)} m")           # 3.0
print(f"Hydraulic Depth: {channel.hydraulic_depth(y)} m")    # 1.0
```

### Trapezoidal Channel

```python
from open_channel import TrapezoidalChannel

# Create channel: 2m bottom width, 1.5:1 side slope
channel = TrapezoidalChannel(b=2.0, z=1.5)

y = 1.5
print(f"Area: {channel.area(y):.2f} m²")  # A = (b + zy)y = (2 + 1.5*1.5)*1.5
print(f"Top Width: {channel.top_width(y):.2f} m")  # T = b + 2zy
```

### Triangular Channel

```python
from open_channel import TriangularChannel

# Create channel: 2:1 side slope (no bottom width)
channel = TriangularChannel(z=2.0)

y = 1.0
print(f"Area: {channel.area(y)} m²")  # A = zy² = 2.0
```

### Circular Channel

```python
from open_channel import CircularChannel

# Create a 1.2m diameter pipe
channel = CircularChannel(D=1.2)

# Calculate at half-full (y = D/2)
y = 0.6
print(f"Area: {channel.area(y):.4f} m²")
print(f"Top Width: {channel.top_width(y):.2f} m")  # = D at half-full
```

---

## Uniform Flow

Manning's Equation: $Q = \frac{k}{n} A R^{2/3} S^{1/2}$

### Calculate Discharge

```python
from open_channel import RectangularChannel
from open_channel.flow.uniform import solve_discharge

channel = RectangularChannel(b=3.0)

# Calculate discharge given depth
Q = solve_discharge(
    channel=channel,
    y=1.0,           # Water depth (m)
    n=0.015,         # Manning's roughness coefficient
    s=0.001,         # Channel bed slope
    unit_system='SI' # or 'English'
)
print(f"Discharge: {Q:.3f} m³/s")
```

### Solve for Normal Depth

```python
from open_channel.flow.uniform import solve_normal_depth

# Find normal depth for given discharge
y_n = solve_normal_depth(
    channel=channel,
    Q=10.0,          # Target discharge (m³/s)
    n=0.015,
    s=0.001
)
print(f"Normal depth: {y_n:.3f} m")
```

---

## Critical Flow

### Froude Number

```python
from open_channel import RectangularChannel
from open_channel.flow.critical import calculate_froude

channel = RectangularChannel(b=3.0)

Fr = calculate_froude(channel, y=1.0, Q=10.0)
print(f"Froude number: {Fr:.3f}")

if Fr < 1:
    print("Subcritical flow")
elif Fr > 1:
    print("Supercritical flow")
else:
    print("Critical flow")
```

### Critical Depth

```python
from open_channel.flow.critical import solve_critical_depth

y_c = solve_critical_depth(channel, Q=10.0)
print(f"Critical depth: {y_c:.3f} m")

# Verify Fr = 1 at critical depth
Fr = calculate_froude(channel, y=y_c, Q=10.0)
print(f"Fr at y_c: {Fr:.6f}")  # ≈ 1.0
```

### Alternate Depths

```python
from open_channel.flow.critical import solve_alternate_depths

# Find subcritical and supercritical depths for given specific energy
y_sup, y_sub = solve_alternate_depths(channel, E=2.0, Q=10.0)
print(f"Supercritical depth: {y_sup:.3f} m")
print(f"Subcritical depth: {y_sub:.3f} m")
```

---

## Gradually Varied Flow

### Direct Step Method

Calculate distance between two known depths.

```python
from open_channel import RectangularChannel
from open_channel.flow.gvf import direct_step_method

channel = RectangularChannel(b=3.0)

# Find distance between depths 1.0m and 1.2m
dx = direct_step_method(
    channel=channel,
    y1=1.0,          # Upstream depth
    y2=1.2,          # Downstream depth
    Q=10.0,          # Discharge
    n=0.015,         # Manning's n
    s0=0.001         # Bed slope
)
print(f"Distance: {dx:.2f} m")
```

### Standard Step Method

Calculate depth at a target station.

```python
from open_channel.flow.gvf import standard_step_method

# Find depth 50m downstream from starting point
y2 = standard_step_method(
    channel=channel,
    x_start=0,       # Starting station
    y_start=1.0,     # Starting depth
    x_target=50,     # Target station
    Q=10.0,
    n=0.015,
    s0=0.001
)
print(f"Depth at x=50m: {y2:.3f} m")
```

---

## Hydraulic Structures

### Hydraulic Jump

```python
from open_channel import RectangularChannel
from open_channel.structures.hydraulic_jump import solve_conjugate_depth
from open_channel.flow.critical import calculate_froude

channel = RectangularChannel(b=3.0)

# Given upstream supercritical conditions
y1 = 0.3
Q = 10.0
Fr1 = calculate_froude(channel, y=y1, Q=Q)
print(f"Upstream Froude: {Fr1:.2f}")

# Calculate conjugate depth and energy loss
y2, delta_E = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
print(f"Conjugate depth: {y2:.3f} m")
print(f"Energy loss: {delta_E:.3f} m")
```

### Weirs

#### Rectangular Weir

```python
from open_channel.structures.weirs import rectangular_weir_discharge

# Q = Cd * L * H^(3/2)
Q = rectangular_weir_discharge(
    Cd=1.84,    # Discharge coefficient (SI, sharp-crested)
    L=2.0,      # Weir crest length (m)
    H=0.5       # Head over weir (m)
)
print(f"Discharge: {Q:.3f} m³/s")
```

#### V-Notch Weir

```python
import math
from open_channel.structures.weirs import vnotch_weir_discharge

# Q = Cd * tan(θ/2) * H^(5/2)
Q = vnotch_weir_discharge(
    Cd=1.38,           # Discharge coefficient (SI, 90° notch)
    theta=math.pi/2,   # Notch angle (radians)
    H=0.3              # Head over vertex (m)
)
print(f"Discharge: {Q:.4f} m³/s")
```

---

## Error Handling

All functions validate inputs and raise `ValueError` for invalid parameters:

```python
from open_channel import RectangularChannel

# This will raise ValueError
try:
    channel = RectangularChannel(b=-1.0)  # Negative width
except ValueError as e:
    print(f"Error: {e}")

# Negative depth also raises error
try:
    channel = RectangularChannel(b=3.0)
    channel.area(y=-1.0)
except ValueError as e:
    print(f"Error: {e}")
```

---

## API Reference

### Channels

| Class | Parameters | Description |
|-------|------------|-------------|
| `RectangularChannel(b)` | b: bottom width | Vertical-walled channel |
| `TrapezoidalChannel(b, z)` | b: bottom width, z: side slope | Sloped walls |
| `TriangularChannel(z)` | z: side slope | V-shaped, no bottom |
| `CircularChannel(D)` | D: diameter | Partially-filled pipe |

### Flow Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `solve_discharge(channel, y, n, s)` | Q | Manning's discharge |
| `solve_normal_depth(channel, Q, n, s)` | y_n | Normal depth |
| `calculate_froude(channel, y, Q)` | Fr | Froude number |
| `solve_critical_depth(channel, Q)` | y_c | Critical depth |
| `solve_alternate_depths(channel, E, Q)` | (y_sup, y_sub) | Alternate depths |
| `direct_step_method(...)` | Δx | Distance between depths |
| `standard_step_method(...)` | y | Depth at target station |

### Structure Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `solve_conjugate_depth(channel, y1, Fr1)` | (y2, ΔE) | Jump conjugate depth |
| `rectangular_weir_discharge(Cd, L, H)` | Q | Rectangular weir discharge |
| `vnotch_weir_discharge(Cd, theta, H)` | Q | V-notch weir discharge |
