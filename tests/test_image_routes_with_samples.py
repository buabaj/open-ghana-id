from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
# Put your own sample images in `samples/`:
# - passport: passport.jpg
# - ghana card: ghana_card.jpg
# - voters ID: voters_id.jpg
SAMPLES_DIR = ROOT / "samples"


@pytest.mark.skip(reason="Requires local samples/*.jpg; enable when you add sample images")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_validate_passport_with_sample(client):
    file_path = SAMPLES_DIR / "passport.jpg"
    assert file_path.exists(), "Add a sample passport image as samples/passport.jpg"
    with file_path.open("rb") as f:
        files = {"file": (file_path.name, f, "image/jpeg")}
        response = client.post("/validate-passport", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is not None


@pytest.mark.skip(reason="Requires local samples/*.jpg; enable when you add sample images")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_validate_ghana_card_with_sample(client):
    file_path = SAMPLES_DIR / "ghana_card.jpg"
    assert file_path.exists(), "Add a sample Ghana card image as samples/ghana_card.jpg"
    with file_path.open("rb") as f:
        files = {"file": (file_path.name, f, "image/jpeg")}
        response = client.post("/validate-ghana-card", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is not None


@pytest.mark.skip(reason="Requires local samples/*.jpg; enable when you add sample images")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_validate_voters_id_with_sample(client):
    file_path = SAMPLES_DIR / "voters_id.jpg"
    assert file_path.exists(), "Add a sample voters ID image as samples/voters_id.jpg"
    with file_path.open("rb") as f:
        files = {"file": (file_path.name, f, "image/jpeg")}
        response = client.post("/validate-voters-id", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is not None
