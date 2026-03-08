import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_processing import load_clean_data
from src.kpi_calculations import (
    total_enrollments, top_age_group, dominant_gender,
    top_category, top_level, category_popularity,
    age_category_heatmap_data, gender_level_data
)


# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="EduPro Learner Analytics", layout="wide")
st.title("EduPro Learner Analytics Dashboard")
st.markdown("Understand *who* your learners are and *what* they enroll in.")


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return load_clean_data(r"C:\Users\anany\OneDrive\Desktop\Ananya\projects\learner_analytics\data\processed\edupro_clean_data.csv")

df = load()


# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

age_options = sorted(df["AgeGroup"].dropna().unique().tolist())
selected_ages = st.sidebar.multiselect("Age Groups", age_options, default=age_options)

gender_options = df["Gender"].unique().tolist()
selected_genders = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

category_options = sorted(df["CourseCategory"].unique().tolist())
selected_categories = st.sidebar.multiselect("Course Categories", category_options, default=category_options)

level_options = df["CourseLevel"].unique().tolist()
selected_levels = st.sidebar.multiselect("Course Levels", level_options, default=level_options)


# ── Apply Filters ─────────────────────────────────────────────────────────────
fdf = df[
    (df["AgeGroup"].isin(selected_ages)) &
    (df["Gender"].isin(selected_genders)) &
    (df["CourseCategory"].isin(selected_categories)) &
    (df["CourseLevel"].isin(selected_levels))
]


# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.subheader("Key Performance Indicators")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Enrollments", total_enrollments(fdf))
k2.metric("Top Age Group", top_age_group(fdf) if len(fdf) > 0 else "—")
k3.metric("Dominant Gender", dominant_gender(fdf) if len(fdf) > 0 else "—")
k4.metric("Top Category", top_category(fdf) if len(fdf) > 0 else "—")
k5.metric("Top Course Level", top_level(fdf) if len(fdf) > 0 else "—")

st.divider()


# ── Row 1: Demographics ───────────────────────────────────────────────────────
st.subheader("Learner Demographics")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Age Group Distribution**")
    age_counts = fdf["AgeGroup"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(age_counts.index.astype(str), age_counts.values, color="#4C72B0")
    ax.set_xlabel("Age Group"); ax.set_ylabel("Learners")
    st.pyplot(fig); plt.close()

with col2:
    st.markdown("**Gender Distribution**")
    gender_counts = fdf["Gender"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
           colors=["#4C72B0","#DD8452","#55A868"])
    st.pyplot(fig); plt.close()

st.divider()


# ── Row 2: Course Popularity ──────────────────────────────────────────────────
st.subheader("Course Category & Level Popularity")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Enrollments by Course Category**")
    cat_data = category_popularity(fdf)
    fig, ax = plt.subplots()
    ax.barh(cat_data["CourseCategory"], cat_data["count"], color="#55A868")
    ax.set_xlabel("Enrollments")
    st.pyplot(fig); plt.close()

with col4:
    st.markdown("**Course Level Distribution**")
    level_counts = fdf["CourseLevel"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(level_counts.index, level_counts.values, color="#DD8452")
    ax.set_xlabel("Level"); ax.set_ylabel("Enrollments")
    st.pyplot(fig); plt.close()

st.divider()


# ── Row 3: Cross-Demographic Analysis ────────────────────────────────────────
st.subheader("Demographics × Course Preference")
col5, col6 = st.columns(2)

with col5:
    st.markdown("**Age Group vs Course Category (Heatmap)**")
    heatmap_data = age_category_heatmap_data(fdf)
    if not heatmap_data.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Blues", ax=ax)
        ax.set_ylabel("Age Group")
        st.pyplot(fig); plt.close()
    else:
        st.info("No data for selected filters.")

with col6:
    st.markdown("**Gender vs Course Level**")
    gl_data = gender_level_data(fdf)
    if not gl_data.empty:
        fig, ax = plt.subplots()
        gl_data.plot(kind="bar", ax=ax, colormap="Set2")
        ax.set_xlabel("Gender"); ax.set_ylabel("Enrollments")
        ax.legend(title="Level")
        plt.xticks(rotation=0)
        st.pyplot(fig); plt.close()
    else:
        st.info("No data for selected filters.")

st.divider()
st.caption("EduPro Learner Analytics | Data-Driven Course Strategy")