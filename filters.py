import streamlit as st
import pandas as pd


def create_filters(df):
    """
    Create all dashboard filters
    Returns filtered dataframe
    """

    st.sidebar.header("Dashboard Filters")

    # DATE RANGE FILTER
    
    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date())
    )

    filtered_df = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date)
            &
            (filtered_df["Date"].dt.date <= end_date)
        ]

    
    # CATEGORY FILTER
    
    crime_types = sorted(
        filtered_df["Primary Type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_crimes = st.sidebar.multiselect(
        "Crime Type",
        crime_types,
        default=[]
    )

    if selected_crimes:
        filtered_df = filtered_df[
            filtered_df["Primary Type"]
            .isin(selected_crimes)
        ]

    # DISTRICT MULTISELECT
    
    districts = sorted(
        filtered_df["District"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_districts = st.sidebar.multiselect(
        "District",
        districts,
        default=[]
    )

    if selected_districts:
        filtered_df = filtered_df[
            filtered_df["District"]
            .isin(selected_districts)
        ]

    # ARREST FILTER
    
    arrest_options = ["All", "True", "False"]

    arrest_filter = st.sidebar.selectbox(
        "Arrest Status",
        arrest_options
    )

    if arrest_filter != "All":
        arrest_value = arrest_filter == "True"

        filtered_df = filtered_df[
            filtered_df["Arrest"] == arrest_value
        ]

    # DOMESTIC FILTER
    
    domestic_options = ["All", "True", "False"]

    domestic_filter = st.sidebar.selectbox(
        "Domestic Crime",
        domestic_options
    )

    if domestic_filter != "All":
        domestic_value = domestic_filter == "True"

        filtered_df = filtered_df[
            filtered_df["Domestic"] == domestic_value
        ]

    # YEAR RANGE SLIDER
   
    min_year = int(filtered_df["Year"].min())
    max_year = int(filtered_df["Year"].max())

    year_range = st.sidebar.slider(
        "Year Range",
        min_year,
        max_year,
        (min_year, max_year)
    )

    filtered_df = filtered_df[
        (filtered_df["Year"] >= year_range[0])
        &
        (filtered_df["Year"] <= year_range[1])
    ]

  
    # NUMERICAL RANGE FILTER
    # COMMUNITY AREA
    
    community_data = filtered_df[
        "Community Area"
    ].dropna()

    if len(community_data) > 0:

        min_area = int(community_data.min())
        max_area = int(community_data.max())

        area_range = st.sidebar.slider(
            "Community Area Range",
            min_area,
            max_area,
            (min_area, max_area)
        )

        filtered_df = filtered_df[
            (filtered_df["Community Area"] >= area_range[0])
            &
            (filtered_df["Community Area"] <= area_range[1])
        ]

    
    # SEARCH FILTER
   
    keyword = st.sidebar.text_input(
        "Search Crime Description"
    )

    if keyword:

        filtered_df = filtered_df[
            filtered_df["Description"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    
    # RESET FILTERS
    
    st.sidebar.markdown("---")

    if st.sidebar.button("Reset Filters"):
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.write(
        f"Filtered Records: {len(filtered_df):,}"
    )

    return filtered_df