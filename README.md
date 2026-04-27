# CivicZone

CivicZone is the planned CivicSuite module for parcel-aware zoning and land-use Q&A.

Current state: **v0.1.0.dev0 schema foundation in development**. This repo currently ships a package shell, health/root endpoints, documentation gates, canonical zoning schema models, and Alembic migration scaffold. It does **not** yet answer zoning questions, ingest GIS data, make zoning determinations, or replace planner review.

## What CivicZone Will Do

- Let residents enter an address or parcel and see zoning context.
- Explain allowed-use, setback, overlay, and review-path questions with citations.
- Refuse or escalate zoning-determination requests.
- Route ambiguous, low-confidence, variance, CUP, and out-of-jurisdiction questions to staff.
- Use CivicCode as the authoritative municipal-code source.

## What Is Not Shipped Yet

- Parcel lookup runtime.
- GIS import or Esri integration.
- Zoning Q&A.
- Planner review queue.
- Public resident UI beyond the landing page.
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

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
