"""Birthday endpoint (task 5)."""

import sqlite3
from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query

from api.db import get_db
from api.models import Member, member_from_row

router = APIRouter(prefix="/members/birthdays", tags=["birthdays"])

# The server's clock runs on UTC. "Today" for the club means today in Los Angeles.
LA = ZoneInfo("America/Los_Angeles")


# =====================================================================
# TASK 5: GET /members/birthdays/today?date=2027-02-28
# =====================================================================
#   - `?date=` is optional and arrives as `target` (a date object, or None).
#     If it's None, use today's date in LA time (hint: datetime.now(LA).date()).
#     FastAPI parses "2027-02-28" into a date for you.
#   - return ACTIVE members whose birthday month and day match
#     (birthday is stored as 'YYYY-MM-DD'; the year doesn't matter)
#   - Feb 29 birthdays: in a non-leap year, include them on Feb 28
#   - nobody today is not an error: return an empty list
@router.get("/today", response_model=list[Member])
def birthdays_today(
    target: date | None = Query(None, alias="date"),
    db: sqlite3.Connection = Depends(get_db),
) -> list[Member]:
    raise HTTPException(501, "Not built yet (task 5)")
