"""Member lookup endpoints (task 3).

Use member_from_row(row) from api/models.py to turn a database row into a Member.

SQL safety: always pass user input as a `?` parameter:
    db.execute("SELECT * FROM members WHERE discord_id = ?", (discord_id,))
Never build SQL with f-strings or +. That's how SQL injection happens.
"""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from api.db import get_db
from api.models import Member, member_from_row

router = APIRouter(prefix="/members", tags=["members"])


# =====================================================================
# TASK 3a: GET /members?name=ali  (search)
# =====================================================================
#   - partial, case-insensitive match on name ("ali" finds "Alice Chen" and "Alina Park")
#     hint: WHERE name LIKE '%' || ? || '%'   (SQLite's LIKE ignores case for English letters)
#   - sort by name
#   - no matches is not an error: return an empty list
@router.get("", response_model=list[Member])
def search_members(name: str, db: sqlite3.Connection = Depends(get_db)) -> list[Member]:
    raise HTTPException(501, "Not built yet (task 3)")




# =====================================================================
# TASK 3b: GET /members/{discord_id}  (lookup one person)
# =====================================================================
#   - return that one Member
#   - 404 "Member not found" if there's no row
#     (this also happens for real members whose Discord ID hasn't been collected yet)
@router.get("/{discord_id}", response_model=Member)
def get_member(discord_id: str, db: sqlite3.Connection = Depends(get_db)) -> Member:
    raise HTTPException(501, "Not built yet (task 3)")
