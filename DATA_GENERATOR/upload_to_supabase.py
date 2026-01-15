"""Upload historical ARGO data to Supabase."""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DATA_GENERATOR.env_utils import load_environment
load_environment()

from DATA_GENERATOR.pipeline.netcdf_fetcher import fetch_argo_data
from DATA_GENERATOR.pipeline.db_loader import load_into_postgres

def main():
    # Full date range from Sept 2025 to Jan 2026
    chunks = [
        # September 2025
        ("2025-09-01", "2025-09-10"),
        ("2025-09-11", "2025-09-20"),
        ("2025-09-21", "2025-09-30"),
        # October 2025
        ("2025-10-01", "2025-10-10"),
        ("2025-10-11", "2025-10-20"),
        ("2025-10-21", "2025-10-31"),
        # November 2025
        ("2025-11-01", "2025-11-10"),
        ("2025-11-11", "2025-11-20"),
        ("2025-11-21", "2025-11-30"),
        # December 2025
        ("2025-12-01", "2025-12-10"),
        ("2025-12-11", "2025-12-20"),
        ("2025-12-21", "2025-12-31"),
        # January 2026
        ("2026-01-01", "2026-01-10"),
        ("2026-01-11", "2026-01-15"),
    ]
    
    total_inserted = 0
    
    for start_str, end_str in chunks:
        print(f"\n{'='*60}")
        print(f"📅 Fetching: {start_str} to {end_str}")
        print('='*60)
        
        start = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end = datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        
        try:
            df = fetch_argo_data(start, end, progress_callback=print)
            
            if df is not None and not df.empty:
                print(f"\n📊 Fetched {len(df)} records")
                total, inserted, _ = load_into_postgres(df)
                print(f"✅ Inserted {inserted} new records (of {total})")
                total_inserted += inserted
            else:
                print("⚠️ No data fetched for this period")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print(f"🎉 TOTAL NEW RECORDS INSERTED: {total_inserted}")
    print('='*60)

if __name__ == "__main__":
    main()
