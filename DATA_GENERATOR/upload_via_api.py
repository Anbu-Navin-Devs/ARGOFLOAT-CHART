"""
Upload ARGO data to Supabase using REST API
This bypasses the SQL pooler which may have circuit breaker issues
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

# Supabase credentials
SUPABASE_URL = "https://khrqbfssaanpcxdnnplc.supabase.co"
SUPABASE_KEY = None  # Will need to get from dashboard

def get_supabase_key():
    """Get Supabase anon key from environment or prompt"""
    key = os.getenv('SUPABASE_KEY')
    if not key:
        print("=" * 60)
        print("SUPABASE ANON KEY REQUIRED")
        print("=" * 60)
        print("Go to: https://supabase.com/dashboard/project/khrqbfssaanpcxdnnplc/settings/api")
        print("Copy the 'anon public' key")
        print("=" * 60)
        key = input("Paste your Supabase anon key: ").strip()
    return key

def test_connection(key):
    """Test if we can connect to Supabase"""
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Try to get count
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/argo_data?select=count",
        headers={**headers, "Prefer": "count=exact"},
    )
    
    if response.status_code == 200:
        count = response.headers.get('content-range', '').split('/')[-1]
        print(f"✓ Connected! Current records: {count}")
        return True
    else:
        print(f"✗ Connection failed: {response.status_code} - {response.text}")
        return False

def fetch_argo_data(start_date, end_date):
    """Fetch ARGO data from ERDDAP"""
    base_url = "https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats-index.csv"
    
    # Build constraints
    constraints = f"time>={start_date}T00:00:00Z&time<={end_date}T23:59:59Z"
    variables = "platform_code,time,latitude,longitude,pres,temp,psal,doxy"
    
    url = f"{base_url}?{variables}&{constraints}"
    print(f"Fetching data from {start_date} to {end_date}...")
    
    try:
        response = requests.get(url, timeout=300)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), skiprows=[1])  # Skip units row
            print(f"  Fetched {len(df)} records")
            return df
        else:
            print(f"  Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def upload_batch(df_batch, headers):
    """Upload a batch of data to Supabase"""
    records = []
    for _, row in df_batch.iterrows():
        record = {
            "float_id": int(row.get('platform_code', 0)) if pd.notna(row.get('platform_code')) else None,
            "timestamp": row.get('time'),
            "latitude": float(row.get('latitude')) if pd.notna(row.get('latitude')) else None,
            "longitude": float(row.get('longitude')) if pd.notna(row.get('longitude')) else None,
            "pressure": float(row.get('pres')) if pd.notna(row.get('pres')) else None,
            "temperature": float(row.get('temp')) if pd.notna(row.get('temp')) else None,
            "salinity": float(row.get('psal')) if pd.notna(row.get('psal')) else None,
            "dissolved_oxygen": float(row.get('doxy')) if pd.notna(row.get('doxy')) else None,
        }
        if record['float_id'] is not None:
            records.append(record)
    
    if not records:
        return 0
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/argo_data",
        headers={**headers, "Prefer": "return=minimal"},
        json=records
    )
    
    if response.status_code in [200, 201]:
        return len(records)
    else:
        print(f"    Upload error: {response.status_code} - {response.text[:200]}")
        return 0

def main():
    print("=" * 60)
    print("ARGO Data Upload to Supabase via REST API")
    print("=" * 60)
    
    # Get API key
    key = get_supabase_key()
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Test connection
    if not test_connection(key):
        print("\nCannot connect. Check your API key.")
        return
    
    # Date range: Sept 1, 2025 to Jan 15, 2026
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 1, 15)
    
    total_uploaded = 0
    current = start_date
    
    while current <= end_date:
        # Fetch one week at a time
        week_end = min(current + timedelta(days=7), end_date)
        
        df = fetch_argo_data(
            current.strftime("%Y-%m-%d"),
            week_end.strftime("%Y-%m-%d")
        )
        
        if df is not None and len(df) > 0:
            # Upload in batches of 1000
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                uploaded = upload_batch(batch, headers)
                total_uploaded += uploaded
                print(f"    Batch {i//batch_size + 1}: {uploaded} records uploaded (Total: {total_uploaded})")
        
        current = week_end + timedelta(days=1)
    
    print("=" * 60)
    print(f"COMPLETE! Total records uploaded: {total_uploaded}")
    print("=" * 60)

if __name__ == "__main__":
    main()
