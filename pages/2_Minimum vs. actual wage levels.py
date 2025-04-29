# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px

# heatmap
st.set_page_config(page_title="Minimum-to-Average Wage Map", layout="centered")

@st.cache_data
def load_data():
    YEARS = [str(y) for y in range(2017, 2024)]
    df = (
        pd.read_csv("Minimum_to_average_wage_rate.csv")
          .query("`Time period.1` == 'Mean'")
          .set_index("country")[YEARS]
    )
    return YEARS, df

YEARS, df = load_data()

scheme = st.radio(
    "Choose colour scale",
    ("Sequential (YlGnBu)", "Diverging (RdBu_r, centred at 50)")
)

fig, ax = plt.subplots(figsize=(10, 7))
if scheme.startswith("Sequential"):
    im = ax.imshow(df.values, aspect="auto", cmap="YlGnBu")
else:
    norm = mcolors.TwoSlopeNorm(
        vmin=df.values.min(), vcenter=50, vmax=df.values.max()
    )
    im = ax.imshow(df.values, aspect="auto", cmap="RdBu_r", norm=norm)

ax.set_xticks(range(len(YEARS)), YEARS)
ax.set_yticks(range(len(df.index)), df.index)
ax.set_title("Minimum-to-average wage ratio (%) • 2017-2023")

cbar = fig.colorbar(im, ax=ax)
cbar.set_label("ratio %")

plt.tight_layout()

st.pyplot(fig)



# slopegraph

import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = (
        pd.read_csv("Minimum_to_average_wage_rate.csv")
          .query("`Time period.1` == 'Mean'")
          .set_index("country")[["2017", "2023"]]
          .dropna()
    )
    df["Δ"] = df["2023"] - df["2017"]
    return df

df = load_data()

st.sidebar.header("Options")
sort_by = st.sidebar.radio(
    "Sort countries by …",
    ("Alphabetical", "2017 ratio", "2023 ratio", "Change (Δ)"),
    index=3
)
top_n = st.sidebar.slider(
    "Show top N countries (after sorting)",
    min_value=5,
    max_value=len(df),
    value=min(25, len(df))
)


if sort_by == "Alphabetical":
    df_plot = df.sort_index()
elif sort_by == "2017 ratio":
    df_plot = df.sort_values("2017", ascending=False)
elif sort_by == "2023 ratio":
    df_plot = df.sort_values("2023", ascending=False)
else:  # Change
    df_plot = df.sort_values("Δ", ascending=False)

df_plot = df_plot.head(top_n)

fig, ax = plt.subplots(figsize=(8, 10))

x0, x1 = 0, 1
for country, row in df_plot.iterrows():
    ax.plot([x0, x1], [row["2017"], row["2023"]],
            linewidth=1.2,
            color="tab:blue" if row["Δ"] >= 0 else "tab:red")
    ax.text(x0 - 0.03, row["2017"], country,
            ha="right", va="center", fontsize=8)


ax.set_xticks([x0, x1], ["2017", "2023"])
ax.set_ylabel("Minimum-to-average wage ratio (%)")
ax.set_title(f"Change in minimum-/average-wage ratio, 2017 → 2023\n(top {top_n} countries)")
for spine in ("top", "right", "bottom"):
    ax.spines[spine].set_visible(False)
ax.tick_params(left=False)
plt.tight_layout()

st.pyplot(fig)

with st.expander("Show underlying data"):
    st.dataframe(df_plot[["2017", "2023", "Δ"]])



# Scattered plot
@st.cache_data
def load_data():
    YEARS = [str(y) for y in range(2017, 2024)]
    df = (
        pd.read_csv("Minimum_to_average_wage_rate.csv")
          .query("`Time period.1` == 'Mean'")
          .set_index("country")[YEARS]
    )
    return df

data = load_data()
all_countries = sorted(data.index.unique())

st.sidebar.header("Select exactly four countries")
selected = st.sidebar.multiselect(
    "Countries",
    all_countries,
    default=["Germany", "Spain", "Poland", "France"]
)

if len(selected) != 4:
    st.warning("Please select exactly **four** countries.")
    st.stop()

YEARS = [str(y) for y in range(2017, 2024)]
df_plot = (
    data.loc[selected, YEARS]
        .transpose()          # rows → years, columns → countries
)
df_plot.index = df_plot.index.astype(int)   # nicer x-axis ticks

fig, ax = plt.subplots(figsize=(7, 5))

for country in df_plot.columns:
    ax.plot(df_plot.index, df_plot[country],
            marker="o", label=country)

ax.set_xlabel("Year")
ax.set_ylabel("Minimum-to-average wage ratio (%)")
ax.set_title("Trajectory of wage-floor ratio (2017-2023)")
ax.legend()
plt.tight_layout()

st.pyplot(fig)

with st.expander("Show data table"):
    st.dataframe(df_plot)


# wage_map_app.py

@st.cache_data
def load_data():
    YEARS = [str(y) for y in range(2017, 2024)]
    df = (
        pd.read_csv("Minimum_to_average_wage_rate.csv")
          .query("`Time period.1` == 'Mean'")
          .melt(id_vars="country", value_vars=YEARS,
                var_name="year", value_name="ratio")
    )
    return df

df = load_data()

st.sidebar.header("Options")
palette = st.sidebar.selectbox(
    "Colour palette",
    ["Blues", "Viridis", "Cividis", "Plasma", "Turbo"],
    index=0
)

fig = px.choropleth(
    df,
    locations="country",
    locationmode="country names",
    color="ratio",
    animation_frame="year",
    range_color=[df["ratio"].min(), df["ratio"].max()],
    color_continuous_scale=palette,
    title="Minimum-to-average wage ratio (%) • 2017-2023"
)
fig.update_layout(coloraxis_colorbar_title="ratio %")

st.plotly_chart(fig, use_container_width=True)

with st.expander("Download the animation as HTML"):
    html_bytes = fig.to_html(full_html=False, include_plotlyjs="cdn").encode()
    st.download_button(
        "Download interactive map",
        data=html_bytes,
        file_name="wage_ratio_animation.html",
        mime="text/html"
    )


st.markdown(
    """
### Key take-aways

- **Raising the floor is now the norm, but pace differs.**  
  Most countries deepen in colour over time, showing that minimum wages are gaining ground relative to average wages almost everywhere. The magnitude, however, ranges from a multi-point jump (e.g. Germany) to near-stagnation (e.g. United States).

- **Latin-American wage policies are in a different league.**  
  With ratios exceeding 60 %, Costa Rica and Colombia set minimum wages that are proportionally far higher than any OECD country—approaching a *living-wage* philosophy rather than a basic safety-net.

- **Anglophone divergence persists.**  
  The UK sits mid-table (~45 %), Australia hovers around the global median (~40 %), and the US remains the clear laggard, highlighting very different legislative trajectories despite similar labour-market structures.

- **Eastern-European ratios are catching up fast.**  
  Poland, Hungary, Latvia, and Lithuania all deepen markedly, suggesting their statutory minima are rising faster than average earnings—possibly to curb in-work poverty and stem emigration.

- **Compression, not reversal.**  
  No country with a high ratio in 2017 shows a sustained fall; changes are flat or upward. The global picture is one of gradual compression of the lower tail of the wage distribution rather than any rollback at the top.
    """
)