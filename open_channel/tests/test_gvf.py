"""
Tests for Gradually Varied Flow (GVF) calculations.
"""

import pytest

from open_channel.channels import RectangularChannel
from open_channel.flow.gvf import direct_step_method, standard_step_method


class TestDirectStepMethod:
    """Tests for direct_step_method function."""

    def test_basic_calculation(self):
        """Test basic direct step calculation."""
        channel = RectangularChannel(b=3.0)
        dx = direct_step_method(
            channel,
            y1=1.0,
            y2=1.2,
            Q=10.0,
            n=0.015,
            s0=0.001,
        )
        # Distance should be positive (downstream)
        assert dx != 0

    def test_symmetric_depths(self):
        """Test that swapping depths gives opposite distance."""
        channel = RectangularChannel(b=3.0)
        dx1 = direct_step_method(
            channel, y1=1.0, y2=1.2, Q=10.0, n=0.015, s0=0.001
        )
        dx2 = direct_step_method(
            channel, y1=1.2, y2=1.0, Q=10.0, n=0.015, s0=0.001
        )
        assert dx1 == pytest.approx(-dx2, rel=0.01)

    def test_invalid_discharge(self):
        """Test that invalid discharge raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            direct_step_method(
                channel, y1=1.0, y2=1.2, Q=0, n=0.015, s0=0.001
            )

    def test_invalid_manning_n(self):
        """Test that invalid Manning's n raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            direct_step_method(
                channel, y1=1.0, y2=1.2, Q=10.0, n=0, s0=0.001
            )

    def test_invalid_slope(self):
        """Test that invalid slope raises error."""
        channel = RectangularChannel(b=3.0)
        with pytest.raises(ValueError):
            direct_step_method(
                channel, y1=1.0, y2=1.2, Q=10.0, n=0.015, s0=0
            )


class TestStandardStepMethod:
    """Tests for standard_step_method function."""

    def test_basic_calculation(self):
        """Test basic standard step calculation using known direct step result."""
        channel = RectangularChannel(b=3.0)
        
        # First use direct step to find a distance for known depth change
        y1, y2_expected = 1.0, 1.05
        dx = direct_step_method(
            channel, y1=y1, y2=y2_expected, Q=5.0, n=0.015, s0=0.001
        )
        
        # Now use standard step to find depth at that distance
        y2 = standard_step_method(
            channel,
            x_start=0,
            y_start=y1,
            x_target=dx,
            Q=5.0,
            n=0.015,
            s0=0.001,
        )
        assert y2 == pytest.approx(y2_expected, rel=0.01)

    def test_zero_distance(self):
        """Test that zero distance returns starting depth."""
        channel = RectangularChannel(b=3.0)
        y2 = standard_step_method(
            channel,
            x_start=0,
            y_start=1.5,
            x_target=0,
            Q=10.0,
            n=0.015,
            s0=0.001,
        )
        assert y2 == pytest.approx(1.5, rel=0.01)

    def test_consistency_with_direct_step(self):
        """Test that standard step is consistent with direct step."""
        channel = RectangularChannel(b=3.0)
        
        # Use direct step to find distance between two depths
        y1, y2 = 1.0, 1.1
        dx = direct_step_method(
            channel, y1=y1, y2=y2, Q=10.0, n=0.015, s0=0.001
        )
        
        # Use standard step to find depth at that distance
        y2_calc = standard_step_method(
            channel,
            x_start=0,
            y_start=y1,
            x_target=dx,
            Q=10.0,
            n=0.015,
            s0=0.001,
        )
        
        # Should get approximately the same depth
        assert y2_calc == pytest.approx(y2, rel=0.05)

    def test_invalid_inputs(self):
        """Test that invalid inputs raise errors."""
        channel = RectangularChannel(b=3.0)
        
        with pytest.raises(ValueError):
            standard_step_method(
                channel, x_start=0, y_start=1.0, x_target=100,
                Q=0, n=0.015, s0=0.001
            )
