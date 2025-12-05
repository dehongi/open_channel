"""
Tests for channel geometry classes.
"""

import math
import pytest

from open_channel.channels import (
    RectangularChannel,
    TrapezoidalChannel,
    TriangularChannel,
    CircularChannel,
)


class TestRectangularChannel:
    """Tests for RectangularChannel."""

    def test_init_valid(self):
        """Test valid initialization."""
        channel = RectangularChannel(b=3.0)
        assert channel.b == 3.0

    def test_init_invalid_width(self):
        """Test that negative width raises error."""
        with pytest.raises(ValueError):
            RectangularChannel(b=-1.0)
        with pytest.raises(ValueError):
            RectangularChannel(b=0)

    def test_area(self):
        """Test area calculation: A = b * y."""
        channel = RectangularChannel(b=2.0)
        assert channel.area(y=1.0) == pytest.approx(2.0)
        assert channel.area(y=3.0) == pytest.approx(6.0)

    def test_wetted_perimeter(self):
        """Test wetted perimeter: P = b + 2y."""
        channel = RectangularChannel(b=2.0)
        assert channel.wetted_perimeter(y=1.0) == pytest.approx(4.0)
        assert channel.wetted_perimeter(y=2.0) == pytest.approx(6.0)

    def test_top_width(self):
        """Test top width: T = b."""
        channel = RectangularChannel(b=3.0)
        assert channel.top_width(y=1.0) == pytest.approx(3.0)
        assert channel.top_width(y=5.0) == pytest.approx(3.0)

    def test_hydraulic_radius(self):
        """Test hydraulic radius: R = A / P."""
        channel = RectangularChannel(b=2.0)
        # R = 2 / 4 = 0.5
        assert channel.hydraulic_radius(y=1.0) == pytest.approx(0.5)

    def test_hydraulic_depth(self):
        """Test hydraulic depth: Dh = A / T = y for rectangular."""
        channel = RectangularChannel(b=2.0)
        assert channel.hydraulic_depth(y=1.0) == pytest.approx(1.0)
        assert channel.hydraulic_depth(y=2.5) == pytest.approx(2.5)

    def test_negative_depth_raises(self):
        """Test that negative depth raises error."""
        channel = RectangularChannel(b=2.0)
        with pytest.raises(ValueError):
            channel.area(y=-1.0)


class TestTrapezoidalChannel:
    """Tests for TrapezoidalChannel."""

    def test_init_valid(self):
        """Test valid initialization."""
        channel = TrapezoidalChannel(b=2.0, z=1.5)
        assert channel.b == 2.0
        assert channel.z == 1.5

    def test_init_invalid(self):
        """Test invalid initialization."""
        with pytest.raises(ValueError):
            TrapezoidalChannel(b=-1.0, z=1.0)
        with pytest.raises(ValueError):
            TrapezoidalChannel(b=2.0, z=-1.0)

    def test_area(self):
        """Test area: A = (b + z*y) * y."""
        channel = TrapezoidalChannel(b=2.0, z=1.0)
        # A = (2 + 1*1) * 1 = 3
        assert channel.area(y=1.0) == pytest.approx(3.0)
        # A = (2 + 1*2) * 2 = 8
        assert channel.area(y=2.0) == pytest.approx(8.0)

    def test_wetted_perimeter(self):
        """Test wetted perimeter: P = b + 2y * sqrt(1 + z²)."""
        channel = TrapezoidalChannel(b=2.0, z=1.0)
        # P = 2 + 2*1 * sqrt(2) = 2 + 2*sqrt(2)
        expected = 2.0 + 2.0 * math.sqrt(2)
        assert channel.wetted_perimeter(y=1.0) == pytest.approx(expected)

    def test_top_width(self):
        """Test top width: T = b + 2zy."""
        channel = TrapezoidalChannel(b=2.0, z=1.0)
        # T = 2 + 2*1*1 = 4
        assert channel.top_width(y=1.0) == pytest.approx(4.0)


class TestTriangularChannel:
    """Tests for TriangularChannel."""

    def test_init_valid(self):
        """Test valid initialization."""
        channel = TriangularChannel(z=2.0)
        assert channel.z == 2.0

    def test_init_invalid(self):
        """Test invalid initialization."""
        with pytest.raises(ValueError):
            TriangularChannel(z=0)
        with pytest.raises(ValueError):
            TriangularChannel(z=-1.0)

    def test_area(self):
        """Test area: A = z * y²."""
        channel = TriangularChannel(z=2.0)
        # A = 2 * 1² = 2
        assert channel.area(y=1.0) == pytest.approx(2.0)
        # A = 2 * 3² = 18
        assert channel.area(y=3.0) == pytest.approx(18.0)

    def test_wetted_perimeter(self):
        """Test wetted perimeter: P = 2y * sqrt(1 + z²)."""
        channel = TriangularChannel(z=2.0)
        # P = 2*1 * sqrt(1 + 4) = 2 * sqrt(5)
        expected = 2.0 * math.sqrt(5)
        assert channel.wetted_perimeter(y=1.0) == pytest.approx(expected)

    def test_top_width(self):
        """Test top width: T = 2zy."""
        channel = TriangularChannel(z=2.0)
        # T = 2*2*1 = 4
        assert channel.top_width(y=1.0) == pytest.approx(4.0)


class TestCircularChannel:
    """Tests for CircularChannel."""

    def test_init_valid(self):
        """Test valid initialization."""
        channel = CircularChannel(D=2.0)
        assert channel.D == 2.0

    def test_init_invalid(self):
        """Test invalid initialization."""
        with pytest.raises(ValueError):
            CircularChannel(D=0)
        with pytest.raises(ValueError):
            CircularChannel(D=-1.0)

    def test_half_full_area(self):
        """Test area at half-full: A = πD²/8."""
        channel = CircularChannel(D=2.0)
        # At y = D/2 = 1.0, θ = π, A = D²/8 * (π - 0) = π/2
        expected = math.pi / 2
        assert channel.area(y=1.0) == pytest.approx(expected)

    def test_half_full_perimeter(self):
        """Test perimeter at half-full: P = πD/2."""
        channel = CircularChannel(D=2.0)
        # At y = D/2, θ = π, P = πD/2 = π
        expected = math.pi
        assert channel.wetted_perimeter(y=1.0) == pytest.approx(expected)

    def test_half_full_top_width(self):
        """Test top width at half-full: T = D."""
        channel = CircularChannel(D=2.0)
        # At y = D/2, θ = π, T = D * sin(π/2) = D = 2
        assert channel.top_width(y=1.0) == pytest.approx(2.0)

    def test_depth_exceeds_diameter_raises(self):
        """Test that depth > diameter raises error."""
        channel = CircularChannel(D=1.0)
        with pytest.raises(ValueError):
            channel.area(y=1.5)

    def test_full_pipe(self):
        """Test calculations at full pipe (y = D)."""
        channel = CircularChannel(D=2.0)
        # θ = 2π, A = D²/8 * (2π - 0) = πD²/4 = π
        expected_area = math.pi
        assert channel.area(y=2.0) == pytest.approx(expected_area)
