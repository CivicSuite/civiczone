# CivicZone User Manual

## For Residents And Municipal Decision-Makers

CivicZone is planned to answer routine parcel-aware zoning questions with citations. It is not a zoning determination tool, not legal advice, and not a replacement for planner review.

Current state: `0.1.0.dev0` planner-escalation foundation exists in development. The package, health endpoints, canonical zoning schema, Alembic migrations, sample parcel/zone lookup API, sample use/dimensional rule APIs, citation-grounded sample Q&A, and staff-context samples exist. Live LLM calls, live GIS import, authentication/RBAC, and public workflow screens are not implemented yet.

## For IT And Technical Staff

CivicZone is a FastAPI Python package pinned to `civiccore==0.2.0`. The current runtime exposes:

- `GET /`
- `GET /health`
- Canonical SQLAlchemy models for zones, overlays, parcels, use rules, dimensional rules, citations, precedents, interpretation notes, and zone questions.
- Alembic migration `civiczone_0001_schema`.
- `POST /api/v1/civiczone/parcels/lookup` for sample parcel lookup.
- `POST /api/v1/civiczone/rules/use` for sample use status.
- `POST /api/v1/civiczone/rules/dimensional` for sample dimensional rules.
- `POST /api/v1/civiczone/questions/answer` for citation-grounded sample questions.
- `POST /api/v1/civiczone/planner-review/classify` for sample escalation classification.
- `GET /api/v1/civiczone/staff/precedents/{precedent_id}` for staff-only sample context.

Run local verification with:

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## Architecture

```mermaid
flowchart LR
  Resident["Resident or planner"] --> CivicZone["CivicZone"]
  CivicZone --> CivicCore["CivicCore v0.2.0"]
  CivicZone --> CivicCode["CivicCode v0.1.0"]
  CivicZone -. future .-> GIS["GIS / assessor sources"]
```

CivicZone depends on CivicCore and CivicCode. CivicCore does not depend on CivicZone.
