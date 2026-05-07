from fastapi.testclient import TestClient

import civiczone
from civiczone.main import app


client = TestClient(app)


def test_package_version_is_100() -> None:
    assert civiczone.__version__ == "1.0.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicZone"
    assert payload["version"] == "1.0.0"
    assert payload["status"] == "v1 parcel-aware zoning Q&A runtime"
    assert "optional database-backed parcel/rule" in payload["message"]
    assert "staff workflow APIs" in payload["message"]
    assert "does not make zoning determinations" in payload["message"]
    assert payload["next_step"].startswith("Configure local parcel/rule data")
    assert "trusted municipal access layer" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiczone"
    assert payload["version"] == "1.0.0"
    assert payload["civiccore_version"] == "1.0.0"
