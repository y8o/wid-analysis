import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# Connect to database
conn = sqlite3.connect("data/wid_world.db")

# Countries of interest
countries = ['US', 'FR', 'GB', 'JP', 'CN']

# Step 1: Find common variable for top 1% income share
query_vars = f"""
SELECT country, variable
FROM data
WHERE percentile = 'p99p100'
  AND country IN ({','.join(f"'{c}'" for c in countries)});
"""
df_vars = pd.read_sql_query(query_vars, conn)

# Pivot to see overlap
pivot = df_vars.pivot_table(index='variable', columns='country', aggfunc='size', fill_value=0)
common_vars = pivot[(pivot[countries[0]] > 0)]
for c in countries[1:]:
    common_vars = common_vars[common_vars[c] > 0]
common_variable_list = common_vars.index.tolist()

# Stop if no common variable found
if not common_variable_list:
    print("❌ No common variable found across all countries.")
    conn.close()
    exit()

selected_variable = common_variable_list[0]
print(f"✅ Using variable: {selected_variable}")

# Step 2: Query income share data
query_data = f"""
SELECT country, year, value
FROM data
WHERE variable = '{selected_variable}'
  AND percentile = 'p99p100'
  AND country IN ({','.join(f"'{c}'" for c in countries)})
  AND year >= 1980
ORDER BY country, year;
"""
df = pd.read_sql_query(query_data, conn)
conn.close()

# Step 3: Map country codes
country_map = {
    'US': 'United States',
    'FR': 'France',
    'GB': 'United Kingdom',
    'JP': 'Japan',
    'CN': 'China'
}
df['country'] = df['country'].map(country_map)

# Step 4: Convert to percentage
df['value'] = df['value'] * 100

# Step 5: Plot
plt.figure(figsize=(12, 7))
for country in df['country'].unique():
    subset = df[df['country'] == country]
    plt.plot(subset['year'], subset['value'], label=country)

plt.title(f"Top 1% Pre-Tax Income Share (1980–Present)\nVariable: {selected_variable}")
plt.xlabel("Year")
plt.ylabel("Income Share (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Step 6: Save
os.makedirs("output", exist_ok=True)
output_path = f"output/top1_income_share_{selected_variable}_intl.png"
plt.savefig(output_path, dpi=300)
plt.show()
