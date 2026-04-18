from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed" / "climate_cleaned.csv"
PLOTS = BASE_DIR / "outputs" / "plots"
REPORTS = BASE_DIR / "outputs" / "reports"

st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")
st.title("🌍 Climate Trend Analyzer Dashboard")
st.write("A beginner-friendly dashboard for exploring synthetic climate trend data.")

if not PROCESSED.exists():
    st.warning("Run main.py first to generate the processed data and output plots.")
else:
    df = pd.read_csv(PROCESSED, parse_dates=["date"])
    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", len(df))
    c2.metric("Start Date", str(df['date'].min().date()))
    c3.metric("End Date", str(df['date'].max().date()))

    st.subheader("Saved Visual Outputs")
    for title, file_name in [
        ("Yearly Temperature Trend", "temperature_trend.png"),
        ("Yearly Rainfall Trend", "rainfall_trend.png"),
        ("Seasonal Pattern", "seasonal_pattern.png"),
        ("Temperature Forecast", "temperature_forecast.png"),
    ]:
        path = PLOTS / file_name
        if path.exists():
            st.markdown(f"### {title}")
            st.image(str(path))

    st.subheader("Generated Reports")
    for report_file in ["summary_report.txt", "temperature_anomalies.csv", "rainfall_anomalies.csv", "temperature_forecast.csv"]:
        path = REPORTS / report_file
        if path.exists():
            st.markdown(f"**{report_file}**")
            if report_file.endswith(".txt"):
                st.code(path.read_text(encoding="utf-8"))
            else:
                st.dataframe(pd.read_csv(path).head(20), use_container_width=True)
