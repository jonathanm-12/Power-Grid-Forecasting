"""Test template for :mod:`src.data_loader`.

Suggested coverage:

* ``DataLoader.__init__`` accepts existing paths and rejects missing files.
* ``load_grid_data`` parses timestamps and removes rows with invalid timestamps.
* ``_parse_noaa_numeric`` handles valid values, missing-value sentinels, and
  malformed or non-string input.
* ``load_weather_data`` parses NOAA fields and supplies missing output columns.
* ``load_outage_data`` parses start times and removes invalid rows.
* ``merge_all`` aligns grid and weather observations and adds outage details.

Use pytest's ``tmp_path`` fixture to create small, isolated CSV inputs. Add
shared fixtures below if several tests need the same sample datasets.
"""

# Future imports could include:
#
# import pandas as pd
# import pytest
#
# from src.data_loader import DataLoader

import pandas as pd
import pytest
import numpy as np

from src.data_loader import DataLoader

class TestDataLoader:
    """
    Test class for DataLoader
    """

    def setup_method(self):
        """
        Initialize the tests for DataLoader class
        """
  
        # use existing paths from the data directory
        grid_file = "data/generated/live_grid_load.csv"
        weather_file = "data/raw/weather_hudson_station.csv"
        outages_file = "data/raw/project_electrical_outages.csv"

        self.data_loader = DataLoader(grid_file, weather_file, outages_file)

    def teardown_method(self):
        """
        Clean up after tests
        """
        del self.data_loader


    def test_init_path_exists(self):
        """
        Test that DataLoader initializes correctly with random, non-existing paths.
        """

        # validate that a "FileNotFoundError" is raised when the paths do not exist
        with pytest.raises(FileNotFoundError):
            DataLoader("non_existing_grid.csv", "non_existing_weather.csv", "non_existing_outage.csv")



    def test_load_grid_data(self):
        """
        Test that load_grid_data correctly loads and cleans the grid data.
        """

        df = self.data_loader.load_grid_data()

        # ensure timestamp col exists
        assert "Timestamp" in df.columns

        # ensure no null values
        assert df['Timestamp'].notnull().all()  

    def test_parse_noaa_numeric(self):
        """
        Test that _parse_noaa_numeric correctly parses NOAA numeric values.
        """

        # valid value
        assert self.data_loader._parse_noaa_numeric("+0001,1") == 0.1

        # valid value 2
        assert self.data_loader._parse_noaa_numeric("4569,9") == 456.9

        # missing val in cell
        assert self.data_loader._parse_noaa_numeric("94567,9") is np.nan

        # malformed input
        assert self.data_loader._parse_noaa_numeric("invalid") is np.nan

        # non-string input
        assert self.data_loader._parse_noaa_numeric(12345) is np.nan

# Add fixtures here.


# Add tests here.
