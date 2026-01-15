"""
Upload Extended ARGO Data to Supabase via REST API
This script fetches ARGO float data from ERDDAP and uploads to Supabase
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
import time

# Supabase configuration
SUPABASE_URL = "https://khrqbfssaanpcxdnnplc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtocnFiZnNzYWFucGN4ZG5ucGxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTQxMTAsImV4cCI6MjA4NDAzMDExMH0.1M6nzLx67qy6Ash92k3jHxpuJ8QvyCyKt2m5w_L_M7s"

# ERDDAP base URL for ARGO data
ERDDAP_URL = "https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats.csv"

def get_current_count():
    """Get current record count in Supabase"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Prefer": "count=exact"
    }
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=count", headers=headers)
    if r.status_code in [200, 206]:
        count = r.headers.get('content-range', '0-0/0').split('/')[-1]
        return int(count)
    return 0

def get_date_range_in_db():
    """Get the date range of existing data"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    # Get min date
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=timestamp&order=timestamp.asc&limit=1", headers=headers)
    min_date = None
    if r.status_code == 200 and r.json():
        min_date = r.json()[0].get('timestamp', '')[:10]
    
    # Get max date
    r = requests.get(f"{SUPABASE_URL}/rest/v1/argo_data?select=timestamp&order=timestamp.desc&limit=1", headers=headers)
    max_date = None
    if r.status_code == 200 and r.json():
        max_date = r.json()[0].get('timestamp', '')[:10]
    
    return min_date, max_date

def fetch_argo_data(start_date, end_date):
    """Fetch ARGO profile data from ERDDAP"""
    # Build query with proper constraints
    base_url = "https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats.csv"
    
    # Select specific variables
    variables = "platform_number,time,latitude,longitude,pres,temp,psal,doxy"
    
    # Time constraints (ISO format)
    time_start = f"{start_date}T00:00:00Z"
    time_end = f"{end_date}T23:59:59Z"
    
    url = f"{base_url}?{variables}&time>={time_start}&time<={time_end}&orderBy(%22time%22)"
    
    print(f"  Fetching: {start_date} to {end_date}...")
    
    try:
        response = requests.get(url, timeout=300)
        if response.status_code == 200:
            # Parse CSV, skip the units row (second row)
            df = pd.read_csv(StringIO(response.text), skiprows=[1])
            print(f"    Got {len(df)} records")
            return df
        else:
            print(f"    Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"    Exception: {str(e)[:100]}")
        return None

def upload_batch_to_supabase(records):
    """Upload a batch of records to Supabase"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/argo_data",
        headers=headers,
        json=records
    )
    
    if response.status_code in [200, 201]:
        return len(records)
    else:
        print(f"      Upload error: {response.status_code} - {response.text[:200]}")
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
            if record['float_id'] is not None and record['timestamp'] is not None:
                records.append(record)
        except Exception as e:
            continue
    return records

def main():
    print("=" * 60)
    print("ARGO Data Upload to Supabase")
    print("=" * 60)
    
    # Check current status
    current_count = get_current_count()
    print(f"Current records in Supabase: {current_count:,}")
    
    min_date, max_date = get_date_range_in_db()
    print(f"Current date range: {min_date} to {max_date}")
    
    # We want to add data BEFORE Dec 20, 2025 (go back to Sept 1, 2025)
    # Target: Sept 1, 2025 to Dec 19, 2025
    
    print("\n" + "=" * 60)
    print("Uploading historical data: Sept 1 to Dec 19, 2025")
    print("=" * 60)
    
    total_uploaded = 0
    
    # Process in weekly chunks
    start = datetime(2025, 9, 1)
    end = datetime(2025, 12, 19)
    
    current = start
    while current <= end:
        week_end = min(current + timedelta(days=6), end)
        
        # Fetch data
        df = fetch_argo_data(
            current.strftime("%Y-%m-%d"),
            week_end.strftime("%Y-%m-%d")
        )
        
        if df is not None and len(df) > 0:
            # Process and upload in batches
            records = process_dataframe(df)
            print(f"    Processing {len(records)} valid records...")
            
            batch_size = 500
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                uploaded = upload_batch_to_supabase(batch)
                total_uploaded += uploaded
                if (i // batch_size) % 10 == 0:
                    print(f"      Progress: {i+len(batch)}/{len(records)} | Total uploaded: {total_uploaded:,}")
                time.sleep(0.1)  # Small delay to avoid rate limits
        
        current = week_end + timedelta(days=1)
    
    # Also get data after Jan 13, 2026 up to today
    print("\n" + "=" * 60)
    print("Uploading recent data: Jan 14 to Jan 15, 2026")
    print("=" * 60)
    
    df = fetch_argo_data("2026-01-14", "2026-01-15")
    if df is not None and len(df) > 0:
        records = process_dataframe(df)
        batch_size = 500
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            uploaded = upload_batch_to_supabase(batch)
            total_uploaded += uploaded
            time.sleep(0.1)
    
    # Final count
    print("\n" + "=" * 60)
    final_count = get_current_count()
    print(f"COMPLETE!")
    print(f"Records uploaded this session: {total_uploaded:,}")
    print(f"Total records in Supabase: {final_count:,}")
    print("=" * 60)

if __name__ == "__main__":
    main()
