"""Spotted endpoints: tasks 1, 2 and 4 all live in this file.

Three people edit this file at once. To keep merges clean:
  - only edit inside your own TASK block,
  - the imports you need are already here; add new ones only if you must.

Every endpoint starts as a 501 ("Not Implemented") placeholder. Replace the
`raise HTTPException(501, ...)` line with your real code.
"""

import sqlite3
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from api.db import get_db
from api.models import LeaderboardEntry, SpotIn, SpotResult, UserStats

router = APIRouter(tags=["spotted"])


# =====================================================================
# TASK 1: POST /spots  (record a spot)
# =====================================================================
# The bot sends raw facts about a #spotted message (see SpotIn in api/models.py).
# Your job is to decide whether it counts:
#   - dedupe spotted_ids and remove the spotter's own id
#     -> 400 "Mention at least one other person" if nobody is left
#   - at least one attachment type must start with "image/"
#     -> 400 "Spots need a photo" otherwise
#   - if this message_id is already in the spots table -> 409
#   - insert one row per spotted person, created_at = now in UTC (ISO 8601)
#   - return SpotResult(points_awarded=<number of rows inserted>)
@router.post("/spots", status_code=201, response_model=SpotResult)
def create_spot(body: SpotIn, db: sqlite3.Connection = Depends(get_db)) -> SpotResult:
    raise HTTPException(501, "Not built yet (task 1)")




# =====================================================================
# TASK 2: GET /users/{discord_id}/stats  (personal stats)
# =====================================================================
# Return a UserStats for this person:
#   - spots_given:    rows where spotter_id = discord_id
#   - spots_received: rows where spotted_id = discord_id
#   - rank:           their place on the all-time leaderboard (None if they gave no spots)
#   - top_target_id:  the spotted_id they've spotted most (None if nobody)
# Someone with no spots is not an error: return zeros/None with status 200.
@router.get("/users/{discord_id}/stats", response_model=UserStats)
def user_stats(discord_id: str, db: sqlite3.Connection = Depends(get_db)) -> UserStats:
    raise HTTPException(501, "Not built yet (task 2)")




# =====================================================================
# TASK 4: GET /leaderboard?limit=10&period=all  (top spotters)
# =====================================================================
#   - limit:  how many rows, must be 1-25 (hint: Query(..., ge=, le=) -> automatic 422)
#   - period: "all" or "week" (week = created_at within the last 7 days)
#   - points = number of spot rows where they are the spotter
#   - order by points (highest first); ties go to whoever reached the score first
#     (the one whose most recent spot is earlier)
#   - return a list of LeaderboardEntry with rank starting at 1
@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(
    limit: int = 10,
    period: str = "all",
    db: sqlite3.Connection = Depends(get_db),
) -> list[LeaderboardEntry]:
    raise HTTPException(501, "Not built yet (task 4)")
