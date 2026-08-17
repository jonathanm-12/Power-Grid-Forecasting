from pathlib import Path

from data_loader import DataLoader
from power_station import PowerStation
from load_forecaster import LoadForecaster
from outage_analyzer import OutageAnalyzer
from risk_model import RiskModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent

loader = DataLoader(
    PROJECT_ROOT / "live_grid_load.csv",
    PROJECT_ROOT / "data" / "raw" / "weather_hudson_station.csv",
    PROJECT_ROOT / "data" / "raw" / "project_electrical_outages.csv"
)

merged = loader.merge_all()

station = PowerStation(
    "Hudson Substation",
    40.728,
    -74.078,
    rated_capacity=85
)

station.load_history = merged['Load_Percent'].tolist()

forecaster = LoadForecaster(merged)
forecast_hour = forecaster.forecast_next_hour()

outages = loader.load_outage_data()
out_analyzer = OutageAnalyzer(outages)
out_prob = out_analyzer.compute_outage_probability(
    merged['Timestamp'].iloc[-1]
)

risk_engine = RiskModel(station.rated_capacity)

risk_score = risk_engine.compute_risk_score(
    forecast_hour,
    out_prob,
    merged['temperature_C'].iloc[-1]
)

risk_level = risk_engine.classify(risk_score)

print("Next-hour forecast:", forecast_hour)
print("Outage probability:", out_prob)
print("Risk score:", risk_score, "=>", risk_level)
