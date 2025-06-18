# WID Income Share Analysis

This project analyzes the top 1% income share across countries using data from the World Inequality Database (WID).

## Data Source

The data was downloaded from the [World Inequality Database](https://wid.world/data/), which provides extensive historical data on income and wealth inequality by country.

## Setup and Processing

1. **Download CSV Files**  
   Visit the WID data portal and download relevant CSV files, such as:
   - WID_countries.csv
   - WID_data.csv

2. **Load Into SQLite**  
   These files are loaded into a local SQLite database using a custom Python script. The database (`wid_world.db`) contains the following tables:
   - countries
   - metadata
   - data (main table for inequality indicators)

3. **Query and Visualization**  
   Python and matplotlib are used to query the data and generate visualizations. Currently, the project includes a plot comparing the top 1% pre-tax income share in the U.S. from 1915 to 2020, seen below
![Top 1% Income Share - USA](output/usa_top1_income_share.png)
