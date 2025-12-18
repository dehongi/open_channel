# Open Channel Hydraulics

A modular Python library for solving open channel hydraulics problems including geometric calculations, uniform flow, critical flow, gradually varied flow profiles, and hydraulic structures.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Channel Geometry** - Rectangular, Trapezoidal, Triangular, and Circular channels
- **Uniform Flow** - Manning's equation for discharge and normal depth
- **Critical Flow** - Froude number, critical depth, and alternate depths
- **Gradually Varied Flow** - Direct Step and Standard Step methods
- **Hydraulic Structures** - Hydraulic jumps and weir discharge calculations
- **Unit Systems** - Support for both SI and English units

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd open_channel

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install the package
pip install -e ".[dev]"
```

## Quick Start

```python
from open_channel import RectangularChannel
from open_channel.flow.uniform import solve_discharge, solve_normal_depth

# Create a 3m wide rectangular channel
channel = RectangularChannel(b=3.0)

# Calculate discharge for 1m depth, Manning's n=0.015, slope=0.001
Q = solve_discharge(channel, y=1.0, n=0.015, s=0.001)
print(f"Discharge: {Q:.3f} m³/s")  # ~4.479 m³/s

# Solve for normal depth given discharge
y_n = solve_normal_depth(channel, Q=10.0, n=0.015, s=0.001)
print(f"Normal depth: {y_n:.3f} m")
```

## Practical Examples

Check the `examples/` directory for ready-to-run scripts covering common engineering problems:

1. **[Channel Design](examples/01_channel_design.py)** - Iterative design of a trapezoidal channel to meet specific constraints.
2. **[Backwater Curve](examples/02_backwater_curve.py)** - Computing an M1 water surface profile upstream of a dam.
3. **[Hydraulic Jump Analysis](examples/03_hydraulic_jump.py)** - Analyzing energy dissipation and stability of a hydraulic jump.
4. **[Storm Drain Capacity](examples/04_storm_drain.py)** - Using English units to calculate circular pipe flow capacity.
5. **[GVF Visualization](examples/05_drawdown_curve.py)** - Generating and plotting a drawdown curve (M2 profile) with Matplotlib.

To run an example:

```bash
python examples/01_channel_design.py
```

## Documentation

- [docs/USAGE.md](docs/USAGE.md) - Comprehensive usage documentation
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - Detailed engineering examples and walk-throughs


## Running Tests

```bash
pytest open_channel/tests/ -v
```

## Dependencies

- Python 3.8+
- NumPy >= 1.20.0
- SciPy >= 1.7.0

## License

MIT License - see LICENSE file for details.
