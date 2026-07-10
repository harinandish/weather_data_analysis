"""
weather_eda.py
--------------
Task 1 -- Analyze Daily Weather Data

Explores a small daily weather dataset (temperature, precipitation,
humidity) to compute summary statistics and visualize trends.

Usage:
    python generate_data.py      # creates data/daily_weather.csv (skip if you have your own)
    python weather_eda.py        # runs the full EDA, saves plots to outputs/

Tech used: Python, Pandas, Matplotlib, Seaborn
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path("data/daily_weather.csv")
OUTPUT_DIR = Path("outputs")

sns.set_theme(style="whitegrid")


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the dataset and parse dates."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python generate_data.py` first, "
            "or place your own CSV at this path."
        )
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: drop exact duplicates, fill small gaps in humidity."""
    df = df.drop_duplicates()
    df = df.sort_values(["city", "date"]).reset_index(drop=True)

    # Fill missing humidity readings with each city's rolling 7-day average,
    # falling back to the city-wide mean for any leftover gaps.
    df["humidity_pct"] = df.groupby("city")["humidity_pct"].transform(
        lambda s: s.fillna(s.rolling(7, min_periods=1, center=True).mean())
    )
    df["humidity_pct"] = df["humidity_pct"].fillna(df.groupby("city")["humidity_pct"].transform("mean"))

    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print overall and per-city summary statistics to the console."""
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Rows: {len(df):,} | Cities: {df['city'].nunique()} | "
          f"Date range: {df['date'].min().date()} -> {df['date'].max().date()}\n")

    print("Overall summary statistics:")
    print(df[["temperature_c", "precipitation_mm", "humidity_pct"]].describe().round(2))

    print("\nPer-city averages:")
    print(
        df.groupby("city")[["temperature_c", "precipitation_mm", "humidity_pct"]]
        .mean()
        .round(2)
    )

    print("\nRainiest day per city:")
    idx = df.groupby("city")["precipitation_mm"].idxmax()
    print(df.loc[idx, ["city", "date", "precipitation_mm"]].to_string(index=False))

    print("\nHottest day per city:")
    idx = df.groupby("city")["temperature_c"].idxmax()
    print(df.loc[idx, ["city", "date", "temperature_c"]].to_string(index=False))
    print()


def plot_temperature_trend(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(11, 5))
    for city, group in df.groupby("city"):
        plt.plot(group["date"], group["temperature_c"], label=city, linewidth=1.2)
    plt.title("Daily Temperature Trend by City")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "01_temperature_trend.png", dpi=150)
    plt.close()


def plot_monthly_precipitation(df: pd.DataFrame, out_dir: Path) -> None:
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    monthly = (
        df.groupby(["city", "month"])["precipitation_mm"]
        .sum()
        .reset_index()
    )
    plt.figure(figsize=(12, 5))
    sns.barplot(data=monthly, x="month", y="precipitation_mm", hue="city", order=month_order)
    plt.title("Total Monthly Precipitation by City")
    plt.xlabel("Month")
    plt.ylabel("Precipitation (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_dir / "02_monthly_precipitation.png", dpi=150)
    plt.close()


def plot_humidity_distribution(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x="city", y="humidity_pct")
    plt.title("Humidity Distribution by City")
    plt.xlabel("City")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    plt.savefig(out_dir / "03_humidity_distribution.png", dpi=150)
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(5.5, 4.5))
    corr = df[["temperature_c", "precipitation_mm", "humidity_pct"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
    plt.title("Correlation Between Weather Variables")
    plt.tight_layout()
    plt.savefig(out_dir / "04_correlation_heatmap.png", dpi=150)
    plt.close()


def plot_temp_vs_humidity(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(7, 5.5))
    sns.scatterplot(data=df, x="temperature_c", y="humidity_pct", hue="city", alpha=0.6, s=25)
    plt.title("Temperature vs. Humidity")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    plt.savefig(out_dir / "05_temperature_vs_humidity.png", dpi=150)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = load_data()
    df = clean_data(df)

    print_summary(df)

    plot_temperature_trend(df, OUTPUT_DIR)
    plot_monthly_precipitation(df, OUTPUT_DIR)
    plot_humidity_distribution(df, OUTPUT_DIR)
    plot_correlation_heatmap(df, OUTPUT_DIR)
    plot_temp_vs_humidity(df, OUTPUT_DIR)

    print(f"Saved 5 charts to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
