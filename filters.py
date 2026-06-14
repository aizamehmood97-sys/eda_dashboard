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
            try:
                min_date = date_data.min().date()
                max_date = date_data.max().date()

                if min_date == max_date:
                    st.sidebar.info(
                        f"All data is from a single date: {min_date}"
                    )
                else:
                    date_range = st.sidebar.date_input(
                        "Select Date Range",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )
                    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                        start_date = pd.to_datetime(date_range[0])
                        end_date = pd.to_datetime(date_range[1])
                        filtered_df = filtered_df[
                            (filtered_df["Date"] >= start_date) &
                            (filtered_df["Date"] <= end_date)
                        ]
            except Exception:
                st.sidebar.warning("Date filter could not be applied.")

    # ====================================
    # CRIME TYPE FILTER
    # ====================================

    if "Primary Type" in df.columns:
        try:
            crime_types = sorted(
                df["Primary Type"].dropna().unique().tolist()
            )
            selected_crime = st.sidebar.selectbox(
                "Crime Type",
                ["All"] + crime_types
            )
            if selected_crime != "All":
                filtered_df = filtered_df[
                    filtered_df["Primary Type"] == selected_crime
                ]
        except Exception:
            st.sidebar.warning("Crime Type filter could not be applied.")

    # ====================================
    # DISTRICT FILTER
    # ====================================

    if "District" in df.columns:
        try:
            districts = sorted(
                df["District"]
                .dropna()
                .astype(float)   # float first to handle ".0" values
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
                    filtered_df["District"].astype(float).astype(int)
                    == selected_district
                ]
        except Exception:
            st.sidebar.warning("District filter could not be applied.")

    # ====================================
    # ARREST FILTER
    # ====================================

    try:
        arrest_option = st.sidebar.selectbox(
            "Arrest Status",
            ["All", True, False]
        )
        if arrest_option != "All":
            filtered_df = filtered_df[
                filtered_df["Arrest"] == arrest_option
            ]
    except Exception:
        st.sidebar.warning("Arrest filter could not be applied.")

    # ====================================
    # DOMESTIC FILTER
    # ====================================

    try:
        domestic_option = st.sidebar.selectbox(
            "Domestic Crime",
            ["All", True, False]
        )
        if domestic_option != "All":
            filtered_df = filtered_df[
                filtered_df["Domestic"] == domestic_option
            ]
    except Exception:
        st.sidebar.warning("Domestic filter could not be applied.")

    # ====================================
    # YEAR RANGE FILTER
    # ====================================

    if "Year" in df.columns:
        try:
            year_data = df["Year"].dropna()
            if not year_data.empty:
                min_year = int(year_data.min())
                max_year = int(year_data.max())

                if min_year == max_year:
                    st.sidebar.info(f"All data is from year: {min_year}")
                else:
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
        except Exception:
            st.sidebar.warning("Year Range filter could not be applied.")

    # ====================================
    # COMMUNITY AREA FILTER
    # ====================================

    if "Community Area" in df.columns:
        try:
            area_data = df["Community Area"].dropna()
            if not area_data.empty:
                min_area = int(area_data.min())
                max_area = int(area_data.max())

                if min_area == max_area:
                    st.sidebar.info(
                        f"All data is from Community Area: {min_area}"
                    )
                else:
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
        except Exception:
            st.sidebar.warning("Community Area filter could not be applied.")

    # ====================================
    # EMPTY RESULT WARNING
    # ====================================

    if filtered_df.empty:
        st.sidebar.error(
            "⚠️ No records match the selected filters. "
            "Charts will show placeholder messages."
        )

    return filtered_df
