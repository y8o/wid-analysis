import os
import pandas as pd
import sqlite3
import glob

# Set your data directory path
DATA_DIR = "data"
conn = sqlite3.connect("wid_world.db")

# Load WID_countries.csv first
print("Loading countries...")
df_countries = pd.read_csv(os.path.join(DATA_DIR, "WID_countries.csv"), sep=";")
df_countries.to_sql("countries", conn, if_exists="replace", index=False)

# Helper function to load one file at a time
def insert_csv_files(file_list, table_name):
    for f in file_list:
        print(f"Inserting {os.path.basename(f)} into {table_name}...")
        try:
            df = pd.read_csv(f, sep=";")
            df.to_sql(table_name, conn, if_exists="append", index=False)
        except Exception as e:
            print(f"⚠️ Error loading {f}: {e}")

# Insert data files (one at a time)
data_files = glob.glob(os.path.join(DATA_DIR, "WID_data_*.csv"))
insert_csv_files(data_files, "data")

# Insert metadata files (one at a time)
meta_files = glob.glob(os.path.join(DATA_DIR, "WID_metadata_*.csv"))
insert_csv_files(meta_files, "metadata")

conn.close()
print("✅ All files loaded safely into SQLite.")
