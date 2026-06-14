import streamlit as st
import pandas as pd


def create_filters(df):

    filtered_df = df.copy()

    st.sidebar.header("Dashboard Filters")

    # ====================================
    # DATE RANGE FILTER
    # ====================================

    if "Date" in df.columns:

        date_data = df["Date"].dropna()

        if not date_data.empty:

            min_date = date_data.min().date()
            max_date = date_data.max().date()

            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if len(date_range) == 2:

                start_date = pd.to_datetime(date_range[0])
                end_date = pd.to_datetime(date_range[1])

                filtered_df = filtered_df[
                    (filtered_df["Date"] >= start_date) &
                    (filtered_df["Date"] <= end_date)
                ]

    # ====================================
    # CRIME TYPE FILTER
    # ====================================

    if "Primary Type" in df.columns:

        crime_types = sorted(
            df["Primary Type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_crime = st.sidebar.selectbox(
            "Crime Type",
            ["All"] + crime_types
        )

        if selected_crime != "All":

            filtered_df = filtered_df[
                filtered_df["Primary Type"]
                == selected_crime
            ]

    # ====================================
    # DISTRICT FILTER
    # ====================================

    if "District" in df.columns:

        districts = sorted(
            df["District"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        selected_district = st.sidebar.selectbox(
            "District",
            ["All"] + districts
        )

        if selected_district != "All":

            filtered_df = filtered_df[
                filtered_df["District"]
                == selected_district
            ]

    # ====================================
    # ARREST FILTER
    # ====================================

    arrest_option = st.sidebar.selectbox(
        "Arrest Status",
        ["All", True, False]
    )

    if arrest_option != "All":

        filtered_df = filtered_df[
            filtered_df["Arrest"] == arrest_option
        ]

    # ====================================
    # DOMESTIC FILTER
    # ====================================

    domestic_option = st.sidebar.selectbox(
        "Domestic Crime",
        ["All", True, False]
    )

    if domestic_option != "All":

        filtered_df = filtered_df[
            filtered_df["Domestic"] == domestic_option
        ]

    # ====================================
    # YEAR RANGE FILTER
    # ====================================

    if "Year" in df.columns:

        year_data = df["Year"].dropna()

        if not year_data.empty:

            min_year = int(year_data.min())
            max_year = int(year_data.max())

            year_range = st.sidebar.slider(
                "Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )

            filtered_df = filtered_df[
                (filtered_df["Year"] >= year_range[0]) &
                (filtered_df["Year"] <= year_range[1])
            ]

    # ====================================
    # COMMUNITY AREA FILTER
    # ====================================

    if "Community Area" in df.columns:

        area_data = df["Community Area"].dropna()

        if not area_data.empty:

            min_area = int(area_data.min())
            max_area = int(area_data.max())

            area_range = st.sidebar.slider(
                "Community Area Range",
                min_value=min_area,
                max_value=max_area,
                value=(min_area, max_area)
            )

            filtered_df = filtered_df[
                (filtered_df["Community Area"] >= area_range[0]) &
                (filtered_df["Community Area"] <= area_range[1])
            ]

    return filtered_df
   
