# Test Cases

The following five test cases cover all functional requirements of the dashboard.

## Test Coverage Mapping

- **TC1** covers **FR1** and **FR2**
- **TC2** covers **FR3**
- **TC3** covers **FR4**
- **TC4** covers **FR5**
- **TC5** covers **FR6** and **FR7**

---

## TC1

**Title:** Verify overview section and KPI filters

**Description:**  
This test checks whether the dashboard displays the overview information correctly and whether the key metrics section updates according to the selected year and indicator, including the **All years** option.

**Related requirements:** FR1, FR2

**Steps and input data:**  
1. Launch the Streamlit dashboard.  
2. Confirm that the page title and introductory explanation are visible.  
3. Read the information box explaining **Premature deaths** and **Years of life lost**.  
4. In the key metrics section, select **Premature deaths** as the indicator.  
5. Select a specific year from the key metrics year filter.  
6. Observe the four summary cards.  
7. Change the year filter to **All years**.  
8. Observe whether the values update again.

**Dependencies:**  
Dashboard deployed successfully and cleaned dataset loaded correctly.

**Expected result:**  
The overview text and indicator explanation should be visible. The key metrics cards should load successfully and update when the year or indicator selection changes. The **All years** option should work without errors.

---

## TC2

**Title:** Verify Top 10 Regions chart functionality

**Description:**  
This test checks whether the Top 10 Regions chart displays correctly and updates based on the selected year and indicator.

**Related requirements:** FR3

**Steps and input data:**  
1. Open the dashboard.  
2. Scroll to the **Top 10 Regions by Impact** section.  
3. Select a year from the chart’s year filter.  
4. Select **Premature deaths** as the indicator.  
5. Observe the chart output.  
6. Change the indicator to **Years of life lost**.  
7. Change the year again and observe the updated chart.

**Dependencies:**  
Top regions data available for the chosen years and indicators.

**Expected result:**  
A bar chart showing the top 10 impacted regions should be displayed. The chart should update correctly whenever the year or indicator changes. No error should occur during interaction.

---

## TC3

**Title:** Verify interactive Europe impact map

**Description:**  
This test checks whether the dashboard displays country-level totals on a Europe map and whether the map updates based on selected filters.

**Related requirements:** FR4

**Steps and input data:**  
1. Open the dashboard.  
2. Scroll to the **Impact Map** section.  
3. Select a year from the map year filter.  
4. Select an indicator.  
5. Hover over at least three countries on the map.  
6. Confirm that country names and impact values appear.  
7. Change the year and indicator again.  
8. Observe whether the map refreshes correctly.

**Dependencies:**  
Country code mappings and aggregated country totals available in the dataset.

**Expected result:**  
The Europe choropleth map should display correctly. Hovering over a country should show the country name and total impact value. Changing the filters should refresh the map without crashing.

---

## TC4

**Title:** Verify comparison chart for selected regions

**Description:**  
This test checks whether users can compare regions by selecting between 2 and 10 regions and whether appropriate messages appear when the selection is invalid.

**Related requirements:** FR5

**Steps and input data:**  
1. Open the dashboard.  
2. Scroll to the **Compare Selected Regions** section.  
3. Select a year and indicator.  
4. Select exactly 2 regions from the multiselect box.  
5. Observe the comparison chart.  
6. Increase the selection to 5 regions.  
7. Observe the updated chart.  
8. Reduce the selection to only 1 region.  
9. Observe the system response.  
10. Select more than 10 regions and observe the system response.

**Dependencies:**  
At least two regions available in the selected filter context.

**Expected result:**  
The comparison chart should appear when 2 to 10 regions are selected. If fewer than 2 regions are selected, the dashboard should show an informational message instead of failing. If more than 10 regions are selected, the dashboard should limit the selection and warn the user appropriately.

---

## TC5

**Title:** Verify trend chart and filtered data table

**Description:**  
This test checks whether the trend chart displays values over time correctly and whether the filtered data table matches the key metrics selection.

**Related requirements:** FR6, FR7

**Steps and input data:**  
1. Open the dashboard.  
2. Scroll to the **Trend Over Time** section.  
3. Select **Premature deaths** as the trend indicator.  
4. Select **All regions combined** as the trend region.  
5. Observe the line chart.  
6. Change the trend region to a specific region and observe the chart again.  
7. Go to the key metrics section and choose an indicator and year.  
8. Open the **Show filtered data from the key metrics selection** expander.  
9. Check whether the displayed table reflects the same selection used in the key metrics section.

**Dependencies:**  
Trend data and filtered summary data available for the selected indicator and region.

**Expected result:**  
The line chart should show a time trend for the selected indicator and update when a specific region is selected. The filtered data table should open successfully and display data that matches the current key metrics selection.