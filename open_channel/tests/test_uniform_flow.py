"""
Tests for uniform flow (Manning's equation) calculations.
"""

import pytest

from open_channel.channels import RectangularChannel, TrapezoidalChannel
from open_channel.flow.uniform import solve_discharge, solve_normal_depth
from open_channel.config import UnitSystem


class TestSolveDischarge:
    """Tests for solve_discharge function."""

    def test_rectangular_channel_si(self):
        """Test discharge calculation for rectangular channel (SI)."""
        channel = RectangularChannel(b=3.0)
        # Q = (1/n) * A * R^(2/3) * S^(1/2)
        # A = 3 * 1 = 3, P = 3 + 2 = 5, R = 3/5 = 0.6
        # Q = (1/0.015) * 3 * 0.6^(2/3) * 0.001^0.5
        Q = solve_discharge(channel, y=1.0, n=0.015, s=0.001)
        assert Q > 0
        assert Q == pytest.approx(4.479, rel=0.01)

    def test_trapezoidal_channel_si(self):
        """Test discharge calculation for trapezoidal channel (SI)."""
        channel = TrapezoidalChannel(b=2.0, z=1.0)
        Q = solve_discharge(channel, y=1.0, n=0.020, s=0.0005)
        assert Q > 0

    def test_english_units(self):
        """Test discharge calculation with English units."""
        channel = RectangularChannel(b=10.0)  # 10 ft wide
        Q_si = solve_discharge(channel, y=3.0, n=0.015, s=0.001, unit_system=UnitSystem.SI)
        Q_eng = solve_discharge(channel, y=3.0, n=0.015, s=0.001, unit_system=UnitSystem.ENGLISH)
        # English system should give higher discharge (k = 1.486 vs 1.0)
        assert Q_eng > Q_si
        assert Q_eng / Q_si == pytest.approx(1.486, rel=0.01)

    def test_invalid_manning_n(self):
        """Test that invalid Manning's n raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_discharge(channel, y=1.0, n=0, s=0.001)
        with pytest.raises(ValueError):
            solve_discharge(channel, y=1.0, n=-0.015, s=0.001)

    def test_invalid_slope(self):
        """Test that invalid slope raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_discharge(channel, y=1.0, n=0.015, s=0)
        with pytest.raises(ValueError):
            solve_discharge(channel, y=1.0, n=0.015, s=-0.001)


class TestSolveNormalDepth:
    """Tests for solve_normal_depth function."""

    def test_rectangular_channel(self):
        """Test normal depth solver for rectangular channel."""
        channel = RectangularChannel(b=3.0)
        
        # First calculate discharge at known depth
        y_known = 1.5
        Q = solve_discharge(channel, y=y_known, n=0.015, s=0.001)
        
        # Now solve for normal depth - should get back the same depth
        y_n = solve_normal_depth(channel, Q=Q, n=0.015, s=0.001)
        assert y_n == pytest.approx(y_known, rel=0.001)

    def test_trapezoidal_channel(self):
        """Test normal depth solver for trapezoidal channel."""
        channel = TrapezoidalChannel(b=2.0, z=1.5)
        
        y_known = 2.0
        Q = solve_discharge(channel, y=y_known, n=0.020, s=0.0005)
        y_n = solve_normal_depth(channel, Q=Q, n=0.020, s=0.0005)
        assert y_n == pytest.approx(y_known, rel=0.001)

    def test_invalid_discharge(self):
        """Test that invalid discharge raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_normal_depth(channel, Q=0, n=0.015, s=0.001)
        with pytest.raises(ValueError):
            solve_normal_depth(channel, Q=-10, n=0.015, s=0.001)

    def test_custom_bounds(self):
        """Test solver with custom depth bounds."""
        channel = RectangularChannel(b=3.0)
        Q = 50.0  # Large discharge requires deeper depth
        y_n = solve_normal_depth(channel, Q=Q, n=0.015, s=0.001, y_min=0.1, y_max=50.0)
        assert y_n > 0
