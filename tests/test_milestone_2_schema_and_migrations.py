from __future__ import annotations

import importlib
from pathlib import Path
import subprocess
import time
import uuid

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text


ROOT = Path(__file__).resolve().parents[1]

CANONICAL_TABLES = [
    "zones",
    "overlays",
    "parcels",
    "use_categories",
    "use_rules",
    "dimensional_rules",
    "citations",
    "precedents",
    "interpretation_notes",
    "zone_questions",
]


def test_canonical_models_use_civiccore_base_and_schema() -> None:
    models = importlib.import_module("civiczone.models")
    civiccore_db = importlib.import_module("civiccore.db")

    assert models.Base is civiccore_db.Base
    assert sorted(models.Base.metadata.tables) == sorted(
        f"civiczone.{table_name}" for table_name in CANONICAL_TABLES
    )
    for table_name in CANONICAL_TABLES:
        assert models.Base.metadata.tables[f"civiczone.{table_name}"].schema == "civiczone"


def test_each_canonical_table_has_foundation_columns() -> None:
    models = importlib.import_module("civiczone.models")

    for table_name in CANONICAL_TABLES:
        table = models.Base.metadata.tables[f"civiczone.{table_name}"]
        assert {"id", "created_at", "updated_at"} <= set(table.columns.keys())


def test_alembic_scaffold_exists_and_uses_separate_version_table() -> None:
    expected = [
        ROOT / "civiczone" / "migrations" / "alembic.ini",
        ROOT / "civiczone" / "migrations" / "env.py",
        ROOT / "civiczone" / "migrations" / "versions" / "civiczone_0001_schema.py",
    ]
    for path in expected:
        assert path.exists()

    env_text = (ROOT / "civiczone" / "migrations" / "env.py").read_text(encoding="utf-8")
    assert "civiccore.migrations.runner" in env_text
    assert "subprocess.run" in env_text
    assert 'version_table="alembic_version_civiczone"' in env_text


def test_migration_declares_all_canonical_tables() -> None:
    migration_text = (
        ROOT / "civiczone" / "migrations" / "versions" / "civiczone_0001_schema.py"
    ).read_text(encoding="utf-8")

    assert 'revision = "civiczone_0001_schema"' in migration_text
    assert 'op.execute("CREATE SCHEMA IF NOT EXISTS civiczone")' in migration_text
    assert "idempotent_create_table" in migration_text
    for table_name in CANONICAL_TABLES:
        assert f'"{table_name}"' in migration_text


def test_alembic_command_upgrades_real_pgvector_database(monkeypatch: pytest.MonkeyPatch) -> None:
    name = f"civiczone-m2-{uuid.uuid4().hex[:12]}"
    subprocess.run(
        [
            "docker",
            "run",
            "--name",
            name,
            "-e",
            "POSTGRES_PASSWORD=postgres",
            "-e",
            "POSTGRES_USER=postgres",
            "-e",
            "POSTGRES_DB=civiczone_test",
            "-p",
            "5432",
            "-d",
            "pgvector/pgvector:pg17",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    try:
        mapped = subprocess.run(
            ["docker", "port", name, "5432/tcp"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        port = mapped.rsplit(":", maxsplit=1)[-1]
        db_url = f"postgresql+psycopg2://postgres:postgres@localhost:{port}/civiczone_test"
        engine = create_engine(db_url)

        deadline = time.monotonic() + 30
        while True:
            try:
                with engine.connect() as connection:
                    connection.execute(text("select 1"))
                break
            except Exception:
                if time.monotonic() > deadline:
                    raise
                time.sleep(1)

        monkeypatch.setenv("DATABASE_URL", db_url)
        cfg = Config(str(ROOT / "civiczone" / "migrations" / "alembic.ini"))

        command.upgrade(cfg, "head")
        command.upgrade(cfg, "head")

        with engine.connect() as connection:
            civiccore_revision = connection.execute(
                text("select version_num from alembic_version_civiccore")
            ).scalar_one()
            civiczone_revision = connection.execute(
                text("select version_num from alembic_version_civiczone")
            ).scalar_one()
            civiczone_tables = set(
                connection.execute(
                    text(
                        """
                        select table_name
                        from information_schema.tables
                        where table_schema = 'civiczone'
                        """
                    )
                ).scalars()
            )

        assert civiccore_revision == "civiccore_0002_llm"
        assert civiczone_revision == "civiczone_0001_schema"
        assert civiczone_tables == set(CANONICAL_TABLES)
    finally:
        subprocess.run(["docker", "rm", "-f", name], check=False, capture_output=True, text=True)
