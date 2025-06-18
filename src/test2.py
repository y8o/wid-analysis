import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# Use this confirmed variable
selected_variable = 'shwealj992'  # Share of wealth of top 1%

# Step 1: Connect to database
conn = sqlite3.connect("data/wid_world.db")

# Step 2: Query data
query = f"""
SELECT country, year, value
FROM data
WHERE variable = '{selected_variable}'
  AND percentile = 'p99p100'
  AND country IN ('US', 'FR', 'BR')
  AND year >= 1980
ORDER BY country, year;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Step 3: Map country codes to names
df['country'] = df['country'].str.strip().str.upper()
country_map = {'US': 'United States', 'FR': 'France', 'BR': 'Brazil'}
df['country'] = df['country'].map(country_map)
df = df.dropna(subset=['country'])

# Step 4: Plot
plt.figure(figsize=(10, 6))
for country in df['country'].unique():
    subset = df[df['country'] == country]
    plt.plot(subset['year'], subset['value'], label=country)

plt.title(f"Top 1% Wealth Share (1980–Present)\nVariable: {selected_variable}")
plt.xlabel("Year")
plt.ylabel("Share of Total Wealth (Top 1%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Step 5: Save the figure
os.makedirs("output", exist_ok=True)
output_path = f"output/top1_wealth_share_{selected_variable}.png"
plt.savefig(output_path, dpi=300)
plt.show()
