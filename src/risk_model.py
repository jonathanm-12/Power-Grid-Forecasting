"""
Estimates risk from load, outage probability, and weather.
Module name: risk_model.py
"""

class RiskModel:
    """Estimate outage risk for a specific power station."""

    def __init__(self, station):
        """Create a risk model composed with a PowerStation instance."""
        self.station = station

    def compute_risk_score(self, load_percent, outage_prob, temperature):
        """
        Weighted scoring model.
        """

        # load is determined as a percentage of the station's rated capacity
        load_factor = load_percent / self.station.rated_capacity

        # normalize temperature to a 0-1 scale (assuming 40 degrees Celsius as a high-risk threshold)
        temp_factor = temperature / 40.0 if temperature is not None else 0.0

        # risk is a weighted sum of load, outage probability, and temperature factors
        risk = 0.6 * load_factor + 0.25 * outage_prob + 0.15 * temp_factor
        return risk

    def classify(self, score):
        """
        Assess risk score and label it as Low, Moderate, High, or Critical.
        """
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        elif score < 0.85:
            return "High"
        return "Critical"
