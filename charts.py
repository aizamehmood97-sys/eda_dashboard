import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

sns.set_style("whitegrid")

# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _empty_notice(title: str, reason: str = "No data available for the current filters."):
    """Render a placeholder when there is nothing to plot."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.set_title(title)
    ax.text(
        0.5, 0.5, reason,
        ha="center", va="center",
        transform=ax.transAxes,
        fontsize=12, color="grey"
    )
    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)


def _required_cols(df: pd.DataFrame, cols: list[str]) -> bool:
    """Return True only when all cols exist and the df is non-empty."""
    return not df.empty and all(c in df.columns for c in cols)


# ─────────────────────────────────────────────
# TREND CHARTS
# ─────────────────────────────────────────────

def plot_line_chart(df):
    title = "Crime Trend Over Years"
    if not _required_cols(df, ["Year"]):
        _empty_notice(title)
        return
    try:
        yearly = df.groupby("Year").size()
        if yearly.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(yearly.index, yearly.values, marker="o")
        ax.set_title(title)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Crimes")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_area_chart(df):
    title = "Crime Volume Area Chart"
    if not _required_cols(df, ["Year"]):
        _empty_notice(title)
        return
    try:
        yearly = df.groupby("Year").size()
        if yearly.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(yearly.index, yearly.values, alpha=0.5)
        ax.set_title(title)
        ax.set_xlabel("Year")
        ax.set_ylabel("Crimes")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# CRIME TYPE CHARTS
# ─────────────────────────────────────────────

def plot_bar_chart(df):
    title = "Top 10 Crime Types"
    if not _required_cols(df, ["Primary Type"]):
        _empty_notice(title)
        return
    try:
        top_crimes = df["Primary Type"].value_counts().head(10)
        if top_crimes.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=top_crimes.values, y=top_crimes.index, ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_pie_chart(df):
    title = "Top 5 Crime Categories"
    if not _required_cols(df, ["Primary Type"]):
        _empty_notice(title)
        return
    try:
        crime_counts = df["Primary Type"].value_counts().head(5)
        if crime_counts.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(crime_counts, labels=crime_counts.index, autopct="%1.1f%%")
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# DISTRIBUTION CHARTS
# ─────────────────────────────────────────────

def plot_histogram(df):
    title = "Crime Distribution by Year"
    if not _required_cols(df, ["Year"]):
        _empty_notice(title)
        return
    try:
        year_data = df["Year"].dropna()
        if year_data.empty or year_data.nunique() < 2:
            _empty_notice(title, "Not enough year variation to plot histogram.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(data=df, x="Year", bins=10, kde=True, ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_count_plot(df):
    title = "Arrest Distribution"
    if not _required_cols(df, ["Arrest"]):
        _empty_notice(title)
        return
    try:
        if df["Arrest"].dropna().empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.countplot(data=df, x="Arrest", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# DOMESTIC CHARTS
# ─────────────────────────────────────────────

def plot_domestic_count(df):
    title = "Domestic Crime Distribution"
    if not _required_cols(df, ["Domestic"]):
        _empty_notice(title)
        return
    try:
        if df["Domestic"].dropna().empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.countplot(data=df, x="Domestic", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_domestic_trend(df):
    title = "Domestic Crimes Over Years"
    if not _required_cols(df, ["Domestic", "Year"]):
        _empty_notice(title)
        return
    try:
        domestic = (
            df[df["Domestic"] == True]
            .groupby("Year")
            .size()
        )
        if domestic.empty:
            _empty_notice(title, "No domestic crimes in selected filters.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(domestic.index, domestic.values, marker="o")
        ax.set_title(title)
        ax.set_xlabel("Year")
        ax.set_ylabel("Domestic Crime Count")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# DISTRICT CHARTS
# ─────────────────────────────────────────────

def plot_box_plot(df):
    title = "District Crime Distribution"
    if not _required_cols(df, ["District", "Year"]):
        _empty_notice(title)
        return
    try:
        top_districts = df["District"].value_counts().head(10).index
        temp = df[df["District"].isin(top_districts)]
        if temp.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=temp, x="District", y="Year", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_violin_plot(df):
    title = "District Crime Density"
    if not _required_cols(df, ["District", "Year"]):
        _empty_notice(title)
        return
    try:
        top_districts = df["District"].value_counts().head(10).index
        temp = df[df["District"].isin(top_districts)]
        if temp.empty or temp["Year"].dropna().nunique() < 2:
            _empty_notice(title, "Not enough data variation for violin plot.")
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.violinplot(data=temp, x="District", y="Year", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_top_districts(df):
    title = "Top 10 Crime Districts"
    if not _required_cols(df, ["District"]):
        _empty_notice(title)
        return
    try:
        district_counts = df["District"].value_counts().head(10)
        if district_counts.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            x=district_counts.index.astype(str),
            y=district_counts.values,
            ax=ax
        )
        ax.set_title(title)
        ax.set_xlabel("District")
        ax.set_ylabel("Crime Count")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# HEATMAPS
# ─────────────────────────────────────────────

def plot_heatmap(df):
    title = "Correlation Heatmap"
    numeric_cols = ["Beat", "District", "Ward", "Community Area",
                    "Year", "Latitude", "Longitude"]
    available = [c for c in numeric_cols if c in df.columns]
    if len(available) < 2 or df.empty:
        _empty_notice(title, "Not enough numeric columns for correlation.")
        return
    try:
        corr = df[available].dropna(how="all").corr()
        if corr.empty or corr.isnull().all(axis=None):
            _empty_notice(title, "Correlation matrix is empty.")
            return
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_district_heatmap(df):
    title = "District vs Crime Type Heatmap"
    if not _required_cols(df, ["District", "Primary Type"]):
        _empty_notice(title)
        return
    try:
        temp = df.dropna(subset=["District", "Primary Type"])
        if temp.empty:
            _empty_notice(title, "No data after dropping nulls.")
            return

        crosstab = pd.crosstab(temp["District"], temp["Primary Type"])

        if crosstab.empty or crosstab.shape[0] == 0 or crosstab.shape[1] == 0:
            _empty_notice(title, "Cross-tabulation produced no data.")
            return

        # Limit to top 10 crime types to keep the chart readable
        crosstab = crosstab.iloc[:, :10]

        # Guard against all-NaN / all-zero slices (causes fmin error)
        if (crosstab.values == 0).all() or pd.isnull(crosstab.values).all():
            _empty_notice(title, "All values are zero for current filters.")
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(crosstab, cmap="YlOrRd", ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# LOCATION / GEO CHARTS
# ─────────────────────────────────────────────

def plot_location_description(df):
    title = "Top Crime Locations"
    if not _required_cols(df, ["Location Description"]):
        _empty_notice(title)
        return
    try:
        top_locations = df["Location Description"].value_counts().head(10)
        if top_locations.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=top_locations.values, y=top_locations.index, ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_scatter(df):
    title = "Crime Location Scatter Plot"
    if not _required_cols(df, ["Latitude", "Longitude", "Arrest"]):
        _empty_notice(title)
        return
    try:
        temp = df.dropna(subset=["Latitude", "Longitude"])
        if temp.empty:
            _empty_notice(title, "No geo-coded records in the current filters.")
            return
        sample_size = min(5000, len(temp))
        temp = temp.sample(sample_size, random_state=42)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=temp,
            x="Longitude", y="Latitude",
            hue="Arrest", alpha=0.6, ax=ax
        )
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# MONTHLY & HOURLY
# ─────────────────────────────────────────────

def plot_monthly_crimes(df):
    title = "Crimes by Month"
    if not _required_cols(df, ["Date"]):
        _empty_notice(title)
        return
    try:
        temp = df.dropna(subset=["Date"]).copy()
        if temp.empty:
            _empty_notice(title)
            return
        temp["Month"] = temp["Date"].dt.month
        monthly = temp.groupby("Month").size()
        if monthly.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=monthly.index, y=monthly.values, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Month")
        ax.set_ylabel("Crime Count")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


def plot_hourly_crimes(df):
    title = "Crime Occurrence by Hour"
    if not _required_cols(df, ["Date"]):
        _empty_notice(title)
        return
    try:
        temp = df.dropna(subset=["Date"]).copy()
        if temp.empty:
            _empty_notice(title)
            return
        temp["Hour"] = temp["Date"].dt.hour
        hourly = temp.groupby("Hour").size()
        if hourly.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(hourly.index, hourly.values, marker="o")
        ax.set_title(title)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Crime Count")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")


# ─────────────────────────────────────────────
# ARREST RATE
# ─────────────────────────────────────────────

def plot_arrest_by_crime(df):
    title = "Top Crime Types by Arrest Rate"
    if not _required_cols(df, ["Primary Type", "Arrest"]):
        _empty_notice(title)
        return
    try:
        temp = df.dropna(subset=["Primary Type", "Arrest"])
        if temp.empty:
            _empty_notice(title)
            return
        arrest_rate = (
            temp.groupby("Primary Type")["Arrest"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        if arrest_rate.empty:
            _empty_notice(title)
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=arrest_rate.values * 100, y=arrest_rate.index, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Arrest Rate (%)")
        ax.set_ylabel("Crime Type")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        _empty_notice(title, f"Could not render chart: {e}")
