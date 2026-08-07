"""
power_station.py
Represents a Hudson County power station with load history and capacity.
"""
class PowerStation:
    def __init__(self, name: str, latitude: float, longitude: float, rated_capacity: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.rated_capacity = rated_capacity
        self.load_history = []

    def add_load(self, load_percent: float):
        self.load_history.append(load_percent)

    def compute_average_load(self):
        if not self.load_history:
            return 0.0
        return sum(self.load_history) / len(self.load_history)

    def compute_peak_load(self):
        return max(self.load_history) if self.load_history else 0.0

    def __str__(self):
        return f"{self.name} @({self.latitude},{self.longitude}) capacity={self.rated_capacity}%"

    def __lt__(self, other):
        return self.rated_capacity < other.rated_capacity
