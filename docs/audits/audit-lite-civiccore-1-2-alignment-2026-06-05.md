# Audit Lite - CivicCore 1.2 Alignment
**Date:** 2026-06-05
**Scope:** Reviewed the CivicZone dependency, tests, and current-facing docs updated to align with the published CivicCore v1.2.0 wheel.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. CivicZone now installs CivicCore v1.2.0 from the published release wheel, `/health` independently proves the imported runtime version, and the schema test accepts CivicCore-owned metadata while still requiring every CivicZone table. No escalation is needed for this scoped dependency-alignment change.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `pyproject.toml` pins the published CivicCore v1.2.0 wheel by direct URL and SHA256 hash, preserving the release-wheel install contract.
- `tests/test_runtime_foundation.py` checks both the wheel URL/hash and `/health` runtime version, so a stale dependency or fake doc-only update fails.
- `tests/test_milestone_2_schema_and_migrations.py` filters metadata to `civiczone.` tables before comparing canonical zoning tables, which matches CivicCore v1.2.0's shared `Base` behavior without weakening CivicZone table coverage.
- Current-facing docs and QA notes no longer contain stale previous-version CivicCore claims.

## Verification

- Targeted tests: `3 passed, 1 warning`
- Full test suite: `71 passed, 1 skipped, 1 warning`
- Release gate: `VERIFY-RELEASE: PASSED`
- Stale pin scan: no remaining matches for the previous CivicCore URL/hash/version strings.

## Escalation recommendation

No escalation needed. This was a scoped compatibility slice with direct regression coverage and a passing release gate.
