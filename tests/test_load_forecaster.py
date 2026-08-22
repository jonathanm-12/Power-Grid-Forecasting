%cd Power-Grid-Forecasting
import pandas as pd
import pytest

from src.load_forecaster import LoadForecaster


class TestLoadForecaster:
    """Test class for LoadForecaster."""

    def setup_method(self):
        """Initialize a LoadForecaster with sample load data."""

    def teardown_method(self):
        """Clean up after each test."""
        del self.load_forecaster
