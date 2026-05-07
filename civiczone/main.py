"""FastAPI runtime foundation for CivicZone."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from civiczone import __version__
from civiczone.parcel_lookup import ParcelLookupError, ParcelLookupRepository, lookup_parcel
from civiczone.public_ui import render_public_lookup_page
from civiczone.question_ledger import ZoneQuestionLedgerRepository
from civiczone.qa import answer_zoning_question
from civiczone.rule_lookup import RuleLookupError, RuleLookupRepository, lookup_dimensional_rule, lookup_use_rule
from civiczone.staff_context import classify_for_planner_review, get_staff_precedent


app = FastAPI(
    title="CivicZone",
    version=__version__,
    description="Parcel-aware zoning and land-use Q&A foundation for CivicSuite.",
)

_parcel_lookup_repository: ParcelLookupRepository | None = None
_rule_lookup_repository: RuleLookupRepository | None = None
_question_ledger_repository: ZoneQuestionLedgerRepository | None = None
_parcel_rule_db_url: str | None = None


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicZone",
        "version": __version__,
        "status": "public UI foundation plus parcel/rule persistence",
        "message": (
            "CivicZone package, API foundation, canonical schema, Alembic migrations, "
            "sample parcel lookup, use-rule lookup, dimensional prechecks, optional database-backed parcel/rule lookup records, "
            "citation-grounded sample Q&A, planner escalation, and an accessible public sample UI are online; "
            "live GIS ingestion and planner review workflows are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: live GIS ingestion, production data wiring, authentication/RBAC, and planner review workflows",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civiczone",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civiczone", response_class=HTMLResponse)
def public_civiczone_page() -> str:
    """Return the accessible public sample UI."""

    return render_public_lookup_page()


class ParcelLookupRequest(BaseModel):
    parcel_number: str | None = Field(default=None)
    address: str | None = Field(default=None)


class UseRuleLookupRequest(BaseModel):
    zone_code: str
    use: str


class DimensionalRuleLookupRequest(BaseModel):
    zone_code: str
    rule_type: str


class ZoneQuestionRequest(BaseModel):
    zone_code: str
    question: str


class PlannerReviewRequest(BaseModel):
    question: str


@app.post("/api/v1/civiczone/parcels/lookup")
def parcel_lookup(request: ParcelLookupRequest) -> dict[str, object]:
    if not request.parcel_number and not request.address:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Provide either parcel_number or address.",
                "fix": "Send parcel_number '100-200-300' or address '123 Main St' in this development build.",
            },
        )

    result = _lookup_parcel(parcel_number=request.parcel_number, address=request.address)
    if isinstance(result, ParcelLookupError):
        raise HTTPException(status_code=404, detail={"message": result.message, "fix": result.fix})

    return {
        "parcel_number": result.parcel_number,
        "address": result.address,
        "zone": {"code": result.zone_code, "name": result.zone_name},
        "overlays": list(result.overlays),
        "constraints": list(result.constraints),
        "source": result.source,
        "disclaimer": result.disclaimer,
    }


@app.post("/api/v1/civiczone/rules/use")
def use_rule_lookup(request: UseRuleLookupRequest) -> dict[str, str]:
    result = _lookup_use_rule(zone_code=request.zone_code, use=request.use)
    if isinstance(result, RuleLookupError):
        raise HTTPException(status_code=404, detail={"message": result.message, "fix": result.fix})
    return {
        "zone_code": result.zone_code,
        "use": result.use,
        "status": result.status,
        "review_path": result.review_path,
        "citation": result.citation,
        "disclaimer": result.disclaimer,
    }


@app.post("/api/v1/civiczone/rules/dimensional")
def dimensional_rule_lookup(request: DimensionalRuleLookupRequest) -> dict[str, str]:
    result = _lookup_dimensional_rule(zone_code=request.zone_code, rule_type=request.rule_type)
    if isinstance(result, RuleLookupError):
        raise HTTPException(status_code=404, detail={"message": result.message, "fix": result.fix})
    return {
        "zone_code": result.zone_code,
        "rule_type": result.rule_type,
        "value": result.value,
        "citation": result.citation,
        "disclaimer": result.disclaimer,
    }


@app.post("/api/v1/civiczone/questions/answer")
def zone_question_answer(request: ZoneQuestionRequest) -> dict[str, object]:
    result = answer_zoning_question(
        zone_code=request.zone_code,
        question=request.question,
        use_rule_lookup=_lookup_use_rule,
        dimensional_rule_lookup=_lookup_dimensional_rule,
    )
    ledger_record = _record_zone_question(
        zone_code=request.zone_code,
        question=request.question,
        result=result,
    )
    return {
        "status": result.status,
        "answer": result.answer,
        "citations": list(result.citations),
        "disclaimer": result.disclaimer,
        "ledger_record_id": ledger_record.id if ledger_record is not None else None,
    }


@app.post("/api/v1/civiczone/planner-review/classify")
def planner_review_classify(request: PlannerReviewRequest) -> dict[str, str]:
    result = classify_for_planner_review(request.question)
    return {"status": result.status, "reason": result.reason, "next_step": result.next_step}


@app.get("/api/v1/civiczone/staff/precedents/{precedent_id}")
def staff_precedent(precedent_id: str) -> dict[str, str]:
    precedent = get_staff_precedent(precedent_id)
    if precedent is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "Staff precedent not found.", "fix": "Try precedent_id 'historic-adu'."},
        )
    return {
        "title": precedent.title,
        "summary": precedent.summary,
        "visibility": precedent.visibility,
    }


def _parcel_rule_database_url() -> str | None:
    return os.environ.get("CIVICZONE_PARCEL_RULE_DB_URL")


def _get_parcel_repository() -> ParcelLookupRepository:
    global _parcel_lookup_repository, _parcel_rule_db_url
    db_url = _parcel_rule_database_url()
    if db_url is None:
        raise RuntimeError("CIVICZONE_PARCEL_RULE_DB_URL is not configured.")
    if _parcel_lookup_repository is None or db_url != _parcel_rule_db_url:
        _reset_configured_repositories()
        _parcel_rule_db_url = db_url
        _parcel_lookup_repository = ParcelLookupRepository(db_url=db_url)
    return _parcel_lookup_repository


def _get_rule_repository() -> RuleLookupRepository:
    global _parcel_rule_db_url, _rule_lookup_repository
    db_url = _parcel_rule_database_url()
    if db_url is None:
        raise RuntimeError("CIVICZONE_PARCEL_RULE_DB_URL is not configured.")
    if _rule_lookup_repository is None or db_url != _parcel_rule_db_url:
        _reset_configured_repositories()
        _parcel_rule_db_url = db_url
        _rule_lookup_repository = RuleLookupRepository(db_url=db_url)
    return _rule_lookup_repository


def _get_question_ledger_repository() -> ZoneQuestionLedgerRepository:
    global _parcel_rule_db_url, _question_ledger_repository
    db_url = _parcel_rule_database_url()
    if db_url is None:
        raise RuntimeError("CIVICZONE_PARCEL_RULE_DB_URL is not configured.")
    if _question_ledger_repository is None or db_url != _parcel_rule_db_url:
        _reset_configured_repositories()
        _parcel_rule_db_url = db_url
        _question_ledger_repository = ZoneQuestionLedgerRepository(db_url=db_url)
    return _question_ledger_repository


def _lookup_parcel(*, parcel_number: str | None = None, address: str | None = None):
    if _parcel_rule_database_url() is None:
        return lookup_parcel(parcel_number=parcel_number, address=address)
    return _get_parcel_repository().lookup(parcel_number=parcel_number, address=address)


def _lookup_use_rule(*, zone_code: str, use: str):
    if _parcel_rule_database_url() is None:
        return lookup_use_rule(zone_code=zone_code, use=use)
    return _get_rule_repository().lookup_use_rule(zone_code=zone_code, use=use)


def _lookup_dimensional_rule(*, zone_code: str, rule_type: str):
    if _parcel_rule_database_url() is None:
        return lookup_dimensional_rule(zone_code=zone_code, rule_type=rule_type)
    return _get_rule_repository().lookup_dimensional_rule(zone_code=zone_code, rule_type=rule_type)


def _record_zone_question(*, zone_code: str, question: str, result):
    if _parcel_rule_database_url() is None:
        return None
    escalation_reason = None
    if result.status == "escalate":
        escalation_reason = "Planner review required before relying on this answer."
    elif result.status == "refused":
        escalation_reason = "No cited zoning answer was available from the configured dataset."
    return _get_question_ledger_repository().record_answer(
        zone_code=zone_code,
        question_text=question,
        audience="resident",
        status=result.status,
        answer_text=result.answer,
        citations=result.citations,
        disclaimer=result.disclaimer,
        escalation_reason=escalation_reason,
    )


def _dispose_repository(repository: object | None) -> None:
    engine = getattr(repository, "engine", None)
    if engine is not None:
        engine.dispose()


def _reset_configured_repositories() -> None:
    global _parcel_lookup_repository, _rule_lookup_repository, _question_ledger_repository
    _dispose_repository(_parcel_lookup_repository)
    _dispose_repository(_rule_lookup_repository)
    _dispose_repository(_question_ledger_repository)
    _parcel_lookup_repository = None
    _rule_lookup_repository = None
    _question_ledger_repository = None
