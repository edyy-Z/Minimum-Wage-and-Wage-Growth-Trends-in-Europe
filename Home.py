import streamlit as st, base64, pathlib

st.set_page_config(page_title="Background-image demo")

img_path = pathlib.Path("image.jpeg")     
b64_img   = base64.b64encode(img_path.read_bytes()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64_img}");
        background-size: cover;            /* fill screen without distortion */
        background-attachment: fixed;      /* optional parallax effect      */
    }}
    </style>
    """,
    unsafe_allow_html=True
)



st.title("Minimum Wage and Wage Growth Trends in Europe")
st.markdown(
    """
**Team members:** Yongjun Zhu · Yue Wei · Lan Wang · Yuanjing Zhu
    """
)

st.header("Abstract")
st.markdown(
    """
We investigate minimum-wage dynamics across Europe and their links to economic growth and geography.  
Our study tackles five core questions:

1. **Evolution of minimum wages (2017–2023).**  
   How have nominal and real minimum wages changed across regions and income groups?

2. **Minimum vs. actual wage levels.**  
   Using OECD and ILO data, how do statutory minima compare with broader wage distributions?

3. **Economic-growth connection.**  
   Does faster GDP growth (World Bank data) coincide with stronger wage increases?

4. **Geographical disparities.**  
   What regional patterns emerge when we map wage policies and trends?

5. **Power of interactive visualisation.**  
   How can maps and time-series dashboards enhance understanding of wage dynamics?

---

### Data & Methods
* **Sources:** ILO, OECD, World Bank.  
* **Pre-processing:** harmonise country names, handle missing values, align currencies/inflation.  
* **Visualisation stack:**  
  * `seaborn` / `matplotlib` – line charts for Europe-wide and per-country trends  
  * `Folium` + OpenStreetMap – interactive choropleth with pop-ups & year slider  
* **Goal:** deliver a clear, data-driven picture of wage policies, economic context, and regional disparities across Europe.
    """,
    unsafe_allow_html=False
)

