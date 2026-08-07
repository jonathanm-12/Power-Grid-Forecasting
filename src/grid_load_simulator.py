"""
Module name: GridLoadSimulator.py
Generates simulated grid load data and outputs it to a CSV file.

Output file:
    live_grid_load.csv

Columns produced:
    Timestamp
    Load_Percent
    Temperature_C
    Season
    Day_Type
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate_grid_load(
    start="2024-01-01 00:00",
    periods=24*30,  # 30 days hourly data
    freq="h",
):
    # Create timestamps
    timestamps = pd.date_range(start=start, periods=periods, freq=freq)

    # Seasonal temperature patterns
    temps = []
    loads = []

    for ts in timestamps:
        # Basic seasonal temperature pattern
        month = ts.month
        if month in [12, 1, 2]:  # Winter
            base_temp = np.random.normal(0, 5)
        elif month in [3, 4, 5]:  # Spring
            base_temp = np.random.normal(10, 5)
        elif month in [6, 7, 8]:  # Summer
            base_temp = np.random.normal(27, 4)
        else:  # Fall
            base_temp = np.random.normal(14, 5)

        # Hourly variations in load
        hour = ts.hour
        if 0 <= hour <= 6:
            base_load = np.random.normal(40, 5)
        elif 7 <= hour <= 15:
            base_load = np.random.normal(55, 7)
        elif 16 <= hour <= 21:
            base_load = np.random.normal(75, 8)
        else:
            base_load = np.random.normal(55, 5)

        # Temperature influence on load:
        temp_factor = base_temp * 0.25
        final_load = max(0, min(100, base_load + temp_factor))

        temps.append(base_temp)
        loads.append(final_load)

    # Determine season label
    def season_of(ts):
        m = ts.month
        if m in [12, 1, 2]: return "Winter"
        if m in [3, 4, 5]: return "Spring"
        if m in [6, 7, 8]: return "Summer"
        return "Fall"

    # Determine weekday/weekend label
    def day_type(ts):
        return "Weekend" if ts.weekday() >= 5 else "Weekday"

    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Load_Percent": loads,
        "Temperature_C": temps,
        "Season": [season_of(ts) for ts in timestamps],
        "Day_Type": [day_type(ts) for ts in timestamps],
    })

    return df

def generate_csv(output_path="live_grid_load.csv"):
    df = simulate_grid_load()
    df.to_csv(output_path, index=False)
    print(f"Grid load CSV successfully created: {output_path}")

if __name__ == "__main__":
    generate_csv()
  
from GridLoadSimulator import generate_csv
generate_csv()
