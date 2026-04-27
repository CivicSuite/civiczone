# Milestone 8 Done - v0.1.0 Release

Date: 2026-04-27

## Scope

- Synchronized package, runtime, tests, release gate, and current-facing documentation to `0.1.0`.
- Removed current-facing `0.1.0.dev0` references from release surfaces.
- Updated root endpoint to point beyond the milestone sprint into the post-v0.1.0 roadmap.
- Prepared build artifacts for the GitHub release: wheel, sdist, and SHA256SUMS.

## Verification

- `bash scripts/verify-release.sh`: passing.
- `python -m pytest -q`: passing.
- `python -m ruff check .`: passing.
- Current-facing version surface scan: `0.1.0` present and `0.1.0.dev0` absent.

## Boundaries

CivicZone v0.1.0 remains a foundation release. It does not ship live GIS ingestion, live LLM calls, authentication/RBAC, planner review queues, official zoning determinations, or legal advice.
