# Power Grid Load Forecasting and Outage Risk Analyzer

> **Project status:** In development for the AAI/CPE/EE 551 course project. Items marked **Planned** describe the intended final system and must be updated as the implementation is completed.

## Project overview

Electric grids must continuously balance supply and demand. Unexpected demand, equipment limitations, and weather-driven changes can increase congestion and the likelihood of service interruptions. 

The initial study area is Hoboken and Hudson County, New Jersey, using nearby New York Harbor weather observations where appropriate. The final workflow is intended to:

- load and validate historical weather, outage, and electrical-load data;
- align time-stamped records from multiple sources;
- forecast short-term electrical load;
- estimate outage risk from forecast weather and expected grid load;
- categorize risk as low, medium, or high; and
- present results in plots and, if time permits, a selectable regional map.

The current repository contains two historical datasets, a live synthetic load simulator, early model examples, the team proposal, and the course requirements. The integrated model and required `main.ipynb` notebook are still planned.

## Team

| Team member | Email | Stevens ID |
| --- | --- | --- |
| Larry Hagood | lhagood@stevens.edu | 20027091 |
| Jonathan Mikalov | jmikalov@stevens.edu | 20030528 |
| Daniela Montoya | dmontoya@stevens.edu | 20038486 |

### Main contributions

Complete this table before final submission. Describe functional work such as program logic, data preparation, testing, debugging, or documentation rather than cosmetic changes.

| Team member | Main contributions |
| --- | --- |
| Larry Hagood | **TODO:** Add completed modules, analyses, tests, and documentation. |
| Jonathan Mikalov | **TODO:** Add completed modules, analyses, tests, and documentation. |
| Daniela Montoya | **TODO:** Add completed modules, analyses, tests, and documentation. |

Each team member must make at least five meaningful commits to the shared GitHub repository.

## Repository structure

```text
.
├── data/
│   ├── generated/                  # Simulator and model outputs
│   └── raw/
│       ├── project_electrical_outages.csv
│       └── weather_hudson_station.csv
├── docs/
│   ├── course_project.pdf              # Assignment and grading rubric
│   ├── data_collection_options.docx    # Candidate public data sources
│   └── team_project_proposal.docx      # Approved project plan
├── examples/
│   ├── hagood_chatgpt_example.py       # Exploratory example; placeholder URLs
│   └── hagood_grok_example.py          # Exploratory example; placeholder URLs
├── prompts/
│   └── hagood_prompt.txt                # Prompt associated with examples
├── src/
│   └── grid_load_simulator.py          # Runnable synthetic live-load simulator
├── .gitignore
└── README.md
```

Expected final additions:

```text
.
├── main.ipynb                 # Required main program and demonstration
├── requirements.txt           # Pinned runtime and development dependencies
├── src/
│   ├── data_manager.py       # Data loading, validation, and alignment
│   ├── power_station.py      # Station attributes and load/risk behavior
│   ├── outage_model.py       # Training, evaluation, and prediction
│   └── visualization.py      # Forecast and risk plots
└── tests/                    # Pytest test suite
```

The final module names may change as the design develops. Keep this section synchronized with the repository.

## Academic integrity note

The course requirements state that AI tools may not be used to design the project. This repository currently retains AI-named exploratory examples and their prompt for provenance; they are not part of the final application. Before using or submitting any such material, the team should confirm its acceptability with the instructor and remove it from the submission if required. All submitted implementation and documentation must comply with the course policy.

## Data

### Included datasets

| File | Contents | Current shape/use |
| --- | --- | --- |
| `data/raw/project_electrical_outages.csv` | Hudson County outage start time, duration, and affected-customer statistics | 1,307 records for model targets and outage analysis |
| `data/raw/weather_hudson_station.csv` | Hourly station observations including timestamp, wind, visibility, temperature, dew point, and pressure | 8,687 records for cleaning and weather features |
| `data/generated/live_grid_load.csv` | Synthetic timestamp, load percentage, temperature, season, and day type | Created when the load simulator runs; not committed |

The included weather file identifies its station as **The Battery, New York**, near the initial Hudson County study area. Its compact NOAA-style fields require parsing and quality-code handling before model training.

### Candidate public sources

The team identified the following sources for the final data pipeline:

- [U.S. Energy Information Administration Hourly Electric Grid Monitor](https://www.eia.gov/electricity/gridmonitor/about) for electrical demand and grid trends;
- [Event-Correlated Outage Dataset in America](https://catalog.data.gov/dataset/event-correlated-outage-dataset-in-america) for outage records;
- NOAA Integrated Surface Database or [Global Historical Climatology Network Hourly](https://www.ncei.noaa.gov/products/global-historical-climatology-network-hourly) for historical weather;
- [NOAA Storm Events Database](https://www.ncei.noaa.gov/stormevents/) for severe-weather context; and
- [Census TIGER/Line county boundaries](https://www.census.gov/geographies/mapping-files/2025/geo/tiger-line-file.html) for an optional county risk map.

Before final submission, document the exact download URL, access date, license or public-use status, geographic coverage, units, and preprocessing performed for every dataset used by the model.

## Proposed solution design

### Data flow

```text
Historical weather ─┐
Historical load    ─┼─> clean and align ─> train/evaluate model
Past outages       ─┘                              |
                                                          v
Forecast weather + expected load ─> predict risk ─> tables and plots
```

### Planned objects

The proposal defines a composition relationship between two meaningful classes:

1. A data or power-station class will hold station identity, capacity, location, historical loads, weather, outages, and forecast records. It will provide validation and preprocessing behavior.
2. An outage-model class will contain or reference the station data object, train on its prepared records, and return load forecasts and outage-risk predictions.

The final names, constructor arguments, public methods, and relationship should be documented here once implemented.

### Planned modeling workflow

1. Read the raw CSV files and validate required columns and values.
2. Convert timestamps to one consistent timezone and hourly interval.
3. Decode weather fields and normalize all units.
4. Join weather, grid-load, and outage observations by time and region.
5. Engineer time, weather-extreme, load, lag, and rolling-window features.
6. Split training and test data chronologically to avoid future-data leakage.
7. Train and evaluate a baseline forecasting/risk model.
8. Apply the model to up to ten days of forecast weather and expected load.
9. Save prediction tables and produce load/risk visualizations.

Model choice, risk thresholds, evaluation metrics, and assumptions must be recorded after they have been tested. The scripts in `examples/` are references only: their `example.com` URLs are placeholders and they are not the final application.

## Environment and dependencies

The course permits Python 3.12, 3.13, or 3.14. The team should develop and test against one shared version; **Python 3.12 is the current recommended project baseline** unless the team records a different choice here.

The current simulator uses only Python's standard library. The planned integrated project is expected to use:

- Jupyter and ipykernel for the required notebook;
- pandas and NumPy for table and numerical processing;
- Matplotlib for visualization;
- scikit-learn for baseline machine-learning models; and
- pytest for automated tests.

### Windows setup

Open PowerShell in the repository root and run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install jupyter ipykernel pandas numpy matplotlib scikit-learn pytest
python -m ipykernel install --user --name power-grid-forecasting --display-name "Python (Power Grid Forecasting)"
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in the same window and activate the environment again.

### macOS setup

Open Terminal in the repository root and run:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyter ipykernel pandas numpy matplotlib scikit-learn pytest
python -m ipykernel install --user --name power-grid-forecasting --display-name "Python (Power Grid Forecasting)"
```

Before final submission, generate and commit `requirements.txt`, then replace the package-install command above with:

```bash
python -m pip install -r requirements.txt
```

## How to run

### Current load simulator

After activating the environment, run this command from the repository root:

```bash
python src/grid_load_simulator.py
```

The program prints a new simulated Hoboken-area reading every 10 seconds and rewrites `data/generated/live_grid_load.csv` with the newest observation first. Press `Ctrl+C` once to stop it cleanly.

### Final notebook workflow — planned

These instructions apply after `main.ipynb` and the remaining modules have been implemented:

1. Confirm that both raw CSV files are present under `data/raw/`.
2. Activate the project virtual environment.
3. Start Jupyter with `python -m jupyter lab` from the repository root.
4. Open `main.ipynb`.
5. Select the **Python (Power Grid Forecasting)** kernel.
6. Choose **Kernel > Restart Kernel and Run All Cells**.
7. Confirm that data-validation and model-evaluation cells complete without errors.
8. Review the forecast table and plots produced by the final cells.
9. Confirm that generated files appear under `data/generated/`.

Before submission, replace this planned section with the exact notebook inputs, prompts, expected output filenames, approximate runtime, and troubleshooting steps verified on both Windows and macOS.

## Testing

The final test suite will run from the repository root with:

```bash
python -m pytest -v
```

At minimum, tests should cover:

- valid and invalid weather/load inputs;
- missing files or required columns;
- timestamp and unit conversion;
- numerical forecast output ranges;
- outage-risk threshold boundaries; and
- class string representation and comparison behavior.

No `tests/` directory is present yet. Add at least two functional pytest cases and update this section with the observed passing result before submission.

## Course requirement traceability

Status key: **Present** means visible in the current project source, **Partial** means an early example exists but is not integrated, and **Planned** means implementation evidence is still required.

### Part 1

| # | Requirement | Planned project evidence | Status |
| --- | --- | --- | --- |
| 1 | Two meaningful related classes | Station/data object composed into the outage forecasting model | Planned |
| 2 | Two meaningful functions | Data preparation, model training, load forecasting, and risk prediction functions | Partial — simulator functions exist |
| 3 | Two advanced libraries | pandas/NumPy for processing, Matplotlib for plots, scikit-learn for modeling | Partial — examples only |
| 4 | Two exception scenarios and two pytest cases | File/schema validation, invalid values, forecasting and threshold tests | Planned |
| 5 | Meaningful data I/O | Read raw CSVs and write generated predictions | Present in simulator; model I/O planned |
| 6 | Two loops and two conditionals | Dataset iteration, live updates, seasonal and risk rules | Present in simulator |
| 7 | Mutable and immutable types | DataFrames/lists/dicts/sets plus tuples, strings, and numeric constants | Partial |
| 8 | `__str__()` and another operator overload | Station display plus capacity or risk comparison using `__eq__()` or `__lt__()` | Planned |
| 9 | Module/class/function documentation | Module headers, docstrings, type hints, and meaningful comments | Partial |
| 10 | Main-module behavior | `if __name__ == "__main__":` entry points and `main.ipynb` | Present in simulator; notebook planned |

### Part 2

The proposal selects these four components for the final implementation:

| Component | Planned use | Status |
| --- | --- | --- |
| Core-type comprehension | Build or filter feature/record collections | Planned |
| Built-in library/module | `csv`, `datetime`, `pathlib`, or `collections` in core data handling | Present in simulator |
| Generator | Yield daily or hourly load records without loading duplicate copies | Planned |
| Special function | Use `map()` or `zip()` for aligned transformations | Planned |

The simulator also uses `collections.deque`, a linear queue structure, as additional evidence. In the final README, link each completed requirement to its exact module, class, function, notebook section, or test.

## Timeline and milestones

- [x] **Week 1:** Define the problem, identify candidate data, outline classes, and create the repository.
- [ ] **Week 2:** Implement data I/O and core classes; prepare preliminary visualizations.
- [ ] **Week 3:** Build forecasting and risk models; add exception handling, operator overloads, and docstrings.
- [ ] **Week 4:** Complete `main.ipynb`, pytest coverage, a generator, comprehension, and special-function usage.
- [ ] **Week 5:** Integrate, debug, demonstrate, finalize setup instructions, and clean the repository.
- [ ] **Before August 24, 2026:** Run the notebook from a fresh environment, verify tests on Windows and macOS, complete contribution records, and submit the public GitHub repository link.

## Assumptions and limitations

- The current load simulator creates synthetic data and is not a utility operational tool.
- The included weather station is nearby but is not physically located in Hoboken.
- Historical correlations do not establish that weather or high load caused an outage.
- Rare outage events may create severe class imbalance and require suitable metrics and validation.
- Forecast quality depends on geographic alignment, timestamps, units, missing-value treatment, and access to representative grid-load data.
- Predictions are educational estimates and must not be used for emergency or infrastructure decisions.

## Final submission checklist

- [ ] `main.ipynb` runs from top to bottom without errors using the documented kernel.
- [ ] All required modules, datasets, and dependency files are committed.
- [ ] Public data sources, licenses, units, and preprocessing are documented.
- [ ] Both meaningful classes and their relationship are implemented.
- [ ] All Part 1 requirements have direct evidence in the traceability table.
- [ ] At least four Part 2 components have direct evidence in the traceability table.
- [ ] At least two exception scenarios are demonstrated.
- [ ] At least two functional pytest tests pass.
- [ ] Every module, class, and function has the required header/docstring/comment quality.
- [ ] Windows and macOS setup/run instructions have been tested from a fresh clone.
- [ ] Each member has at least five meaningful commits and documented contributions.
- [ ] The repository is public and contains everything needed for grading.

## Project documents

- [Team project proposal](docs/team_project_proposal.docx)
- [Course project requirements and rubric](docs/course_project.pdf)
- [Data-collection notes](docs/data_collection_options.docx)

## License

**TODO:** Choose a repository license and document any dataset-specific terms before making the final repository public.
