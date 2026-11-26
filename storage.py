import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path

from stats import study_day

#folder to run it from
BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "study_tracker.db"
SCHEMA_FILE = BASE_DIR / "schema.sql"

@contextmanager
def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with connect() as conn:
        conn.executescript(SCHEMA_FILE.read_text())

#SUBJECTS
def add_subject(name: str) -> int:
    name = name.strip()
    if not name:
        raise ValueError("Subject name cannot be empty.")
    try:
        with connect() as conn:
            cursor = conn.execute("INSERT INTO subjects (name) VALUES (?)",(name,))
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError(f"Subject '{name}' already exists.") from None

def list_subjects(include_archived: bool = False) -> list[dict]:
    sql = "SELECT id, name, archived FROM subjects"
    if not include_archived:
        sql += " WHERE archived = 0"
    sql += " ORDER BY name"
    with connect() as conn:
        return [dict(row) for row in conn.execute(sql)]

#SESSIONS
def add_session(
    subject_id: int,
    minutes: int,
    day: str | None = None,
    source: str = "manual",
    started_at: str | None = None,
    note: str | None = None,
) -> int:
    if not isinstance(minutes, int) or minutes <= 0:
        raise ValueError("Minutes must be a whole number above 0.")
    if day is None:
        day = study_day(datetim.now()).isoformat()
    else:
        try:
            day = date.fromisoformat(day).isoformat()
        except(TypeError, ValueError):
            raise ValueError("Date must look like YYYY-MM-DD.") from None
    try:
        with connect() as conn:
            cursor = conn.execute(
                "INSERT INTO sessions (subject_id, minutes, date, started_at, source, note) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (subject_id, minutes, day, started_at, source, note),
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Could not save the session. Check that the subject exists.") from None
    
sql = """
    SELECT sessions.id, subjects.name AS subject, sessions.minutes,
            sessions.date, sessions.source, sessions.note
    FROM sessions
    JOIN subjects ON subjects.id = sessions.subject_id
    ORDER BY sessions.date DESC, sessions.id DESC
"""
params = ()
if limit is not None:
    sql += " LIMIT ?"
    params = (limit,)
with connect() as conn:
    return [dict(row) for row in conn.execute(sql, params)]







    