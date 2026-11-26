CREATE TABLE IF NOT EXISTS subjects (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE COLLATE NOCASE, 
    archived INTEGER NOT NULL DEFAULT 0
             CHECK (archived IN (0, 1))
);

CREATE TABLE IF NOT EXISTS sessions (
    id         INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL
               REFERENCES subjects(id),
    minutes    INTEGER NOT NULL
               CHECK (minutes > 0),
    date       TEXT NOT NULL,
    started_at TEXT,
    source     TEXT NOT NULL DEFAULT 'manual'
               CHECK (source IN ('manual', 'timer')),
    note       TEXT
);
