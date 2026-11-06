import os, sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "failsafe.db"

def database_path():
    return Path(os.getenv("FAILSAFE_DB_PATH", str(DEFAULT_DB)))

def get_connection():
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    return db

def initialise_database():
    with get_connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS clinic_records (
          record_id TEXT PRIMARY KEY, clinic_code TEXT NOT NULL,
          reporting_date TEXT NOT NULL, department TEXT NOT NULL,
          metric TEXT NOT NULL, value REAL NOT NULL CHECK(value >= 0),
          unit TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'api',
          sync_status TEXT NOT NULL DEFAULT 'pending'
            CHECK(sync_status IN ('pending','synced')),
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_records_clinic ON clinic_records(clinic_code);
        CREATE INDEX IF NOT EXISTS idx_records_sync ON clinic_records(sync_status);
        CREATE INDEX IF NOT EXISTS idx_records_date ON clinic_records(reporting_date);
        """)

def as_dict(row):
    return dict(row)
