CivicZone
=========

CivicZone is CivicSuite's parcel-aware zoning and land-use Q&A module.

Current state: v1.0.0 product release. This repo ships a FastAPI service, health/root endpoints, documentation gates, canonical zoning schema models, Alembic migrations, deterministic parcel/zone lookup, cited use-rule lookup, cited dimensional-rule prechecks, resident Q&A with refusal and escalation rules, optional database-backed parcel/rule and resident-question ledger records through CIVICZONE_PARCEL_RULE_DB_URL, staff workflow APIs, staff-only precedent protection, an accessible resident UI at /civiczone, adversarial local integration mocks, and civiccore==1.0.0 dependency alignment.

Product boundaries:

- CivicZone gives informational zoning context with citations.
- CivicZone refuses or escalates zoning-determination, legal-advice, out-of-jurisdiction, stale-data, low-confidence, and uncited-answer requests.
- CivicZone does not make zoning determinations, approve permits, replace planner review, or call live external vendor systems by default.
- CivicZone integration behavior is validated with local adversarial mocks for Esri ArcGIS REST, GeoJSON fallback, CivicCode, CivicClerk, CivicPlan, CivicAccess, county assessor, and CKAN boundaries.

Set CIVICZONE_PARCEL_RULE_DB_URL to enable persistent parcel, use-rule, dimensional-rule, and resident-question ledger records. When unset, CivicZone uses deterministic in-memory sample data and does not persist question rows.

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
