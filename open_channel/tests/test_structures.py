"""
Tests for hydraulic structures calculations.
"""

import math
import pytest

from open_channel.channels import RectangularChannel, TrapezoidalChannel
from open_channel.structures.hydraulic_jump import solve_conjugate_depth
from open_channel.structures.weirs import (
    rectangular_weir_discharge,
    vnotch_weir_discharge,
)


class TestHydraulicJump:
    """Tests for hydraulic jump calculations."""

    def test_basic_conjugate_depth(self):
        """Test basic conjugate depth calculation."""
        channel = RectangularChannel(b=3.0)
        y1 = 0.5
        Fr1 = 3.0  # Supercritical flow
        
        y2, delta_E = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
        
        # y2 should be greater than y1 (subcritical)
        assert y2 > y1
        # Energy loss should be positive
        assert delta_E > 0

    def test_conjugate_depth_formula(self):
        """Test that conjugate depth follows known formula."""
        channel = RectangularChannel(b=3.0)
        y1 = 0.4
        Fr1 = 4.0
        
        # Known formula: y2/y1 = 0.5 * (sqrt(1 + 8*Fr1²) - 1)
        y2_expected = y1 * 0.5 * (math.sqrt(1 + 8 * Fr1**2) - 1)
        
        y2, _ = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
        assert y2 == pytest.approx(y2_expected, rel=0.001)

    def test_energy_loss_formula(self):
        """Test that energy loss follows known formula."""
        channel = RectangularChannel(b=3.0)
        y1 = 0.5
        Fr1 = 2.5
        
        y2, delta_E = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
        
        # Known formula: ΔE = (y2 - y1)³ / (4*y1*y2)
        delta_E_expected = (y2 - y1)**3 / (4 * y1 * y2)
        assert delta_E == pytest.approx(delta_E_expected, rel=0.001)

    def test_subcritical_froude_raises(self):
        """Test that Fr ≤ 1 raises error (no jump possible)."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_conjugate_depth(channel, y1=1.0, Fr1=0.8)
        with pytest.raises(ValueError):
            solve_conjugate_depth(channel, y1=1.0, Fr1=1.0)

    def test_non_rectangular_raises(self):
        """Test that non-rectangular channel raises error."""
        channel = TrapezoidalChannel(b=3.0, z=1.0)
        with pytest.raises(TypeError):
            solve_conjugate_depth(channel, y1=0.5, Fr1=3.0)

    def test_invalid_depth_raises(self):
        """Test that invalid depth raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            solve_conjugate_depth(channel, y1=0, Fr1=3.0)
        with pytest.raises(ValueError):
            solve_conjugate_depth(channel, y1=-0.5, Fr1=3.0)


class TestRectangularWeir:
    """Tests for rectangular weir discharge."""

    def test_basic_discharge(self):
        """Test basic discharge calculation."""
        Q = rectangular_weir_discharge(Cd=1.84, L=2.0, H=0.5)
        # Q = 1.84 * 2.0 * 0.5^1.5 = 1.84 * 2.0 * 0.3536 ≈ 1.30
        assert Q == pytest.approx(1.301, rel=0.01)

    def test_discharge_scales_with_length(self):
        """Test that discharge scales linearly with length."""
        Q1 = rectangular_weir_discharge(Cd=1.84, L=1.0, H=0.5)
        Q2 = rectangular_weir_discharge(Cd=1.84, L=2.0, H=0.5)
        assert Q2 == pytest.approx(2 * Q1, rel=0.001)

    def test_discharge_scales_with_head(self):
        """Test that discharge scales with H^1.5."""
        Q1 = rectangular_weir_discharge(Cd=1.84, L=2.0, H=1.0)
        Q2 = rectangular_weir_discharge(Cd=1.84, L=2.0, H=2.0)
        # Q2/Q1 = (2/1)^1.5 = 2.828
        assert Q2 / Q1 == pytest.approx(2**1.5, rel=0.001)

    def test_invalid_inputs(self):
        """Test that invalid inputs raise errors."""
        with pytest.raises(ValueError):
            rectangular_weir_discharge(Cd=0, L=2.0, H=0.5)
        with pytest.raises(ValueError):
            rectangular_weir_discharge(Cd=1.84, L=0, H=0.5)
        with pytest.raises(ValueError):
            rectangular_weir_discharge(Cd=1.84, L=2.0, H=0)


class TestVNotchWeir:
    """Tests for V-notch weir discharge."""

    def test_90_degree_notch(self):
        """Test 90-degree V-notch weir."""
        theta = math.pi / 2  # 90 degrees
        Q = vnotch_weir_discharge(Cd=1.38, theta=theta, H=0.3)
        # Q = 1.38 * tan(45°) * 0.3^2.5 = 1.38 * 1.0 * 0.0493 ≈ 0.068
        expected = 1.38 * math.tan(theta/2) * 0.3**2.5
        assert Q == pytest.approx(expected, rel=0.001)

    def test_discharge_scales_with_head(self):
        """Test that discharge scales with H^2.5."""
        theta = math.pi / 2
        Q1 = vnotch_weir_discharge(Cd=1.38, theta=theta, H=1.0)
        Q2 = vnotch_weir_discharge(Cd=1.38, theta=theta, H=2.0)
        # Q2/Q1 = (2/1)^2.5 = 5.657
        assert Q2 / Q1 == pytest.approx(2**2.5, rel=0.001)

    def test_invalid_angle(self):
        """Test that invalid angle raises error."""
        with pytest.raises(ValueError):
            vnotch_weir_discharge(Cd=1.38, theta=0, H=0.3)
        with pytest.raises(ValueError):
            vnotch_weir_discharge(Cd=1.38, theta=math.pi + 0.1, H=0.3)

    def test_invalid_inputs(self):
        """Test that invalid inputs raise errors."""
        with pytest.raises(ValueError):
            vnotch_weir_discharge(Cd=0, theta=math.pi/2, H=0.3)
        with pytest.raises(ValueError):
            vnotch_weir_discharge(Cd=1.38, theta=math.pi/2, H=0)
