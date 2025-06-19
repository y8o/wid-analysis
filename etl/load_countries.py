import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database/wid_world.db")
cursor = conn.cursor()

# Ensure the 'countries' table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS countries (
    alpha2 TEXT,
    titlename TEXT,
    shortname TEXT,
    region TEXT,
    region2 TEXT
)
""")
conn.commit()

# Load the countries CSV file
df = pd.read_csv("data/WID_countries.csv", sep=";", encoding="utf-8")

# Insert into the 'countries' table
df.to_sql("countries", conn, if_exists="replace", index=False)

conn.close()
print("Country codes loaded into 'countries' table.")
