import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("data/wid_world.db")

# Query top 1% income share over time
query = """
SELECT country, year, value
FROM data
WHERE variable = 'sptinci999'
  AND percentile = 'p99p100'
  AND country IN ('US')
ORDER BY country, year;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Optional: map country codes to names
country_map = {'US': 'United States'}
df['country'] = df['country'].map(country_map)

# Plot
plt.figure(figsize=(10,6))
for country in df['country'].unique():
    subset = df[df['country'] == country]
    plt.plot(subset['year'], subset['value'], label=country)

plt.title("Top 1% Pre-Tax Income Share in the United States (1915–2020)")
plt.xlabel("Year")
plt.ylabel("Income Share")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/usa_top1_income_share.png", dpi=300)
plt.show()
