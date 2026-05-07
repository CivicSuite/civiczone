# CivicZone

CivicZone is the planned CivicSuite module for parcel-aware zoning and land-use Q&A.

Current state: **v0.1.1 public UI foundation release plus production-depth parcel/rule and resident-question persistence slices**. This repo ships a package shell, health/root endpoints, documentation gates, canonical zoning schema models, Alembic migration scaffold, sample parcel/zone lookup API, sample use/dimensional rule APIs, optional database-backed parcel/rule lookup records and resident question ledger via `CIVICZONE_PARCEL_RULE_DB_URL`, citation-grounded sample Q&A, planner-escalation/staff-context samples, an accessible public sample UI at `/civiczone`, and `civiccore==1.0.0` dependency alignment. It does **not** yet use live LLM calls, ingest live GIS data, make zoning determinations, or replace planner review.

## What CivicZone Will Do

- Let residents enter an address or parcel and see zoning context.
- Explain allowed-use, setback, overlay, and review-path questions with citations.
- Refuse or escalate zoning-determination requests.
- Route ambiguous, low-confidence, variance, CUP, and out-of-jurisdiction questions to staff.
- Use CivicCode as the authoritative municipal-code source.

## What Is Not Shipped Yet

- Live GIS import or Esri integration.
- Production GIS/assessor synchronization.
- Live or AI-generated zoning Q&A beyond deterministic cited sample answers.
- Planner review queue.
- Production resident UI connected to live GIS, authentication, and planner review workflows.
- Legal/zoning determinations.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Foundation

- `GET /` returns current module status and next milestone.
- `GET /health` returns package and CivicCore version information.
- `GET /civiczone` returns the accessible public sample UI.
- `POST /api/v1/civiczone/parcels/lookup` returns sample parcel zone context for `100-200-300` / `123 Main St`.
- `POST /api/v1/civiczone/rules/use` returns sample use status with citation.
- `POST /api/v1/civiczone/rules/dimensional` returns sample dimensional rule values with citation.
- `POST /api/v1/civiczone/questions/answer` answers sample resident questions only when citations are available and records a local question-ledger row when `CIVICZONE_PARCEL_RULE_DB_URL` is configured.
- `POST /api/v1/civiczone/planner-review/classify` identifies sample discretionary-review triggers.
- `GET /api/v1/civiczone/staff/precedents/{precedent_id}` returns staff-only sample precedent context.

Set `CIVICZONE_PARCEL_RULE_DB_URL` to enable persistent parcel, use-rule, dimensional-rule, and resident-question ledger records. When unset, CivicZone continues to use deterministic in-memory sample data for local development and documentation examples and does not persist question rows.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
