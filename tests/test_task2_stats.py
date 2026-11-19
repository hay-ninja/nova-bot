"""TASK 2 flow test. Delete the `pytestmark` line when you start, then fill in the test."""

import pytest

from tests.helpers import make_spot

pytestmark = pytest.mark.skip(reason="Task 2 not built yet")

ALICE, BOB, CAROL = "100000000000000001", "100000000000000002", "100000000000000003"


def test_stats_flow(client, db):
    # 1. make_spot: Alice spots Bob twice and Carol once; Bob spots Alice once
    # 2. GET /users/{ALICE}/stats -> given 3, received 1, rank 1, top_target_id BOB
    # 3. GET stats for someone with no spots -> 200 with zeros and None
    ...
