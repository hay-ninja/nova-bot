"""Shortcuts for putting data straight into the test database.

Use these to set up a test without depending on another task's endpoint.
Task 2's test, for example, can create spots with make_spot() even if POST /spots
isn't built yet.
"""

import itertools
import sqlite3
from datetime import datetime, timezone

_message_ids = itertools.count(900_000_000_000_000_000)


def make_spot(
    db: sqlite3.Connection,
    spotter_id: str,
    spotted_id: str,
    *,
    message_id: str | None = None,
    channel_id: str = "500000000000000000",
    created_at: datetime | None = None,
) -> None:
    """Insert one spot row. created_at defaults to now (UTC)."""
    db.execute(
        "INSERT INTO spots (message_id, channel_id, spotter_id, spotted_id, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            message_id or str(next(_message_ids)),
            channel_id,
            spotter_id,
            spotted_id,
            (created_at or datetime.now(timezone.utc)).isoformat(),
        ),
    )
    db.commit()


def make_member(db: sqlite3.Connection, name: str, **fields) -> None:
    """Insert one member. Pass any other column as a keyword, e.g.
    make_member(db, "Bob Martinez", discord_id="100000000000000002", birthday="2005-02-28", active=0)
    """
    columns = {"name": name, "active": 1, **fields}
    names = ", ".join(columns)
    placeholders = ", ".join("?" for _ in columns)
    db.execute(f"INSERT INTO members ({names}) VALUES ({placeholders})", tuple(columns.values()))
    db.commit()
