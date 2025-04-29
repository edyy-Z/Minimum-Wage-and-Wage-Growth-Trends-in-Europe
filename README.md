# Minimum Wage and Wage Growth Trends in Europe

Group member: Yongjun Zhu, Yue Wei, Lan Wang, Yuanjing Zhu

## Abstract 
We are interested in analyzing minimum wage trends across Europe, their relationship with economic growth, and regional disparities in wage policies. Our study will address the following key questions:
How has minimum wages evolved across European countries from 2017 to 2023? We will examine trends in nominal and real wage growth, comparing across regions and income groups.
How do minimum wages compare to actual wage levels across different countries? Using data from the OECD and ILO, we will investigate wage distributions and disparities.
What is the relationship between economic growth and wage trends? By incorporating GDP data from the World Bank, we will assess whether higher GDP growth correlates with stronger wage increases.
How do wage policies and trends vary geographically? We will employ geospatial visualization to map wage growth rates and compare regional differences.
How can interactive data visualizations enhance the understanding of wage trends? Through interactive maps and time-series visualizations, we aim to present an intuitive representation of wage dynamics across Europe.
For our analysis, we will clean and preprocess datasets from the ILO, OECD, and World Bank, ensuring consistency in country names and handling missing values appropriately. Using seaborn and matplotlib, we will create line charts to illustrate wage trends over time for Europe as a whole and for individual countries. Additionally, we will use OpenStreetMap with Folium to develop an interactive choropleth map, where users can explore country-specific wage information with popups and a time slider. Our project aims to provide a clear, data-driven visualization of wage policies and economic trends across Europe.

## Data
1. ILO Globel Wage Dataset ：https://www.ilo.org/publications/flagship-reports/global-wage-report-2024-25-wage-inequality-decreasing-globally
   -This dataset contains real and nominal wage data across European countries from 2017-2023, tracking wage growth trends.
   -Key variables include country, region, nominal wage levels, real wage growth (%), income groups.
2. OECD Minimum Wage Dataset: https://data-explorer.oecd.org/vis?df[ds]=DisseminateFinalDMZ&df[id]=DSD_EARNINGS%40MIN2AVE&df[ag]=OECD.ELS.SAE&dq=......&pd=2000%2C&to[TIME_PERIOD]=false&vw=tb
   -This dataset contains official minimum wage data for OECD countries, allowing comparison with actual wages.
   -Key Variables include country, legal minimum wage levels (converted into a common currency for comparability), changes over time.
3. World Bank GDP Dataset: https://data.worldbank.org/indicator/NY.GDP.MKTP.KD
   -This dataset Includes GDP (constant 2015 US$) for European nations, allowing us to study economic growth and its impact on wages.
   -Key Variables include country, GDP (constant 2015 US$), GDP growth rate.


[![Open in Streamlit]((https://urban-computing-machine-jjqpjrgr79jwfjjgx-8501.app.github.dev/))](http://20.42.11.17:8501)
