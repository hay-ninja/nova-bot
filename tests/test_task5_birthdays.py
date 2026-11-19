"""TASK 5 flow test. Delete the `pytestmark` line when you start, then fill in the test."""

import pytest

from tests.helpers import make_member

pytestmark = pytest.mark.skip(reason="Task 5 not built yet")


def test_birthday_flow(client, db):
    # 1. make_member: an active member born 2005-02-28, an INACTIVE member born 2005-02-28,
    #    and an active member born 2004-02-29
    # 2. GET /members/birthdays/today?date=2027-02-28 -> the active Feb 28 one and the Feb 29 one
    # 3. GET ?date=2028-02-28 (leap year) -> only the active Feb 28 one
    # 4. the inactive member never appears
    ...
