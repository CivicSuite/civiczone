from __future__ import annotations

import sqlalchemy as sa
from fastapi.testclient import TestClient

import civiczone.main as main_module
from civiczone.main import app
from civiczone.question_ledger import ZoneQuestionLedgerRepository
from civiczone.rule_lookup import RuleLookupRepository, UseRuleResult


client = TestClient(app)


def _reset_repositories() -> None:
    if main_module._parcel_lookup_repository is not None:
        main_module._parcel_lookup_repository.engine.dispose()
        main_module._parcel_lookup_repository = None
    if main_module._rule_lookup_repository is not None:
        main_module._rule_lookup_repository.engine.dispose()
        main_module._rule_lookup_repository = None
    if main_module._question_ledger_repository is not None:
        main_module._question_ledger_repository.engine.dispose()
        main_module._question_ledger_repository = None
    main_module._parcel_rule_db_url = None


def test_question_api_uses_configured_rule_database_and_records_ledger(monkeypatch, tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'question-ledger.db'}"
    rules = RuleLookupRepository(db_url=db_url, seed_defaults=False)
    rules.seed_use_rules(
        [
            UseRuleResult(
                zone_code="MX-1",
                use="ADU",
                status="review required",
                review_path="Submit the pre-application worksheet before relying on this answer.",
                citation="BMC 21.10.040",
            )
        ]
    )
    rules.engine.dispose()
    monkeypatch.setenv("CIVICZONE_PARCEL_RULE_DB_URL", db_url)

    try:
        response = client.post(
            "/api/v1/civiczone/questions/answer",
            json={"zone_code": "MX-1", "question": "Can I build an ADU?"},
        )
    finally:
        _reset_repositories()

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "answered"
    assert payload["citations"] == ["BMC 21.10.040"]
    assert payload["ledger_record_id"]

    ledger = ZoneQuestionLedgerRepository(db_url=db_url)
    records = ledger.list_records()
    assert len(records) == 1
    assert records[0].zone_code == "MX-1"
    assert records[0].question_text == "Can I build an ADU?"
    assert records[0].status == "answered"
    assert records[0].citation_payload == ("BMC 21.10.040",)
    ledger.engine.dispose()


def test_question_ledger_records_refusals_with_actionable_reason(monkeypatch, tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'question-refusal-ledger.db'}"
    RuleLookupRepository(db_url=db_url, seed_defaults=False).engine.dispose()
    monkeypatch.setenv("CIVICZONE_PARCEL_RULE_DB_URL", db_url)

    try:
        response = client.post(
            "/api/v1/civiczone/questions/answer",
            json={"zone_code": "MX-1", "question": "Can I build an ADU?"},
        )
    finally:
        _reset_repositories()

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "refused"
    assert "Load use rules into CIVICZONE_PARCEL_RULE_DB_URL" in payload["answer"]

    ledger = ZoneQuestionLedgerRepository(db_url=db_url)
    records = ledger.list_records()
    assert len(records) == 1
    assert records[0].status == "refused"
    assert records[0].citation_payload == ()
    assert records[0].escalation_reason == (
        "No cited zoning answer was available from the configured dataset."
    )
    ledger.engine.dispose()


def test_question_ledger_migration_declares_runtime_table() -> None:
    migration_path = (
        "civiczone/migrations/versions/civiczone_0003_question_ledger.py"
    )
    text = open(migration_path, encoding="utf-8").read()

    assert 'revision = "civiczone_0003_question_ledger"' in text
    assert 'down_revision = "civiczone_0002_parcel_rules"' in text
    assert '"zone_question_ledger_records"' in text
    assert '"citation_payload"' in text
    assert "postgresql.JSONB()" in text


def test_sqlite_question_ledger_schema_is_created(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'question-schema.db'}"
    ledger = ZoneQuestionLedgerRepository(db_url=db_url)

    inspector = sa.inspect(ledger.engine)
    assert inspector.has_table("zone_question_ledger_records")

    ledger.engine.dispose()


def test_repository_cache_resets_question_ledger_when_database_url_changes(monkeypatch, tmp_path) -> None:
    first_db_url = f"sqlite:///{tmp_path / 'first-question.db'}"
    second_db_url = f"sqlite:///{tmp_path / 'second-question.db'}"

    try:
        monkeypatch.setenv("CIVICZONE_PARCEL_RULE_DB_URL", first_db_url)
        first_ledger = main_module._get_question_ledger_repository()

        monkeypatch.setenv("CIVICZONE_PARCEL_RULE_DB_URL", second_db_url)
        second_rules = main_module._get_rule_repository()

        assert first_ledger is not None
        assert second_rules is not None
        assert main_module._question_ledger_repository is None
        assert main_module._parcel_rule_db_url == second_db_url
    finally:
        _reset_repositories()
