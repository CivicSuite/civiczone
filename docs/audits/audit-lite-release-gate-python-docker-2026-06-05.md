# Audit Lite - Release Gate Python/Docker Hygiene
**Date:** 2026-06-05
**Scope:** CivicZone release-gate slice that makes Docker-backed pgvector migration tests skip when Docker is unavailable and makes `scripts/verify-release.sh` prefer the repo-local virtualenv interpreter before global Python.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. The change removes two false-red release-gate modes without weakening the real migration test when Docker is available: the Docker-backed pgvector integration still runs when a daemon is reachable, and release verification now uses the repo-local venv instead of leaking in global CivicCore. No audit-lite findings remain.

## Severity Rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's Working
- `tests/test_milestone_2_schema_and_migrations.py` now probes `docker info` before the real pgvector migration integration test and skips only when Docker is unavailable.
- `tests/test_milestone_2_schema_and_migrations.py` includes a regression test proving Docker API failure returns unavailable instead of crashing the release gate.
- `scripts/verify-release.sh` now prefers `.venv/bin/python` and `.venv/Scripts/python.exe` before global `python3`, avoiding the observed global CivicCore contamination when the repo venv has the pinned CivicCore dependency.
- `tests/test_runtime_foundation.py` guards the interpreter-order contract.

## Verification
- Targeted: `2 passed`.
- Full venv suite: `71 passed, 1 skipped`.
- Release gate: `VERIFY-RELEASE: PASSED`.

## Escalation Recommendation
No escalation needed for this slice. It is scoped to test/release-gate determinism and does not change CivicZone runtime behavior.
