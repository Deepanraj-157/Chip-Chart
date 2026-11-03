def test_ready_without_database(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["database"] == "not configured"