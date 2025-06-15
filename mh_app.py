#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# --- Imports ---
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- MENTAL HEALTH IN TECH ---
st.title("MENTAL HEALTH IN TECH - INSIGHTS BY EVARISTE N.")

# --- Load & Clean Dataset ---
df = pd.read_csv("data.csv")
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")  # Standardize column names

# --- Age Filter ---
age_range = st.slider("Select Age Range", 18, 70, (25, 40), key="age_slider")
filtered = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]

# --- Sidebar Filters ---
st.sidebar.header("Filter Responses")

# Gender filter with 'All' option
gender_options = ['All'] + sorted(filtered['gender'].dropna().unique())
gender_filter = st.sidebar.selectbox("Filter by Gender", gender_options)

# Medical coverage filter with 'All' option
coverage_options = ['All'] + sorted(filtered['medical_coverage'].dropna().unique())
coverage_filter = st.sidebar.selectbox("Has Medical Coverage?", coverage_options)

# Apply gender filter
if gender_filter != 'All':
    filtered = filtered[filtered['gender'] == gender_filter]

# Apply coverage filter
if coverage_filter != 'All':
    filtered = filtered[filtered['medical_coverage'] == coverage_filter]

# --- Visualizations ---

# 1. Mental Health by Country
st.subheader("Mental Health Status by Country (Top 10)")
top_countries = filtered['country'].value_counts().nlargest(10).index
subset = filtered[filtered['country'].isin(top_countries)]
fig, ax = plt.subplots()
sns.countplot(data=subset, y="country", hue="mental_health", ax=ax)
st.pyplot(fig)

# 2. Age Distribution
st.subheader("Age Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered['age'], bins=30, kde=True, ax=ax, color="skyblue")
st.pyplot(fig)

# 3. Gender Breakdown (Pie)
st.subheader("Gender Distribution")
gender_counts = filtered['gender'].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
ax.axis("equal")
st.pyplot(fig)

# 4. Mental Health vs. Tech Company
st.subheader("Mental Health by Tech Company Employment")
fig, ax = plt.subplots()
sns.countplot(data=filtered, x="tech_company", hue="mental_health", ax=ax)
st.pyplot(fig)

# 5. Coworker Discussion vs Mental Health
st.subheader("Discussion with Coworkers vs Mental Health")
fig, ax = plt.subplots()
sns.countplot(data=filtered, x="mh_coworker_discussion", hue="mental_health", ax=ax)
st.pyplot(fig)

