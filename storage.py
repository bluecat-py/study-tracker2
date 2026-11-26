import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path

from stats import study_day

#folder to run it from
BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "study_tracker.db"
SCHEMA_FILE = BASE_DIR / "schema.sql"