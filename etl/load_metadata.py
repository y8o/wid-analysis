import pandas as pd
import sqlite3
from glob import glob
import os

# Create or connect to SQLite database
os.makedirs("data", exist_ok=True)
os.makedirs("etl", exist_ok=True)
db_path = "database/wid_world.db"
conn = sqlite3.connect(db_path)

# Function to load all metadata CSVs into a single SQLite table
metadata_files = sorted(glob("data/WID_metadata_*.csv"))

for i, file in enumerate(metadata_files):
    print(f"Loading {file}...")
    df = pd.read_csv(file, sep=";", encoding="utf-8")

    # Create table on first file, append afterwards
    if i == 0:
        df.to_sql("metadata", conn, index=False, if_exists="replace")
    else:
        df.to_sql("metadata", conn, index=False, if_exists="append")

print("\nAll metadata files loaded into 'metadata' table successfully.")

conn.close()
