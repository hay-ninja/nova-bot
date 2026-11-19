# How it works

Read this on day 1. It covers the big picture, what an API is, and how one command travels through the system.

## The big picture

![Architecture](architecture.png)

The same thing in more detail:

```mermaid
flowchart LR
    subgraph D["Discord (Discord's servers)"]
        U["You in #spotted / #bot"]
    end

    subgraph L["Your laptop (or the prod VM)"]
        subgraph B["bot/ : discord.py"]
            F["features/*.py<br/>listeners + slash commands"]
            C["api_client.py<br/>sends HTTP requests"]
        end
        subgraph A["api/ : FastAPI"]
            R["routers/*.py<br/>endpoints = the rules"]
            M["models.py<br/>request/response shapes"]
            DB["db.py"]
        end
        S[("spots.db<br/>SQLite: spots + members")]
    end

    U <-- "live connection<br/>events in, messages out" --> F
    F --> C
    C -- "HTTP request<br/>GET /leaderboard" --> R
    R -- "JSON response" --> C
    R --- M
    R --> DB --> S
```

There are **two separate programs**, and you run both:

| | `bot/` | `api/` |
|---|---|---|
| Library | discord.py | FastAPI |
| Talks to | Discord, and the API | the database |
| Job | notice what happened in Discord, ask the API, show the answer | apply the rules, read and write data, answer with JSON |
| Knows about | Discord: users, channels, embeds | spots, members, points |
| Never | decides anything or touches the database | knows Discord exists |

> **The rule:** the bot only translates between Discord and HTTP. It hands the API raw facts, and the API decides.
> Test: if we replaced the bot with a website tomorrow, would this rule still apply? If yes, it belongs in the API.

## What an API is

An **API** is a program that waits for **requests** and sends back **responses**. Ours speaks **HTTP**, the same thing your browser uses, and answers in **JSON**.

A request has:

| Part | Example | What it's for |
|---|---|---|
| **Method** | `GET`, `POST` | `GET` = read something. `POST` = create something. (Also `PUT`/`PATCH` = change, `DELETE` = remove.) |
| **Path** | `/users/123/stats` | *what* you want. Parts in `{braces}` in the code are **path parameters**: `/users/{discord_id}/stats` |
| **Query parameters** | `?limit=10&period=week` | options for the request, after the `?` |
| **Body** | `{"spotter_id": "111", ...}` | data you're sending, usually with `POST` |

A response has:

| Part | Example |
|---|---|
| **Status code** | `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `409 Conflict`, `422 Unprocessable`, `500 Server Error`, `501 Not Implemented` |
| **Body** | `[{"rank": 1, "user_id": "111", "points": 7}]` |

Status codes are a **contract**. The caller reads the number to know what happened before it even looks at the body:

| Code | Meaning | In this project |
|---|---|---|
| 2xx | it worked | `200` read OK, `201` spot saved |
| 4xx | **the caller** did something wrong | `400` breaks a rule (no photo), `404` no such member, `409` message already counted, `422` malformed input (FastAPI sends this automatically) |
| 5xx | **the server** broke | `500` a bug in the API, `501` endpoint not built yet |

## How FastAPI turns a function into an endpoint

```python
@router.get("/leaderboard", response_model=list[LeaderboardEntry])   # method + path + response shape
def leaderboard(
    limit: int = 10,                                 # query parameter: ?limit=10
    db: sqlite3.Connection = Depends(get_db),        # "give me a database connection"
) -> list[LeaderboardEntry]:
    rows = db.execute("SELECT ... LIMIT ?", (limit,)).fetchall()
    return [LeaderboardEntry(...) for row in rows]   # FastAPI turns this into JSON
```

- The **decorator** (`@router.get(...)`) says which method and path run this function.
- **Parameters** become path params (if they're in the path), a request body (if they're a Pydantic model), or query params (everything else). FastAPI checks their types and sends `422` if they're wrong.
- `Depends(get_db)` is **dependency injection**: FastAPI opens a database connection before your function runs and closes it after.
- To send an error: `raise HTTPException(404, "Member not found")`.
- `api/models.py` holds the shapes of everything going in and out. That file is the contract between the bot and the API.

## How the bot calls the API

```python
resp = await api.get("/leaderboard", limit=10, period="week")   # GET /leaderboard?limit=10&period=week
resp = await api.post("/spots", json={"spotter_id": "111", ...})

resp.status_code   # 201
resp.json()        # {"points_awarded": 2}
```

`await` means "wait for the answer without freezing the bot", so it can keep handling other people's commands meanwhile. Always check `status_code` before using `resp.json()`.

## One command, start to finish

```mermaid
sequenceDiagram
    actor You
    participant Discord
    participant Bot as bot/ (features/spotted.py)
    participant API as api/ (routers/spotted.py)
    participant DB as spots.db

    You->>Discord: /leaderboard period:week
    Discord->>Bot: interaction event
    Bot->>API: GET /leaderboard?limit=10&period=week
    API->>DB: SELECT spotter_id, COUNT(*) ... GROUP BY ...
    DB-->>API: rows
    API-->>Bot: 200 [{"rank":1,"user_id":"111","points":7}, ...]
    Bot->>Discord: embed "1. <@111> - 7 pts"
    Discord-->>You: leaderboard appears
```

And a spot, where the API says no:

```mermaid
sequenceDiagram
    actor Alice
    participant Discord
    participant Bot
    participant API
    Alice->>Discord: "@Bob" in #spotted (no photo)
    Discord->>Bot: message event
    Bot->>API: POST /spots {spotter_id, spotted_ids, attachment_types: [], ...}
    API-->>Bot: 400 {"detail": "Spots need a photo"}
    Bot->>Discord: reply "Spots need a photo"
```

Notice the bot didn't check for the photo. It passed the facts along, and the API made the call.

## Where things live

```
api/main.py            starts FastAPI, GET /health (worked example)
api/models.py          the contract: shapes of requests and responses
api/db.py              database tables and connections
api/routers/*.py       endpoints (your TASK code goes here)
bot/main.py            connects to Discord, loads features
bot/api_client.py      api.get / api.post
bot/features/*.py      commands and listeners (your TASK code goes here)
tests/                 flow tests; `pytest` runs them
```

## Try it yourself

1. Run the API (`uvicorn api.main:app --reload`) and open http://127.0.0.1:8000/docs.
2. Open `GET /health` → **Try it out** → **Execute**. Look at the status code and JSON.
3. Try `POST /spots` with an empty body `{}`. You'll get `422`, because FastAPI rejected it before any code ran.
4. Run the bot and type `/ping`. That's the same `/health` request, sent by the bot instead of you.
