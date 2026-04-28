# Production-Depth Parcel/Rule Persistence Done

Date: 2026-04-28

## Scope

This slice adds optional database-backed parcel, use-rule, and dimensional-rule lookup records while preserving CivicZone's deterministic sample behavior when no database URL is configured.

## Shipped

- `CIVICZONE_PARCEL_RULE_DB_URL` enables persistent parcel/rule lookup storage.
- `ParcelLookupRepository` stores seeded sample parcel records and serves parcel-number or address lookup from the configured database.
- `RuleLookupRepository` stores seeded sample use-rule and dimensional-rule records and serves existing rule lookup endpoints from the configured database.
- Alembic revision `civiczone_0002_parcel_rules` creates:
  - `civiczone.parcel_lookup_records`
  - `civiczone.use_rule_lookup_records`
  - `civiczone.dimensional_rule_lookup_records`
- API routes automatically use the configured database repositories when `CIVICZONE_PARCEL_RULE_DB_URL` is set, otherwise they keep using in-memory deterministic samples.

## Still Not Shipped

- Live GIS import or Esri integration.
- Production GIS/assessor synchronization.
- Official zoning determinations.
- Live LLM calls.
- Authentication/RBAC and planner review queues.

## Verification

- Targeted persistence and migration tests passed.
- Full release verification must pass before push/merge.
- Browser QA evidence must confirm `docs/index.html` renders the updated persistence status at desktop and mobile widths with zero console errors.
