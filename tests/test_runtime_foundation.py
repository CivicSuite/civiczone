from fastapi.testclient import TestClient

import civiczone
from civiczone.main import app


client = TestClient(app)


def test_package_version_is_011() -> None:
    assert civiczone.__version__ == "0.1.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicZone"
    assert payload["version"] == "0.1.1"
    assert payload["status"] == "public UI foundation plus parcel/rule persistence"
    assert "database-backed parcel/rule lookup records" in payload["message"]
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"].startswith("Post-v0.1.1 roadmap")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiczone"
    assert payload["version"] == "0.1.1"
    assert payload["civiccore_version"] == "0.3.0"
