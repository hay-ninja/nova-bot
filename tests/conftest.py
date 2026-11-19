"""Test setup. pytest runs this automatically.

Every test gets its own brand-new, empty database file, so tests never
see each other's data or touch your real spots.db.

Fixtures you can ask for by adding them as test parameters:
    client  - sends requests to the API:   client.get("/health"), client.post("/spots", json={...})
    db      - a connection to the same test database, for use with tests/helpers.py
"""

import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.db import connect, get_db, init_db
from api.main import app


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.db"
    init_db(path)
    return path


@pytest.fixture
def db(db_path: Path) -> Iterator[sqlite3.Connection]:
    conn = connect(db_path)
    yield conn
    conn.close()


@pytest.fixture
def client(db_path: Path) -> Iterator[TestClient]:
    def get_test_db() -> Iterator[sqlite3.Connection]:
        conn = connect(db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # Swap the real database for the test one in every endpoint.
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
    app.dependency_overrides.clear()
