%cd Power-Grid-Forecasting
import pandas as pd
import pytest
import numpy as np
import pytest

from src.outage_analyzer import OutageAnalyzer

class TestOutageAnalyzer:
    """
    Test class for OutageAnalyzer
    """

    def setup_method(self):
        """
        Initialize the tests for DataLoader class
        """

        # use existing paths from the data directory
        grid_file = "data/generated/live_grid_load.csv"
        weather_file = "data/raw/Weather data for Hudson station.csv"
        outages_file = "data/raw/project_electrical_outages.csv"

        self.outage_analyzer = DataLoader(grid_file, weather_file, outages_file)

    def teardown_method(self):
        """
        Clean up after tests
        """
        del self.outage_analyzer



