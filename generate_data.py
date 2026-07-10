"""
generate_data.py
-----------------
Generates a synthetic but realistic daily weather dataset (temperature,
precipitation, humidity) and saves it to data/daily_weather.csv.

Run this first if data/daily_weather.csv does not already exist:
    python generate_data.py

Replace this script's output with a real dataset (e.g. from Kaggle or the
UCI ML Repository) at any time -- weather_eda.py only expects a CSV with
the columns: date, temperature_c, precipitation_mm, humidity_pct, city.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_DAYS = 365
START_DATE = "2024-01-01"
CITIES = ["Chennai", "Bengaluru", "Hyderabad"]


def generate_city_weather(city: str, dates: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """Create one year of synthetic daily weather for a single city."""
    day_of_year = dates.dayofyear.values

    # City-specific baseline temperature and seasonal amplitude
    baselines = {"Chennai": 29, "Bengaluru": 24, "Hyderabad": 27}
    amplitudes = {"Chennai": 4, "Bengaluru": 3, "Hyderabad": 5}

    base_temp = baselines[city]
    amplitude = amplitudes[city]

    # Seasonal sinusoidal component + daily noise
    seasonal = amplitude * np.sin(2 * np.pi * (day_of_year - 80) / 365)
    noise = rng.normal(0, 1.3, N_DAYS)
    temperature_c = np.round(base_temp + seasonal + noise, 1)

    # Humidity: inversely related to temperature swings, bounded 30-95%
    humidity_base = {"Chennai": 70, "Bengaluru": 55, "Hyderabad": 50}[city]
    humidity_noise = rng.normal(0, 8, N_DAYS)
    humidity_pct = np.clip(humidity_base - seasonal + humidity_noise, 30, 95).round(1)

    # Precipitation: monsoon-heavy months (Jun-Sep, day 152-273) get more rain
    is_monsoon = (day_of_year >= 152) & (day_of_year <= 273)
    rain_prob = np.where(is_monsoon, 0.55, 0.12)
    rains = rng.random(N_DAYS) < rain_prob
    rain_amount = np.where(
        rains,
        rng.gamma(shape=2.0, scale=np.where(is_monsoon, 12, 5)),
        0.0,
    )
    precipitation_mm = np.round(rain_amount, 1)

    return pd.DataFrame(
        {
            "date": dates,
            "city": city,
            "temperature_c": temperature_c,
            "precipitation_mm": precipitation_mm,
            "humidity_pct": humidity_pct,
        }
    )


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    dates = pd.date_range(start=START_DATE, periods=N_DAYS, freq="D")

    frames = [generate_city_weather(city, dates, rng) for city in CITIES]
    df = pd.concat(frames, ignore_index=True)
    df = df.sort_values(["date", "city"]).reset_index(drop=True)

    # Inject a small number of missing values to make the EDA realistic
    missing_idx = rng.choice(df.index, size=int(0.01 * len(df)), replace=False)
    df.loc[missing_idx, "humidity_pct"] = np.nan

    out_path = "data/daily_weather.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows for {len(CITIES)} cities to {out_path}")


if __name__ == "__main__":
    main()
