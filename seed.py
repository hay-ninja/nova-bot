"""Fill your local database with FAKE members and spots, for development only.

    python seed.py           # only works on an empty database
    python seed.py --reset   # wipes ALL spots and members first, then seeds

The fake members look like the real roster after import_members.py cleans it up:
graduation year, GitHub username, formatted phone, comma-separated lists, and
some people with no Discord ID or birthday yet. Never run this on the production server.
"""

import random
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from api import config
from api.db import connect, init_db

LA = ZoneInfo("America/Los_Angeles")
today = datetime.now(LA).date()

COLUMNS = ["discord_id", "name", "pronouns", "major", "year", "birthday",
           "phone", "email", "github", "skills", "involvement", "active"]

MEMBERS = [
    # Spotters: these have Discord IDs, so they show up in spots and the leaderboard.
    dict(discord_id="100000000000000001", name="Alice Chen", pronouns="she/her", major="Computer Science",
         year="2028", birthday="2006-03-14", github="alicechen", skills="Python, React",
         involvement="Dev Team, Hackathon"),
    dict(discord_id="100000000000000002", name="Alina Park", pronouns="she/her", major="Cognitive Science",
         year="2027", birthday="2005-07-02", github=None, skills="Figma",
         involvement="Design Team"),
    dict(discord_id="100000000000000003", name="Bob Martinez", pronouns="he/him", major="Computer Engineering",
         year="2027", birthday="2004-11-30", github="bobm", skills="C++, Embedded, Linux",
         involvement="Officer, Dev Team"),
    dict(discord_id="100000000000000004", name="Carol Nguyen", pronouns="they/them", major="Math of Computation",
         year="2030", birthday="2007-01-09", github="caroln", skills="Python, Data Viz",
         involvement="Dev Team"),
    dict(discord_id="100000000000000005", name="Erin Kim", pronouns="she/her", major="Statistics, Economics",
         year="2029", birthday="2006-02-29", github="erinkim", skills="R, Python",
         involvement="Events"),
    # Birthday is always "today" in LA when you seed, so task 5 has someone to find.
    dict(discord_id="100000000000000006", name="Frank Lee", pronouns="he/him", major="Physics",
         year="2028", birthday=f"2006-{today:%m-%d}", github="franklee", skills="Rust",
         involvement="Dev Team"),
    # Edge cases for tasks 3 and 5:
    # no Discord ID yet; birthday is also today, so the birthday post must use her name
    dict(discord_id=None, name="Grace Liu", pronouns=None, major="Computer Science",
         year="2030", birthday=f"2007-{today:%m-%d}", github=None, skills="Java",
         involvement=None),
    # inactive; birthday is today, but she must NOT get a birthday post
    dict(discord_id="100000000000000008", name="Dana Patel", pronouns="she/her", major="Economics",
         year="2026", birthday=f"2004-{today:%m-%d}", github="danap", skills="Excel, SQL",
         involvement="Officer", active=0),
    # no birthday, almost no info
    dict(discord_id=None, name="Henry Alvarez", pronouns="he/him", major=None,
         year="2029", birthday=None, github=None, skills=None, involvement=None),
]

SPOTTED_CHANNEL = "500000000000000000"


def main() -> None:
    reset = "--reset" in sys.argv
    init_db()
    db = connect()

    existing = db.execute("SELECT (SELECT COUNT(*) FROM spots) + (SELECT COUNT(*) FROM members)").fetchone()[0]
    if existing and not reset:
        sys.exit(f"{config.DATABASE_PATH} already has data. Run `python seed.py --reset` to wipe it and reseed.")
    if reset:
        db.execute("DELETE FROM spots")
        db.execute("DELETE FROM members")

    for i, m in enumerate(MEMBERS, start=1):
        first = m["name"].split()[0].lower()
        row = {"phone": f"(310) 555-01{i:02d}", "email": f"{first}@example.com", "active": 1, **m}
        db.execute(
            f"INSERT INTO members ({', '.join(COLUMNS)}) VALUES ({', '.join('?' for _ in COLUMNS)})",
            tuple(row[c] for c in COLUMNS),
        )

    # 25 random spots over the last 20 days, between members who have Discord IDs.
    # Fixed random seed = the same data on everyone's machine.
    rng = random.Random(42)
    ids = [m["discord_id"] for m in MEMBERS if m["discord_id"]]
    now = datetime.now(timezone.utc)
    for i in range(25):
        spotter = rng.choice(ids)
        spotted = rng.sample([x for x in ids if x != spotter], k=rng.choice([1, 1, 2]))
        when = now - timedelta(days=rng.uniform(0, 20))
        for person in spotted:
            db.execute(
                "INSERT INTO spots (message_id, channel_id, spotter_id, spotted_id, created_at) VALUES (?, ?, ?, ?, ?)",
                (str(800_000_000_000_000_000 + i), SPOTTED_CHANNEL, spotter, person, when.isoformat()),
            )

    db.commit()
    spots = db.execute("SELECT COUNT(*) FROM spots").fetchone()[0]
    db.close()
    print(f"Seeded {len(MEMBERS)} fake members and {spots} spot rows into {config.DATABASE_PATH}")


if __name__ == "__main__":
    main()
