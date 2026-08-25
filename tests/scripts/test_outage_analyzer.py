import pandas as pd
import pytest
import numpy as np
import pytest

from outage_analyzer import OutageAnalyzer

class TestOutageAnalyzer:
    """
    Test class for OutageAnalyzer
    """

    def setup_method(self):
        """
        Initialize the tests for OutageAnalyzer class
        """

        #create a test dataFrame with 2 columns: hour and month
        df = pd.DataFrame({
            "start_time": pd.to_datetime([
                "2026-01-01 00:00",
                "2026-01-01 02:00",
                "2026-01-01 04:00",
                "2026-01-01 06:00",

                "2026-04-01 00:00",
                "2026-04-01 06:00",
                "2026-04-01 12:00",
                "2026-04-01 18:00",

                "2026-07-01 06:00",
                "2026-07-01 08:00",
                "2026-07-01 12:00",
                "2026-07-01 18:00",

                "2026-10-01 06:00",
                "2026-10-01 12:00",
                "2026-10-01 18:00",
                "2026-10-02 06:00"
            ])
        })
        self.outage_analyzer = OutageAnalyzer(df)


    def teardown_method(self):
        """
        Clean up after tests
        """

    def test_unique_outage_days(self):
        """Test that repeated events on a date count as one outage day."""
        outage_days = self.outage_analyzer.unique_outage_days()

        assert isinstance(outage_days, set)
        assert len(outage_days) == 5
        assert pd.Timestamp("2026-10-02").date() in outage_days

    def test_string_and_length_overloads(self):
        """Test the readable summary and outage-event count."""
        assert len(self.outage_analyzer) == 16
        assert str(self.outage_analyzer) == (
            "16 outage events across 5 affected days"
        )

    def test_compute_outage_probability(self):
        """
        Test the compute_outage_probability method
        """

        # Test for occurences of 6:00. They should occur 5 out of 16 total times
        prob_hour_6 = self.outage_analyzer.compute_outage_probability(pd.Timestamp("06:00"))
        assert prob_hour_6 == 0.3125

        # Test for occurences of 12:00. They should occur 3 out of 16 total times
        prob_hour_12 = self.outage_analyzer.compute_outage_probability(pd.Timestamp("12:00"))
        assert prob_hour_12 == 0.1875

        # Test for occurences of 18:00. They should occur 3 out of 16 total times
        prob_hour_18 = self.outage_analyzer.compute_outage_probability(pd.Timestamp("18:00"))
        assert prob_hour_18 == 0.1875

        # Test for occurences of 0:00. They should occur 2 out of 16 total times
        prob_hour_0 = self.outage_analyzer.compute_outage_probability(pd.Timestamp("00:00"))
        assert prob_hour_0 == 0.125

        # Test for occurences of 03:00. They should occur 0 out of 16 total times
        prob_hour_3 = self.outage_analyzer.compute_outage_probability(pd.Timestamp("03:00"))
        assert prob_hour_3 == 0.0


    def test_recent_outages(self):
        """
        Test the recent_outages method
        """

        # Return all occurences from 00:00 to 06:00 on Jan 1.  
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-01-01 06:00"), 6)
        assert len(recent_outages) == 4

        # Return all occurences from 8:00 to 12:00 on Apr 1.
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-04-01 12:00"), 4)
        assert len(recent_outages) == 1

        # Return all occurences from 6:00 to 12:00 on Jul 1.
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-07-01 12:00"), 6)
        assert len(recent_outages) == 3

        # Return all occurences from 6:00 to 12:00 on Oct 1.
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-10-01 12:00"), 6)
        assert len(recent_outages) == 2

        # try a window of 0
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-10-01 12:00"), 0)
        assert len(recent_outages) == 1

        # try a window size of the last 2 days from Oct 1, 2026.
        recent_outages = self.outage_analyzer.recent_outages(pd.Timestamp("2026-10-03 0:00"), 48)
        assert len(recent_outages) == 4


