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
    disclaimer: str = DISCLAIMER


DETERMINATION_PHRASES = ("guarantee", "determination", "approve", "permit me", "legal")


def answer_zoning_question(
    *,
    zone_code: str,
    question: str,
    use_rule_lookup=lookup_use_rule,
    dimensional_rule_lookup=lookup_dimensional_rule,
) -> ZoneAnswer:
    normalized = question.strip().casefold()
    if any(phrase in normalized for phrase in DETERMINATION_PHRASES):
        return ZoneAnswer(
            answer="This request needs planner review because it asks for a determination.",
            citations=(),
            status="escalate",
        )

    if "adu" in normalized:
        rule = use_rule_lookup(zone_code=zone_code, use="ADU")
        if isinstance(rule, UseRuleResult):
            return ZoneAnswer(
                answer=(
                    f"In {rule.zone_code}, an ADU is listed as {rule.status}. "
                    f"{rule.review_path}"
                ),
                citations=(rule.citation,),
                status="answered",
            )
        if isinstance(rule, RuleLookupError):
            return _refused_from_rule_error(rule)

    if "setback" in normalized or "front yard" in normalized:
        rule = dimensional_rule_lookup(zone_code=zone_code, rule_type="front_setback")
        if isinstance(rule, DimensionalRuleResult):
            return ZoneAnswer(
                answer=f"In {rule.zone_code}, the sample front setback is {rule.value}.",
                citations=(rule.citation,),
                status="answered",
            )
        if isinstance(rule, RuleLookupError):
            return _refused_from_rule_error(rule)

    return ZoneAnswer(
        answer="CivicZone cannot answer this sample question with a citation yet.",
        citations=(),
        status="refused",
    )


def _refused_from_rule_error(error: RuleLookupError) -> ZoneAnswer:
    return ZoneAnswer(
        answer=f"{error.message} Fix: {error.fix}",
        citations=(),
        status="refused",
    )
