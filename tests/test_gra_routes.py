from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from services.gra_client import GraUpstreamError


def test_validate_ghana_card_number_valid(client: TestClient):
    with patch("routers.ghana_card_number.validate_ghana_card_number", return_value=True):
        response = client.post(
            "/validate-ghana-card-number",
            json={"card_num": "GHA-000000000-0"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Ghana card number is valid"
    assert "data" not in data


def test_validate_ghana_card_number_invalid(client: TestClient):
    with patch("routers.ghana_card_number.validate_ghana_card_number", return_value=False):
        response = client.post(
            "/validate-ghana-card-number",
            json={"card_num": "GHA-000000000-0"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Ghana card number is invalid"
    assert "data" not in data


def test_validate_ghana_card_number_gra_down(client: TestClient):
    with patch("routers.ghana_card_number.validate_ghana_card_number", side_effect=GraUpstreamError("connection refused")):
        response = client.post(
            "/validate-ghana-card-number",
            json={"card_num": "GHA-000000000-0"},
        )
    assert response.status_code == 502
    data = response.json()
    assert data["success"] is False
    assert "unavailable" in data["message"].lower()


def test_validate_tin_valid(client: TestClient):
    with patch("routers.tin.validate_tin", return_value=True):
        response = client.post(
            "/validate-tin",
            json={"tin_num": "P0000000000"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Personal TIN is valid"
    assert "data" not in data


def test_validate_tin_invalid(client: TestClient):
    with patch("routers.tin.validate_tin", return_value=False):
        response = client.post(
            "/validate-tin",
            json={"tin_num": "P0000000000"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Personal TIN is invalid"
    assert "data" not in data


def test_validate_tin_gra_down(client: TestClient):
    with patch("routers.tin.validate_tin", side_effect=GraUpstreamError("timeout")):
        response = client.post(
            "/validate-tin",
            json={"tin_num": "P0000000000"},
        )
    assert response.status_code == 502
    data = response.json()
    assert data["success"] is False
    assert "unavailable" in data["message"].lower()


def test_validate_tin_empty_returns_400(client: TestClient):
    response = client.post(
        "/validate-tin",
        json={"tin_num": ""},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


def test_validate_ghana_card_number_empty_returns_400(client: TestClient):
    response = client.post(
        "/validate-ghana-card-number",
        json={"card_num": ""},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
