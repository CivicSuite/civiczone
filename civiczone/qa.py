from __future__ import annotations

from dataclasses import dataclass

from civiczone.rule_lookup import (
    DISCLAIMER,
    DimensionalRuleResult,
    RuleLookupError,
    UseRuleResult,
    lookup_dimensional_rule,
    lookup_use_rule,
)


@dataclass(frozen=True)
class ZoneAnswer:
    answer: str
    citations: tuple[str, ...]
    status: str
    reason: str
    confidence: str
    next_step: str
    disclaimer: str = DISCLAIMER


DETERMINATION_PHRASES = (
    "guarantee",
    "determination",
    "approve",
    "permit me",
    "legal",
    "will the city approve",
)
OUT_OF_JURISDICTION_PHRASES = (
    "outside city limits",
    "county land",
    "unincorporated",
    "another city",
    "neighboring town",
)
LOW_CONFIDENCE_PHRASES = (
    "maybe",
    "approximately",
    "not sure",
    "conflicting",
    "unclear",
    "unknown overlay",
)
DIMENSIONAL_RULE_ALIASES = {
    "front setback": "front_setback",
    "front yard": "front_setback",
    "height": "height",
    "maximum height": "height",
}


def answer_zoning_question(
    *,
    zone_code: str,
    question: str,
    use_rule_lookup=lookup_use_rule,
    dimensional_rule_lookup=lookup_dimensional_rule,
) -> ZoneAnswer:
    normalized = question.strip().casefold()
    if any(phrase in normalized for phrase in OUT_OF_JURISDICTION_PHRASES):
        return ZoneAnswer(
            answer=(
                "CivicZone cannot answer out-of-jurisdiction zoning questions from the "
                "configured city dataset."
            ),
            citations=(),
            status="refused",
            reason="out_of_jurisdiction",
            confidence="none",
            next_step="Contact the jurisdiction that regulates the parcel before relying on zoning guidance.",
        )
    if any(phrase in normalized for phrase in LOW_CONFIDENCE_PHRASES):
        return ZoneAnswer(
            answer="This request needs planner review because the available zoning context is low confidence.",
            citations=(),
            status="escalate",
            reason="low_confidence",
            confidence="low",
            next_step="Route the question to planning staff with parcel, overlay, and source context attached.",
        )
    if any(phrase in normalized for phrase in DETERMINATION_PHRASES):
        return ZoneAnswer(
            answer="This request needs planner review because it asks for a determination.",
            citations=(),
            status="escalate",
            reason="determination_request",
            confidence="none",
            next_step="Route to planning staff; CivicZone provides information, not approvals or determinations.",
        )

    dimensional_candidate = _extract_dimensional_rule_candidate(normalized)
    if dimensional_candidate is not None:
        rule = dimensional_rule_lookup(zone_code=zone_code, rule_type=dimensional_candidate)
        if isinstance(rule, DimensionalRuleResult):
            return ZoneAnswer(
                answer=f"In {rule.zone_code}, the {rule.rule_type.replace('_', ' ')} is {rule.value}.",
                citations=(rule.citation,),
                status="answered",
                reason="cited_dimensional_rule",
                confidence="high",
                next_step="Confirm parcel-specific overlays before relying on the informational answer.",
            )
        if isinstance(rule, RuleLookupError):
            return _refused_from_rule_error(rule)

    use_candidate = _extract_use_candidate(normalized)
    if use_candidate is not None:
        rule = use_rule_lookup(zone_code=zone_code, use=use_candidate)
        if isinstance(rule, UseRuleResult):
            return ZoneAnswer(
                answer=(
                    f"In {rule.zone_code}, {rule.use} is listed as {rule.status}. "
                    f"{rule.review_path}"
                ),
                citations=(rule.citation,),
                status="answered",
                reason="cited_use_rule",
                confidence="high",
                next_step="Confirm parcel-specific overlays before relying on the informational answer.",
            )
        if isinstance(rule, RuleLookupError):
            return _refused_from_rule_error(rule)

    return ZoneAnswer(
        answer="CivicZone cannot answer this question with a citation yet.",
        citations=(),
        status="refused",
        reason="no_cited_rule",
        confidence="none",
        next_step="Ask with a supported zoning use or dimensional rule, or route to planning staff.",
    )


def _extract_use_candidate(normalized_question: str) -> str | None:
    if "adu" in normalized_question:
        return "ADU"
    starters = (
        "can i build ",
        "can i open ",
        "is a ",
        "is an ",
        "is ",
        "are ",
    )
    for starter in starters:
        index = normalized_question.find(starter)
        if index == -1:
            continue
        candidate = normalized_question[index + len(starter):]
        candidate = candidate.removesuffix(" allowed")
        candidate = candidate.removesuffix(" permitted")
        candidate = candidate.removesuffix(" conditional")
        candidate = candidate.strip(" ?.")
        if candidate.startswith("a "):
            candidate = candidate.removeprefix("a ")
        if candidate.startswith("an "):
            candidate = candidate.removeprefix("an ")
        if candidate:
            return candidate
    return None


def _extract_dimensional_rule_candidate(normalized_question: str) -> str | None:
    for phrase, rule_type in DIMENSIONAL_RULE_ALIASES.items():
        if phrase in normalized_question:
            return rule_type
    if normalized_question.startswith("what is my "):
        return normalized_question.removeprefix("what is my ").strip(" ?.").replace(" ", "_")
    if normalized_question.startswith("what is the "):
        return normalized_question.removeprefix("what is the ").strip(" ?.").replace(" ", "_")
    return None


def _refused_from_rule_error(error: RuleLookupError) -> ZoneAnswer:
    return ZoneAnswer(
        answer=f"{error.message} Fix: {error.fix}",
        citations=(),
        status="refused",
        reason="rule_lookup_failed",
        confidence="none",
        next_step=error.fix,
    )
