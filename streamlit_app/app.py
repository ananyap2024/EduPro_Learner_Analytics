import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
from src.data_processing import load_clean_data
from src.kpi_calculations import (
    total_enrollments, top_age_group, dominant_gender,
    top_category, top_level, category_popularity,
    age_category_heatmap_data, gender_level_data
)

# ── Palette 1: Demographics (Age Group bar + Gender pie) ─────────────────────
# Slate tones — cool greys with hints of blue, green and steel
DEMO_PALETTE = ["#9DA4CC", "#7B84B0",  "#6A74A5",  "#5C6694"]

# ── Palette 2: Course Charts (Category bar + Level bar) ──────────────────────
# Muted Sage — dusty greens, soft teals, muted olive
COURSE_PALETTE = [ "#5F9EA0","#7FAF8A", "#8FAF85", "#6B9E96", "#A0B89A"]

# ── Blues (heatmap + gender vs course level) ─────────────────────
BLUES_CMAP = "Blues"

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="EduPro Learner Analytics", layout="wide")
st.title("EduPro Learner Analytics Dashboard")
st.markdown("Understand *who* your learners are and *what* they enroll in.")


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return load_clean_data(r"C:\Users\anany\OneDrive\Desktop\Ananya\projects\um-learner_analytics\data\processed\edupro_clean_data.csv")

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
k2.metric("Top Age Group",    top_age_group(fdf)    if len(fdf) > 0 else "—")
k3.metric("Dominant Gender",  dominant_gender(fdf)  if len(fdf) > 0 else "—")
k4.metric("Top Category",     top_category(fdf)     if len(fdf) > 0 else "—")
k5.metric("Top Course Level", top_level(fdf)        if len(fdf) > 0 else "—")

st.divider()

# ── Row 1: Demographics — DEMO_PALETTE ───────────────────────────────────────
st.subheader("Learner Demographics")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Age Group Distribution**")
    age_counts = fdf["AgeGroup"].value_counts().sort_index()
    n = len(age_counts)
    bar_colors = DEMO_PALETTE[:n]          # one warm color per age group bar
    fig, ax = plt.subplots()
    ax.bar(age_counts.index.astype(str), age_counts.values, color=bar_colors)
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Learners")
    st.pyplot(fig); plt.close()

with col2:
    st.markdown("**Gender Distribution**")
    gender_counts = fdf["Gender"].value_counts()
    n = len(gender_counts)
    pie_colors = DEMO_PALETTE[:n]          # same warm palette for pie slices
    fig, ax = plt.subplots()
    ax.pie(gender_counts.values, labels=gender_counts.index,
           autopct="%1.1f%%", colors=pie_colors)
    st.pyplot(fig); plt.close()

st.divider()

# ── Row 2: Course Charts — COURSE_PALETTE ────────────────────────────────────
st.subheader("Course Category & Level Popularity")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Enrollments by Course Category**")
    cat_data = category_popularity(fdf)
    n = len(cat_data)
    # Cycle through COURSE_PALETTE for as many categories as exist
    bar_colors = [COURSE_PALETTE[i % len(COURSE_PALETTE)] for i in range(n)]
    fig, ax = plt.subplots()
    ax.barh(cat_data["CourseCategory"], cat_data["count"], color=bar_colors)
    ax.set_xlabel("Enrollments")
    st.pyplot(fig); plt.close()

with col4:
    st.markdown("**Course Level Distribution**")
    level_counts = fdf["CourseLevel"].value_counts()
    n = len(level_counts)
    bar_colors = COURSE_PALETTE[:n]        # one cool color per level bar
    fig, ax = plt.subplots()
    ax.bar(level_counts.index, level_counts.values, color=bar_colors)
    ax.set_xlabel("Level")
    ax.set_ylabel("Enrollments")
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
        sns.heatmap(heatmap_data, annot=True, fmt=".0f",
                    cmap=BLUES_CMAP, ax=ax)
        ax.set_ylabel("Age Group")
        st.pyplot(fig); plt.close()
    else:
        st.info("No data for selected filters.")

with col6:
    st.markdown("**Gender vs Course Level**")
    gl_data = gender_level_data(fdf)
    if not gl_data.empty:
        n_cols = len(gl_data.columns)
        group_colors = [cm.Blues(0.35 + 0.55 * i / max(n_cols - 1, 1))
                        for i in range(n_cols)]
        fig, ax = plt.subplots()
        gl_data.plot(kind="bar", ax=ax, color=group_colors)
        ax.set_xlabel("Gender")
        ax.set_ylabel("Enrollments")
        ax.legend(title="Level")
        plt.xticks(rotation=0)
        st.pyplot(fig); plt.close()
    else:
        st.info("No data for selected filters.")

st.divider()
st.caption("EduPro Learner Analytics | Data-Driven Course Strategy")