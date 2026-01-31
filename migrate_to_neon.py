"""
FloatChart - Database Migration Script
Migrates data from CockroachDB to Neon PostgreSQL (2020-2026 only)

This script:
1. Connects to source (CockroachDB) and destination (Neon)
2. Creates table in Neon
3. Copies only 2020-2026 data (~15-20M rows)
4. Creates optimized indexes

Usage:
    python migrate_to_neon.py
"""

import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()

# ========================================
# CONFIGURE THESE BEFORE RUNNING
# ========================================

# Source: CockroachDB (your current database)
SOURCE_DB_URL = os.getenv("DATABASE_URL")  # Your CockroachDB URL

# Destination: Neon PostgreSQL 
# Set this in your .env file as NEON_DATABASE_URL or replace here
DEST_DB_URL = os.getenv("NEON_DATABASE_URL")

# Data range to migrate (last 6 years - 2020 to 2026)
START_YEAR = 2020
END_YEAR = 2026

BATCH_SIZE = 5000  # Rows per batch (smaller for stability)

# ========================================

def create_table(conn):
    """Create the argo_data table in destination."""
    cursor = conn.cursor()
    
    # Drop if exists (fresh start)
    cursor.execute("DROP TABLE IF EXISTS argo_data CASCADE")
    
    # Create table
    cursor.execute("""
        CREATE TABLE argo_data (
            id SERIAL PRIMARY KEY,
            float_id BIGINT,
            timestamp TIMESTAMP,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            temperature DOUBLE PRECISION,
            salinity DOUBLE PRECISION,
            pressure DOUBLE PRECISION,
            UNIQUE(float_id, timestamp, pressure)
        )
    """)
    
    conn.commit()
    print("✅ Table created")


def create_indexes(conn):
    """Create optimized indexes for fast queries."""
    cursor = conn.cursor()
    
    indexes = [
        "CREATE INDEX idx_argo_timestamp ON argo_data(timestamp)",
        "CREATE INDEX idx_argo_float ON argo_data(float_id)",
        "CREATE INDEX idx_argo_location ON argo_data(latitude, longitude)",
        "CREATE INDEX idx_argo_float_time ON argo_data(float_id, timestamp DESC)",
        "CREATE INDEX idx_argo_geo_time ON argo_data(latitude, longitude, timestamp DESC)",
        "CREATE INDEX idx_argo_time_geo ON argo_data(timestamp, latitude, longitude)",
    ]
    
    for idx_sql in indexes:
        try:
            cursor.execute(idx_sql)
            print(f"  ✓ {idx_sql.split('idx_')[1].split(' ')[0]}")
        except Exception as e:
            print(f"  ⚠ Index error: {e}")
    
    conn.commit()
    print("✅ Indexes created")


def migrate_data(source_conn, dest_conn):
    """Migrate data from source to destination in batches."""
    source_cursor = source_conn.cursor()
    dest_cursor = dest_conn.cursor()
    
    # Count source rows
    source_cursor.execute(f"""
        SELECT COUNT(*) FROM argo_data 
        WHERE timestamp >= '{START_YEAR}-01-01' AND timestamp < '{END_YEAR + 1}-01-01'
    """)
    total_rows = source_cursor.fetchone()[0]
    print(f"\n📊 Rows to migrate: {total_rows:,} ({START_YEAR}-{END_YEAR})")
    
    # Fetch and insert in batches
    offset = 0
    migrated = 0
    start_time = datetime.now()
    
    while True:
        source_cursor.execute(f"""
            SELECT float_id, timestamp, latitude, longitude, temperature, salinity, pressure
            FROM argo_data
            WHERE timestamp >= '{START_YEAR}-01-01' AND timestamp < '{END_YEAR + 1}-01-01'
            ORDER BY timestamp
            LIMIT {BATCH_SIZE} OFFSET {offset}
        """)
        
        rows = source_cursor.fetchall()
        if not rows:
            break
        
        # Insert into destination
        execute_values(
            dest_cursor,
            """
            INSERT INTO argo_data (float_id, timestamp, latitude, longitude, temperature, salinity, pressure)
            VALUES %s
            ON CONFLICT (float_id, timestamp, pressure) DO NOTHING
            """,
            rows,
            page_size=1000
        )
        dest_conn.commit()
        
        migrated += len(rows)
        offset += BATCH_SIZE
        
        # Progress
        elapsed = (datetime.now() - start_time).seconds or 1
        rate = migrated / elapsed
        remaining = (total_rows - migrated) / rate if rate > 0 else 0
        
        print(f"\r  Migrated: {migrated:,}/{total_rows:,} ({migrated*100//total_rows}%) - {rate:.0f} rows/sec - ETA: {remaining/60:.1f} min", end="", flush=True)
    
    print(f"\n\n✅ Migration complete! {migrated:,} rows transferred")


def verify_migration(dest_conn):
    """Verify the migration was successful."""
    cursor = dest_conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM argo_data")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT float_id) FROM argo_data")
    floats = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM argo_data")
    min_date, max_date = cursor.fetchone()
    
    print(f"\n📊 Verification:")
    print(f"   Total records: {total:,}")
    print(f"   Unique floats: {floats:,}")
    print(f"   Date range: {min_date} to {max_date}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║     FloatChart - CockroachDB to Neon Migration                ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    if "neon" not in DEST_DB_URL.lower() and "NEON" not in DEST_DB_URL:
        print("⚠️  Warning: DEST_DB_URL doesn't look like a Neon URL")
        print(f"   Current: {DEST_DB_URL[:50]}...")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    print(f"🔗 Connecting to source (CockroachDB)...")
    source_conn = psycopg2.connect(SOURCE_DB_URL)
    print("   ✓ Connected")
    
    print(f"🔗 Connecting to destination (Neon)...")
    dest_conn = psycopg2.connect(DEST_DB_URL)
    print("   ✓ Connected")
    
    print(f"\n📦 Creating table...")
    create_table(dest_conn)
    
    print(f"\n🚀 Starting migration ({START_YEAR}-{END_YEAR})...")
    migrate_data(source_conn, dest_conn)
    
    print(f"\n🔧 Creating indexes...")
    create_indexes(dest_conn)
    
    verify_migration(dest_conn)
    
    source_conn.close()
    dest_conn.close()
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                    ✅ MIGRATION COMPLETE!                      ║
╚═══════════════════════════════════════════════════════════════╝

Next steps:
1. Update your .env with the Neon DATABASE_URL
2. Deploy to Railway with the new DATABASE_URL
3. Test the app - it should be 3-5x faster!

""")


if __name__ == "__main__":
    main()
