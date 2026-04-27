CivicZone
=========

CivicZone is the planned CivicSuite module for parcel-aware zoning and land-use Q&A.

Current state: v0.1.0.dev0 public UI foundation in development. This repo currently ships a package shell, health/root endpoints, documentation gates, canonical zoning schema models, Alembic migration scaffold, sample parcel/zone lookup API, sample use/dimensional rule APIs, citation-grounded sample Q&A, planner-escalation/staff-context samples, and an accessible public sample UI at /civiczone. It does not yet use live LLM calls, ingest live GIS data, make zoning determinations, or replace planner review.

Developer quickstart:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh

Code license: Apache 2.0.
Documentation license: CC BY 4.0.
