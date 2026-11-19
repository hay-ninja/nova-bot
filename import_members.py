"""Load the REAL member roster from Notion's CSV export into the members table.
Run this only on the server.

    python import_members.py "/path/to/Team Roster ....csv"

Use the Team Roster view's CSV, not the "_all" file. "_all" includes alumni.
In Notion: open the roster, click ... > Export > Markdown & CSV.

Notion's column names are used as they are:
    Name, Discord ID, Pronouns, Major(s), Year, Birthdays, Phone Number,
    Email, Github, Skills, Involvement, Alumni
Only Name is required. Other columns (Companies, Project(s), Created Time) are ignored.
Add a "Discord ID" text column in Notion as IDs get collected. Members without
one are still imported; they just can't be @-mentioned yet.

This REPLACES the whole members table (spots are untouched). Re-run it whenever
the roster changes. Keep the CSV out of the repo folder; it holds personal info.
"""

import csv
import re
import sys
from datetime import datetime

from api import config
from api.db import connect, init_db

COLUMNS = ["discord_id", "name", "pronouns", "major", "year", "birthday",
           "phone", "email", "github", "skills", "involvement", "active"]

# Notion header (lowercased) -> our column
HEADER_MAP = {
    "name": "name",
    "discord id": "discord_id",
    "discord_id": "discord_id",
    "pronouns": "pronouns",
    "major(s)": "major",
    "major": "major",
    "year": "year",
    "birthdays": "birthday",
    "birthday": "birthday",
    "phone number": "phone",
    "phone": "phone",
    "email": "email",
    "github": "github",
    "skills": "skills",
    "involvement": "involvement",
    "alumni": "alumni",
    "active": "active",
}

# Notion exports dates like "November 3, 2005"; a few other formats are accepted too.
DATE_FORMATS = ["%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y"]

# Invisible characters that sneak in from copy-paste (e.g. U+202C in phone numbers).
INVISIBLE = re.compile(r"[​-‏‪-‮⁠﻿]")


def clean(text: str | None) -> str:
    return INVISIBLE.sub("", text or "").strip()


def parse_birthday(text: str) -> str | None:
    if not text:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"unrecognized birthday {text!r}")


def parse_phone(text: str) -> str | None:
    """Most entries are bare digits ("3105550123"); format US numbers as (310) 555-0123."""
    if not text:
        return None
    digits = re.sub(r"\D", "", text)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return text  # international or unusual: keep as typed


def parse_github(text: str) -> str | None:
    """Accept "https://github.com/user/", "github.com/user", "@user" or "user"; keep the username."""
    if not text:
        return None
    text = re.sub(r"^(https?://)?(www\.)?github\.com/", "", text, flags=re.I)
    return text.strip("/@ ").split("/")[0] or None


def parse_pronouns(text: str) -> str | None:
    """'He/Him' -> 'he/him', 'she / her' -> 'she/her'."""
    return re.sub(r"\s*/\s*", "/", text.lower()) if text else None


def parse_year(text: str) -> str | None:
    """'2030, newbie!' -> '2030'."""
    if not text:
        return None
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return match.group(0) if match else text


def parse_active(row: dict) -> int:
    """Alumni = Yes means inactive. An "Active" column works too. Neither column -> active."""
    if row.get("alumni"):
        return 0 if row["alumni"].lower() in {"yes", "true", "1"} else 1
    if row.get("active"):
        return 0 if row["active"].lower() in {"no", "false", "0", "inactive"} else 1
    return 1


def main() -> None:
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(paths) != 1:
        sys.exit('usage: python import_members.py "<roster.csv>" [--list-missing]')

    with open(paths[0], newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        notion_headers = next(reader, [])
        headers = [HEADER_MAP.get(clean(h).lower()) for h in notion_headers]
        if "name" not in headers:
            sys.exit(f"CSV has no Name column. Found: {notion_headers}")
        raw_rows = [dict(zip(headers, (clean(v) for v in values))) for values in reader]

    rows, problems, seen_ids = [], [], {}
    for line, raw in enumerate(raw_rows, start=2):
        raw.pop(None, None)  # columns we don't use
        name = raw.get("name", "")
        if not name:
            continue  # blank row
        discord_id = raw.get("discord_id") or None
        if discord_id and not discord_id.isdigit():
            problems.append(f"line {line} ({name}): Discord ID {discord_id!r} should be digits only (right-click > Copy User ID)")
            continue
        if discord_id in seen_ids:
            problems.append(f"line {line} ({name}): Discord ID already used by {seen_ids[discord_id]}")
            continue
        try:
            birthday = parse_birthday(raw.get("birthday", ""))
        except ValueError as e:
            problems.append(f"line {line} ({name}): {e}")
            continue
        if discord_id:
            seen_ids[discord_id] = name

        rows.append({
            "discord_id": discord_id,
            "name": name,
            "pronouns": parse_pronouns(raw.get("pronouns", "")),
            "major": raw.get("major") or None,
            "year": parse_year(raw.get("year", "")),
            "birthday": birthday,
            "phone": parse_phone(raw.get("phone", "")),
            "email": raw.get("email") or None,
            "github": parse_github(raw.get("github", "")),
            "skills": raw.get("skills") or None,
            "involvement": raw.get("involvement") or None,
            "active": parse_active(raw),
        })

    if problems:
        print("Fix these rows in Notion, re-export, and run again (nothing was imported):")
        print("\n".join(f"  {p}" for p in problems))
        sys.exit(1)

    init_db()
    db = connect()
    with db:  # one transaction: all rows or none
        db.execute("DELETE FROM members")
        db.executemany(
            f"INSERT INTO members ({', '.join(COLUMNS)}) VALUES ({', '.join('?' for _ in COLUMNS)})",
            [tuple(r[c] for c in COLUMNS) for r in rows],
        )
    db.close()

    active = sum(r["active"] for r in rows)
    no_id = [r["name"] for r in rows if not r["discord_id"]]
    no_bday = sum(1 for r in rows if not r["birthday"])
    print(f"Imported {len(rows)} members ({active} active) into {config.DATABASE_PATH}")
    print(f"  {len(rows) - len(no_id)} have a Discord ID; {len(no_id)} don't yet")
    print(f"  {no_bday} have no birthday (they'll never get a birthday post)")
    if no_id and "--list-missing" not in sys.argv:
        print("  (add --list-missing to print who still needs a Discord ID)")
    elif no_id:
        print("  Missing Discord ID: " + ", ".join(sorted(no_id)))


if __name__ == "__main__":
    main()
