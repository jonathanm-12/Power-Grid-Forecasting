"""
Estimates risk from load, outage probability, and weather.
Module name: risk_model.py
"""

class RiskModel:
    def __init__(self, station_capacity: float):
        self.capacity = station_capacity

    def compute_risk_score(self, load_percent, outage_prob, temperature):
        """
        Weighted scoring model. Adjust freely.
        """
        load_factor = load_percent / self.capacity
        temp_factor = temperature / 40.0 if temperature is not None else 0.0
        risk = 0.6 * load_factor + 0.25 * outage_prob + 0.15 * temp_factor
        return risk

    def classify(self, score):
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        elif score < 0.85:
            return "High"
        return "Critical"