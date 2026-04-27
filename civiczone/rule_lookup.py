from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = "Informational only; this is not a zoning determination."


@dataclass(frozen=True)
class UseRuleResult:
    zone_code: str
    use: str
    status: str
    review_path: str
    citation: str
    disclaimer: str = DISCLAIMER


@dataclass(frozen=True)
class DimensionalRuleResult:
    zone_code: str
    rule_type: str
    value: str
    citation: str
    disclaimer: str = DISCLAIMER


@dataclass(frozen=True)
class RuleLookupError:
    message: str
    fix: str


USE_RULES = {
    ("R-2", "adu"): UseRuleResult(
        zone_code="R-2",
        use="ADU",
        status="conditional",
        review_path="Planner review required before relying on this answer.",
        citation="CMC 18.42.030",
    ),
    ("R-2", "single-family dwelling"): UseRuleResult(
        zone_code="R-2",
        use="single-family dwelling",
        status="allowed",
        review_path="Confirm parcel-specific overlays before permitting.",
        citation="CMC 18.20.020",
    ),
    ("R-2", "restaurant"): UseRuleResult(
        zone_code="R-2",
        use="restaurant",
        status="not listed",
        review_path="Escalate to planning staff for interpretation.",
        citation="CMC 18.20.020",
    ),
}

DIMENSIONAL_RULES = {
    ("R-2", "front_setback"): DimensionalRuleResult(
        zone_code="R-2",
        rule_type="front_setback",
        value="20 feet minimum",
        citation="CMC 18.20.050(A)",
    ),
    ("R-2", "height"): DimensionalRuleResult(
        zone_code="R-2",
        rule_type="height",
        value="35 feet maximum",
        citation="CMC 18.20.050(B)",
    ),
}


def lookup_use_rule(*, zone_code: str, use: str) -> UseRuleResult | RuleLookupError:
    key = (zone_code.strip().upper(), use.strip().casefold())
    result = USE_RULES.get(key)
    if result:
        return result
    return RuleLookupError(
        message="Use rule not found in the CivicZone sample dataset.",
        fix="Try zone_code 'R-2' with use 'ADU', 'single-family dwelling', or 'restaurant'.",
    )


def lookup_dimensional_rule(*, zone_code: str, rule_type: str) -> DimensionalRuleResult | RuleLookupError:
    key = (zone_code.strip().upper(), rule_type.strip().casefold())
    result = DIMENSIONAL_RULES.get(key)
    if result:
        return result
    return RuleLookupError(
        message="Dimensional rule not found in the CivicZone sample dataset.",
        fix="Try zone_code 'R-2' with rule_type 'front_setback' or 'height'.",
    )
