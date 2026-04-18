import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("year", as_index=False).agg(
        avg_temperature_c=("temperature_c", "mean"),
        total_rainfall_mm=("rainfall_mm", "sum"),
        avg_humidity_pct=("humidity_pct", "mean"),
    )


def seasonal_summary(df: pd.DataFrame) -> pd.DataFrame:
    season_order = ["Winter", "Summer", "Monsoon", "Autumn"]
    summary = df.groupby("season", as_index=False).agg(
        avg_temperature_c=("temperature_c", "mean"),
        avg_rainfall_mm=("rainfall_mm", "mean"),
        avg_humidity_pct=("humidity_pct", "mean"),
    )
    summary["season"] = pd.Categorical(summary["season"], categories=season_order, ordered=True)
    return summary.sort_values("season")


def temperature_trend(df_yearly: pd.DataFrame) -> dict:
    X = df_yearly[["year"]]
    y = df_yearly["avg_temperature_c"]
    model = LinearRegression()
    model.fit(X, y)
    slope = float(model.coef_[0])
    predictions = model.predict(X)
    return {
        "slope_per_year": slope,
        "predictions": predictions,
        "model": model,
    }


def detect_anomalies(df: pd.DataFrame, column: str, z_threshold: float = 2.8) -> pd.DataFrame:
    values = df[column]
    z_scores = (values - values.mean()) / values.std(ddof=0)
    anomalies = df.loc[np.abs(z_scores) > z_threshold, ["date", "city", column, "season"]].copy()
    anomalies["z_score"] = z_scores[np.abs(z_scores) > z_threshold].round(2).values
    anomalies["anomaly_type"] = np.where(anomalies["z_score"] > 0, "High", "Low")
    return anomalies.sort_values("date")
