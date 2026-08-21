"""Minimal pytest scaffold for the power-grid project."""

import pytest

from src.power_station import PowerStation


@pytest.fixture
def station():
    """Return a small PowerStation instance for tests."""
    return PowerStation(
        "Test Station",
        latitude=40.728,
        longitude=-74.078,
        rated_capacity=85,
    )


def test_power_station_stub(station):
    """Verify that the test framework and project imports work."""
    assert station.name == "Test Station"
    assert station.rated_capacity == 85
