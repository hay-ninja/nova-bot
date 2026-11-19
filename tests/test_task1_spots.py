"""TASK 1 flow test. Delete the `pytestmark` line when you start, then fill in the test."""

import pytest

pytestmark = pytest.mark.skip(reason="Task 1 not built yet")

ALICE, BOB, CAROL = "100000000000000001", "100000000000000002", "100000000000000003"


def test_spot_flow(client, db):
    # 1. Alice posts a photo mentioning Bob, Bob again, Carol, and herself
    #    -> 201 and points_awarded == 2 (duplicate and self-mention don't count)
    # 2. the same message_id again -> 409
    # 3. a new message with no image attachment -> 400
    # 4. check the spots table has exactly 2 rows
    ...
