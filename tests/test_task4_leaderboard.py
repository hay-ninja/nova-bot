"""TASK 4 flow test. Delete the `pytestmark` line when you start, then fill in the test."""

from datetime import datetime, timedelta, timezone

import pytest

from tests.helpers import make_spot

pytestmark = pytest.mark.skip(reason="Task 4 not built yet")

ALICE, BOB, CAROL = "100000000000000001", "100000000000000002", "100000000000000003"


def test_leaderboard_flow(client, db):
    now = datetime.now(timezone.utc)
    # 1. make_spot with created_at: Alice has 3 spots, one of them 10 days old;
    #    Bob has 2 recent spots; Carol has 2 spots, both earlier than Bob's
    # 2. GET /leaderboard?period=all  -> Alice (3), then Carol before Bob (tie, Carol reached 2 first)
    # 3. GET /leaderboard?period=week -> Alice has only 2 now
    # 4. GET /leaderboard?limit=0 -> 422
    ...
