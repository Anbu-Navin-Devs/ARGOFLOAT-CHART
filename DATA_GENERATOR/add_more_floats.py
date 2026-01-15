"""
Add more ARGO floats and recent data
"""

import requests
import random
from datetime import datetime, timedelta
import time

SUPABASE_URL = "https://khrqbfssaanpcxdnnplc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtocnFiZnNzYWFucGN4ZG5ucGxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTQxMTAsImV4cCI6MjA4NDAzMDExMH0.1M6nzLx67qy6Ash92k3jHxpuJ8QvyCyKt2m5w_L_M7s"

# Additional floats from different ocean regions
EXTRA_FLOATS = [
    # Arabian Sea
    (2903100, 15, 65), (2903101, 18, 62), (2903102, 12, 68),
    # Pacific
    (5905001, 5, 140), (5905002, 10, 145), (5905003, -5, 150),
    # Atlantic  
    (6901001, 25, -40), (6901002, 30, -35), (6901003, 20, -45),
    # Southern Ocean
    (1901001, -50, 60), (1901002, -55, 80), (1901003, -45, 100),
]

PRESSURE_LEVELS = [10, 50, 100, 200, 500, 1000, 1500, 2000]

def upload_batch(records):
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

def generate_profile(float_id, timestamp, lat, lon):
    records = []
    for pressure in PRESSURE_LEVELS:
        # Adjust temperature based on latitude
        base_temp = 28 - abs(lat) * 0.3
        if pressure < 100:
            temp = base_temp + random.uniform(-2, 2) - (pressure * 0.02)
        elif pressure < 500:
            temp = base_temp - 8 + random.uniform(-3, 3) - ((pressure - 100) * 0.015)
        else:
            temp = 5 + random.uniform(-2, 2)
        
        salinity = 34.5 + random.uniform(-0.5, 0.5) + (pressure * 0.0003)
        doxy = 180 - pressure * 0.05 + random.uniform(-20, 20)
        
        records.append({
            "float_id": float_id,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "latitude": round(lat + random.uniform(-0.3, 0.3), 6),
            "longitude": round(lon + random.uniform(-0.3, 0.3), 6),
            "pressure": pressure,
            "temperature": round(max(temp, 0), 4),
            "salinity": round(salinity, 4),
            "dissolved_oxygen": round(max(doxy, 50), 4)
        })
    return records

def main():
    print("Adding more floats and recent data...")
    
    total = 0
    batch = []
    
    # Add extra floats for the full date range
    start = datetime(2025, 9, 1)
    end = datetime(2026, 1, 15)
    
    for float_id, base_lat, base_lon in EXTRA_FLOATS:
        current = start
        lat, lon = base_lat, base_lon
        
        while current <= end:
            ts = current.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))
            profile = generate_profile(float_id, ts, lat, lon)
            batch.extend(profile)
            
            # Drift
            lat += random.uniform(-0.1, 0.1)
            lon += random.uniform(-0.1, 0.1)
            
            if len(batch) >= 500:
                uploaded = upload_batch(batch)
                total += uploaded
                batch = []
                time.sleep(0.05)
            
            current += timedelta(days=1)
    
    # Upload remaining
    if batch:
        total += upload_batch(batch)
    
    # Check final count
    headers = {"apikey": SUPABASE_KEY, "Prefer": "count=exact"}
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=count", headers=headers)
    final = r.headers.get('content-range', '0-0/0').split('/')[-1]
    
    print(f"Added {total:,} records from {len(EXTRA_FLOATS)} extra floats")
    print(f"Total records in Supabase: {final}")

if __name__ == "__main__":
    main()
