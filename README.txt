CivicZone
=========

CivicZone is the planned CivicSuite module for parcel-aware zoning and land-use Q&A.

Current state: v0.1.2 public UI foundation release plus production-depth parcel/rule and resident-question persistence slices. This repo ships a package shell, health/root endpoints, documentation gates, canonical zoning schema models, Alembic migration scaffold, sample parcel/zone lookup API, sample use/dimensional rule APIs, optional database-backed parcel/rule lookup records and resident question ledger via CIVICZONE_PARCEL_RULE_DB_URL, citation-grounded sample Q&A, planner-escalation/staff-context samples, an accessible public sample UI at /civiczone, and civiccore==1.0.0 dependency alignment. It does not yet use live LLM calls, ingest live GIS data, make zoning determinations, or replace planner review.

Set CIVICZONE_PARCEL_RULE_DB_URL to enable persistent parcel, use-rule, dimensional-rule, and resident-question ledger records. When unset, CivicZone continues to use deterministic in-memory sample data and does not persist question rows.

Developer quickstart:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh

Code license: Apache 2.0.
Documentation license: CC BY 4.0.
