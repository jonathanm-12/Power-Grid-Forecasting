"""
Module responsible for loading, cleaning and merginf all project datasets:
-Grid load data
-Weather Data
-Electrical outages
Module name: data_loader.py
"""
import pandas as pd
from datetime import datetime
import numpy as np
import os

class DataLoader:
  """
  Handles reading CSV files, cleaning raw values, and merging datasets.
  """
  def __init__(self, grid_path: str, weather_path: str, outage_path: str):
        # return Exception if path doesnt exist
        if not os.path.exists(grid_path):
            raise FileNotFoundError(f"Grid data file not found: {grid_path}")
        if not os.path.exists(weather_path):
            raise FileNotFoundError(f"Weather data file not found: {weather_path}")
        if not os.path.exists(outage_path):
            raise FileNotFoundError(f"Outage data file not found: {outage_path}")      

        self.grid_path = grid_path
        self.weather_path = weather_path
        self.outage_path = outage_path
  
  # Grid Load
  def load_grid_data(self):
    """
    Load the simulated grid data.
    """
    df = pd.read_csv(self.grid_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])
    return df

  # Weather Data Cleaning
  def _parse_noaa_numeric(self, val: str):
        """
        Extract the numeric portion for values like '+0001,1' or '99999,9'.      
        """
        if isinstance(val, str):
            try:
                raw = val.split(',')[0].replace('+', '')
                num = int(raw)
                if num > 9000:  # missing value indicator
                    return np.nan
                return num / 10.0  #TMP often stored as tenths of degrees C
            except:
                return np.nan
        return np.nan

  def load_weather_data(self) -> pd.DataFrame:
        """
        Load weather data and convert key fields.
        """
        df = pd.read_csv(self.weather_path)
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df = df.dropna(subset=['DATE'])

        # Parse temperature
        if 'TMP' in df.columns:
            df['temperature_C'] = df['TMP'].apply(self._parse_noaa_numeric)
        else:
            df['temperature_C'] = np.nan

        # Parse dew point
        if 'DEW' in df.columns:
            df['dewpoint_C'] = df['DEW'].apply(self._parse_noaa_numeric)
        else:
            df['dewpoint_C'] = np.nan

        # Parse sea-level pressure
        if 'SLP (Sea Level Pressure)' in df.columns:
            df['pressure_hPa'] = df['SLP (Sea Level Pressure)'].apply(self._parse_noaa_numeric)
        else:
            df['pressure_hPa'] = np.nan

        return df[['DATE', 'temperature_C', 'dewpoint_C', 'pressure_hPa']]

  # Electrical Outage Data
  def load_outage_data(self):
    """
    Load historic electrical outage data for Hudson County.
    """
    df = pd.read_csv(self.outage_path)
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
    df = df.dropna(subset=['start_time'])
    return df
    
  # Merging  
  def merge_all(self):
    """
    Merge grid, weather and outage data.
    """
    grid = self.load_grid_data().sort_values('Timestamp')
    weather = self.load_weather_data().sort_values('DATE')
    merged = pd.merge_asof(
            grid,
            weather,
            left_on='Timestamp',
            right_on='DATE',
            direction='nearest'
        )

    merged.drop(columns=['DATE'], inplace=True)

    # Add simple outage indicator based on nearest outage events
    outages = self.load_outage_data()
    outages = outages.sort_values('start_time')

    merged['nearest_outage_customers'] = 0
    merged['nearest_outage_duration'] = 0.0

    idx = 0
    for i, row in merged.iterrows():
        ts = row['Timestamp']
        # Find closest outage in history
        while idx + 1 < len(outages) and outages.iloc[idx + 1]['start_time'] < ts:
             idx += 1
        outage = outages.iloc[idx]
        merged.at[i, 'nearest_outage_customers'] = outage['mean_customers']
        merged.at[i, 'nearest_outage_duration'] = outage['duration']

    return merged
