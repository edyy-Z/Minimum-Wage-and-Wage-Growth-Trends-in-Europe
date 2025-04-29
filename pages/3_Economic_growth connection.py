# gdp_wage_app.py
# ───────────────────────────────────────────────────────────────
# 0. Page-wide settings  (must be the first Streamlit command)
# ───────────────────────────────────────────────────────────────
import streamlit as st
st.set_page_config(
    page_title="GDP Growth vs. Real Wage Growth (Europe, 2017-2023)",
    layout="centered"
)

# ───────────────────────────────────────────────────────────────
# 1. Imports & data loading
# ───────────────────────────────────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data(
    wage_path: str = "globalwagereport-2024-25data.xlsx",
    gdp_path: str  = "API_NY.GDP.MKTP.KD_DS2_en_csv_v2_19406.csv"
):
    # 1-A  Real wage growth
    real_df = pd.read_excel(wage_path, sheet_name="Real wage growth")
    real_eu = real_df[real_df["Region"] == "Europe and Central Asia"].copy()
    real_years = list(range(2017, 2024))
    real_eu["real_wage_growth_avg"] = real_eu[real_years].mean(axis=1)
    wage_avg = real_eu[["country_name", "real_wage_growth_avg"]]

    # 1-B  GDP growth
    gdp_raw = pd.read_csv(gdp_path, skiprows=4)
    columns_needed = ["Country Name"] + [str(y) for y in range(2016, 2024)]
    gdp = gdp_raw[columns_needed].copy()

    for yr in range(2017, 2024):
        gdp[f"{yr}_growth"] = (gdp[str(yr)] / gdp[str(yr-1)] - 1) * 100

    growth_cols = [f"{yr}_growth" for yr in range(2017, 2024)]
    gdp["gdp_growth_avg"] = gdp[growth_cols].mean(axis=1, skipna=True)
    gdp_avg = gdp[["Country Name", "gdp_growth_avg"]]

    # 1-C  Merge & clean
    data = wage_avg.merge(
        gdp_avg,
        left_on="country_name",
        right_on="Country Name",
        how="inner"
    ).dropna(subset=["real_wage_growth_avg", "gdp_growth_avg"])

    return data.sort_values("country_name")

data = load_data()

# ───────────────────────────────────────────────────────────────
# 2. Sidebar controls (optional)
# ───────────────────────────────────────────────────────────────
st.sidebar.header("Options")
highlight_country = st.sidebar.selectbox(
    "Highlight a country (optional)",
    ["None"] + data["country_name"].tolist(),
    index=0
)

# ───────────────────────────────────────────────────────────────
# 3. Scatter-plot with regression line
# ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(
    data=data,
    x="gdp_growth_avg",
    y="real_wage_growth_avg",
    scatter_kws={"s": 60, "alpha": 0.8},
    line_kws={"color": "red", "linewidth": 1.5},
    ax=ax
)

# optional annotation
if highlight_country != "None":
    row = data[data["country_name"] == highlight_country].iloc[0]
    ax.scatter(
        row["gdp_growth_avg"],
        row["real_wage_growth_avg"],
        s=120,
        edgecolor="black",
        facecolor="yellow",
        zorder=5
    )
    ax.text(
        row["gdp_growth_avg"],
        row["real_wage_growth_avg"],
        f"  {highlight_country}",
        va="center"
    )

ax.set_title("Relationship between GDP Growth and Real Wage Growth\nEurope, 2017-2023")
ax.set_xlabel("Average GDP Growth Rate (%, 2017-2023)")
ax.set_ylabel("Average Real Wage Growth Rate (%, 2017-2023)")
ax.grid(True)
plt.tight_layout()

st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# 4. Correlation coefficient & data table
# ───────────────────────────────────────────────────────────────
corr = data["gdp_growth_avg"].corr(data["real_wage_growth_avg"])
st.markdown(f"**Correlation coefficient:** {corr:.2f}")

with st.expander("Show underlying data"):
    st.dataframe(data[["country_name", "gdp_growth_avg", "real_wage_growth_avg"]])

# ───────────────────────────────────────────────────────────────
# 5. Findings summary (text section)
# ───────────────────────────────────────────────────────────────
st.markdown(
    """
### Findings: GDP Growth vs. Real Wage Growth (Europe, 2017 – 2023)

- **Correlation coefficient:** **−0.17** – a weak, negative relationship between average GDP growth and real-wage growth across European countries.  
- **Interpretation:** Faster economic expansion did **not** translate into proportionally higher real wages; if anything, countries with stronger GDP growth tended to post slightly lower real-wage gains.  
- **Implication:** Macroeconomic growth alone is insufficient to guarantee wage improvements for workers. Inflation, labour-market conditions, government wage policies, and sectoral dynamics likely mediate the link between GDP and pay.  
- **Caveats:**  
  • Analysis relies on country-level averages and a linear model; non-linear patterns or within-country differences are not captured.  
  • External shocks (e.g., pandemic effects) and outliers may blur the longer-term signal.

Further research could explore non-linear relationships, sector-specific trends, and institutional determinants to unpack the observed disconnect.
    """,
    unsafe_allow_html=False
)


# ───────────────────────────────────────────────────────────────
# 0. Page config  (only keep this line if the file
#    will be run as a standalone Streamlit page)
# ───────────────────────────────────────────────────────────────
# ───────────────────────────────────────────────────────────────
# 1. Imports & data loading
# ───────────────────────────────────────────────────────────────
import pandas as pd
import plotly.express as px

@st.cache_data
def load_real_wage_data(xlsx_path="globalwagereport-2024-25data.xlsx"):
    real_df = pd.read_excel(xlsx_path, sheet_name="Real wage growth")
    real_eu = real_df[real_df["Region"] == "Europe and Central Asia"].copy()

    melted = real_eu.melt(
        id_vars=["country_name", "Income group", "Subregion - detailed"],
        value_vars=[2017, 2018, 2019, 2020, 2021, 2022, 2023],
        var_name="Year",
        value_name="Real_Wage_Growth"
    ).dropna(subset=["Real_Wage_Growth"])

    melted["Year"] = melted["Year"].astype(int)
    return melted

df = load_real_wage_data()
subregions = sorted(df["Subregion - detailed"].unique())

# ───────────────────────────────────────────────────────────────
# 2. Sidebar filters
# ───────────────────────────────────────────────────────────────
st.sidebar.header("Filters")

selected_sub = st.sidebar.multiselect(
    "Sub-region(s)",
    subregions,
    default=subregions        # all selected by default
)

df_filtered = df[df["Subregion - detailed"].isin(selected_sub)]

available_countries = sorted(df_filtered["country_name"].unique())
selected_countries = st.sidebar.multiselect(
    "Country selection",
    available_countries,
    default=available_countries[:10]   # first 10 pre-selected
)

df_filtered = df_filtered[df_filtered["country_name"].isin(selected_countries)]

# guardrail: if the user un-selects everything
if df_filtered.empty:
    st.warning("No data for the chosen filters.")
    st.stop()

# ───────────────────────────────────────────────────────────────
# 3. Interactive line chart
# ───────────────────────────────────────────────────────────────
fig = px.line(
    df_filtered,
    x="Year",
    y="Real_Wage_Growth",
    color="country_name",
    line_group="country_name",
    hover_name="country_name",
    labels={
        "Real_Wage_Growth": "Real Wage Growth (%)",
        "Year": "Year"
    },
    title="Interactive Real Wage Growth Trends in Europe (2017 – 2023)"
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="Country",
    height=600,
    width=1000
)

st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# 4. Optional: show underlying table
# ───────────────────────────────────────────────────────────────
with st.expander("Show data table"):
    st.dataframe(
        df_filtered.pivot(index="Year", columns="country_name", values="Real_Wage_Growth")
    )


# econ_vs_wage_app.py
# ───────────────────────────────────────────────────────────────
# 0. PAGE CONFIG  – must be first Streamlit command
# ───────────────────────────────────────────────────────────────
# ───────────────────────────────────────────────────────────────
# 1. IMPORTS & DATA LOADERS
# ───────────────────────────────────────────────────────────────
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(
    wage_file="globalwagereport-2024-25data.xlsx",
    gdp_file="API_NY.GDP.MKTP.KD_DS2_en_csv_v2_19406.csv"
):
    # 1-A  Average real-wage growth
    real_df = pd.read_excel(wage_file, sheet_name="Real wage growth")
    eu = real_df[real_df["Region"] == "Europe and Central Asia"].copy()
    years = list(range(2017, 2024))          # 2017-2023 inclusive
    eu["real_wage_growth_avg"] = eu[years].mean(axis=1, skipna=True)
    wage_avg = eu[["country_name", "real_wage_growth_avg"]]

    # 1-B  Average GDP growth
    gdp_raw = pd.read_csv(gdp_file, skiprows=4)
    cols = ["Country Name"] + [str(y) for y in range(2016, 2024)]
    gdp = gdp_raw[cols].copy()

    for yr in range(2017, 2024):
        gdp[f"{yr}_growth"] = (gdp[str(yr)] / gdp[str(yr-1)] - 1) * 100
    growth_cols = [f"{yr}_growth" for yr in range(2017, 2024)]
    gdp["gdp_growth_avg"] = gdp[growth_cols].mean(axis=1, skipna=True)
    gdp_avg = gdp[["Country Name", "gdp_growth_avg"]]

    # 1-C  Merge
    df = wage_avg.merge(
        gdp_avg,
        left_on="country_name",
        right_on="Country Name",
        how="inner"
    ).dropna(subset=["real_wage_growth_avg", "gdp_growth_avg"])

    return df.sort_values("country_name")

data = load_data()


# ───────────────────────────────────────────────────────────────
# 3. SCATTER-PLOT
# ───────────────────────────────────────────────────────────────
trendline_opt = "ols" if show_trend else None
fig = px.scatter(
    data,
    x="gdp_growth_avg",
    y="real_wage_growth_avg",
    hover_name="country_name",
    trendline=trendline_opt,
    labels={
        "gdp_growth_avg": "Avg. GDP Growth 2017-23 (%)",
        "real_wage_growth_avg": "Avg. Real Wage Growth 2017-23 (%)"
    },
    title="GDP Growth vs. Real Wage Growth  •  Europe (2017-2023)"
)
fig.update_traces(marker=dict(size=point_size))

# optional highlight
if highlight != "None":
    row = data[data["country_name"] == highlight].iloc[0]
    fig.add_scatter(
        x=[row["gdp_growth_avg"]],
        y=[row["real_wage_growth_avg"]],
        mode="markers+text",
        marker=dict(size=point_size*1.6, line=dict(width=2, color="black"), color="yellow"),
        text=[highlight],
        textposition="top center",
        showlegend=False
    )

fig.update_layout(template="plotly_white", title_x=0.5, height=600, width=850)
st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# 4. CORRELATION & FINDINGS
# ───────────────────────────────────────────────────────────────
corr = data["gdp_growth_avg"].corr(data["real_wage_growth_avg"])
st.markdown(f"**Correlation coefficient:** `{corr:.2f}`")

st.markdown(
    """
**Interpretation**

The negative value (≈ −0.17) signals a *weak* inverse relationship: on average, faster-growing
economies did **not** enjoy stronger real-wage gains over 2017-2023.  
Macroeconomic expansion alone therefore appears insufficient to lift wages proportionally;
labour-market structures, inflation, and policy choices likely mediate the link.

*Note:* This is a linear, country-level view. Non-linear or within-country effects remain outside the model’s scope.
    """
)

# ───────────────────────────────────────────────────────────────
# 5. DATA TABLE (expandable)
# ───────────────────────────────────────────────────────────────
with st.expander("Show underlying data"):
    st.dataframe(
        data.rename(columns={
            "country_name": "Country",
            "gdp_growth_avg": "Avg GDP Growth (%)",
            "real_wage_growth_avg": "Avg Real Wage Growth (%)"
        })
    )
