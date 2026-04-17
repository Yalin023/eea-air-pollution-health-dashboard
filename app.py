import streamlit as st
import pandas as pd
import plotly.express as px

#page
st.set_page_config(
    page_title="Air Pollution & Health Impact Dashboard",
    page_icon="🌍",
    layout="wide"
)

#styles
st.markdown("""
<style>
    .main {
        background-color: #0b1220;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 700;
    }

    p, div, li {
        color: #d1d5db;
        font-size: 1rem;
    }

    .intro-text {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-bottom: 1rem;
    }

    .section-note {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: -0.4rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #111827, #1e293b);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        margin-bottom: 12px;
        min-height: 145px;
    }

    .metric-title {
        font-size: 0.92rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #22d3ee;
        word-break: break-word;
        line-height: 1.2;
    }

    .metric-highlight {
        font-size: 1.9rem;
        font-weight: 700;
        color: #f59e0b;
        word-break: break-word;
        line-height: 1.2;
    }

    .info-box {
        background-color: #111827;
        border-left: 5px solid #22d3ee;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .insight-box {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        margin-top: 10px;
    }

    .toc-box {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px;
        margin-top: 0.8rem;
    }

    .toc-box a {
        color: #22d3ee;
        text-decoration: none;
        display: block;
        margin: 0.45rem 0;
        font-weight: 500;
    }

    .toc-box a:hover {
        color: #f59e0b;
    }

    .small-note {
        color: #94a3b8;
        font-size: 0.92rem;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

#helper functions
def get_unit_label(indicator_name: str) -> str:
    if indicator_name == "Premature deaths":
        return "people"
    if indicator_name == "Years of life lost":
        return "years"
    return "units"

def get_measure_explanation(indicator_name: str) -> str:
    if indicator_name == "Premature deaths":
        return "estimated number of people"
    if indicator_name == "Years of life lost":
        return "total number of years"
    return "measured value"

def aggregate_region_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=["region_code", "region_name", "value"])
    return (
        dataframe.groupby(["region_code", "region_name"], as_index=False)["value"]
        .sum()
        .sort_values("value", ascending=False)
    )

#Map regions
ISO3_MAP = {
    "AL": "ALB", "AT": "AUT", "BE": "BEL", "BG": "BGR", "CH": "CHE", "CY": "CYP",
    "CZ": "CZE", "DE": "DEU", "DK": "DNK", "EE": "EST", "EL": "GRC", "ES": "ESP",
    "FI": "FIN", "FR": "FRA", "HR": "HRV", "HU": "HUN", "IE": "IRL", "IS": "ISL",
    "IT": "ITA", "LI": "LIE", "LT": "LTU", "LU": "LUX", "LV": "LVA", "ME": "MNE",
    "MK": "MKD", "MT": "MLT", "NL": "NLD", "NO": "NOR", "PL": "POL", "PT": "PRT",
    "RO": "ROU", "RS": "SRB", "SE": "SWE", "SI": "SVN", "SK": "SVK"
}

COUNTRY_NAME_MAP = {
    "AL": "Albania", "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CH": "Switzerland",
    "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
    "EL": "Greece", "ES": "Spain", "FI": "Finland", "FR": "France", "HR": "Croatia",
    "HU": "Hungary", "IE": "Ireland", "IS": "Iceland", "IT": "Italy", "LI": "Liechtenstein",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "ME": "Montenegro",
    "MK": "North Macedonia", "MT": "Malta", "NL": "Netherlands", "NO": "Norway",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RS": "Serbia", "SE": "Sweden",
    "SI": "Slovenia", "SK": "Slovakia"
}

#Data loading
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/eea_air_pollution_cleaned.csv")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    if "indicator_short" not in df.columns and "indicator_code" in df.columns:
        indicator_map = {
            "PMD": "Premature deaths",
            "YLL": "Years of life lost"
        }
        df["indicator_short"] = df["indicator_code"].map(indicator_map).fillna(df["indicator_code"])

    if "region_code" not in df.columns and "geo" in df.columns:
        df["region_code"] = df["geo"]

    if "region_name" not in df.columns and "geo_label" in df.columns:
        df["region_name"] = df["geo_label"]

    df["region_code"] = df["region_code"].astype(str)
    df["country_prefix"] = df["region_code"].str[:2]
    df["geo_len"] = df["region_code"].str.len()

    max_geo_len = df.groupby("country_prefix")["geo_len"].transform("max")
    df["is_finest_level"] = df["geo_len"].eq(max_geo_len)

    df["country_code"] = df["country_prefix"].map(ISO3_MAP)
    df["country_name"] = df["country_prefix"].map(COUNTRY_NAME_MAP)

    return df

df = load_data()
analysis_df = df[df["is_finest_level"]].copy()

years = sorted(analysis_df["year"].dropna().astype(int).unique())
metric_year_options = ["All years"] + years
indicators = sorted(analysis_df["indicator_short"].dropna().unique())
all_regions = sorted(analysis_df["region_name"].dropna().unique())

#Navigation bar
st.sidebar.title("Navigation Bar")
st.sidebar.markdown('<div class="small-note">Chart filters are placed above each chart. Click to redirect to a preffered page</div>', unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="toc-box">
    <a href="#overview">Overview</a>
    <a href="#key-metrics">Key Metrics</a>
    <a href="#top-regions">Top 10 Regions</a>
    <a href="#impact-map">Impact Map</a>
    <a href="#comparison-chart">Region Comparison</a>
    <a href="#trend-over-time">Trend Over Time</a>
    <a href="#filtered-data">Filtered Data</a>
    <a href="#insight-summary">Insight Summary</a>
</div>
""", unsafe_allow_html=True)

#Title
st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
st.title("Air Pollution & Health Impact Dashboard")
st.markdown(
    '<div class="intro-text">This dashboard showing how air pollution affects health across European regions. '
    'Each chart has its own filters directly above it, so you can explore different views individually.</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
    <strong>How to read this dashboard:</strong><br>
    • <strong>Premature deaths</strong> : estimated number of people whose deaths are linked to air pollution.<br>
    • <strong>Years of life lost</strong> : total number of years lost because of early death linked to air pollution.<br>
    • Higher values indicate a greater health risks.<br>
    • The dashboard uses the finest available regional level for regional comparisons, then aggregates to country totals for the map.
    </div>
    """,
    unsafe_allow_html=True
)

#KPI
st.markdown('<div id="key-metrics"></div>', unsafe_allow_html=True)
st.header("Key Metrics")
st.markdown(
    '<div class="section-note">These cards summarise the selected indicator for one year or across all years. Values are shown as people or years, depending on the indicator.</div>',
    unsafe_allow_html=True
)

metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    metric_year = st.selectbox(
        "Key metrics year",
        metric_year_options,
        index=0,
        key="metric_year"
    )
with metric_col2:
    metric_indicator = st.selectbox(
        "Key metrics indicator",
        indicators,
        key="metric_indicator"
    )

if metric_year == "All years":
    metric_df = analysis_df[
        analysis_df["indicator_short"] == metric_indicator
    ].copy()
    metric_period_label = "All years"
else:
    metric_df = analysis_df[
        (analysis_df["year"] == metric_year) &
        (analysis_df["indicator_short"] == metric_indicator)
    ].copy()
    metric_period_label = str(metric_year)

metric_region_summary = aggregate_region_data(metric_df)
metric_unit = get_unit_label(metric_indicator)
metric_explanation = get_measure_explanation(metric_indicator)

if not metric_region_summary.empty:
    total_value = metric_region_summary["value"].sum()
    avg_value = metric_region_summary["value"].mean()
    max_row = metric_region_summary.loc[metric_region_summary["value"].idxmax()]
    max_region = max_row["region_name"]
    max_region_value = max_row["value"]
else:
    total_value = 0
    avg_value = 0
    max_region = "No data"
    max_region_value = 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total impact ({metric_unit})</div>
        <div class="metric-value">{int(total_value):,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average per region ({metric_unit})</div>
        <div class="metric-value">{int(avg_value):,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Highest impacted region</div>
        <div class="metric-highlight">{max_region}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Highest region value ({metric_unit})</div>
        <div class="metric-value">{int(max_region_value):,}</div>
    </div>
    """, unsafe_allow_html=True)

st.caption(
    f"For {metric_indicator.lower()}, the values represent the {metric_explanation}. "
    f"The current key metrics view is based on: {metric_period_label}."
)

#Top 10 regions
st.markdown('<div id="top-regions"></div>', unsafe_allow_html=True)
st.header("Top 10 Regions by Impact")
st.markdown(
    '<div class="section-note">It shows only the top 10 regions for those settings.</div>',
    unsafe_allow_html=True
)

top_filter_col1, top_filter_col2 = st.columns(2)
with top_filter_col1:
    top_year = st.selectbox(
        "Top regions year",
        years,
        index=len(years) - 1,
        key="top_year"
    )
with top_filter_col2:
    top_indicator = st.selectbox(
        "Top regions indicator",
        indicators,
        key="top_indicator"
    )

top_df = analysis_df[
    (analysis_df["year"] == top_year) &
    (analysis_df["indicator_short"] == top_indicator)
].copy()

top_region_summary = aggregate_region_data(top_df)
top_regions = (
    top_region_summary.nlargest(10, "value")
    .sort_values("value", ascending=True)
)

if not top_regions.empty:
    fig_bar = px.bar(
        top_regions,
        x="value",
        y="region_name",
        orientation="h",
        text="value",
        color="value",
        color_continuous_scale=["#164e63", "#0891b2", "#22d3ee", "#f59e0b"],
        labels={"region_name": "Region", "value": f"Impact value ({get_unit_label(top_indicator)})"}
    )
    fig_bar.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Impact: %{x:,.0f}<extra></extra>"
    )
    fig_bar.update_layout(
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        font_color="#f8fafc",
        xaxis_title=f"Impact value ({get_unit_label(top_indicator)})",
        yaxis_title="Region",
        coloraxis_showscale=False,
        height=560,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
else:
    st.warning("No data available for the selected top-regions filters.")

#Map
st.markdown('<div id="impact-map"></div>', unsafe_allow_html=True)
st.header("Impact Map")
st.markdown(
    '<div class="section-note">Hover over a country to see its total impact.</div>',
    unsafe_allow_html=True
)

map_filter_col1, map_filter_col2 = st.columns(2)
with map_filter_col1:
    map_year = st.selectbox(
        "Map year",
        years,
        index=len(years) - 1,
        key="map_year"
    )
with map_filter_col2:
    map_indicator = st.selectbox(
        "Map indicator",
        indicators,
        key="map_indicator"
    )

map_df = analysis_df[
    (analysis_df["year"] == map_year) &
    (analysis_df["indicator_short"] == map_indicator)
].copy()

country_map_df = (
    map_df.dropna(subset=["country_code"])
    .groupby(["country_code", "country_name"], as_index=False)["value"]
    .sum()
)

if not country_map_df.empty:
    fig_map = px.choropleth(
        country_map_df,
        locations="country_code",
        color="value",
        hover_name="country_name",
        hover_data={"value": ":,.0f", "country_code": False},
        color_continuous_scale=["#164e63", "#0891b2", "#22d3ee", "#f59e0b"],
        scope="europe",
        labels={"value": f"Impact ({get_unit_label(map_indicator)})"}
    )

    fig_map.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Impact: %{z:,.0f}<extra></extra>"
    )

    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="#0b1220",
        showcountries=True,
        countrycolor="#475569",
        showcoastlines=True,
        coastlinecolor="#334155",
        uirevision="keep-map-view"
    )

    fig_map.update_layout(
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        font_color="#f8fafc",
        height=860,
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision="keep-map-view",
        coloraxis_colorbar=dict(
            title=f"Impact ({get_unit_label(map_indicator)})",
            thickness=18,
            len=0.72,
            y=0.5
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "scrollZoom": True,
            "displaylogo": False
        }
    )
else:
    st.warning("No map data available for the selected map filters.")

#Comparison chart
st.markdown('<div id="comparison-chart"></div>', unsafe_allow_html=True)
st.header("Compare Selected Regions")
st.markdown(
    '<div class="section-note">Select a year, indicator, and 2 to 10 regions.</div>',
    unsafe_allow_html=True
)

compare_col1, compare_col2, compare_col3 = st.columns([1, 1, 2])

with compare_col1:
    compare_year = st.selectbox(
        "Comparison year",
        years,
        index=len(years) - 1,
        key="compare_year"
    )

with compare_col2:
    compare_indicator = st.selectbox(
        "Comparison indicator",
        indicators,
        key="compare_indicator"
    )

compare_base_df = analysis_df[
    (analysis_df["year"] == compare_year) &
    (analysis_df["indicator_short"] == compare_indicator)
].copy()

available_compare_regions = sorted(compare_base_df["region_name"].dropna().unique())

with compare_col3:
    compare_regions = st.multiselect(
        "Select 2 to 10 regions",
        options=available_compare_regions,
        default=available_compare_regions[:2] if len(available_compare_regions) >= 2 else available_compare_regions
    )

if len(compare_regions) > 10:
    st.warning("Only the first 10 selected regions will be used.")
    compare_regions = compare_regions[:10]

if len(compare_regions) < 2:
    st.info("Select at least 2 regions to show the comparison chart.")
else:
    compare_chart_df = compare_base_df[
        compare_base_df["region_name"].isin(compare_regions)
    ].copy()

    compare_chart_df = aggregate_region_data(compare_chart_df)
    compare_chart_df = compare_chart_df.sort_values("value", ascending=False)

    fig_compare = px.bar(
        compare_chart_df,
        x="region_name",
        y="value",
        text="value",
        color="value",
        color_continuous_scale=["#164e63", "#0891b2", "#22d3ee", "#f59e0b"],
        labels={"region_name": "Region", "value": f"Impact value ({get_unit_label(compare_indicator)})"}
    )

    fig_compare.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Impact: %{y:,.0f}<extra></extra>"
    )

    fig_compare.update_layout(
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        font_color="#f8fafc",
        xaxis_title="Region",
        yaxis_title=f"Impact value ({get_unit_label(compare_indicator)})",
        coloraxis_showscale=False,
        height=560,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_compare, use_container_width=True, config={"displayModeBar": False})

#Trend over-time
st.markdown('<div id="trend-over-time"></div>', unsafe_allow_html=True)
st.header("Trend Over Time")
st.markdown(
    '<div class="section-note">Shows the total trend across the full time period.</div>',
    unsafe_allow_html=True
)

trend_col1, trend_col2 = st.columns([1, 1])
with trend_col1:
    trend_indicator = st.selectbox(
        "Trend indicator",
        indicators,
        key="trend_indicator"
    )
with trend_col2:
    trend_region_option = st.selectbox(
        "Trend region",
        ["All regions combined"] + all_regions,
        key="trend_region"
    )

trend_df = analysis_df[
    analysis_df["indicator_short"] == trend_indicator
].copy()

if trend_region_option != "All regions combined":
    trend_df = trend_df[trend_df["region_name"] == trend_region_option]

trend_data = (
    trend_df.groupby("year", as_index=False)["value"]
    .sum()
    .sort_values("year")
)

if not trend_data.empty:
    fig_line = px.line(
        trend_data,
        x="year",
        y="value",
        markers=True,
        labels={"year": "Year", "value": f"Impact value ({get_unit_label(trend_indicator)})"}
    )
    fig_line.update_traces(
        line=dict(color="#22d3ee", width=4),
        marker=dict(size=7, color="#f59e0b"),
        hovertemplate="Year: %{x}<br>Impact: %{y:,.0f}<extra></extra>"
    )
    fig_line.update_layout(
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        font_color="#f8fafc",
        xaxis_title="Year",
        yaxis_title=f"Impact value ({get_unit_label(trend_indicator)})",
        xaxis=dict(tickmode="linear", dtick=2),
        height=560,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
else:
    st.warning("No trend data available for the selected trend filters.")

#Filtered data
st.markdown('<div id="filtered-data"></div>', unsafe_allow_html=True)
with st.expander("Show filtered data from the key metrics selection"):
    filtered_table_df = metric_region_summary.copy()
    if not filtered_table_df.empty:
        filtered_table_df["unit"] = metric_unit
    st.dataframe(filtered_table_df, use_container_width=True)

#Insights
st.markdown('<div id="insight-summary"></div>', unsafe_allow_html=True)
st.header("Insight Summary")

if not metric_region_summary.empty:
    st.markdown(f"""
<div class="insight-box">
Across <strong>all years</strong>, the selected metric view for <strong>{metric_indicator}</strong> shows that the highest cumulative impact is recorded in 
<strong>{max_region}</strong>, with a value of <strong>{int(max_region_value):,}</strong> {metric_unit}. This means that, when the full time period is considered together, 
<strong>{max_region}</strong> stands out as the region with the greatest overall health burden linked to this indicator.<br><br>

The supporting charts help explain this pattern from different angles: the Top 10 Regions chart highlights the highest regional values, the map shows how the impact is distributed across countries, 
the comparison chart allows direct comparison between selected regions, and the trend chart shows how the selected indicator changes over time.
</div>
""", unsafe_allow_html=True)
else:
    st.info("No insight is available because the current key-metrics filters returned no data.")