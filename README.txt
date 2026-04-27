CivicZone
=========

CivicZone is the planned CivicSuite module for parcel-aware zoning and land-use Q&A.

Current state: v0.1.0.dev0 runtime foundation in development. This repo currently ships a package shell, health/root endpoints, documentation gates, and milestone plan. It does not yet answer zoning questions, ingest GIS data, make zoning determinations, or replace planner review.

Developer quickstart:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh

Code license: Apache 2.0.
Documentation license: CC BY 4.0.
