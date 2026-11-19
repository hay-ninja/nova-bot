"""Example flow test. Copy this shape for your task:
1. set up data (helpers or API calls), 2. call the endpoint, 3. assert on status and JSON.
"""

from tests.helpers import make_member, make_spot


def test_health_counts_spots_and_members(client, db):
    make_member(db, "100000000000000001", "Alice Chen")
    make_spot(db, spotter_id="100000000000000001", spotted_id="100000000000000002")
    make_spot(db, spotter_id="100000000000000001", spotted_id="100000000000000003")

    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "spots": 2, "members": 1}
