from pathlib import Path
import numpy as np
import pandas as pd


def generate_synthetic_climate_data(output_path: str, start_date: str = "2015-01-01", end_date: str = "2024-12-31") -> pd.DataFrame:
    """Generate synthetic daily climate data for a virtual city."""
    rng = np.random.default_rng(42)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    n = len(dates)

    day_of_year = dates.dayofyear.values
    years_from_start = dates.year.values - dates.year.min()

    # Seasonal temperature + warming trend
    temperature = (
        24
        + 10 * np.sin(2 * np.pi * day_of_year / 365.25)
        + 0.12 * years_from_start
        + rng.normal(0, 1.5, n)
    )

    # Humidity with seasonal pattern
    humidity = (
        65
        + 12 * np.cos(2 * np.pi * day_of_year / 365.25)
        + rng.normal(0, 4, n)
    )

    # Rainfall with monsoon-like seasonality
    rainfall_base = 3 + 6 * np.maximum(0, np.sin(2 * np.pi * (day_of_year - 140) / 365.25))
    rainfall = np.maximum(0, rainfall_base + rng.normal(0, 2.2, n))

    # Wind speed
    wind_speed = np.maximum(0, 8 + 2 * np.sin(2 * np.pi * (day_of_year + 30) / 365.25) + rng.normal(0, 1.2, n))

    df = pd.DataFrame({
        "date": dates,
        "city": "VirtualCity",
        "temperature_c": temperature.round(2),
        "rainfall_mm": rainfall.round(2),
        "humidity_pct": np.clip(humidity, 20, 100).round(2),
        "wind_speed_kmh": wind_speed.round(2),
    })

    # Add season label
    month = df["date"].dt.month
    season_map = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Summer", 4: "Summer", 5: "Summer",
        6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
        10: "Autumn", 11: "Autumn",
    }
    df["season"] = month.map(season_map)

    # Inject some anomalies
    hot_idx = rng.choice(n, size=12, replace=False)
    flood_idx = rng.choice(n, size=10, replace=False)
    df.loc[hot_idx, "temperature_c"] += rng.uniform(6, 10, size=len(hot_idx))
    df.loc[flood_idx, "rainfall_mm"] += rng.uniform(40, 90, size=len(flood_idx))

    # Small missing values for cleaning practice
    missing_idx = rng.choice(n, size=25, replace=False)
    df.loc[missing_idx[:10], "temperature_c"] = np.nan
    df.loc[missing_idx[10:18], "rainfall_mm"] = np.nan
    df.loc[missing_idx[18:], "humidity_pct"] = np.nan

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return df
