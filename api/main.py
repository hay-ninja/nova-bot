"""The API program. Run it with:  uvicorn api.main:app --reload
Then open http://127.0.0.1:8000/docs to try every endpoint in your browser.
"""

import sqlite3
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from api.db import get_db, init_db
from api.models import Health
from api.routers import birthdays, members, spotted


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # make sure the tables exist before the first request
    yield


app = FastAPI(title="Spotted API", lifespan=lifespan)

# Each router is a group of endpoints living in its own file.
# birthdays comes before members so /members/birthdays/today is matched first.
app.include_router(spotted.router)
app.include_router(birthdays.router)
app.include_router(members.router)


# ---------- Worked example: read this first ----------
# The bot's /ping command calls this endpoint. It shows the whole pattern:
#   1. declare what you need (a database connection) as a parameter,
#   2. run a query,
#   3. return a model; FastAPI turns it into JSON.
@app.get("/health", response_model=Health)
def health(db: sqlite3.Connection = Depends(get_db)) -> Health:
    spots = db.execute("SELECT COUNT(*) FROM spots").fetchone()[0]
    members_count = db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    return Health(status="ok", spots=spots, members=members_count)
