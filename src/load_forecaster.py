"""
Implements simple short-term forecasting: rolling mean and seasonal weighting.
Module name: load_forecaster.py
"""
import pandas as pd

from utils import runtime_logger

class LoadForecaster:
    def __init__(self, merged_df: pd.DataFrame):
        self.df = merged_df.copy()
        self.df = self.df.sort_values('Timestamp')

    @runtime_logger
    def prepare_features(self):
        self.df['hour'] = self.df['Timestamp'].dt.hour
        self.df['weekday'] = self.df['Timestamp'].dt.weekday
        return self.df

    @runtime_logger
    def forecast_next_hour(self):
        """
        Uses last N load values for rolling average forecasting.
        """
        recent = self.df['Load_Percent'].tail(6)  # last ~1 hour of 10-minute data
        return recent.mean()

    @runtime_logger
    def forecast_next_24h(self):
        """
        Projects next 24 hours based on mean of each hour of day historically.
        """
        self.df['hour'] = self.df['Timestamp'].dt.hour
        hour_profile = self.df.groupby('hour')['Load_Percent'].mean()

        forecast = []
        for h in range(24):
            forecast.append(hour_profile.get(h, hour_profile.mean()))

        return pd.Series(forecast)
