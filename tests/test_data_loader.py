import pandas as pd
import pytest
import numpy as np
import pytest

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
        weather_file = "data/raw/Weather data for Hudson station.csv"
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

    def test_load_weather_data(self):
        """
        Test that load_weather_data correctly loads and cleans the weather data.
        """
        df = self.data_loader.load_weather_data()

        # Ensure 4 columns exist: DATE, temperature_C, dewpoint_C, pressure_hPa
        assert "DATE" in df.columns
        assert "temperature_C" in df.columns
        assert "dewpoint_C" in df.columns
        assert "pressure_hPa" in df.columns

        #test that temp, dewpoint, and pressure are numeric using pandas api.types.is_numeric_dtype
        # for more information, see https://pandas.pydata.org/docs/reference/api/pandas.api.types.is_numeric_dtype.html
        assert pd.api.types.is_numeric_dtype(df['temperature_C'])
        assert pd.api.types.is_numeric_dtype(df['dewpoint_C'])
        assert pd.api.types.is_numeric_dtype(df['pressure_hPa'])

        # Ensure column size of 4
        assert len(df.columns) == 4


    def test_load_outages_data(self):
        """
        Test that load_outages_data correctly loads and cleans the outages data.
        """
        df = self.data_loader.load_outage_data()

        # Verify start_time column exists and uses the correct datetime format
        assert "start_time" in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['start_time'])

        #ensure no null values in start_time
        assert df['start_time'].notnull().all()

    def test_merge_all(self):
        """
        Test that merge_all correctly merges the grid, weather, and outage data.
        """
        merged_df = self.data_loader.merge_all()

         # Expected merged columns
        assert "Timestamp" in merged_df.columns
        assert "temperature_C" in merged_df.columns
        assert "dewpoint_C" in merged_df.columns
        assert "pressure_hPa" in merged_df.columns
        assert "nearest_outage_customers" in merged_df.columns
        assert "nearest_outage_duration" in merged_df.columns

        # Weather timestamp should be removed
        assert "DATE" not in merged_df.columns

        # timestamps should not contain any null values
        assert merged_df["Timestamp"].notnull().all()

        # "monotonic increasing" means that timestamps are sorted correctly with no duplicates
        assert merged_df["Timestamp"].is_monotonic_increasing

        # outage values should be populated and nonnegative
        assert merged_df["nearest_outage_customers"].notnull().all()
        assert (merged_df["nearest_outage_customers"] >= 0).all()

        assert merged_df["nearest_outage_duration"].notnull().all()
        assert (merged_df["nearest_outage_duration"] >= 0).all()


