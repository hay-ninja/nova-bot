"""TASK 3 flow test. Delete the `pytestmark` line when you start, then fill in the test."""

import pytest

from tests.helpers import make_member

pytestmark = pytest.mark.skip(reason="Task 3 not built yet")


def test_member_lookup_flow(client, db):
    # 1. make_member: Alice Chen, Alina Park, Bob Martinez (give Bob a few fields, incl. skills="Python, Figma")
    # 2. GET /members?name=ali -> 2 results; "ALI" works too (case-insensitive)
    # 3. GET /members/{bob's id} -> his fields, skills == ["Python", "Figma"]
    # 4. GET /members/{unknown id} -> 404
    ...
