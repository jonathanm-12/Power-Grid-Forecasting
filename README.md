# **Power Grid Load Forecasting and Outage Risk Analyzer** 

##### **AAI/CPE/EE 551 Course Project** 

## **Project Overview** 

Electric power grids must continuously balance electricity supply and demand. Changes in electricity usage, extreme weather, equipment limitations, and other conditions can place additional stress on the grid and increase the possibility of service interruptions. 

This project develops a Python-based Power Grid Load Forecasting and Outage Risk Analyzer focused on the Hoboken and Hudson County, New Jersey area. The program combines electrical load, historical outage, and weather information to explore relationships between grid demand and outage risk. 

The project currently includes tools to: 

- simulate live electrical grid load for the Hoboken area; 

- load and clean weather, outage, and grid-load datasets;  merge time-based observations from multiple datasets;  calculate short-term electrical-load forecasts;  examine historical outage patterns;  estimate an outage-risk score;  classify estimated risk into meaningful categories; and  provide reusable Python classes and utility functions for analysis. 

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
|Larry Hagood|TODO: Add completed modules, analyses, testing,<br>and documentation contributions.|
|Jonathan Mikalov|TODO: Add completed modules, analyses, testing,<br>and documentation contributions.|
|Daniela Montoya|TODO: Add completed modules, analyses, testing,<br>and documentation contributions.|



Power Grid Load Forecasting and Outage Risk Analyzer 

## **Project Design** 

The project separates the major parts of the analysis into individual Python modules. This makes each component easier to understand, test, and modify independently. 

Overall workflow: 



<!-- Start of picture text -->
Historical Weather Data ─────┐<br>Historical Outage Data ──────┼──> Data Loading / Cleaning<br>Simulated Grid Load ─────────┘             |<br>                                           v<br>                                     Merged Dataset<br>                                           |<br>┌────────────────────┴────────────────────┐<br>                      v                                         v<br>               Load Forecasting                         Outage Analysis<br>                      |                                         |<br>└────────────────────┬────────────────────┘<br>                                           v<br>                                      Risk Model<br>                                           |<br>                                           v<br>                               Risk Score / Classification<br><!-- End of picture text -->

The current implementation uses a combination of object-oriented programming, data processing, simulation, forecasting, generators, conditionals, loops, and file input/output. 

## **Project Components** 

### **Grid Load Simulator** 

GridLoadSimulator.py simulates live electrical demand for the Hoboken, New Jersey area. Rather than requiring access to a utility company's real-time operational grid, the simulator creates synthetic load and temperature observations based on time of day, weekday versus weekend, season, simulated outdoor temperature, and small random variations. 

Simulated grid load is limited to approximately 25% to 85%. Weekday demand rises during the morning and generally reaches its highest level during the late afternoon and early evening. Weekend behavior is adjusted to produce a broader daytime demand period. Summer demand is increased to approximate additional airconditioning use, while winter demand is generally reduced. 

The simulator produces a new observation every 10 seconds with the following columns: 

Timestamp Load_Percent Temperature_C 

Power Grid Load Forecasting and Outage Risk Analyzer 

Season 

###### Day_Type 

The observations are written to live_grid_load.csv. The newest observation is stored first. The simulator retains up to 1,000 readings, representing approximately 2.8 hours of simulated history at the current update interval. Press Ctrl+C to stop it cleanly. 

##### **Important: Grid-load and temperature values produced by this module are synthetic. They should not be interpreted as real measurements from the Hoboken electrical grid.** 

### **Data Loader** 

data_loader.py contains the DataLoader class and is responsible for bringing the project's datasets into a common form for analysis. It accepts paths to grid-load data, weather data, and electrical-outage data. 

#### **Grid Data** 

Grid-load timestamps are converted into pandas datetime values. Records containing invalid timestamps are removed before further processing. 

#### **Weather Data** 

The weather dataset contains NOAA-style fields that require additional processing. The loader parses selected measurements including temperature, dew point, and sea-level pressure. Encoded or missing NOAA values are converted into values that can be handled during analysis. 

#### **Outage Data** 

Historical electrical-outage records are loaded from CSV and their outage start times are converted into datetime values. 

#### **Dataset Merging** 

The merge_all() method combines grid-load and weather observations using their timestamps. Historical outage information is then associated with the resulting data so that load, weather, and outage characteristics can be examined together. 

### **Power Station** 

power_station.py defines the PowerStation class. A station stores its name, latitude, longitude, rated capacity, and historical load values. The class can calculate average and peak load. 

- __str__() provides a readable description of the station. 

- __lt__() allows two PowerStation objects to be compared according to rated capacity. 

### **Load Forecaster** 

load_forecaster.py contains the LoadForecaster class, which performs basic short-term electrical-load forecasting. 

#### **Next-Hour Forecast** 

The next-hour forecast is calculated using the mean of the most recent load observations. 

Power Grid Load Forecasting and Outage Risk Analyzer 

#### **24-Hour Forecast** 

For longer forecasts, historical observations are grouped according to hour of day. The mean historical load for each hour is then used to construct a 24-hour load profile. This is a straightforward educational baseline rather than a production utility-demand forecasting model. 

### **Outage Analyzer** 

outage_analyzer.py defines the OutageAnalyzer class. It examines historical outage records and creates timebased information such as outage hour and month. 

- counting outages according to month; 

- calculating a simple historical outage probability for a particular hour; and 

- retrieving outages that occurred within a specified number of hours before a timestamp. 

The current probability calculation is intentionally simple: it calculates the fraction of historical outages occurring during the same hour of day as the requested timestamp. 

### **Risk Model** 

risk_model.py contains the RiskModel class. The model combines forecast electrical load, historical outage probability, and temperature. 

Risk = 

60% load factor + 25% outage probability 

+ 15% temperature factor 

|**Risk Score**|**Classifcation**|
|---|---|
|Less than 0.30|Low|
|0.30 to less than 0.60|Moderate|
|0.60 to less than 0.85|High|
|0.85 orgreater|Critical|



These thresholds are part of the project's current educational model and should not be interpreted as official utility-industry outage thresholds. 

### **Utility Functions** 

#### **Runtime Logger** 

runtime_logger is a decorator that measures how long a decorated function takes to execute. 

#### **Hourly Load Generator** 

hourly_load_generator() is a Python generator that yields grid-load records individually rather than returning another complete copy of the dataset. 

#### **Unique Outage Days** 

unique_outage_days() uses a Python set to obtain the unique dates represented in the historical outage dataset. 

Power Grid Load Forecasting and Outage Risk Analyzer 

## **Data** 

### **Historical Weather Data** 

The included weather dataset contains hourly observations from The Battery, New York, a nearby weather station used to represent conditions around the initial Hudson County study area. Some fields use compact NOAA-style representations and missing-value codes, so the raw values require preprocessing before analysis. 

### **Historical Electrical Outage Data** 

The included outage dataset contains historical outage information for Hudson County, New Jersey. The data is used to examine outage timing, duration, and affected customers. 

### **Simulated Grid Load Data** 

GridLoadSimulator.py generates a synthetic live dataset so the rest of the program can operate on a consistent stream of load observations. The generated file is live_grid_load.csv. 

## **Data Sources Investigated** 

- U.S. Energy Information Administration (EIA) Hourly Electric Grid Monitor 

- U.S. Department of Energy / Data.gov outage datasets 

- NOAA Integrated Surface Database 

- NOAA Global Historical Climatology Network Hourly 

- NOAA Storm Events Database 

- U.S. Census TIGER/Line geographic boundaries 

The Census geographic dataset was investigated as a possible basis for a selectable or color-coded regional outage-risk map. 

## **Requirements** 

### **Python** 

The project is intended for a modern Python 3 environment. Python 3.12 is the recommended baseline unless the team selects and documents another course-supported version. 

### **Python Packages** 

Current integrated-project dependencies include: 

pandas 

numpy 

Development and final-project components may also use: 

jupyter ipykernel matplotlib 

pytest 

Power Grid Load Forecasting and Outage Risk Analyzer 

## **Installation** 

### **Windows** 

py -3.12 -m venv .venv .venv\Scripts\Activate.ps1 python -m pip install --upgrade pip 

python -m pip install pandas numpy jupyter ipykernel matplotlib pytest 

### **macOS / Linux** 

python3.12 -m venv .venv source .venv/bin/activate python -m pip install --upgrade pip python -m pip install pandas numpy jupyter ipykernel matplotlib pytest 

TODO before final submission: Create a requirements.txt containing the exact package versions used by the completed project. Once it exists, installation can use: python -m pip install -r requirements.txt 

## **Running the Project** 

### **1. Start the Grid Load Simulator** 

python GridLoadSimulator.py 

The simulator writes a new observation to live_grid_load.csv every 10 seconds. Leave it running long enough to collect the amount of data needed for the desired analysis, then press Ctrl+C. 

### **2. Confirm the Input Data** 

live_grid_load.csv 

Weather data for Hudson station.csv 

Project electrical outages data.csv 

### **3. Load and Merge the Data** 

from data_loader import DataLoader 

loader = DataLoader( 

"live_grid_load.csv", 

"Weather data for Hudson station.csv", 

"Project electrical outages data.csv" 

) 

merged = loader.merge_all() 

### **4. Forecast Load** 

from load_forecaster import LoadForecaster 

Power Grid Load Forecasting and Outage Risk Analyzer 

forecaster = LoadForecaster(merged) 

forecast_hour = forecaster.forecast_next_hour() 

### **5. Analyze Outage History** 

from outage_analyzer import OutageAnalyzer 

outages = loader.load_outage_data() 

analyzer = OutageAnalyzer(outages) 

outage_probability = analyzer.compute_outage_probability( 

merged["Timestamp"].iloc[-1] 

) 

### **6. Estimate Risk** 

from risk_model import RiskModel 

risk_model = RiskModel(station_capacity=85) 

risk_score = risk_model.compute_risk_score( 

forecast_hour, outage_probability, merged["temperature_C"].iloc[-1] 

) risk_level = risk_model.classify(risk_score) 

## **Example Output** 

During an integrated development test, the modules successfully produced values for the next-hour forecast, historical outage probability, risk score, and risk classification. An example run produced: 

Next-hour forecast: 68.71 Outage probability: 0.0375 Risk score: 0.4921 => Moderate 

Because grid-load simulation includes random variation, results will not necessarily be identical between runs. 

## **Course Requirement Traceability** 

### **Part 1** 

|**Requirement**|**Current Project Evidence**|
|---|---|
||Multiple project classes including DataLoader,|
|Two meaningful related classes|PowerStation, LoadForecaster, OutageAnalyzer, and|
||RiskModel|
|Meaningful functions|Data loading, simulation, forecasting, outage<br>analysis,and risk calculations|



Power Grid Load Forecasting and Outage Risk Analyzer 

|Advanced libraries|pandas and NumPy<br>|
|---|---|
|Exception scenarios /pytest|TODO: Complete and document fnalpytest cases<br>|
|Data input/output|Multiple CSV fles are read; the simulator writes<br>live_grid_load.csv|
|Loops and conditionals|Grid simulation, dataset processing, forecasting,<br>season/time/load logic,and risk classifcation|
|Mutable and immutable types|Lists, sets, DataFrames, tuples, strings, and<br>numerical values|
|Operator overloading|PowerStation.__str__()and PowerStation.__lt__()|
|Documentation|Modules and major functions/classes include<br>documentation; perform fnal review|
|Main-module behavior|GridLoadSimulator.py uses if __name__ ==<br>'__main__':|



### **Part 2** 

|**Component**|**Current Project Evidence**|
|---|---|
|Comprehension|List comprehensions are used when constructing<br>project data|
|Built-in module/library|csv, math, random, datetime, pathlib, collections,<br>time, and functools are represented across project<br>modules|
|Generator|hourly_load_generator() yields individual load<br>records<br>|
|Special function|TODO: Verify fnal map(), zip(), flter(), lambda, or<br>reduce()implementation before submission|



## **Testing** 

Formal pytest coverage should be completed before final submission. Useful tests include: 

- valid grid-load data; 

- malformed or missing timestamps; 

- missing CSV files; 

- NOAA missing-value handling; 

- weather-value parsing; 

- empty station load history; 

- average and peak station load calculations; 

- forecast output; 

- empty outage datasets; 

- outage-probability calculations; 

- risk-score calculations; and 

- boundaries between Low, Moderate, High, and Critical classifications. 

python -m pytest -v 

## **Current Limitations** 

- Grid-load observations generated by GridLoadSimulator.py are synthetic. 

- The simulator does not connect to a live utility power grid. 

Power Grid Load Forecasting and Outage Risk Analyzer 

- The weather station used in the historical dataset is near Hudson County but is not physically located in Hoboken. 

- Historical correlation between weather, load, and outage events does not demonstrate causation. 

- The current forecasting methods are baseline statistical forecasts rather than trained utility forecasting models. 

- The outage probability model uses historical hour-of-day frequency and does not by itself predict whether an individual outage will occur. 

- The risk formula and classification thresholds are project-defined educational values rather than industrystandard utility thresholds. 

- Random variation in the simulator means results may differ between runs. 

- Rare outages can create significant class imbalance. 

- Results depend strongly on timestamp alignment, geographic compatibility, missing-value treatment, and source-data quality. 

The project's forecasts and risk classifications must not be used for emergency planning, infrastructure operation, or real-world utility decisions. 

## **Future Improvements** 

- replace simulated grid load with an appropriate real-world regional load feed; 

- incorporate weather forecasts for future risk estimation; 

- develop more advanced machine-learning forecasting models; 

- evaluate model accuracy against held-out historical data; 

- add additional weather variables and severe-weather information; 

- improve temporal matching between outage and weather observations; 

- account for outage duration and number of affected customers; 

- create visual load and outage-risk plots; 

- develop an interactive county or regional risk map; 

- support additional locations outside Hudson County; and 

- create a user interface for selecting a location and viewing forecasts. 

## **Final Submission Checklist** 

- ☐ Confirm that all required Python modules are included in the repository. 

- ☐ Confirm that all required CSV datasets are included or provide instructions for obtaining them. 

- ☐ Create and verify requirements.txt. 

- ☐ Complete the required main.ipynb notebook if applicable. 

- ☐ Add and run the required pytest tests. 

- ☐ Verify the required special-function implementation. 

- ☐ Confirm all modules, classes, and functions meet course documentation requirements. 

- ☐ Add each team member's main contributions. 

- ☐ Verify setup instructions from a clean environment. 

- ☐ Confirm that file paths work from the repository root. 

- ☐ Update the repository structure in the README to match the final submission. 

- ☐ Document exact dataset sources and preprocessing. 

- ☐ Confirm each team member has the required number of meaningful commits. 

Power Grid Load Forecasting and Outage Risk Analyzer 

- ☐ Remove obsolete exploratory files that are not part of the final submission. 

- ☐ Review all TODO items. 

- ☐ Confirm the final repository complies with course academic-integrity requirements. 

## **Academic Integrity** 

This project should be submitted in accordance with the course's academic-integrity and AI-use policies. Any exploratory or AI-assisted material retained during development should be reviewed against the instructor's requirements before submission. The final repository should contain only material that the team is permitted to submit and can explain, maintain, and demonstrate. 

## **Disclaimer** 

This software was created as a college programming project for educational purposes. It is not a utility monitoring, emergency-management, or infrastructure-control system. 

Grid-load simulation, outage probability, forecasting, and risk classifications are simplified educational models and should not be interpreted as operational predictions. 

## **License** 

TODO: Select an appropriate repository license and document any dataset-specific licensing or public-use requirements before final publication. 

Power Grid Load Forecasting and Outage Risk Analyzer 

