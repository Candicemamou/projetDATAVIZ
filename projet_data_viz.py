import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import missingno as msno
import pycountry
import plotly.express as px

st.set_page_config(page_title="In-work Poverty in Europe", layout="wide")
st.markdown("<p style='font-size:13px; color:black;'>Candice Mamou</p>", unsafe_allow_html=True)

st.title("In-work at-risk-of-poverty in Europe")


st.markdown("""
#EFREIDataStories2025  
#EFREIParis #DataVisualization #Streamlit #DataStorytelling #OpenData #StudentProjects  
#DataViz #DataAnalytics #DataScience #MachineLearning #AI #BigData #Python  
#DashboardDesign #VisualStorytelling #InformationDesign #InsightDriven #DataCulture  
#CareerInData #DataProfessionals #LinkedInLearning #TechCommunity #OpenData #PublicData
""")


st.markdown("> Explore how employment and income inequality interact across Europe (2005–2024).")

st.caption("Source: Eurostat (EU-SILC) — data.europa.eu — Open data license")

st.markdown("""
###  About this dataset

This dataset comes from **Eurostat’s EU-SILC survey**.  
It measures the **share of employed people** whose **disposable income** (after taxes and social transfers)  
is **below 60% of their country’s median income**.  

In other words, it shows how many people are **“working poor”** — employed but still living **at risk of poverty**.  

Data are:
- **Annual** (each row = one year),
- broken down by **country**, **sex**, and **age group**,
- measured in **percent (PC)**,
- focused on people with work status **EMP** (employed).
""")

# Load and clean dataset
#skeleton required by the teacher

from pathlib import Path
import pandas as pd
import streamlit as st

from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(src: str | None = None, cache_version: int = 1):
    # 1) URL passée en argument (utile pour tester une URL raw GitHub)
    if src:
        return pd.read_csv(src, sep=None, engine="python", encoding="utf-8")

    # 2) Fichier local, d’abord à côté du script, puis dans le cwd
    try:
        here = Path(__file__).parent
    except NameError:
        # fallback ultra-robuste si __file__ n'est pas défini
        here = Path.cwd()

    candidates = [
        here / "estat_ilc_iw01_en.csv",
        Path("estat_ilc_iw01_en.csv"),
    ]
    for p in candidates:
        if p.exists():
            return pd.read_csv(p, sep=None, engine="python", encoding="utf-8")

    # 3) Secret optionnel (Manage app → Settings → Secrets)
    url = st.secrets.get("DATA_URL", "")
    if url:
        return pd.read_csv(url, sep=None, engine="python", encoding="utf-8")

    # 4) Message clair si rien trouvé
    st.error("❌ CSV introuvable. Place `estat_ilc_iw01_en.csv` dans le repo (même dossier que ce script) "
             "ou ajoute `DATA_URL` dans Secrets avec le lien vers le CSV.")
    st.stop()

# IMPORTANT : change le numéro pour invalider le cache après modif
raw = load_data(cache_version=2)


df = raw.copy()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
df = df[~df["geo"].str.startswith(("EA", "EU", "EFTA"))]

# Basic info
st.subheader("Basic information")
st.write("**Rows:**", len(df))
st.write("**Columns:**", len(df.columns))
st.write("**Total missing values:**", int(df.isna().sum().sum()))

# Missing values (compact visual)

st.subheader("How complete is the dataset?")
st.caption("You can filter by country, sex, age, and year using the left menu.")
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

if df.isna().sum().sum() > 0:
    completeness = df.notna().mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(3, 0.8), dpi=1000)  # 👈 résolution augmentée
    ax.bar(
        completeness.index,
        completeness.values,
        color="skyblue"
    )
    ax.set_ylim(0, 1.05)
    ax.set_title("Data completeness per column", fontsize=6)
    ax.tick_params(axis='x', labelrotation=45, labelsize=5)
    ax.tick_params(axis='y', labelsize=5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    st.pyplot(fig, clear_figure=True)


# Column description

st.subheader("Meaning of columns (in English)")
st.markdown("""
- **dataflow** — Eurostat table ID (metadata)  
- **last_update** — Last update date in Eurostat  
- **freq** — Frequency: A = annual  
- **wstatus** — Work status: EMP = employed  
- **sex** — M (male), F (female), T (total)  
- **age** — Age group (Y18-24, Y25-54, Y55-64, TOTAL)  
- **unit** — PC = percent  
- **geo** — Country code (FR, DE, ES, etc.)  
- **time_period** — Year of observation  
- **obs_value** — % of working poor  
- **obs_flag** — Data quality flag  
- **conf_status** — Validation status
""")

# Drop useless columns and fill missing values

df = df.drop(df.columns[:2], axis=1)
if "obs_value" in df.columns:
    df["obs_value"] = df["obs_value"].fillna(df["obs_value"].median())
if "conf_status" in df.columns:
    df["conf_status"] = df["conf_status"].fillna("unknown")
if "obs_flag" in df.columns:
    df["obs_flag"] = df["obs_flag"].fillna("OK")

df["year"] = pd.to_datetime(df["time_period"].astype(str), errors="coerce").dt.year
df = df.drop(columns=["time_period"], errors="ignore")

# --- DATA PREVIEW --- #
st.markdown("## Explore the dataset")

st.caption("Here’s a preview of the cleaned and filtered dataset used in this dashboard:")

# Select a few filters to preview



# Filter and rename ages

valid_ages = ["TOTAL", "Y18-24", "Y25-54", "Y55-64"]
df = df[df["age"].isin(valid_ages)]
age_labels = {
    "TOTAL": "All ages",
    "Y18-24": "18–24 years",
    "Y25-54": "25–54 years",
    "Y55-64": "55–64 years"
}
df["age_label"] = df["age"].map(age_labels)
df = df.drop(columns=["age"], errors="ignore")

cols_to_drop = ["wstatus", "unit", "freq", "conf_status"]
df = df.drop(columns=cols_to_drop, errors="ignore")


# Replace country codes with full country names

import pycountry

# Clean country codes
df["geo"] = df["geo"].astype(str).str.strip().str.upper()

# Handle special Eurostat codes manually
SPECIAL_NAME = {
    "EL": "Greece",          # Eurostat uses EL for Greece
    "UK": "United Kingdom",  # sometimes used instead of GB
    "XK": "Kosovo",          # optional, appears in some datasets
}

SPECIAL_ISO3 = {
    "EL": "GRC",
    "UK": "GBR",
    "XK": "XKX",
}

def country_name(code: str) -> str:
    """Convert a 2-letter country code to full country name."""
    if code in SPECIAL_NAME:
        return SPECIAL_NAME[code]
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code

def to_iso3(code: str) -> str:
    """Convert a 2-letter country code to ISO3 code for map visualization."""
    if code in SPECIAL_ISO3:
        return SPECIAL_ISO3[code]
    country = pycountry.countries.get(alpha_2=code)
    return country.alpha_3 if country else None

# Apply mapping to dataset
df["country"] = df["geo"].apply(country_name)


# Keep only reliable countries ( the one with at least 5 years of data)
min_years = 5
country_counts = df.groupby("country")["year"].nunique()
good_countries = country_counts[country_counts >= min_years].index
df = df[df["country"].isin(good_countries)]

# -- Sidebar filters

# Preview table controls
preview_country = st.selectbox("Select a country to preview:", sorted(df["country"].unique()))
preview_year = st.slider(
    "Select year for preview:",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

df_preview = df[(df["country"] == preview_country) & (df["year"] == preview_year)]
st.dataframe(df_preview.head(10), use_container_width=True)


st.sidebar.header("Filters")

countries = sorted(df["country"].dropna().unique().tolist())
sexes = sorted(df["sex"].dropna().unique().tolist())
ages = sorted(df["age_label"].dropna().unique().tolist())
years = sorted(df["year"].dropna().unique().tolist())

selected_country = st.sidebar.selectbox("Select a country:", countries)
selected_sex = st.sidebar.selectbox("Select sex:", sexes)
selected_age_label = st.sidebar.selectbox("Select age group:", ages)

selected_year = st.sidebar.slider(
    "Select year:",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=int(max(years)),
    step=1
)

selected_countries_multi = st.sidebar.multiselect(
    "Select countries for line charts:",
    countries,
    default=[selected_country]
)

# ---------- CLICKABLE SUMMARY (TABS) ----------
tabs = st.tabs([
    "What are the main indicators?",
    "How has in-work poverty evolved over time?",
    "How does this compare to the European average?",
    "Which countries are most and least affected?",
    "Are there gender differences in in-work poverty?",
    "Which age groups are most at risk?",
    "Did economic crises worsen in-work poverty?",
    "Is there a North–South or East–West divide?",
    "Where in Europe is in-work poverty highest?",
    "What can we learn from this?"
])

# KPI — key indicators, as requested 
with tabs[0]:
    st.markdown("## What are the main indicators?")

    # KPIs at the selected single year (clearer than averaging a range)
    eu_avg = df[(df["sex"] == selected_sex) & (df["age_label"] == selected_age_label) & (df["year"] == selected_year)]["obs_value"].mean()

    country_avg = df[
        (df["country"] == selected_country) &
        (df["sex"] == selected_sex) &
        (df["age_label"] == selected_age_label) &
        (df["year"] == selected_year)
    ]["obs_value"].mean()

    diff = country_avg - eu_avg

    col1, col2, col3 = st.columns(3)
    col1.metric(f"EU in {selected_year} (%)", f"{eu_avg:.1f}" if pd.notna(eu_avg) else "—")
    col2.metric(f"{selected_country} in {selected_year} (%)", f"{country_avg:.1f}" if pd.notna(country_avg) else "—")
    col3.metric("Difference vs EU", f"{diff:+.1f}" if pd.notna(diff) else "—")

# 1. Evolution over time
with tabs[1]:
    st.markdown("## How has in-work poverty evolved over time?")
    st.caption("Filters: countries (multiselect), sex, age.")

    # Build a line for each selected country
    fig, ax = plt.subplots(figsize=(6, 3))
    for c in selected_countries_multi:
        trend = (
            df[(df["country"] == c) &
               (df["sex"] == selected_sex) &
               (df["age_label"] == selected_age_label)]
            .groupby("year")["obs_value"].mean().reset_index()
        )
        if not trend.empty:
            ax.plot(trend["year"], trend["obs_value"], marker="o", linewidth=2, label=c)

    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("In-work poverty rate (%)", fontsize=9)
    ax.set_title(f"Trend over time — {selected_sex}, {selected_age_label}", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(ncols=2, fontsize=8)
    st.pyplot(fig)

# 2. Comparison with EU average
with tabs[2]:
    st.markdown("### How does this compare to the European average?")
    st.caption("Filters: countries (multiselect), sex, age group.")

    eu_trend = (
        df[(df["sex"] == selected_sex) & (df["age_label"] == selected_age_label)]
        .groupby("year")["obs_value"].mean().reset_index()
    )

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(eu_trend["year"], eu_trend["obs_value"], label="EU average", color="gray", linestyle="--")

    for c in selected_countries_multi:
        trend = (
            df[(df["country"] == c) &
               (df["sex"] == selected_sex) &
               (df["age_label"] == selected_age_label)]
            .groupby("year")["obs_value"].mean().reset_index()
        )
        if not trend.empty:
            ax.plot(trend["year"], trend["obs_value"], marker="o", label=c)

    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("In-work poverty rate (%)", fontsize=9)
    ax.set_title(f"Countries vs EU average — {selected_sex}, {selected_age_label}", fontsize=10)
    ax.legend(ncols=2, fontsize=8)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# 3.Comparison between countries
with tabs[3]:
    st.markdown("## Which countries are most and least affected?")
    st.caption("Filters: sex, age group, and selected year.")

    year_for_comparison = selected_year  

    df_compare = (
        df[(df["year"] == year_for_comparison) &
           (df["sex"] == selected_sex) &
           (df["age_label"] == selected_age_label)]
        .dropna(subset=["obs_value"])
        .groupby("country")["obs_value"]
        .mean()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df_compare.index, df_compare.values, color="mediumseagreen", edgecolor="none")
    ax.set_xlabel("In-work poverty rate (%)", fontsize=9)
    ax.set_ylabel("Country", fontsize=9)
    ax.set_title(f"In-work poverty by country — {year_for_comparison}", fontsize=10)
    st.pyplot(fig)

# 4. Gender gap 
with tabs[4]:
    st.markdown("## Are there gender differences in in-work poverty?")
    st.caption("Filters: country and age group.")

    df_gender = (
        df[(df["country"] == selected_country) &
           (df["age_label"] == selected_age_label) &
           (df["sex"].isin(['M', 'F']))]
        .groupby(["year", "sex"])["obs_value"].mean().reset_index()
    )

    if not df_gender.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        for sex in df_gender["sex"].unique():
            sub = df_gender[df_gender["sex"] == sex]
            ax.plot(sub["year"], sub["obs_value"], marker="o", label="Male" if sex == "M" else "Female")
        ax.legend(title="Sex")
        ax.set_xlabel("Year", fontsize=9)
        ax.set_ylabel("In-work poverty rate (%)", fontsize=9)
        ax.set_title(f"Gender gap in {selected_country}", fontsize=10)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# 5. Age group comparison
with tabs[5]:
    st.markdown("## Which age groups are most at risk?")
    st.caption("Filters: country and sex.")

    latest_year = int(df["year"].max())
    df_age = (
        df[(df["country"] == selected_country) &
           (df["year"] == latest_year) &
           (df["sex"] == selected_sex)]
        .groupby("age_label")["obs_value"]
        .mean()
        .reset_index()
    )

    if not df_age.empty:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(df_age["age_label"], df_age["obs_value"], color="orange", edgecolor="none")
        ax.set_ylabel("In-work poverty rate (%)", fontsize=9)
        ax.set_xlabel("Age group", fontsize=9)
        ax.set_title(f"In-work poverty by age — {selected_country}, {latest_year}", fontsize=10)
        st.pyplot(fig)

with tabs[6]:
    st.markdown("## Did economic crises worsen in-work poverty?")
    st.caption("How did in-work poverty rates react after 2008 (financial crisis), 2020 (COVID), and 2022 (inflation shock)?")

    # EU average over time
    eu_crisis = (
        df.groupby("year")["obs_value"]
        .mean()
        .reset_index()
        .sort_values("year")
    )

    # Preview table
    st.write("### Average EU in-work poverty rate by year")
    st.dataframe(eu_crisis)

    # Plot with shaded crisis periods
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(eu_crisis["year"], eu_crisis["obs_value"], color="royalblue", marker="o", linewidth=2)
    ax.set_title("EU Average In-Work Poverty Rate (2005–2024)", fontsize=10)
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate (%)")

    # Highlight crisis periods
    ax.axvspan(2008, 2010, color="red", alpha=0.1, label="Financial crisis")
    ax.axvspan(2020, 2021, color="orange", alpha=0.15, label="COVID-19")
    ax.axvspan(2022, 2023, color="purple", alpha=0.1, label="Inflation")

    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)
    st.pyplot(fig)

with tabs[7]:
    st.markdown("## Is there a North–South or East–West divide in Europe?")
    st.caption("Grouping countries into broad European regions to compare average in-work poverty rates.")

    # Manual region mapping
    region_map = {
        "North": ["DK", "FI", "SE", "NO", "IS"],
        "West": ["FR", "BE", "DE", "NL", "LU", "AT", "IE", "UK"],
        "South": ["ES", "IT", "PT", "GR", "MT", "CY"],
        "East": ["PL", "CZ", "SK", "HU", "RO", "BG", "EE", "LV", "LT", "SI", "HR"]
    }

    def assign_region(code):
        for region, codes in region_map.items():
            if code in codes:
                return region
        return "Other"

    df["region"] = df["geo"].apply(assign_region)

    # Choose year (reuse main one)
    year_region = selected_year

    df_region = (
        df[df["year"] == year_region]
        .groupby("region")["obs_value"]
        .mean()
        .reset_index()
        .sort_values("obs_value", ascending=False)
    )

    # Preview table
    st.write(f"### Regional averages in {year_region}")
    st.dataframe(df_region)

    # Plot comparison
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(df_region["region"], df_region["obs_value"], color="teal", edgecolor="none")
    ax.set_xlabel("European region")
    ax.set_ylabel("In-work poverty rate (%)")
    ax.set_title(f"Average In-Work Poverty by Region — {year_region}")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

# 6.Map of Europe
with tabs[8]:
    st.markdown("## Where in Europe is in-work poverty highest?")
    st.caption("Filters: sex, age group, and year.")

    year_for_map = selected_year

    df_map = (
        df[(df["year"] == year_for_map) &
           (df["sex"] == selected_sex) &
           (df["age_label"] == selected_age_label)]
        .dropna(subset=["obs_value"])
    )

    df_map["iso3"] = df_map["geo"].apply(to_iso3)
    df_map = df_map.dropna(subset=["iso3"])

    if not df_map.empty:
        fig = px.choropleth(
            df_map,
            locations="iso3",
            color="obs_value",
            hover_name="country",
            color_continuous_scale="Reds",
            title=f"In-work poverty across Europe — {year_for_map}",
            scope="europe"
        )
        fig.update_layout(width=1000, height=600, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

# 7.Conclusion
with tabs[9]:
    st.markdown("## What can we learn from this?")

    # Recalcul local (scope) des KPI pour l'année sélectionnée
    eu_avg_c = df[
        (df["sex"] == selected_sex) &
        (df["age_label"] == selected_age_label) &
        (df["year"] == selected_year)
    ]["obs_value"].mean()

    country_avg_c = df[
        (df["country"] == selected_country) &
        (df["sex"] == selected_sex) &
        (df["age_label"] == selected_age_label) &
        (df["year"] == selected_year)
    ]["obs_value"].mean()

    diff_c = country_avg_c - eu_avg_c

    st.success(f"""
**Main findings ({selected_year}):**
- EU average: **{eu_avg_c:.1f}%**
- {selected_country}: **{country_avg_c:.1f}%**
- Difference vs EU: **{diff_c:+.1f} points**
""")

    st.markdown("### Fun facts :")
    st.info(
        "**Did you know?**\n"
        "- Even full-time workers can be at risk of poverty if wages are below living standards.\n"
        "- In 2022, over 9% of employed people in the EU were still living at risk of poverty.\n"
        "- Nordic countries tend to have the lowest in-work poverty rates in Europe.\n"
        "- Gender gaps in poverty are often linked to part-time work and care responsibilities."
    )
