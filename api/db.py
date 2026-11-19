"""The database: one SQLite file with two tables.

Endpoints get a connection by declaring `db: sqlite3.Connection = Depends(get_db)`.
FastAPI opens the connection before your function runs, and commits and closes it
after your function returns. You never call connect() yourself in an endpoint.
"""

import sqlite3
from collections.abc import Iterator
from pathlib import Path

from api import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS spots (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id  TEXT NOT NULL,
    channel_id  TEXT NOT NULL,
    spotter_id  TEXT NOT NULL,
    spotted_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL,          -- ISO 8601 in UTC, e.g. 2026-11-18T20:15:00+00:00
    UNIQUE (message_id, spotted_id)     -- one row per person spotted in a post
);
CREATE INDEX IF NOT EXISTS idx_spots_spotter ON spots (spotter_id);
CREATE INDEX IF NOT EXISTS idx_spots_spotted ON spots (spotted_id);

CREATE TABLE IF NOT EXISTS members (
    discord_id   TEXT PRIMARY KEY,      -- Discord user ID, stored as text
    name         TEXT NOT NULL,
    pronouns     TEXT,
    major        TEXT,
    year         TEXT,
    birthday     TEXT,                  -- 'YYYY-MM-DD'
    phone        TEXT,
    email        TEXT,
    github       TEXT,
    skills       TEXT,                  -- comma-separated, e.g. 'Python, Figma'
    involvement  TEXT,
    active       INTEGER NOT NULL DEFAULT 1   -- 1 = active, 0 = inactive
);
"""


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    """Open the database. Rows come back as sqlite3.Row, so you can use row["name"]."""
    # check_same_thread=False: FastAPI may open the connection on one thread
    # and run your endpoint on another.
    conn = sqlite3.connect(path or config.DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str | Path | None = None) -> None:
    """Create the tables if they don't exist yet. Safe to run every startup."""
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: one connection per request, committed when the request succeeds."""
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
