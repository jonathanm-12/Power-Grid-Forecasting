"""
Computes outage frequency patterns, basic probabilities, and severity scores.
Module name: outage_analyzer.py
"""
import pandas as pd
import numpy as np

class OutageAnalyzer:
    def __init__(self, outage_df: pd.DataFrame):
        self.outages = outage_df.copy()
        self.outages['hour'] = self.outages['start_time'].dt.hour
        self.outages['month'] = self.outages['start_time'].dt.month

    def outages_by_season(self):
        return self.outages.groupby('month').size()

    def compute_outage_probability(self, timestamp):
        """
        Probability = (# of outages at same hour)/total outages
        """
        hour = timestamp.hour
        total = len(self.outages)
        occ = len(self.outages[self.outages['hour'] == hour])
        return occ / total if total > 0 else 0.0

    def recent_outages(self, timestamp, window_hours=6):
        """
        Returns outages in the last X hours.
        """
        start = timestamp - pd.Timedelta(hours=window_hours)
        return self.outages[(self.outages['start_time'] >= start) &
                            (self.outages['start_time'] <= timestamp)]
