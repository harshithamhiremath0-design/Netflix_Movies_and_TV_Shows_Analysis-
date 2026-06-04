import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils.load_data import load_data
from utils.charts import (
    movies_vs_tv,
    release_year_chart,
    top_countries,
    rating_chart
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎬 Netflix Analytics Dashboard")
st.markdown("Detailed Data Analysis using Streamlit")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.sidebar.file_uploader(
    "Upload Netflix Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = load_data(uploaded_file)

    st.sidebar.success("Dataset Loaded Successfully")

    # ----------------------------------------------
    # SIDEBAR FILTERS
    # ----------------------------------------------

    st.sidebar.header("Filters")

    content_type = st.sidebar.multiselect(
        "Select Type",
        options=df["type"].unique(),
        default=df["type"].unique()
    )

    df = df[df["type"].isin(content_type)]

    # ----------------------------------------------
    # KPI SECTION
    # ----------------------------------------------

    total_titles = len(df)

    total_movies = len(df[df["type"] == "Movie"])

    total_tv = len(df[df["type"] == "TV Show"])

    total_countries = df["country"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Titles", total_titles)

    col2.metric("Movies", total_movies)

    col3.metric("TV Shows", total_tv)

    col4.metric("Countries", total_countries)

    st.divider()

    # ----------------------------------------------
    # CHARTS
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            movies_vs_tv(df),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            rating_chart(df),
            use_container_width=True
        )

    st.plotly_chart(
        release_year_chart(df),
        use_container_width=True
    )

    st.plotly_chart(
        top_countries(df),
        use_container_width=True
    )

    # ----------------------------------------------
    # TOP GENRES
    # ----------------------------------------------

    st.subheader("Top Genres")

    genres = (
        df['listed_in']
        .str.split(',')
        .explode()
        .value_counts()
        .head(15)
    )

    fig = px.bar(
        x=genres.index,
        y=genres.values,
        labels={'x':'Genre','y':'Count'}
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------
    # WORD CLOUD
    # ----------------------------------------------

    st.subheader("Description Word Cloud")

    text = " ".join(df["description"].astype(str))

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="black"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)

    # ----------------------------------------------
    # DATA PREVIEW
    # ----------------------------------------------

    st.subheader("Dataset Preview")

    st.dataframe(df)

else:

    st.info("Upload Netflix CSV Dataset")
