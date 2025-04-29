# create a fresh env called “wage-viz” with Python 3.11
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from pathlib import Path
import matplotlib.colors as mcolors



# -------------------------------------------------------
# 1. Data loading (cached)
# -------------------------------------------------------
@st.cache_data
def load_data(fp):
    real_df = pd.read_excel(fp, sheet_name="Real wage growth")
    nom_df  = pd.read_excel(fp, sheet_name="Nominal wage")
    return real_df, nom_df

# -------------------------------------------------------
# 2. Pre-processing (also cached so it runs once per file)
# -------------------------------------------------------
@st.cache_data
def preprocess(real_df, nom_df):
    # Keep only the European & Central Asia economies
    real_eu = real_df[real_df["Region"] == "Europe and Central Asia"].copy()
    nom_eu  = nom_df.merge(
        real_df[["country_name", "Region", "Subregion - detailed", "Income group"]],
        left_on="countryname",
        right_on="country_name",
        how="left",
    )
    nom_eu  = nom_eu[nom_eu["Region"] == "Europe and Central Asia"]

    # Years of interest
    real_years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    nom_years  = [2017, 2018, 2019, 2020, 2021, 2022, 2023]

    # ---- 1) Nominal growth by sub-region
    nom_growth = nom_eu[["countryname", "Subregion - detailed", "Income group"]].copy()
    for yr in nom_years[1:]:
        nom_growth[yr] = (nom_eu[yr] / nom_eu[yr - 1] - 1) * 100
    nom_sub_avg = nom_growth.groupby("Subregion - detailed")[nom_years[1:]] \
                            .mean(numeric_only=True) \
                            .sort_index()

    # ---- 2) Real growth by sub-region
    real_subset  = real_eu[["Subregion - detailed", "Income group"] + real_years]
    real_sub_avg = real_subset.groupby("Subregion - detailed")[real_years].mean()

    # ---- 3) Nominal vs real by income group
    nom_income_avg  = nom_growth.groupby("Income group")[nom_years[1:]].mean() \
                                .mean(axis=1)           # 2018-23 average
    real_income_avg = real_subset.groupby("Income group")[real_years].mean() \
                                  .mean(axis=1)

    return {
        "nom_sub_avg":   nom_sub_avg,
        "real_sub_avg":  real_sub_avg,
        "nom_income":    nom_income_avg,
        "real_income":   real_income_avg,
        "nom_years":     nom_years,
        "real_years":    real_years,
    }

# -------------------------------------------------------
# 3. Streamlit UI
# -------------------------------------------------------
def main():
    st.set_page_config(page_title="European Minimum-Wage Growth", layout="centered")
    st.title("European Minimum-Wage Growth Dashboard")

    # ---- File input
    fp = st.text_input("Path to Excel file",
                       value="globalwagereport-2024-25data.xlsx")
    try:
        real_df, nom_df = load_data(fp)
    except Exception as e:
        st.error(f"Could not open file: {e}")
        st.stop()

    data = preprocess(real_df, nom_df)

    # --------------------------------------------------
    #  Plot 1: Nominal growth by sub-region
    # --------------------------------------------------
    st.subheader("1) Nominal minimum-wage growth by European sub-region")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for sub in data["nom_sub_avg"].index:
        ax1.plot(data["nom_years"][1:], data["nom_sub_avg"].loc[sub], label=sub)
    ax1.set_title("Average nominal minimum-wage growth (2018-2023)")
    ax1.set_xlabel("Year"); ax1.set_ylabel("Growth rate (%)")
    ax1.legend()
    st.pyplot(fig1)

    st.markdown("""
    **Nominal Minimum-Wage Growth (2018 – 2023)**  
    Central Asia had the highest wage growth, but it was **very unstable**.  
    Eastern Europe also grew faster than Western and Northern Europe, which stayed **low and steady**.  
    ➡️ *Some regions raised minimum wages quickly, but not evenly across Europe.*
    """)

    # --------------------------------------------------
    #  Plot 2: Real growth by sub-region
    # --------------------------------------------------
    st.subheader("2) Real minimum-wage growth by European sub-region")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for sub in data["real_sub_avg"].index.sort_values():
        ax2.plot(data["real_years"], data["real_sub_avg"].loc[sub], label=sub)
    ax2.set_title("Average real minimum-wage growth (2017-2023)")
    ax2.set_xlabel("Year"); ax2.set_ylabel("Growth rate (%)")
    ax2.legend()
    st.pyplot(fig2)

    st.markdown("""
    **Real Minimum-Wage Growth (2017 – 2023)**  
    After adjusting for inflation, wage growth was **much lower**.  
    Many regions—especially Eastern and Northern Europe—*lost ground* in 2022 as inflation spiked.  
    ➡️ *Even when wages rose on paper, people in many countries could actually afford less.*
    """)

    # --------------------------------------------------
    #  Plot 3: Nominal vs real by income group
    # --------------------------------------------------
    st.subheader("3) Nominal vs real growth by income group (avg. 2017-2023)")
    inc_groups = data["nom_income"].index
    x = range(len(inc_groups))

    fig3, ax3 = plt.subplots(figsize=(7, 5))
    ax3.bar(x,                         data["nom_income"].values,
            width=0.4, label="Nominal", align="center")
    ax3.bar([i+0.4 for i in x],        data["real_income"].reindex(inc_groups).values,
            width=0.4, label="Real",    align="center")
    ax3.set_xticks([i+0.2 for i in x]); ax3.set_xticklabels(inc_groups)
    ax3.set_ylabel("Average growth rate (%)")
    ax3.set_title("Nominal vs real minimum-wage growth by income group")
    ax3.legend()
    st.pyplot(fig3)

if __name__ == "__main__":
    main()



st.markdown("""
**Nominal vs Real Growth by Income Group**  
*Lower-middle-income* countries posted the **biggest jump** in nominal wages but only **small real gains**.  
*High-income* countries saw steadier but smaller changes.  
➡️ *Lower-income countries raised wages faster, but inflation took away much of the benefit.*
""")