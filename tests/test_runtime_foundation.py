import tomllib
from pathlib import Path

from fastapi.testclient import TestClient

import civiczone
from civiczone.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_100() -> None:
    assert civiczone.__version__ == "0.2.1"


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data["project"]["dependencies"]

    assert data["tool"]["hatch"]["metadata"]["allow-direct-references"] is True
    assert (
        "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/"
        "v1.1.0/civiccore-1.1.0-py3-none-any.whl#sha256=3ab146f4fea2ae99640d5b1b013be1a9676de5f91b783eaeaa913043a2ae2b87"
    ) in dependencies
    assert "civiccore==1.1.0" not in dependencies


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicZone"
    assert payload["version"] == "0.2.1"
    assert payload["status"] == "v1 parcel-aware zoning Q&A runtime"
    assert "optional database-backed parcel/rule" in payload["message"]
    assert "staff workflow APIs" in payload["message"]
    assert "does not make zoning determinations" in payload["message"]
    assert payload["next_step"].startswith("Configure local parcel/rule data")
    assert "trusted staff proxy CIDR list" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiczone"
    assert payload["version"] == "0.2.1"
    assert payload["civiccore_version"] == "1.1.0"


def test_release_gate_prefers_native_unix_python_before_windows_launcher() -> None:
    script = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8")

    python3_probe = "command -v python3"
    python_probe = "command -v python)"
    assert python3_probe in script
    assert python_probe in script
    assert script.index(python3_probe) < script.index(python_probe)


def test_documentation_gate_blocks_stale_product_release_claims() -> None:
    script = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert "current state: published v0.2.0" in script
    assert "recovery label recovered" in script
    assert "current product release" in script


def test_current_docs_mark_v1_label_as_recovered_without_product_release_overclaim() -> None:
    docs = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "README.txt": (ROOT / "README.txt").read_text(encoding="utf-8"),
        "USER-MANUAL.md": (ROOT / "USER-MANUAL.md").read_text(encoding="utf-8"),
        "USER-MANUAL.txt": (ROOT / "USER-MANUAL.txt").read_text(encoding="utf-8"),
        "docs/index.html": (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    }

    for path, text in docs.items():
        lowered = text.lower()
        assert "0.2.1" in lowered, path
        assert "provisional" not in lowered, path
