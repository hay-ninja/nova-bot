"""Settings for the API, read from the .env file in the repo root."""

import os

from dotenv import load_dotenv

load_dotenv()

# Path to the SQLite file. It is created automatically if it doesn't exist.
DATABASE_PATH = os.getenv("DATABASE_PATH", "spots.db")
