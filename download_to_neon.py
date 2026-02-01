"""
Direct script to download ARGO data to Neon database.
Downloads Indian Ocean data for 2025.
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from io import StringIO
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load environment
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file")
    sys.exit(1)

print(f"📊 Connecting to Neon database...")
print(f"   URL: {DATABASE_URL[:50]}...")

# Connect to Neon
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False  # Use explicit commits for better performance
    cursor = conn.cursor()
    print("✅ Connected to Neon!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# Create table
print("\n📋 Creating argo_data table...")
cursor.execute("""
    DROP TABLE IF EXISTS argo_data;
    CREATE TABLE argo_data (
        id SERIAL PRIMARY KEY,
        float_id BIGINT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL,
        temperature DOUBLE PRECISION,
        salinity DOUBLE PRECISION,
        pressure DOUBLE PRECISION
    );
    
    CREATE INDEX idx_argo_float_id ON argo_data(float_id);
    CREATE INDEX idx_argo_timestamp ON argo_data(timestamp);
    CREATE INDEX idx_argo_location ON argo_data(latitude, longitude);
""")
conn.commit()
print("✅ Table created with indexes!")

# ERDDAP settings
ERDDAP_URL = "https://erddap.ifremer.fr/erddap/tabledap"
DATASET_ID = "ArgoFloats"

# Indian Ocean bounds
LAT_MIN, LAT_MAX = -40, 25
LON_MIN, LON_MAX = 30, 120

# Date range: 2025 first half (keep data small for 0.5GB limit)
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 6, 30)

print(f"\n🌊 Downloading Indian Ocean data...")
print(f"   Region: Lat {LAT_MIN}° to {LAT_MAX}°, Lon {LON_MIN}° to {LON_MAX}°")
print(f"   Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")

total_records = 0
chunk_days = 30
current_date = START_DATE

while current_date < END_DATE:
    chunk_end = min(current_date + timedelta(days=chunk_days), END_DATE)
    
    print(f"\n📥 Fetching {current_date.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}...")
    
    url = (
        f"{ERDDAP_URL}/{DATASET_ID}.csv?"
        f"platform_number,time,latitude,longitude,temp,psal,pres"
        f"&time>={current_date.strftime('%Y-%m-%dT00:00:00Z')}"
        f"&time<={chunk_end.strftime('%Y-%m-%dT23:59:59Z')}"
        f"&latitude>={LAT_MIN}&latitude<={LAT_MAX}"
        f"&longitude>={LON_MIN}&longitude<={LON_MAX}"
        f"&orderBy(%22time%22)"
    )
    
    try:
        response = requests.get(url, timeout=300)
        
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), skiprows=[1])
            
            if not df.empty:
                # Rename columns
                df = df.rename(columns={
                    "platform_number": "float_id",
                    "time": "timestamp",
                    "temp": "temperature",
                    "psal": "salinity",
                    "pres": "pressure"
                })
                
                # Clean data
                df["float_id"] = df["float_id"].astype(str).str.extract(r'(\d+)')
                df["float_id"] = pd.to_numeric(df["float_id"], errors='coerce')
                df = df.dropna(subset=["float_id", "latitude", "longitude", "timestamp"])
                
                # Insert to database
                values = []
                for _, row in df.iterrows():
                    try:
                        val = (
                            int(row["float_id"]),
                            row["timestamp"],
                            float(row["latitude"]),
                            float(row["longitude"]),
                            float(row["temperature"]) if pd.notna(row.get("temperature")) else None,
                            float(row["salinity"]) if pd.notna(row.get("salinity")) else None,
                            float(row["pressure"]) if pd.notna(row.get("pressure")) else None
                        )
                        values.append(val)
                    except (ValueError, TypeError):
                        continue
                
                if values:
                    # Insert in batches of 1000
                    batch_size = 1000
                    for i in range(0, len(values), batch_size):
                        batch = values[i:i + batch_size]
                        execute_values(
                            cursor,
                            """INSERT INTO argo_data 
                               (float_id, timestamp, latitude, longitude, temperature, salinity, pressure)
                               VALUES %s""",
                            batch,
                            page_size=500
                        )
                    conn.commit()
                    total_records += len(values)
                    print(f"   ✅ Inserted {len(values)} records (Total: {total_records})")
                else:
                    print(f"   ⚠️ No valid records in this chunk")
            else:
                print(f"   ⚠️ No data returned for this period")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except requests.Timeout:
        print(f"   ⏰ Timeout - skipping this chunk")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    current_date = chunk_end

# Final stats
print(f"\n" + "="*50)
cursor.execute("SELECT COUNT(*), COUNT(DISTINCT float_id), MIN(timestamp), MAX(timestamp) FROM argo_data")
stats = cursor.fetchone()
print(f"✅ Download Complete!")
print(f"   Total Records: {stats[0]:,}")
print(f"   Unique Floats: {stats[1]:,}")
print(f"   Date Range: {stats[2]} to {stats[3]}")
print("="*50)

cursor.close()
conn.close()
print("\n🎉 Data successfully loaded to Neon!")
