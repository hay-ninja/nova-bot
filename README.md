# Spotted bot

The club's Discord bot: spot people in `#spotted`, climb the leaderboard, look up members, and get birthday shout-outs.

## How it fits together

```
Discord  <->  bot/  --HTTP-->  api/  -->  spots.db
```

There are two programs:

- **`bot/`** (discord.py) stays connected to Discord. It notices messages and slash commands, asks the API, and shows the answer. **It never decides anything.**
- **`api/`** (FastAPI) holds the rules and the data. It answers HTTP requests with JSON. **It knows nothing about Discord.**

> The bot only translates between Discord and HTTP. It hands the API raw facts, and the API decides.
> Test: if we replaced the bot with a website tomorrow, would this rule still apply? If yes, it belongs in the API.

**Start by reading the worked example**, `/ping`, end to end: `bot/features/health.py` → `bot/api_client.py` → `api/main.py` (`health()`).

## Setup (once)

You need Python 3.12 or newer, and git.

1. **Make your own test bot.** Never share bot tokens.
   1. In the [Developer Portal](https://discord.com/developers/applications), click New Application and name it `spotted-dev-<yourname>`.
   2. Open the **Bot** tab, click Reset Token, and copy the token.
   3. On the same tab, turn on **Message Content Intent**.
   4. Open OAuth2 → URL Generator. Under scopes, check `bot` and `applications.commands`. Under permissions, check View Channels, Send Messages, Embed Links, Add Reactions and Read Message History.
   5. Open the generated URL and add the bot to the **practice server**.
2. **Clone the repo and install:**
   ```
   git clone https://github.com/hay-ninja/nova-bot.git
   cd nova-bot
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```
3. **Set up `.env`.** Copy `.env.example` to `.env` and fill in your token, plus the practice server's ID and channel IDs. To get an ID, turn on Developer Mode (User Settings → Advanced), then right-click → Copy ID.
4. **Load fake data:** `python seed.py`

## Running (two terminals, venv active in both)

```
uvicorn api.main:app --reload     # terminal 1: the API
python -m bot.main                # terminal 2: the bot
```

- Open http://127.0.0.1:8000/docs to try any endpoint in your browser.
- In the practice server, `/ping` should answer with spot and member counts.
- Unbuilt endpoints return **501**, and unbuilt commands reply "🚧 not built yet".

Run the tests with `pytest`.

## Your task

Search the code for `TASK <your number>`. Each task has a stub on both sides plus a test file:

| # | Task | API (`api/routers/`) | Bot (`bot/features/`) | Test |
|---|---|---|---|---|
| 1 | Record spots | `spotted.py`: `POST /spots` | `spotted.py`: `on_message` | `tests/test_task1_spots.py` |
| 2 | Personal stats | `spotted.py`: `GET /users/{id}/stats` | `spotted.py`: `/mystats` | `tests/test_task2_stats.py` |
| 3 | Member lookup | `members.py`: both endpoints | `members.py`: `/member` | `tests/test_task3_members.py` |
| 4 | Leaderboard | `spotted.py`: `GET /leaderboard` | `spotted.py`: `/leaderboard` | `tests/test_task4_leaderboard.py` |
| 5 | Birthdays | `birthdays.py` | `birthdays.py`: daily post | `tests/test_task5_birthdays.py` |

The exact request and response shapes are in `api/models.py`, and on `/docs` once the API is running.

Suggested order: build the API endpoint first and test it in `/docs`, then write your flow test, then do the bot side.

## Workflow

1. `git checkout -b task-<n>-<short-name>`
2. Commit as you go. Only edit inside your own `TASK` block in the shared files.
3. Before opening a PR: `pytest` passes, and you've tried your feature in the practice server.
4. Open a pull request into `main` and ask Haydn for review.

## Rules

- Test only in the **practice server**, with **your own bot**.
- Never commit `.env`, `*.db` or `*.csv` (`.gitignore` blocks them).
- `seed.py` data is fake. Real member info only exists on the production server.
