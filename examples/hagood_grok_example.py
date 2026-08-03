import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import requests
import joblib
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIG ====================
# Replace with real API endpoints or file paths
DATA_SOURCES = {
    'historical_weather': 'https://example.com/api/weather/historical.csv',
    'historical_outages': 'https://example.com/api/outages/past.csv',
    'historical_load': 'https://example.com/api/load/historical.csv',
    'forecast_weather': 'https://example.com/api/weather/forecast.csv',  # 10-day
}

MODEL_PATH = 'outage_predictor_model.pkl'
PREDICTION_DAYS = 10
# ===============================================

def fetch_data(url):
    """Fetch CSV from online source."""
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(pd.compat.StringIO(response.text))

def load_all_data():
    """Load and merge historical data."""
    weather_hist = fetch_data(DATA_SOURCES['historical_weather'])
    outages = fetch_data(DATA_SOURCES['historical_outages'])
    load_hist = fetch_data(DATA_SOURCES['historical_load'])
    
    # Standardize datetime columns
    for df in [weather_hist, outages, load_hist]:
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        elif 'date' in df.columns:
            df['timestamp'] = pd.to_datetime(df['date'])
    
    # Merge on timestamp (resample to hourly or daily as needed)
    merged = weather_hist.merge(load_hist, on='timestamp', how='left')
    # Aggregate outages to same granularity (e.g., daily count + total duration)
    outages_daily = outages.resample('D', on='timestamp').agg({
        'duration': 'sum',           # total outage minutes/hours
        'outage_id': 'count'         # number of outages
    }).rename(columns={'outage_id': 'outage_count'}).reset_index()
    
    merged = merged.merge(outages_daily, on='timestamp', how='left').fillna(0)
    merged['date'] = merged['timestamp'].dt.date
    return merged

def engineer_features(df):
    """Create useful features for outage prediction."""
    df = df.copy()
    
    # Weather extremes
    df['high_wind'] = (df['wind_speed'] > 40).astype(int)  # mph example threshold
    df['heavy_precip'] = (df['precipitation'] > 0.5).astype(int)  # inches
    df['extreme_temp'] = ((df['temperature'] > 95) | (df['temperature'] < 20)).astype(int)
    
    # Load features
    df['high_load'] = (df['grid_load'] > df['grid_load'].quantile(0.85)).astype(int)
    
    # Temporal features
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Lagged features (previous day outages, etc.)
    df = df.sort_values('timestamp')
    df['outage_count_lag1'] = df['outage_count'].shift(1)
    df['duration_lag1'] = df['duration'].shift(1)
    
    # Rolling statistics
    df['outage_rolling_7d'] = df['outage_count'].rolling(7).mean()
    
    return df.dropna()  # or handle NaNs more gracefully

def train_model(data):
    """Train a simple model to predict outage count/duration."""
    features = [
        'temperature', 'precipitation', 'wind_speed',
        'grid_load', 'high_wind', 'heavy_precip', 'extreme_temp', 'high_load',
        'day_of_week', 'month', 'is_weekend',
        'outage_count_lag1', 'duration_lag1', 'outage_rolling_7d'
    ]
    
    X = data[features]
    y_count = data['outage_count']      # Predict number of outages
    # y_duration = data['duration']     # Could also model duration separately
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_count, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Quick evaluation
    print("Model R² score:", model.score(X_test_scaled, y_test))
    
    # Save model + scaler
    joblib.dump({'model': model, 'scaler': scaler, 'features': features}, MODEL_PATH)
    return model, scaler, features

def make_forecast():
    """Load forecast and predict outages."""
    forecast = fetch_data(DATA_SOURCES['forecast_weather'])
    forecast['timestamp'] = pd.to_datetime(forecast['timestamp'])
    
    # You'd also need forecast load (or assume/estimate it)
    # For simplicity, reuse recent average load or fetch if available
    recent_load = fetch_data(DATA_SOURCES['historical_load']).tail(24)['grid_load'].mean()
    forecast['grid_load'] = recent_load  # placeholder
    
    # Engineer same features as training
    forecast = engineer_features(forecast)  # Note: lags will be tricky; use last known values
    
    # Load model
    saved = joblib.load(MODEL_PATH)
    model = saved['model']
    scaler = saved['scaler']
    features = saved['features']
    
    X_forecast = forecast[features]
    X_scaled = scaler.transform(X_forecast)
    
    forecast['predicted_outage_count'] = model.predict(X_scaled).round(1)
    forecast['predicted_duration_hours'] = forecast['predicted_outage_count'] * 2.5  # rough estimate
    
    return forecast[['timestamp', 'temperature', 'precipitation', 'wind_speed',
                     'predicted_outage_count', 'predicted_duration_hours']]

def main():
    print("Loading historical data...")
    historical = load_all_data()
    historical = engineer_features(historical)
    
    print("Training model...")
    train_model(historical)
    
    print("Generating 10-day forecast...")
    predictions = make_forecast()
    
    print("\n=== Power Outage Predictions ===")
    print(predictions.to_string(index=False))
    
    # Optional: save to CSV for dashboard
    predictions.to_csv('outage_forecast.csv', index=False)

if __name__ == "__main__":
    main()
