CivicZone
=========

CivicZone is CivicSuite's parcel-aware zoning and land-use Q&A module.

Current state: published v1.0.0 label under suite-wide release-recovery review. This repo contains a FastAPI service, health/root endpoints, documentation gates, canonical zoning schema models, Alembic migrations, deterministic parcel/zone lookup, cited use-rule lookup, cited dimensional-rule prechecks, resident Q&A with refusal and escalation rules, optional database-backed parcel/rule, resident-question ledger, and staff-workflow records through CIVICZONE_PARCEL_RULE_DB_URL, staff-only precedent protection, an accessible resident UI at /civiczone, adversarial local integration mocks, and CivicCore v1.0.0 release-wheel dependency alignment. Do not promote the v1 label as a fresh product-ready claim until recovery gates, post-merge CI, and broader suite retest evidence re-earn that status.

Product boundaries:

- CivicZone gives informational zoning context with citations.
- CivicZone refuses or escalates zoning-determination, legal-advice, out-of-jurisdiction, stale-data, low-confidence, and uncited-answer requests.
- CivicZone does not make zoning determinations, approve permits, replace planner review, or call live external vendor systems by default.
- CivicZone integration behavior is validated with local adversarial mocks for Esri ArcGIS REST, GeoJSON fallback, CivicCode, CivicClerk, CivicPlan, CivicAccess, county assessor, and CKAN boundaries.

Set CIVICZONE_PARCEL_RULE_DB_URL to enable persistent parcel, use-rule, dimensional-rule, resident-question ledger, and staff workflow records. When unset, CivicZone uses deterministic in-memory sample data and does not persist question or staff workflow rows.

Staff workflow endpoints require trusted municipal access headers:

- X-CivicZone-Principal
- X-CivicZone-Role: planner, staff, or zoning_admin

Developer quickstart:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh

Code license: Apache 2.0.
Documentation license: CC BY 4.0.
