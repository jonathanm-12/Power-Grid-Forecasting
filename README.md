# **Power Grid Load Forecasting and Outage Risk Analyzer**

##### **AAI/CPE/EE 551 Course Project**

## **Project Overview**

Electric power grids must continuously balance electricity supply and demand. Changes in electricity usage, extreme weather, equipment limitations, and other conditions can place additional stress on the grid and increase the possibility of service interruptions.

This project develops a Python-based Power Grid Load Forecasting and Outage Risk Analyzer focused on the Hudson County, New Jersey area. The program combines electrical load, historical outage, and weather information to explore relationships between grid demand and outage risk.

The project currently includes tools to:

- Simulate live electrical grid load for the Hoboken area.

- Load and clean weather, outage, and grid-load datasets.

- Merge time-based observations from multiple datasets.

- Calculate short-term electrical-load forecasts.

- Examine historical outage patterns.

- Estimate an outage-risk score.

- Classify estimated risk into meaningful categories.

- Provide reusable Python classes and utility functions for analysis.

This project was developed for the AAI/CPE/EE 551 course at Stevens Institute of Technology.

## **Team**

|**Team Member**|**Email**|**Stevens ID**|
|---|---|---|
|LarryHagood|lhagood@stevens.edu|20027091|
|Jonathan Mikalov|jmikalov@stevens.edu|20030528|
|Daniela Montoya|dmontoya@stevens.edu|20038486|

### **Main Contributions**

Complete this section before the final submission with each team member's primary contributions.

|**Team Member**|**Main Contributions**|
|---|---|
|Larry Hagood| Processed CSV datasets, integrated analysis workflow, generated grid load simulator. |
|Jonathan Mikalov| Established a framework for unit tests and focused on repo cleanup and readability.|
|Daniela Montoya| Developed risk model and forecasting architecture.|

## **Project Design**

The project separates the major parts of the analysis into individual Python modules. This makes each component easier to understand, test, and modify independently.

Overall workflow:

```text
Historical Weather Data ─────┐
Historical Outage Data ──────┼──> Data Loading / Cleaning
Simulated Grid Load ─────────┘              |
                                            v
                                      Merged Dataset
                                            |
                       ┌────────────────────┴────────────────────┐
                       v                                         v
                Load Forecasting                         Outage Analysis
                       |                                         |
                       └────────────────────┬────────────────────┘
                                            v
                                       Risk Model
                                            |
                                            v
                                Risk Score / Classification
```

The current implementation uses a combination of object-oriented programming, data processing, simulation, forecasting, generators, conditionals, loops, and file input/output.


## **Data**

### **Historical Weather Data**

The included weather dataset contains hourly observations from The Battery, New York, a nearby weather station used to represent conditions around the initial Hudson County study area. Some fields use compact NOAA-style representations and missing-value codes, so the raw values require preprocessing before analysis.

### **Historical Electrical Outage Data**

The included outage dataset contains historical outage information for Hudson County, New Jersey. The data is used to examine outage timing, duration, and affected customers.

### **Simulated Grid Load Data**

`GridLoadSimulator.py` generates a synthetic live dataset so the rest of the program can operate on a consistent stream of load observations. The generated file is `live_grid_load.csv`.

## **Data Sources**

- [Event-Correlated Outage Dataset in America](https://catalog.data.gov/dataset/event-correlated-outage-dataset-in-america) — historical electrical outage data published through Data.gov

- [NOAA Integrated Surface Database](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database) — global hourly weather observations from land-based stations

### **Additional Sources Investigated**

- U.S. Energy Information Administration (EIA) Hourly Electric Grid Monitor

- NOAA Global Historical Climatology Network Hourly

- NOAA Storm Events Database

- U.S. Census TIGER/Line geographic boundaries


## **Installation**

### **Windows**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas numpy jupyter ipykernel matplotlib pytest
```

### **macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pandas numpy jupyter ipykernel matplotlib pytest
```

TODO before final submission: Create a `requirements.txt` containing the exact package versions used by the completed project. Once it exists, installation can use:

```bash
python -m pip install -r requirements.txt
```

## **Running the Project**

### **Run the Complete Analysis**

```bash
jupyter notebook src/main.ipynb
```

Open `main.ipynb` and select **Run All**. The notebook imports the project modules, loads the included datasets, calculates the next-hour forecast and outage risk, and displays the results and visualizations.

### **1. Start the Grid Load Simulator**

```bash
python GridLoadSimulator.py
```

The simulator writes a new observation to `live_grid_load.csv` every 10 seconds. Leave it running long enough to collect the amount of data needed for the desired analysis, then press `Ctrl+C`.

### **2. Confirm the Input Data**

- `live_grid_load.csv`

- `Weather data for Hudson station.csv`

- `Project electrical outages data.csv`

### **3. Load and Merge the Data**

```python
from data_loader import DataLoader

loader = DataLoader(
    "live_grid_load.csv",
    "Weather data for Hudson station.csv",
    "Project electrical outages data.csv"
)

merged = loader.merge_all()
```

### **4. Forecast Load**

```python
from load_forecaster import LoadForecaster

forecaster = LoadForecaster(merged)
forecast_hour = forecaster.forecast_next_hour()
```

### **5. Analyze Outage History**

```python
from outage_analyzer import OutageAnalyzer

outages = loader.load_outage_data()
analyzer = OutageAnalyzer(outages)
outage_probability = analyzer.compute_outage_probability(
    merged["Timestamp"].iloc[-1]
)
```

### **6. Estimate Risk**

```python
from risk_model import RiskModel
from power_station import PowerStation

station = PowerStation(
    "Hudson Substation", 40.728, -74.078, rated_capacity=85
)
risk_model = RiskModel(station)
risk_score = risk_model.compute_risk_score(
    forecast_hour, outage_probability, merged["temperature_C"].iloc[-1]
)
risk_level = risk_model.classify(risk_score)
```

## **Example Output**

During an integrated development test, the modules successfully produced values for the next-hour forecast, historical outage probability, risk score, and risk classification. An example run produced:

```text
Next-hour forecast: 68.71
Outage probability: 0.0375
Risk score: 0.4921 => Moderate
```

Because grid-load simulation includes random variation, results will not necessarily be identical between runs.

## **Course Requirement Traceability**

### **Python**

The project is intended for a modern Python 3 environment. Python 3.12 is the recommended baseline.

### **Part 1**

|**#**|**Requirement**|**Current Project Evidence**|
|---:|---|---|
|1|Two meaningful related classes|`RiskModel` is composed with a `PowerStation`: its constructor stores the station instance and uses the station's rated capacity when calculating risk. Both classes have constructors, attributes, methods, and instances in `main.ipynb`. This relationship currently depends on retaining `PowerStation`.|
|2|Two meaningful functions|`plot_load_over_time()`, `plot_outages_by_month()`, and `plot_risk_over_time()` directly communicate load, outage, and risk results. They currently reside in `main.ipynb`; move them to a `.py` visualization module if the course requires every helper function to be imported by the notebook.|
|3|Two advanced libraries|Pandas performs CSV loading, datetime processing, grouping, and dataset merging; NumPy represents missing numeric values; Matplotlib produces the three project visualizations.|
|4|Two exception scenarios and Pytest tests|`DataLoader` raises `FileNotFoundError` for missing inputs, while `_parse_noaa_numeric()` handles malformed NOAA values by returning `np.nan`. The verified suite contains 16 passing tests.|
|5|Meaningful data I/O|`DataLoader` reads grid-load, weather, and electrical-outage CSV files and converts them into analysis-ready DataFrames.|
|6|Two loops and two conditionals|`DataLoader.merge_all()` uses a `for` loop and a `while` loop. File validation, NOAA parsing, outage probability, and risk classification provide multiple `if` statements.|
|7|Mutable and immutable types|Forecast values use a mutable list and unique outage dates use a mutable set. File paths and labels use immutable strings, while capacities, probabilities, and risk scores use immutable numbers.|
|8|`__str__()` and another overload|`OutageAnalyzer.__str__()` returns a readable outage summary and `OutageAnalyzer.__len__()` returns the event count. `PowerStation` additionally defines `__str__()` and `__lt__()`.|
|9|Docstrings, headers, and comments|Modules contain descriptive headers and many functions have docstrings and comments, but class or constructor docstrings are still missing from `LoadForecaster`, `OutageAnalyzer`, and `DataLoader.__init__()`.|
|10|`__name__` behavior|`main.ipynb` remains the main program and uses `if __name__ == "__main__":` before displaying its visualizations.|

### **Part 2**

The project currently demonstrates four of the selectable Python features:

|**Component**|**Current Project Evidence**|
|---|---|
|List comprehension|`LoadForecaster.forecast_next_24h()` constructs its 24-hour forecast with a list comprehension.|
|Built-in module/library|`DataLoader` uses the standard-library `os` module to validate input paths before loading data.|
|Set operation|`OutageAnalyzer.unique_outage_days()` creates a set of distinct dates containing outages.|
|Linear data structure|The 24-hour forecast and station load history use Python lists, which are dynamic-array linear data structures.|

## **Testing**

The repository currently contains 16 passing Pytest tests:

|**Test Area**|**Tests**|**Coverage**|
|---|---:|---|
|`DataLoader`|6|Path validation, grid loading, NOAA parsing, weather loading, outage loading, and merged-data integrity.|
|`LoadForecaster`|3|Feature preparation, next-hour forecasting, and the 24-hour forecast profile.|
|`OutageAnalyzer`|4|Unique outage days, `__str__()` and `__len__()`, hourly outage probability, and recent-outage windows.|
|`RiskModel`|3|Composition with `PowerStation`, weighted risk-score calculations, and all four classification levels.|
|**Total**|**16**|All tests pass in the current environment.|

Run the complete suite from the repository's `src` directory so the dataset paths used by the tests resolve correctly:

```bash
cd src
python -m pytest -v ../tests/scripts
```

## **Future Improvements**

- Replace simulated grid load with an appropriate real-world regional load feed.

- Incorporate weather forecasts for future risk estimation.

- Develop more advanced machine-learning forecasting models.

- Evaluate model accuracy against held-out historical data.

- Add additional weather variables and severe-weather information.

- Improve temporal matching between outage and weather observations.

- Account for outage duration and number of affected customers.

- Develop an interactive county or regional risk map.

- Support additional locations outside Hudson County.

- Create a user interface for selecting a location and viewing forecasts.
