import pandas as pd
import pytest

from load_forecaster import LoadForecaster
from data_loader import DataLoader

class TestLoadForecaster:
    """Test class for LoadForecaster."""

    def setup_method(self):
        """
        Set up a LoadForecaster instance for testing.
        """

        # initialize a random dataframe that uses certain load percentages beginning at Jan 1
        self.test_df = pd.DataFrame({
            "Timestamp": pd.date_range(
                "2026-01-01",
                periods=8,
                freq="10min",
            ),
            "Load_Percent": [10, 20, 30, 40, 50, 60, 70, 80],
        })

        self.load_forecaster = LoadForecaster(self.test_df)

    def teardown_method(self):
        """Clean up after each test."""
        del self.load_forecaster
        del self.test_df


    def test_prepare_features(self):
        """
        Test the prepare_features method of LoadForecaster.
        """

        df =   self.load_forecaster.prepare_features()

       # verify that 2 separate cols are made for Hour and Weekday
        assert 'hour' in self.load_forecaster.df.columns
        assert 'weekday' in self.load_forecaster.df.columns

        # # verify that the Hour column contains values between 0 and 23
        assert self.load_forecaster.df['hour'].between(0, 23).all()

        # verify that the Weekday column contains values between 0 and 6
        assert self.load_forecaster.df['weekday'].between(0, 6).all()

    def test_forecast_next_hour(self):
        """
        Test the forecast_next_hour method of LoadForecaster.
        """

        next_hour_forecast = self.load_forecaster.forecast_next_hour()

        # Verify that the mean calculates to the last approx hour of 10-min data
        assert sum(self.test_df['Load_Percent'][-6:]) / 6 == next_hour_forecast

    def test_forecast_next_24h(self):
        """
        Test the forecast_next_24h method of LoadForecaster.
        """

        forecast = self.load_forecaster.forecast_next_24h()

        hour_zero_avg = (self.test_df['Load_Percent'][:6]).mean()
        hour_one_avg = (self.test_df['Load_Percent'][6:]).mean()

        # average for missing data
        fallback_avg = (hour_zero_avg + hour_one_avg) / 2

        expected = pd.Series(
            [hour_zero_avg, hour_one_avg] + [fallback_avg] * 22
        )

        assert forecast.equals(expected)



