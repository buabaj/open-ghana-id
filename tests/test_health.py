from __future__ import annotations


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "Welcome to the Open Ghana ID" in body["message"]
    assert "data" not in body


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Service is healthy"
    assert "data" not in body
