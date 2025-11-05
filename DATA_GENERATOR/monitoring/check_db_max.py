"""Quick helper to inspect the latest records stored in Postgres."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    """Print aggregate metrics and recent rows from the argo_data table."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / ".." / ".env",
        script_dir / ".." / ".." / ".env",
        script_dir / ".." / ".." / "ARGO_CHATBOT" / ".env",
    ]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            load_dotenv(resolved)

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in .env files. Please set it and try again.")
        return

    engine = create_engine(database_url)
    with engine.connect() as connection:
        try:
            row = connection.execute(
                text('SELECT COUNT(*) AS cnt, MIN("timestamp") AS min_ts, MAX("timestamp") AS max_ts FROM argo_data')
            ).fetchone()
            if row is None:
                print("No results returned; is the 'argo_data' table present?")
                return

            cnt, min_ts, max_ts = row
            print(f"argo_data rows: {cnt}")
            print(f"min(timestamp): {min_ts}")
            print(f"max(timestamp): {max_ts}")
            sample = connection.execute(
                text('SELECT "float_id","timestamp","latitude","longitude" FROM argo_data ORDER BY "timestamp" DESC LIMIT 5')
            ).fetchall()
            print("\nLatest 5 rows:")
            for record in sample:
                print(record)
        except Exception as exc:  # noqa: BLE001
            print(f"Error querying database: {exc}")


if __name__ == "__main__":
    main()
