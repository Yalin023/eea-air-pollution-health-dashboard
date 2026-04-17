# eea-air-pollution-health-dashboard

## Project Overview

This project is an interactive Streamlit dashboard developed for the **5DATA004C Data Science Project Lifecycle** individual coursework.

The dashboard uses an air pollution and health impact dataset from the **European Environment Agency (EEA)** to help users explore the effects of air pollution across European regions.

The dashboard focuses on two main indicators:

- **Premature deaths**
- **Years of life lost**

It is designed to help users explore the data through filters, summary metrics, charts, a map, comparison views, and trend analysis.

---

## Features

- Overview section with project context
- Key metrics with year and indicator filters
- **All years** option in key metrics
- Top 10 regions chart
- Europe impact map
- Region comparison chart
- Trend over time chart
- Filtered data table
- Insight summary section

---

## Dataset

The dataset used in this project is from the **European Environment Agency (EEA)**.

It contains regional air pollution health impact data across Europe and includes values for:

- Premature deaths
- Years of life lost

The project uses:
- a raw dataset file
- metadata file
- a cleaned dataset prepared for dashboard use

---

## Tools and Technologies

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly Express**
- **GitHub**
- **Streamlit Community Cloud**
- **VS Code**

---

## Project Structure

```text
DSPLC_INV_COURSEWORK/
│
├── .venv/
├── data/
│   ├── cleaned/
│   │   └── eea_air_pollution_cleaned.csv
│   └── raw/
│       ├── eea_s_eu-sdg-nuts23-11-52_p_2005-2023_v01_r00.csv
│       └── Metadata.xlsx
│
├── scripts/
│   └── clean_data.py
│
├── tests/
│   ├── functional_requirements.md
│   ├── non_functional_requirements.md
│   ├── test_cases.md
│   └── test_log.md
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt