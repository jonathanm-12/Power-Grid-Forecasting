
import pandas as pd
import pytest
import numpy as np

from src.risk_model import RiskModel
from src.power_station import PowerStation

class TestRiskModel:
    """
    Test class for RiskModel
    """

    def setup_method(self):
        """
        Initialize the tests for DataLoader class
        """

        self.station = PowerStation(
            "Test Station",
            latitude=40.728,
            longitude=-74.078,
            rated_capacity=85,
        )
        self.risk_model = RiskModel(self.station)


    def teardown_method(self):
        """
        Clean up after tests
        """

    def test_uses_power_station_composition(self):
        """Verify that RiskModel retains its PowerStation instance."""
        assert self.risk_model.station is self.station


    def test_compute_risk_score(self):
        """
        Test compute_risk_score with several combinations.
        """
        capacity = self.station.rated_capacity

        # Typical operating conditions
        score = self.risk_model.compute_risk_score(
            load_percent=80,
            outage_prob=0.4,
            temperature=40,
        )
        expected = (
            0.6 * (80 / capacity)
            + 0.25 * 0.4
            + 0.15 * (40 / 40)
        )
        assert score == expected

        # All inputs are zero
        score = self.risk_model.compute_risk_score(
            load_percent=0,
            outage_prob=0,
            temperature=0,
        )
        assert score == 0.0

        #  using existing capacirtyt
        score = self.risk_model.compute_risk_score(
            load_percent=capacity,
            outage_prob=1.0,
            temperature=40,
        )
        assert score == 1.0

        # Missing temperature should not change the risk
        score = self.risk_model.compute_risk_score(
            load_percent=42.5,
            outage_prob=0.2,
            temperature=None,
        )
        expected = (
            0.6 * (42.5 / capacity)
            + 0.25 * 0.2
        )
        assert score == expected

    def test_classify(self):
        """
        Test classify method with several combinations.
        """

        # Low risk
        score = 0.2
        classification = self.risk_model.classify(score)
        assert classification == "Low"

        # Medium risk
        score = 0.5
        classification = self.risk_model.classify(score)
        assert classification == "Moderate"

        # High risk
        score = 0.8
        classification = self.risk_model.classify(score)
        assert classification == "High"

        # Critical risk
        score = 0.95
        classification = self.risk_model.classify(score)
        assert classification == "Critical"
