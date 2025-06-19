import pandas as pd
import sqlite3
import glob
import os

# Connect to SQLite database
conn = sqlite3.connect("database/wid_world.db")
cursor = conn.cursor()

# Ensure the 'data' table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS data (
    country TEXT,
    variable TEXT,
    percentile TEXT,
    year INTEGER,
    value REAL,
    age TEXT,
    pop TEXT
)
""")
conn.commit()

# Get all WID_data_*.csv files
data_files = glob.glob("data/WID_data_*.csv")

# Load and insert each file
for file in data_files:
    print(f"Processing: {file}")
    df = pd.read_csv(file, sep=';', encoding='utf-8')
    df.to_sql("data", conn, if_exists="append", index=False)

conn.close()
print("All data files loaded into 'data' table.")