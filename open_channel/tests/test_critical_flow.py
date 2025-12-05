"""
Tests for critical flow calculations.
"""

import pytest

from open_channel.channels import RectangularChannel, TrapezoidalChannel
from open_channel.flow.critical import (
    calculate_froude,
    solve_critical_depth,
    solve_alternate_depths,
    _specific_energy,
)
from open_channel.config import UnitSystem, get_constants


class TestCalculateFroude:
    """Tests for calculate_froude function."""

    def test_subcritical_flow(self):
        """Test Froude number for subcritical flow (Fr < 1)."""
        channel = RectangularChannel(b=3.0)
        # Deep, slow flow should be subcritical
        Fr = calculate_froude(channel, y=2.0, Q=5.0)
        assert Fr < 1

    def test_supercritical_flow(self):
        """Test Froude number for supercritical flow (Fr > 1)."""
        channel = RectangularChannel(b=3.0)
        # Shallow, fast flow should be supercritical
        Fr = calculate_froude(channel, y=0.3, Q=10.0)
        assert Fr > 1

    def test_critical_flow_at_critical_depth(self):
        """Test that Fr ≈ 1 at critical depth."""
        channel = RectangularChannel(b=3.0)
        Q = 10.0
        y_c = solve_critical_depth(channel, Q=Q)
        Fr = calculate_froude(channel, y=y_c, Q=Q)
        assert Fr == pytest.approx(1.0, rel=0.001)

    def test_invalid_discharge(self):
        """Test that invalid discharge raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            calculate_froude(channel, y=1.0, Q=0)
        with pytest.raises(ValueError):
            calculate_froude(channel, y=1.0, Q=-5.0)


class TestSolveCriticalDepth:
    """Tests for solve_critical_depth function."""

    def test_rectangular_channel(self):
        """Test critical depth for rectangular channel."""
        channel = RectangularChannel(b=3.0)
        Q = 10.0
        
        # For rectangular channel: y_c = (Q²/(g*b²))^(1/3)
        g = get_constants(UnitSystem.SI).g
        y_c_expected = (Q**2 / (g * channel.b**2)) ** (1/3)
        
        y_c = solve_critical_depth(channel, Q=Q)
        assert y_c == pytest.approx(y_c_expected, rel=0.001)

    def test_trapezoidal_channel(self):
        """Test critical depth for trapezoidal channel."""
        channel = TrapezoidalChannel(b=2.0, z=1.0)
        Q = 15.0
        y_c = solve_critical_depth(channel, Q=Q)
        
        # Verify Fr ≈ 1 at this depth
        Fr = calculate_froude(channel, y=y_c, Q=Q)
        assert Fr == pytest.approx(1.0, rel=0.001)

    def test_invalid_discharge(self):
        """Test that invalid discharge raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_critical_depth(channel, Q=0)


class TestSolveAlternateDepths:
    """Tests for solve_alternate_depths function."""

    def test_rectangular_channel(self):
        """Test alternate depths for rectangular channel."""
        channel = RectangularChannel(b=3.0)
        Q = 10.0
        
        # First get critical depth
        y_c = solve_critical_depth(channel, Q=Q)
        
        # Calculate specific energy at a subcritical depth
        g = get_constants(UnitSystem.SI).g
        y_sub = y_c * 1.5  # Subcritical depth
        E = _specific_energy(channel, y_sub, Q, g)
        
        # Find alternate depths
        y_supercritical, y_subcritical = solve_alternate_depths(channel, E=E, Q=Q)
        
        # Supercritical depth should be less than critical
        assert y_supercritical < y_c
        # Subcritical depth should be greater than critical
        assert y_subcritical > y_c
        
        # Both depths should have the same specific energy
        E_sup = _specific_energy(channel, y_supercritical, Q, g)
        E_sub = _specific_energy(channel, y_subcritical, Q, g)
        assert E_sup == pytest.approx(E, rel=0.001)
        assert E_sub == pytest.approx(E, rel=0.001)

    def test_invalid_energy(self):
        """Test that invalid energy raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_alternate_depths(channel, E=0, Q=10.0)
        with pytest.raises(ValueError):
            solve_alternate_depths(channel, E=-1.0, Q=10.0)

    def test_invalid_discharge(self):
        """Test that invalid discharge raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_alternate_depths(channel, E=2.0, Q=0)
