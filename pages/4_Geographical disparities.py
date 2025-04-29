# europe_wage_map_app.py
# ───────────────────────────────────────────────────────────────
# 0. PAGE CONFIG  – must be first Streamlit command
import pandas as pd
import folium
import geopandas as gpd
import requests
import zipfile
import io
import os
import streamlit as st
st.set_page_config(
    page_title="Average Annual Wage-Growth Map • Europe (2017-2023)",
    layout="centered"
)

# ───────────────────────────────────────────────────────────────
# 1. IMPORTS & DATA LOADERS
# ───────────────────────────────────────────────────────────────
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

@st.cache_data
def load_wage_data(xlsx_path="globalwagereport-2024-25data.xlsx"):
    df = pd.read_excel(xlsx_path, sheet_name="Real wage growth")
    cols = ["country_name", 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    df = df[cols].dropna(subset=[2017, 2023]).copy()
    df["Total_Growth_Rate"] = ((df[2023] - df[2017]) / df[2017]) * 100
    df["Avg_Annual_Growth_Rate"] = df["Total_Growth_Rate"] / 6
    return df

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    return gpd.read_file(url)

wage_df = load_wage_data()
world   = load_geojson()

europe_set = {
    'Albania','Andorra','Austria','Belarus','Belgium','Bosnia and Herzegovina',
    'Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland',
    'France','Germany','Greece','Hungary','Iceland','Ireland','Italy','Kosovo',
    'Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Moldova','Monaco',
    'Montenegro','Netherlands','North Macedonia','Norway','Poland','Portugal',
    'Romania','San Marino','Serbia','Slovakia','Slovenia','Spain','Sweden',
    'Switzerland','Ukraine','United Kingdom'
}
europe = world[world["name"].isin(europe_set)].copy()

merged = europe.merge(wage_df, left_on="name", right_on="country_name", how="left")

# ───────────────────────────────────────────────────────────────
# 2. SIDEBAR FILTERS
# ───────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
min_rate, max_rate = float(merged["Avg_Annual_Growth_Rate"].min()), float(merged["Avg_Annual_Growth_Rate"].max())
rate_range = st.sidebar.slider(
    "Avg. annual wage-growth range (%)",
    min_value=round(min_rate,1), max_value=round(max_rate,1),
    value=(round(min_rate,1), round(max_rate,1))
)
merged["filter_flag"] = merged["Avg_Annual_Growth_Rate"].between(*rate_range)

# ───────────────────────────────────────────────────────────────
# 3. BUILD FOLIUM MAP
# ───────────────────────────────────────────────────────────────
m = folium.Map(location=[54, 15], zoom_start=4, tiles="cartodbpositron")

folium.Choropleth(
    geo_data=merged,
    data=merged[merged["filter_flag"]],
    columns=["name", "Avg_Annual_Growth_Rate"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.8,
    line_opacity=0.2,
    nan_fill_color="lightgrey",
    legend_name="Average Annual Real-Wage Growth (2017-2023, %)",
    name="Wage growth"
).add_to(m)

folium.GeoJson(
    merged,
    style_function=lambda _: {"fillOpacity": 0, "color": "transparent"},
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "Avg_Annual_Growth_Rate"],
        aliases=["Country", "Avg annual growth (%)"],
        localize=True,
        sticky=False
    )
).add_to(m)

# ───────────────────────────────────────────────────────────────
# 4. DISPLAY MAP & DATA TABLE
# ───────────────────────────────────────────────────────────────
st_folium(m, width=800, height=600)

with st.expander("Show data table"):
    st.dataframe(
        merged[["name", "Avg_Annual_Growth_Rate"]]
          .rename(columns={"name": "Country", "Avg_Annual_Growth_Rate": "Avg Annual Growth (%)"})
          .sort_values("Avg Annual Growth (%)", ascending=False),
        use_container_width=True
    )
# ───────────────────────────────────────────────────────────────
# 5. Key geographic take-aways
# ───────────────────────────────────────────────────────────────
st.markdown(
    """
### Geographic patterns in wage growth (Europe, 2017 – 2023)

- **Eastern Europe** – *Romania, Bulgaria, Poland, etc.*  
  Higher annual real-wage growth, reflecting rapid economic catch-up and labour-market convergence with Western Europe.

- **Western Europe** – *Germany, France, United Kingdom*  
  Moderate growth rates typical of mature, high-productivity economies.

- **Southern Europe** – *Greece, Italy, Spain*  
  Low or stagnant wage growth, still contending with post-crisis structural headwinds.

- **Nordic countries** – *Sweden, Denmark, Finland, Norway*  
  Steady mid-range growth, consistent with their high-income, high-wage equilibrium.

**Interpretation**

Regional differences suggest that wage outcomes are shaped not only by overall economic expansion but also by labour-market institutions, policy choices, and the pace of post-pandemic recovery. Faster growth in the East signals continuing convergence, while the South’s sluggishness points to the need for further structural reforms.
    """
)
