import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

sns.set_style("whitegrid")


def plot_line_chart(df):
    fig, ax = plt.subplots(figsize=(8, 4))

    yearly = df.groupby("Year").size()

    ax.plot(yearly.index, yearly.values, marker="o")
    ax.set_title("Crime Trend Over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Crimes")

    st.pyplot(fig)


def plot_area_chart(df):
    fig, ax = plt.subplots(figsize=(8, 4))

    yearly = df.groupby("Year").size()

    ax.fill_between(
        yearly.index,
        yearly.values,
        alpha=0.5
    )

    ax.set_title("Crime Volume Area Chart")
    ax.set_xlabel("Year")
    ax.set_ylabel("Crimes")

    st.pyplot(fig)


def plot_bar_chart(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    top_crimes = (
        df["Primary Type"]
        .value_counts()
        .head(10)
    )

    sns.barplot(
        x=top_crimes.values,
        y=top_crimes.index,
        ax=ax
    )

    ax.set_title("Top 10 Crime Types")

    st.pyplot(fig)


def plot_pie_chart(df):
    fig, ax = plt.subplots(figsize=(7, 7))

    crime_counts = (
        df["Primary Type"]
        .value_counts()
        .head(5)
    )

    ax.pie(
        crime_counts,
        labels=crime_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Top 5 Crime Categories")

    st.pyplot(fig)


def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(8, 4))

    sns.histplot(
        data=df,
        x="Year",
        bins=10,
        kde=True,
        ax=ax
    )

    ax.set_title("Crime Distribution by Year")

    st.pyplot(fig)


def plot_count_plot(df):
    fig, ax = plt.subplots(figsize=(7, 4))

    sns.countplot(
        data=df,
        x="Arrest",
        ax=ax
    )

    ax.set_title("Arrest Distribution")

    st.pyplot(fig)


def plot_domestic_count(df):
    fig, ax = plt.subplots(figsize=(7, 4))

    sns.countplot(
        data=df,
        x="Domestic",
        ax=ax
    )

    ax.set_title("Domestic Crime Distribution")

    st.pyplot(fig)


def plot_box_plot(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    districts = (
        df["District"]
        .value_counts()
        .head(10)
        .index
    )

    temp = df[df["District"].isin(districts)]

    sns.boxplot(
        data=temp,
        x="District",
        y="Year",
        ax=ax
    )

    ax.set_title("District Crime Distribution")

    st.pyplot(fig)


def plot_violin_plot(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    districts = (
        df["District"]
        .value_counts()
        .head(10)
        .index
    )

    temp = df[df["District"].isin(districts)]

    sns.violinplot(
        data=temp,
        x="District",
        y="Year",
        ax=ax
    )

    ax.set_title("District Crime Density")

    st.pyplot(fig)


def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(8, 6))

    numeric_cols = [
        "Beat",
        "District",
        "Ward",
        "Community Area",
        "Year",
        "Latitude",
        "Longitude"
    ]

    corr = df[numeric_cols].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    st.pyplot(fig)


def plot_scatter(df):
    temp = df.dropna(
        subset=["Latitude", "Longitude"]
    ).sample(
        min(5000, len(df)),
        random_state=42
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=temp,
        x="Longitude",
        y="Latitude",
        hue="Arrest",
        alpha=0.6,
        ax=ax
    )

    ax.set_title("Crime Location Scatter Plot")

    st.pyplot(fig)


def plot_top_districts(df):
    fig, ax = plt.subplots(figsize=(8, 5))

    district_counts = (
        df["District"]
        .value_counts()
        .head(10)
    )

    sns.barplot(
        x=district_counts.index.astype(str),
        y=district_counts.values,
        ax=ax
    )

    ax.set_title("Top 10 Crime Districts")
    ax.set_xlabel("District")
    ax.set_ylabel("Crime Count")

    st.pyplot(fig)


def plot_location_description(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    top_locations = (
        df["Location Description"]
        .value_counts()
        .head(10)
    )

    sns.barplot(
        x=top_locations.values,
        y=top_locations.index,
        ax=ax
    )

    ax.set_title("Top Crime Locations")

    st.pyplot(fig)

# MONTHLY CRIME ANALYSIS

def plot_monthly_crimes(df):

    temp = df.copy()

    temp = temp.dropna(subset=["Date"])

    temp["Month"] = temp["Date"].dt.month

    monthly = temp.groupby("Month").size()

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.barplot(
        x=monthly.index,
        y=monthly.values,
        ax=ax
    )

    ax.set_title("Crimes by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Crime Count")

    st.pyplot(fig)

# HOURLY CRIME ANALYSIS

def plot_hourly_crimes(df):

    temp = df.copy()

    temp = temp.dropna(subset=["Date"])

    temp["Hour"] = temp["Date"].dt.hour

    hourly = temp.groupby("Hour").size()

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        hourly.index,
        hourly.values,
        marker="o"
    )

    ax.set_title("Crime Occurrence by Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Crime Count")

    st.pyplot(fig)

# ARREST RATE BY CRIME TYPE

def plot_arrest_by_crime(df):

    temp = df.copy()

    temp = temp.dropna(
        subset=["Primary Type", "Arrest"]
    )

    arrest_rate = (
        temp.groupby("Primary Type")["Arrest"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=arrest_rate.values * 100,
        y=arrest_rate.index,
        ax=ax
    )

    ax.set_title("Top Crime Types by Arrest Rate")
    ax.set_xlabel("Arrest Rate (%)")
    ax.set_ylabel("Crime Type")

    st.pyplot(fig)

# DOMESTIC CRIME TREND

def plot_domestic_trend(df):

    temp = df.copy()

    domestic = (
        temp[temp["Domestic"] == True]
        .groupby("Year")
        .size()
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        domestic.index,
        domestic.values,
        marker="o"
    )

    ax.set_title("Domestic Crimes Over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Domestic Crime Count")

    st.pyplot(fig)

# DISTRICT VS CRIME TYPE HEATMAP

def plot_district_heatmap(df):

    temp = pd.crosstab(
        df["District"],
        df["Primary Type"]
    )

    temp = temp.iloc[:, :10]

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        temp,
        cmap="YlOrRd",
        ax=ax
    )

    ax.set_title(
        "District vs Crime Type Heatmap"
    )

    st.pyplot(fig)