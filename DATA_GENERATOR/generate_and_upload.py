"""
Generate and Upload ARGO-like data to Supabase
Generates realistic oceanographic data for historical dates
"""

import requests
import random
import math
from datetime import datetime, timedelta
import time

# Supabase configuration
SUPABASE_URL = "https://khrqbfssaanpcxdnnplc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtocnFiZnNzYWFucGN4ZG5ucGxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTQxMTAsImV4cCI6MjA4NDAzMDExMH0.1M6nzLx67qy6Ash92k3jHxpuJ8QvyCyKt2m5w_L_M7s"

# Realistic ARGO float IDs from Bay of Bengal / Indian Ocean region
FLOAT_IDS = [
    2902115, 2902116, 2902117, 2902118, 2902119,
    2902120, 2902121, 2902122, 2902123, 2902124,
    2902125, 2902126, 2902127, 2902128, 2902129,
    2902130, 2902131, 2902132, 2902133, 2902134,
    2902200, 2902201, 2902202, 2902203, 2902204,
    2902205, 2902206, 2902207, 2902208, 2902209,
    2903001, 2903002, 2903003, 2903004, 2903005,
]

# Pressure levels (in dbar)
PRESSURE_LEVELS = [10, 50, 100, 200, 500, 1000, 1500, 2000]

def get_current_count():
    """Get current record count"""
    headers = {"apikey": SUPABASE_KEY, "Prefer": "count=exact"}
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=count", headers=headers, timeout=30)
    if r.status_code in [200, 206]:
        return int(r.headers.get('content-range', '0-0/0').split('/')[-1])
    return 0

def generate_profile(float_id, timestamp, base_lat, base_lon):
    """Generate a realistic depth profile for a float"""
    records = []
    
    # Small random drift from base position
    lat = base_lat + random.uniform(-0.5, 0.5)
    lon = base_lon + random.uniform(-0.5, 0.5)
    
    for pressure in PRESSURE_LEVELS:
        # Temperature decreases with depth (realistic thermocline)
        if pressure < 100:
            temp = 28 + random.uniform(-2, 2) - (pressure * 0.02)
        elif pressure < 500:
            temp = 20 + random.uniform(-3, 3) - ((pressure - 100) * 0.015)
        else:
            temp = 5 + random.uniform(-2, 2) - ((pressure - 500) * 0.002)
        
        # Salinity varies with depth
        salinity = 34.5 + random.uniform(-0.5, 0.5) + (pressure * 0.0003)
        
        # Dissolved oxygen decreases with depth
        if pressure < 100:
            doxy = 200 + random.uniform(-20, 20)
        elif pressure < 500:
            doxy = 150 + random.uniform(-30, 30)
        else:
            doxy = 100 + random.uniform(-20, 20)
        
        records.append({
            "float_id": float_id,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "pressure": pressure,
            "temperature": round(temp, 4),
            "salinity": round(salinity, 4),
            "dissolved_oxygen": round(doxy, 4)
        })
    
    return records

def upload_batch(records):
    """Upload records to Supabase"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/argo_data", headers=headers, json=records, timeout=30)
        return len(records) if r.status_code in [200, 201] else 0
    except:
        return 0

def main():
    print("=" * 60)
    print("ARGO Data Generator & Uploader")
    print("=" * 60)
    
    initial_count = get_current_count()
    print(f"Current records in Supabase: {initial_count:,}")
    
    # Generate data from Sept 1 to Dec 19, 2025 (before existing data)
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2025, 12, 19)
    
    # Float base positions (Bay of Bengal / Indian Ocean)
    float_positions = {}
    for i, fid in enumerate(FLOAT_IDS):
        # Spread across Bay of Bengal region
        lat = 5 + (i % 7) * 2 + random.uniform(-1, 1)
        lon = 80 + (i // 7) * 3 + random.uniform(-1, 1)
        float_positions[fid] = (lat, lon)
    
    total_uploaded = 0
    current_date = start_date
    
    print(f"\nGenerating data from {start_date.date()} to {end_date.date()}")
    print(f"Floats: {len(FLOAT_IDS)}, Pressure levels: {len(PRESSURE_LEVELS)}")
    
    batch = []
    batch_size = 500
    day_count = 0
    
    while current_date <= end_date:
        day_count += 1
        
        # Each float profiles 1-2 times per day
        for float_id in FLOAT_IDS:
            # Random time during the day
            hour = random.randint(0, 23)
            ts = current_date.replace(hour=hour, minute=random.randint(0, 59))
            
            base_lat, base_lon = float_positions[float_id]
            # Drift the float slightly each day
            float_positions[float_id] = (
                base_lat + random.uniform(-0.1, 0.1),
                base_lon + random.uniform(-0.1, 0.1)
            )
            
            profile = generate_profile(float_id, ts, base_lat, base_lon)
            batch.extend(profile)
            
            # Upload when batch is full
            if len(batch) >= batch_size:
                uploaded = upload_batch(batch)
                total_uploaded += uploaded
                batch = []
                time.sleep(0.05)
        
        # Progress every 10 days
        if day_count % 10 == 0:
            print(f"  Day {day_count}: {current_date.date()} - Total uploaded: {total_uploaded:,}")
        
        current_date += timedelta(days=1)
    
    # Upload remaining
    if batch:
        uploaded = upload_batch(batch)
        total_uploaded += uploaded
    
    print("\n" + "=" * 60)
    final_count = get_current_count()
    print(f"COMPLETE!")
    print(f"Records generated & uploaded: {total_uploaded:,}")
    print(f"Total records in Supabase: {final_count:,}")
    print(f"Date range now: Sept 1, 2025 to Jan 13, 2026")
    print("=" * 60)

if __name__ == "__main__":
    main()
