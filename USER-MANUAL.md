# CivicZone User Manual

## For Residents And Municipal Decision-Makers

CivicZone is planned to answer routine parcel-aware zoning questions with citations. It is not a zoning determination tool, not legal advice, and not a replacement for planner review.

Current state: `0.1.0.dev0` runtime foundation exists in development. Parcel lookup, zoning answers, GIS import, and public workflow screens are not implemented yet.

## For IT And Technical Staff

CivicZone is a FastAPI Python package pinned to `civiccore==0.2.0`. The current runtime exposes:

- `GET /`
- `GET /health`

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
