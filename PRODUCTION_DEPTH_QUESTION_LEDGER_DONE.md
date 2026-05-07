# Production-Depth Resident Question Ledger Done

Date: 2026-05-07

## Scope

This slice makes deterministic resident Q&A use configured rule lookup data and records resident question outcomes when `CIVICZONE_PARCEL_RULE_DB_URL` is set. It preserves CivicZone's no-database sample behavior when the environment variable is unset.

## Shipped

- `answer_zoning_question` now accepts repository-aware rule lookup callables.
- `/api/v1/civiczone/questions/answer` uses configured database-backed rule lookup when available.
- `ZoneQuestionLedgerRepository` records resident question status, answer text, citations, disclaimer, and escalation/refusal reason.
- Alembic revision `civiczone_0003_question_ledger` creates `civiczone.zone_question_ledger_records`.
- Repository cache reset logic now invalidates parcel, rule, and question-ledger repositories together when the configured database URL changes.

## Still Not Shipped

- Live GIS import or Esri integration.
- Live LLM calls.
- Authentication/RBAC and planner review queues.
- Official zoning determinations.
- CivicPlan runtime policy-context calls.

## Verification

- Targeted resident Q&A and ledger persistence tests passed.
- Full release verification must pass before push/merge.
- Browser QA must confirm public documentation and sample UI remain readable at desktop and mobile widths with zero console errors.
