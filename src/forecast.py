import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def forecast_temperature(df: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    monthly = df.set_index("date")["temperature_c"].resample("ME").mean()
    model = ARIMA(monthly, order=(2, 1, 2))
    fitted = model.fit()
    forecast = fitted.forecast(steps=periods)
    future_dates = pd.date_range(monthly.index[-1] + pd.offsets.MonthEnd(1), periods=periods, freq="ME")
    return pd.DataFrame({
        "date": future_dates,
        "forecast_temperature_c": forecast.values.round(2)
    })
