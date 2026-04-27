from fastapi.testclient import TestClient

import civiczone
from civiczone.main import app


client = TestClient(app)


def test_package_version_is_dev0() -> None:
    assert civiczone.__version__ == "0.1.0.dev0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicZone"
    assert payload["version"] == "0.1.0.dev0"
    assert payload["status"] == "rule lookup foundation"
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"] == "Milestone 5: citation-grounded resident Q&A"


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiczone"
    assert payload["version"] == "0.1.0.dev0"
    assert payload["civiccore_version"] == "0.2.0"
