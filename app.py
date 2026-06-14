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

# PAGE CONFIG

st.set_page_config(
    page_title="Chicago Crime Dashboard",
    layout="wide"
)

# LOAD DATA

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/Crimes_-_2001_to_Present_20260523.csv",
        low_memory=False
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    return df


df = load_data()

# TITLE

st.title("Chicago Crimes Dashboard (2022–2026)")
st.markdown(
    "Interactive analysis of Chicago crime data."
)

# SIDEBAR FILTERS

filtered_df = create_filters(df)

# KPI SECTION

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Crimes",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Arrests",
        f"{filtered_df['Arrest'].sum():,}"
    )

with col3:
    st.metric(
        "Domestic Crimes",
        f"{filtered_df['Domestic'].sum():,}"
    )

with col4:
    st.metric(
        "Crime Types",
        filtered_df["Primary Type"].nunique()
    )

# DATA PREVIEW

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

# TREND ANALYSIS

st.markdown("---")
st.subheader("Trend Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_line_chart(filtered_df)

with col2:
    plot_area_chart(filtered_df)

# CRIME TYPE ANALYSIS

st.markdown("---")
st.subheader("Crime Type Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_bar_chart(filtered_df)

with col2:
    plot_pie_chart(filtered_df)

# DISTRIBUTION ANALYSIS

st.markdown("---")
st.subheader("Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_histogram(filtered_df)

with col2:
    plot_count_plot(filtered_df)

# DOMESTIC ANALYSIS

st.markdown("---")
st.subheader("Domestic Crime Analysis")

plot_domestic_count(filtered_df)

# DISTRICT ANALYSIS

st.markdown("---")
st.subheader("District Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_box_plot(filtered_df)

with col2:
    plot_violin_plot(filtered_df)

# HEATMAP

st.markdown("---")
st.subheader("Correlation Heatmap")

plot_heatmap(filtered_df)

# LOCATION ANALYSIS

st.markdown("---")
st.subheader("Location Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_top_districts(filtered_df)

with col2:
    plot_location_description(filtered_df)

# GEO ANALYSIS

st.markdown("---")
st.subheader("Geographical Analysis")

plot_scatter(filtered_df)

# MONTHLY & HOURLY ANALYSIS

st.markdown("---")
st.subheader("Monthly & Hourly Crime Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_monthly_crimes(filtered_df)

with col2:
    plot_hourly_crimes(filtered_df)

# ARREST & DOMESTIC TRENDS

st.markdown("---")
st.subheader("Arrest & Domestic Crime Trends")

col1, col2 = st.columns(2)

with col1:
    plot_arrest_by_crime(filtered_df)

with col2:
    plot_domestic_trend(filtered_df)

# DISTRICT HEATMAP

st.markdown("---")
st.subheader("District vs Crime Type Heatmap")

plot_district_heatmap(filtered_df)

# DOWNLOAD FILTERED DATA

st.markdown("---")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_chicago_crimes.csv",
    mime="text/csv"
)