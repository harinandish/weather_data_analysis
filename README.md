# Weather EDA — Analyze Daily Weather Data

> SlashMark BASIC Track — Task 1

A small, self-contained project that explores a daily weather dataset
(temperature, precipitation, humidity) to compute summary statistics and
visualize trends across cities and months.

## Overview

| | |
|---|---|
| **Difficulty** | Beginner |
| **Estimated time** | 4–6 hours |
| **Tech used** | Python, Pandas, Matplotlib, Seaborn |
| **Libraries** | `pandas`, `numpy`, `matplotlib`, `seaborn` |

**Learning outcomes:** data cleaning, exploratory data analysis (EDA),
plotting time-series data, and visualizing distributions.

## Dataset

`data/daily_weather.csv` contains one year (365 days) of daily weather
readings for three Indian cities — **Chennai**, **Bengaluru**, and
**Hyderabad** — with the following columns:

| Column | Description |
|---|---|
| `date` | Calendar date (YYYY-MM-DD) |
| `city` | City name |
| `temperature_c` | Daily average temperature (°C) |
| `precipitation_mm` | Daily rainfall (mm) |
| `humidity_pct` | Relative humidity (%) |

Since no dataset was attached to the task, `generate_data.py` synthesizes a
realistic dataset (seasonal temperature curves, a monsoon-heavy rainy
season, and a small share of missing humidity values so the cleaning step
has something to do). **Swap in a real dataset** — e.g. from
[Kaggle Datasets](https://www.kaggle.com/datasets) or the
[UCI ML Repository](https://archive.ics.uci.edu/) — by replacing
`data/daily_weather.csv` with the same column layout.

## Project structure

```
weather-eda/
├── data/
│   └── daily_weather.csv       # generated (or your own) dataset
├── outputs/                    # charts saved here after running the EDA
│   ├── 01_temperature_trend.png
│   ├── 02_monthly_precipitation.png
│   ├── 03_humidity_distribution.png
│   ├── 04_correlation_heatmap.png
│   └── 05_temperature_vs_humidity.png
├── generate_data.py            # creates the synthetic dataset
├── weather_eda.py               # cleaning, summary stats, and plots
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <your-repo-url>
cd weather-eda
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# 1. Generate the sample dataset (skip if using your own CSV)
python generate_data.py

# 2. Run the full EDA — prints summary stats and saves charts to outputs/
python weather_eda.py
```

## What the analysis covers

1. **Data cleaning** — drops duplicate rows and fills missing humidity
   values using a per-city rolling average.
2. **Summary statistics** — overall and per-city averages, plus the
   hottest and rainiest day recorded for each city.
3. **Temperature trend** — daily temperature line chart per city across
   the full year.
4. **Monthly precipitation** — total rainfall per month per city,
   highlighting the monsoon season.
5. **Humidity distribution** — box plots comparing humidity spread across
   cities.
6. **Correlation heatmap** — relationships between temperature,
   precipitation, and humidity.
7. **Temperature vs. humidity scatter plot** — visual check of how the two
   variables relate.

## Sample output

Console summary (truncated):

```
DATASET OVERVIEW
============================================================
Rows: 1,095 | Cities: 3 | Date range: 2024-01-01 -> 2024-12-30

Per-city averages:
           temperature_c  precipitation_mm  humidity_pct
city
Bengaluru          23.88              5.37         55.24
Chennai            28.99              5.05         69.47
Hyderabad          26.93              5.54         50.04
```

All five charts are written to `outputs/` as PNG files.

## Notes

- Random seed is fixed (`RANDOM_SEED = 42`) in `generate_data.py`, so
  re-running it always reproduces the same dataset.
- To analyze a real dataset instead, just make sure your CSV has the same
  five columns (`date, city, temperature_c, precipitation_mm,
  humidity_pct`) — `weather_eda.py` doesn't need any other changes.

## License

MIT — feel free to reuse and adapt for your own learning projects.
