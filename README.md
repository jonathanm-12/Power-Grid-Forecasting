# Power Grid Forecasting

This project is intended to provide short-term grid-load forecasting, outage-risk estimation, and data visualization using real-world power usage and weather data.

## Repository layout

```text
.
├── data/
│   ├── generated/  # Simulator and model outputs
│   └── raw/        # Source datasets
├── docs/               # Project reports and planning documents
├── examples/           # Early model prototypes
├── prompts/            # Prompts used to produce prototypes
└── src/                # Project source code
```

## Run the load simulator

```bash
python src/grid_load_simulator.py
```

The simulator updates `data/generated/live_grid_load.csv` every 10 seconds. Stop it with `Ctrl+C`.

The scripts under `examples/` are exploratory prototypes. Their `example.com` data URLs are placeholders and must be replaced with real data sources before they can run.
