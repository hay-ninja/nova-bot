"""Settings for the bot, read from the .env file in the repo root."""

import os

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing {name} in .env (copy .env.example to .env and fill it in)")
    return value


DISCORD_TOKEN = _required("DISCORD_TOKEN")

# Discord IDs are numbers here because discord.py compares them with ints
# (message.channel.id, guild.id). They become strings when sent to the API.
GUILD_ID = int(_required("GUILD_ID"))
SPOTTED_CHANNEL_ID = int(_required("SPOTTED_CHANNEL_ID"))
BIRTHDAY_CHANNEL_ID = int(_required("BIRTHDAY_CHANNEL_ID"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
