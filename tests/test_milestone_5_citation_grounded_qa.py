from fastapi.testclient import TestClient

from civiczone.main import app
from civiczone.qa import answer_zoning_question
from civiczone.rule_lookup import UseRuleResult


client = TestClient(app)


def test_adu_question_returns_citation_and_disclaimer() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can I build an ADU?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.42.030",)
    assert result.confidence == "high"
    assert result.reason == "cited_use_rule"
    assert "not a zoning determination" in result.disclaimer


def test_arbitrary_use_question_uses_cited_lookup_result() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can I open a restaurant?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.20.020",)
    assert result.answer == "In R-2, restaurant is listed as not listed. Escalate to planning staff for interpretation."


def test_imported_use_question_can_be_answered_when_lookup_supplies_citation() -> None:
    def lookup_use_rule(*, zone_code: str, use: str):
        assert zone_code == "MX-1"
        assert use == "duplex"
        return UseRuleResult(
            zone_code="MX-1",
            use="duplex",
            status="allowed",
            review_path="Confirm overlays before permitting.",
            citation="MXC 12.10.040",
        )

    result = answer_zoning_question(
        zone_code="MX-1",
        question="Can I build a duplex?",
        use_rule_lookup=lookup_use_rule,
    )

    assert result.status == "answered"
    assert result.citations == ("MXC 12.10.040",)
    assert "duplex is listed as allowed" in result.answer


def test_setback_question_returns_citation() -> None:
    result = answer_zoning_question(zone_code="R-2", question="What is my front setback?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.20.050(A)",)


def test_height_question_uses_dimensional_alias() -> None:
    result = answer_zoning_question(zone_code="R-2", question="What is the maximum height?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.20.050(B)",)
    assert "height is 35 feet maximum" in result.answer


def test_determination_question_escalates_without_citations() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can you approve my permit?")

    assert result.status == "escalate"
    assert result.citations == ()
    assert "planner review" in result.answer
    assert result.reason == "determination_request"


def test_out_of_jurisdiction_question_refuses_with_fix_path() -> None:
    result = answer_zoning_question(
        zone_code="R-2",
        question="What zoning applies to county land outside city limits?",
    )

    assert result.status == "refused"
    assert result.reason == "out_of_jurisdiction"
    assert "Contact the jurisdiction" in result.next_step


def test_low_confidence_question_escalates_to_staff() -> None:
    result = answer_zoning_question(
        zone_code="R-2",
        question="The overlay data is conflicting and unclear.",
    )

    assert result.status == "escalate"
    assert result.reason == "low_confidence"
    assert result.confidence == "low"


def test_unknown_question_refuses_uncited_answer() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can I open a heliport?")

    assert result.status == "refused"
    assert result.citations == ()


def test_question_api_success_shape() -> None:
    response = client.post(
        "/api/v1/civiczone/questions/answer",
        json={"zone_code": "R-2", "question": "Can I build an ADU?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "answered"
    assert payload["citations"] == ["CMC 18.42.030"]
    assert payload["reason"] == "cited_use_rule"
    assert payload["confidence"] == "high"
    assert "Confirm parcel-specific overlays" in payload["next_step"]
    assert payload["ledger_record_id"] is None
    assert "not a zoning determination" in payload["disclaimer"]


def test_question_api_validation_error_is_actionable() -> None:
    response = client.post("/api/v1/civiczone/questions/answer", json={})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "required fields" in detail["message"]
    assert "zone_code" in detail["fix"]
    assert "question" in detail["fix"]
