import sqlite3
import os

# Config
SOURCE_DB = "database/wid_world.db"
TARGET_FOLDER = "demo"
TARGET_DB = os.path.join(TARGET_FOLDER, "demo.db")
countries = ("FR", "US", "GB", "IT","MX")
start_year = 1980

# Make sure demo folder exists
os.makedirs(TARGET_FOLDER, exist_ok=True)

# Connect to source and target databases
with sqlite3.connect(SOURCE_DB) as src_conn, sqlite3.connect(TARGET_DB) as tgt_conn:
    src_cur = src_conn.cursor()
    tgt_cur = tgt_conn.cursor()

    print(f"🔧 Creating demo database at {TARGET_DB}")

    # === Discover shared variables ===
    print("🔎 Finding shared variables...")
    src_cur.execute(f"""
        SELECT country, variable FROM data
        WHERE country IN ({",".join("?" * len(countries))})
    """, countries)

    # Build dictionary: {country: set(variables)}
    country_vars = {}
    for country, var in src_cur.fetchall():
        country_vars.setdefault(country, set()).add(var)

    shared_vars = set.intersection(*country_vars.values())

    if not shared_vars:
        raise RuntimeError("❌ No shared variables found across all selected countries.")
    else:
        print(f"✅ Found {len(shared_vars)} shared variables across {', '.join(countries)}")

    variables = tuple(shared_vars)

    # === Export `data` table ===
    print("📦 Exporting `data` table...")
    src_cur.execute(f"""
        SELECT * FROM data
        WHERE country IN ({",".join("?" * len(countries))})
          AND year >= ?
          AND variable IN ({",".join("?" * len(variables))})
    """, (*countries, start_year, *variables))
    data_rows = src_cur.fetchall()
    tgt_cur.execute("""
        CREATE TABLE data (
            country TEXT, variable TEXT, percentile TEXT,
            year INTEGER, value REAL, age TEXT, pop TEXT
        )
    """)
    tgt_cur.executemany("""
        INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data_rows)
    print(f"✅ Exported {len(data_rows):,} rows from `data`")

    # === Export `metadata` table ===
    print("📦 Exporting `metadata` table...")
    src_cur.execute(f"""
        SELECT * FROM metadata
        WHERE country IN ({",".join("?" * len(countries))})
          AND variable IN ({",".join("?" * len(variables))})
    """, (*countries, *variables))
    meta_rows = src_cur.fetchall()

    tgt_cur.execute("""
        CREATE TABLE metadata (
            country TEXT, variable TEXT, age TEXT, pop TEXT,
            countryname TEXT, shortname TEXT, simpledes TEXT,
            technicaldes TEXT, shorttype TEXT, longtype TEXT,
            shortpop TEXT, longpop TEXT, shortage TEXT,
            longage TEXT, unit TEXT, source TEXT, method TEXT,
            extrapolation TEXT, exception TEXT
        )
    """)
    tgt_cur.executemany("""
        INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, meta_rows)
    print(f"✅ Exported {len(meta_rows)} rows from `metadata`")

    # === Export `countries` table ===
    print("📦 Exporting `countries` table...")
    src_cur.execute(f"""
        SELECT * FROM countries
        WHERE alpha2 IN ({",".join("?" * len(countries))})
    """, countries)
    country_rows = src_cur.fetchall()
    tgt_cur.execute("""
        CREATE TABLE countries (
            alpha2 TEXT, titlename TEXT,
            shortname TEXT, region TEXT, region2 TEXT
        )
    """)
    tgt_cur.executemany("""
        INSERT INTO countries VALUES (?, ?, ?, ?, ?)
    """, country_rows)
    print(f"✅ Exported {len(country_rows)} rows from `countries`")

    # === Check what variables were actually loaded ===
    print("🔍 Verifying coverage of requested countries and variables...")
    exported_vars = {row[1] for row in data_rows}
    missing_vars = sorted(set(variables) - exported_vars)
    if missing_vars:
        print(f"⚠️  These shared variables had no matching `data` in the filtered range: {missing_vars}")
    else:
        print("✅ All shared variables exported successfully.")

    tgt_conn.commit()
    print("🎉 Demo database export complete!")
