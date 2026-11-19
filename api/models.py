"""The API contract: the exact shape of everything that goes in and out.

FastAPI uses these classes to:
  - reject bad request bodies automatically (status 422),
  - shape responses (extra fields are dropped, missing ones are an error),
  - draw the schemas you see on the /docs page.

Discord IDs are always strings. They are too big for JavaScript numbers,
so the /docs page would silently round them if they were ints.
"""

import sqlite3

from pydantic import BaseModel


class Health(BaseModel):
    status: str
    spots: int
    members: int


# ---------- Task 1: POST /spots ----------

class SpotIn(BaseModel):
    """What the bot sends: raw facts about a #spotted message. The API decides what counts."""
    spotter_id: str
    spotted_ids: list[str]           # everyone mentioned, may include duplicates or the spotter
    attachment_types: list[str] = [] # e.g. ["image/png", "video/mp4"]
    message_id: str
    channel_id: str


class SpotResult(BaseModel):
    points_awarded: int


# ---------- Task 2: GET /users/{discord_id}/stats ----------

class UserStats(BaseModel):
    discord_id: str
    spots_given: int
    spots_received: int
    rank: int | None = None          # place on the all-time leaderboard; None if no spots given
    top_target_id: str | None = None # the person they've spotted most; None if nobody


# ---------- Task 4: GET /leaderboard ----------

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    points: int


# ---------- Tasks 3 and 5: members ----------

class Member(BaseModel):
    discord_id: str | None = None    # None until their Discord ID has been collected
    name: str
    pronouns: str | None = None
    major: str | None = None
    year: str | None = None          # graduation year, e.g. "2028"
    birthday: str | None = None      # 'YYYY-MM-DD'
    phone: str | None = None
    email: str | None = None
    github: str | None = None        # username, e.g. "hay-ninja"
    skills: list[str] = []
    involvement: list[str] = []
    active: bool


def _split(text: str | None) -> list[str]:
    return [part.strip() for part in (text or "").split(",") if part.strip()]


def member_from_row(row: sqlite3.Row) -> Member:
    """Turn a row from the members table into a Member (splits lists, converts active)."""
    data = dict(row)
    data.pop("id", None)  # internal row number, not part of the API
    data["skills"] = _split(data.get("skills"))
    data["involvement"] = _split(data.get("involvement"))
    data["active"] = bool(data["active"])
    return Member(**data)
