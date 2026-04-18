from pathlib import Path
import pandas as pd

from src.simulator import generate_synthetic_climate_data
from src.data_loader import load_climate_data
from src.preprocess import preprocess_data
from src.analysis import yearly_summary, seasonal_summary, temperature_trend, detect_anomalies
from src.forecast import forecast_temperature
from src.visualize import plot_temperature_trend, plot_rainfall_trend, plot_seasonal_pattern, plot_forecast


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA = BASE_DIR / "data" / "raw" / "synthetic_climate_data.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "climate_cleaned.csv"
PLOTS_DIR = BASE_DIR / "outputs" / "plots"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"


def save_report(text: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def main():
    print("[1/7] Generating synthetic climate dataset...")
    generate_synthetic_climate_data(str(RAW_DATA))

    print("[2/7] Loading dataset...")
    df = load_climate_data(str(RAW_DATA))

    print("[3/7] Cleaning and preprocessing data...")
    clean_df = preprocess_data(df)
    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(PROCESSED_DATA, index=False)

    print("[4/7] Running trend and seasonal analysis...")
    yearly_df = yearly_summary(clean_df)
    seasonal_df = seasonal_summary(clean_df)
    trend_result = temperature_trend(yearly_df)

    print("[5/7] Detecting anomalies...")
    temp_anomalies = detect_anomalies(clean_df, "temperature_c")
    rain_anomalies = detect_anomalies(clean_df, "rainfall_mm")
    temp_anomalies.to_csv(REPORTS_DIR / "temperature_anomalies.csv", index=False)
    rain_anomalies.to_csv(REPORTS_DIR / "rainfall_anomalies.csv", index=False)

    print("[6/7] Forecasting future monthly temperature...")
    forecast_df = forecast_temperature(clean_df, periods=12)
    forecast_df.to_csv(REPORTS_DIR / "temperature_forecast.csv", index=False)

    print("[7/7] Saving visualizations and summary report...")
    plot_temperature_trend(yearly_df, trend_result["predictions"], str(PLOTS_DIR / "temperature_trend.png"))
    plot_rainfall_trend(yearly_df, str(PLOTS_DIR / "rainfall_trend.png"))
    plot_seasonal_pattern(seasonal_df, str(PLOTS_DIR / "seasonal_pattern.png"))
    history_monthly = clean_df.set_index("date")["temperature_c"].resample("ME").mean()
    plot_forecast(history_monthly, forecast_df, str(PLOTS_DIR / "temperature_forecast.png"))

    summary_lines = [
        "CLIMATE TREND ANALYZER - SUMMARY REPORT",
        "=" * 50,
        f"Years analyzed: {clean_df['year'].min()} to {clean_df['year'].max()}",
        f"Average annual warming trend: {trend_result['slope_per_year']:.3f} °C/year",
        f"Temperature anomalies found: {len(temp_anomalies)}",
        f"Rainfall anomalies found: {len(rain_anomalies)}",
        "",
        "Top Insights:",
        "1. The synthetic city shows a steady long-term warming trend.",
        "2. Rainfall follows a seasonal monsoon pattern with several extreme spikes.",
        "3. Humidity is highest in wetter months and lower during warmer dry periods.",
        "4. Forecasted temperatures suggest the warming pattern may continue in the near future.",
    ]
    save_report("\n".join(summary_lines), REPORTS_DIR / "summary_report.txt")

    print("Project executed successfully.")
    print(f"Processed data saved to: {PROCESSED_DATA}")
    print(f"Plots saved to: {PLOTS_DIR}")
    print(f"Reports saved to: {REPORTS_DIR}")


if __name__ == "__main__":
    main()
