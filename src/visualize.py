from pathlib import Path
import matplotlib.pyplot as plt


def save_plot(fig, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_temperature_trend(yearly_df, trend_predictions, output_path: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(yearly_df["year"], yearly_df["avg_temperature_c"], marker="o", label="Actual")
    ax.plot(yearly_df["year"], trend_predictions, linestyle="--", label="Trend Line")
    ax.set_title("Yearly Average Temperature Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_plot(fig, output_path)


def plot_rainfall_trend(yearly_df, output_path: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(yearly_df["year"], yearly_df["total_rainfall_mm"])
    ax.set_title("Yearly Total Rainfall")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rainfall (mm)")
    ax.grid(True, axis="y", alpha=0.3)
    save_plot(fig, output_path)


def plot_seasonal_pattern(seasonal_df, output_path: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(seasonal_df["season"], seasonal_df["avg_temperature_c"], marker="o", label="Avg Temp")
    ax.plot(seasonal_df["season"], seasonal_df["avg_humidity_pct"], marker="s", label="Avg Humidity")
    ax.set_title("Seasonal Climate Pattern")
    ax.set_xlabel("Season")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_plot(fig, output_path)


def plot_forecast(history_monthly, forecast_df, output_path: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(history_monthly.index, history_monthly.values, label="Historical Monthly Avg Temp")
    ax.plot(forecast_df["date"], forecast_df["forecast_temperature_c"], marker="o", linestyle="--", label="Forecast")
    ax.set_title("Temperature Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_plot(fig, output_path)
