import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ----------------------------
# 1. Load online data tables
# ----------------------------

weather_past = pd.read_csv("https://example.com/past_weather.csv")
outages = pd.read_csv("https://example.com/past_outages.csv")
load_past = pd.read_csv("https://example.com/past_grid_load.csv")
weather_forecast = pd.read_csv("https://example.com/forecast_weather.csv")
load_current = pd.read_csv("https://example.com/current_grid_load.csv")

# Expected columns:
# weather: timestamp, temperature, precipitation, wind_speed
# outages: timestamp, duration_minutes
# load: timestamp, grid_load_mw

# ----------------------------
# 2. Clean timestamps
# ----------------------------

for df in [weather_past, outages, load_past, weather_forecast, load_current]:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# Round to hourly buckets
weather_past["timestamp"] = weather_past["timestamp"].dt.floor("h")
outages["timestamp"] = outages["timestamp"].dt.floor("h")
load_past["timestamp"] = load_past["timestamp"].dt.floor("h")
weather_forecast["timestamp"] = weather_forecast["timestamp"].dt.floor("h")
load_current["timestamp"] = load_current["timestamp"].dt.floor("h")

# ----------------------------
# 3. Build training table
# ----------------------------

data = weather_past.merge(load_past, on="timestamp", how="inner")

# Label: did an outage occur during this hour?
outages["outage"] = 1
outage_labels = outages[["timestamp", "outage"]]

data = data.merge(outage_labels, on="timestamp", how="left")
data["outage"] = data["outage"].fillna(0)

# ----------------------------
# 4. Add useful features
# ----------------------------

data["hour"] = data["timestamp"].dt.hour
data["day_of_week"] = data["timestamp"].dt.dayofweek
data["month"] = data["timestamp"].dt.month

data["high_wind"] = (data["wind_speed"] > 35).astype(int)
data["heavy_rain"] = (data["precipitation"] > 0.5).astype(int)
data["extreme_temp"] = (
    (data["temperature"] < 10) | 
    (data["temperature"] > 95)
).astype(int)

features = [
    "temperature",
    "precipitation",
    "wind_speed",
    "grid_load_mw",
    "hour",
    "day_of_week",
    "month",
    "high_wind",
    "heavy_rain",
    "extreme_temp"
]

X = data[features]
y = data["outage"]

# ----------------------------
# 5. Train model
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, shuffle=False
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
print(classification_report(y_test, preds))

# ----------------------------
# 6. Prepare 10-day forecast
# ----------------------------

# Simple assumption:
# use the latest grid load as a baseline for future grid load.
latest_load = load_current.sort_values("timestamp").iloc[-1]["grid_load_mw"]

future = weather_forecast.copy()
future["grid_load_mw"] = latest_load

future["hour"] = future["timestamp"].dt.hour
future["day_of_week"] = future["timestamp"].dt.dayofweek
future["month"] = future["timestamp"].dt.month

future["high_wind"] = (future["wind_speed"] > 35).astype(int)
future["heavy_rain"] = (future["precipitation"] > 0.5).astype(int)
future["extreme_temp"] = (
    (future["temperature"] < 10) | 
    (future["temperature"] > 95)
).astype(int)

# ----------------------------
# 7. Predict outage risk
# ----------------------------

future["outage_probability"] = model.predict_proba(future[features])[:, 1]

def risk_label(prob):
    if prob >= 0.60:
        return "High"
    elif prob >= 0.30:
        return "Medium"
    else:
        return "Low"

future["risk"] = future["outage_probability"].apply(risk_label)

# ----------------------------
# 8. Output forecast
# ----------------------------

result = future[[
    "timestamp",
    "temperature",
    "precipitation",
    "wind_speed",
    "grid_load_mw",
    "outage_probability",
    "risk"
]]

print(result.to_string(index=False))
