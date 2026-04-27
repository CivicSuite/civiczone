from fastapi.testclient import TestClient

from civiczone.main import app
from civiczone.qa import answer_zoning_question


client = TestClient(app)


def test_adu_question_returns_citation_and_disclaimer() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can I build an ADU?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.42.030",)
    assert "not a zoning determination" in result.disclaimer


def test_setback_question_returns_citation() -> None:
    result = answer_zoning_question(zone_code="R-2", question="What is my front setback?")

    assert result.status == "answered"
    assert result.citations == ("CMC 18.20.050(A)",)


def test_determination_question_escalates_without_citations() -> None:
    result = answer_zoning_question(zone_code="R-2", question="Can you approve my permit?")

    assert result.status == "escalate"
    assert result.citations == ()
    assert "planner review" in result.answer


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
    assert "not a zoning determination" in payload["disclaimer"]
