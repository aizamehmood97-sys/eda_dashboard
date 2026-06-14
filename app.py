import streamlit as st
import pandas as pd

from filters import create_filters

from charts import (
    plot_line_chart,
    plot_area_chart,
    plot_bar_chart,
    plot_pie_chart,
    plot_histogram,
    plot_count_plot,
    plot_domestic_count,
    plot_box_plot,
    plot_violin_plot,
    plot_heatmap,
    plot_scatter,
    plot_top_districts,
    plot_location_description,
    plot_monthly_crimes,
    plot_hourly_crimes,
    plot_arrest_by_crime,
    plot_domestic_trend,
    plot_district_heatmap
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Chicago Crime Dashboard",
    layout="wide"
)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv(
        "Crimes_-_2001_to_Present_20260523.csv",
        low_memory=False
    )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────

st.title("Chicago Crimes Dashboard (2022–2026)")
st.markdown("Interactive analysis of Chicago crime data.")

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────

filtered_df = create_filters(df)

# ─────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Crimes", f"{len(filtered_df):,}")

with col2:
    arrests = int(filtered_df["Arrest"].sum()) if "Arrest" in filtered_df.columns else 0
    st.metric("Arrests", f"{arrests:,}")

with col3:
    domestic = int(filtered_df["Domestic"].sum()) if "Domestic" in filtered_df.columns else 0
    st.metric("Domestic Crimes", f"{domestic:,}")

with col4:
    crime_types = (
        filtered_df["Primary Type"].nunique()
        if "Primary Type" in filtered_df.columns
        else 0
    )
    st.metric("Crime Types", crime_types)

# ─────────────────────────────────────────────
# DATA PREVIEW
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Dataset Preview")

if filtered_df.empty:
    st.info("No records match the current filters.")
else:
    st.dataframe(filtered_df.head(20), use_container_width=True)

# ─────────────────────────────────────────────
# TREND ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Trend Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_line_chart(filtered_df)

with col2:
    plot_area_chart(filtered_df)

# ─────────────────────────────────────────────
# CRIME TYPE ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Crime Type Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_bar_chart(filtered_df)

with col2:
    plot_pie_chart(filtered_df)

# ─────────────────────────────────────────────
# DISTRIBUTION ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_histogram(filtered_df)

with col2:
    plot_count_plot(filtered_df)

# ─────────────────────────────────────────────
# DOMESTIC ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Domestic Crime Analysis")

plot_domestic_count(filtered_df)

# ─────────────────────────────────────────────
# DISTRICT ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("District Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_box_plot(filtered_df)

with col2:
    plot_violin_plot(filtered_df)

# ─────────────────────────────────────────────
# HEATMAP
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Correlation Heatmap")

plot_heatmap(filtered_df)

# ─────────────────────────────────────────────
# LOCATION ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Location Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_top_districts(filtered_df)

with col2:
    plot_location_description(filtered_df)

# ─────────────────────────────────────────────
# GEO ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Geographical Analysis")

plot_scatter(filtered_df)

# ─────────────────────────────────────────────
# MONTHLY & HOURLY ANALYSIS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Monthly & Hourly Crime Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_monthly_crimes(filtered_df)

with col2:
    plot_hourly_crimes(filtered_df)

# ─────────────────────────────────────────────
# ARREST & DOMESTIC TRENDS
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("Arrest & Domestic Crime Trends")

col1, col2 = st.columns(2)

with col1:
    plot_arrest_by_crime(filtered_df)

with col2:
    plot_domestic_trend(filtered_df)

# ─────────────────────────────────────────────
# DISTRICT HEATMAP  ← was the crash point
# ─────────────────────────────────────────────

st.markdown("---")
st.subheader("District vs Crime Type Heatmap")

plot_district_heatmap(filtered_df)

# ─────────────────────────────────────────────
# DOWNLOAD FILTERED DATA
# ─────────────────────────────────────────────

st.markdown("---")

if not filtered_df.empty:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_chicago_crimes.csv",
        mime="text/csv"
    )
else:
    st.info("No data to download for the current filters.")
