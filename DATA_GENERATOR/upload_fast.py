"""
Upload Extended ARGO Data to Supabase via REST API
Uses smaller batches and retry logic for reliability
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
import time

# Supabase configuration
SUPABASE_URL = "https://khrqbfssaanpcxdnnplc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtocnFiZnNzYWFucGN4ZG5ucGxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTQxMTAsImV4cCI6MjA4NDAzMDExMH0.1M6nzLx67qy6Ash92k3jHxpuJ8QvyCyKt2m5w_L_M7s"

def get_current_count():
    """Get current record count in Supabase"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Prefer": "count=exact"
    }
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=count", headers=headers, timeout=30)
    if r.status_code in [200, 206]:
        count = r.headers.get('content-range', '0-0/0').split('/')[-1]
        return int(count)
    return 0

def fetch_argo_data_single_day(date_str):
    """Fetch ARGO data for a single day using ERDDAP"""
    # Use the simpler tabledap query
    base_url = "https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats.csv"
    
    variables = "platform_number,time,latitude,longitude,pres,temp,psal,doxy"
    time_constraint = f"time>={date_str}T00:00:00Z&time<={date_str}T23:59:59Z"
    
    url = f"{base_url}?{variables}&{time_constraint}"
    
    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), skiprows=[1])
            return df
        elif response.status_code == 404:
            return pd.DataFrame()  # No data for this day
        else:
            print(f"    HTTP {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"    Timeout")
        return None
    except Exception as e:
        print(f"    Error: {str(e)[:50]}")
        return None

def upload_batch_to_supabase(records):
    """Upload a batch of records to Supabase"""
    if not records:
        return 0
        
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/argo_data",
            headers=headers,
            json=records,
            timeout=60
        )
        
        if response.status_code in [200, 201]:
            return len(records)
        else:
            return 0
    except:
        return 0

def process_dataframe(df):
    """Convert dataframe to records for upload"""
    records = []
    for _, row in df.iterrows():
        try:
            record = {
                "float_id": int(row.get('platform_number', 0)) if pd.notna(row.get('platform_number')) else None,
                "timestamp": str(row.get('time')) if pd.notna(row.get('time')) else None,
                "latitude": float(row.get('latitude')) if pd.notna(row.get('latitude')) else None,
                "longitude": float(row.get('longitude')) if pd.notna(row.get('longitude')) else None,
                "pressure": float(row.get('pres')) if pd.notna(row.get('pres')) else None,
                "temperature": float(row.get('temp')) if pd.notna(row.get('temp')) else None,
                "salinity": float(row.get('psal')) if pd.notna(row.get('psal')) else None,
                "dissolved_oxygen": float(row.get('doxy')) if pd.notna(row.get('doxy')) else None,
            }
            if record['float_id'] and record['timestamp']:
                records.append(record)
        except:
            continue
    return records

def main():
    print("=" * 60)
    print("ARGO Data Upload to Supabase (Fast Mode)")
    print("=" * 60)
    
    current_count = get_current_count()
    print(f"Current records: {current_count:,}")
    
    total_uploaded = 0
    
    # Upload data day by day from Nov 1, 2025 to Dec 19, 2025
    # (Fewer days to make it faster)
    start = datetime(2025, 11, 1)
    end = datetime(2025, 12, 19)
    
    current = start
    day_count = (end - start).days + 1
    processed = 0
    
    print(f"\nUploading {day_count} days of data...")
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        processed += 1
        
        print(f"[{processed}/{day_count}] {date_str}...", end=" ", flush=True)
        
        df = fetch_argo_data_single_day(date_str)
        
        if df is not None and len(df) > 0:
            records = process_dataframe(df)
            
            # Upload in small batches
            batch_size = 200
            day_uploaded = 0
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                uploaded = upload_batch_to_supabase(batch)
                day_uploaded += uploaded
                time.sleep(0.05)
            
            total_uploaded += day_uploaded
            print(f"✓ {day_uploaded:,} records (Total: {total_uploaded:,})")
        elif df is not None:
            print("No data")
        else:
            print("Failed - skipping")
        
        current += timedelta(days=1)
        time.sleep(0.1)
    
    print("\n" + "=" * 60)
    final_count = get_current_count()
    print(f"COMPLETE!")
    print(f"Uploaded this session: {total_uploaded:,}")
    print(f"Total in Supabase: {final_count:,}")
    print("=" * 60)

if __name__ == "__main__":
    main()
