# CivicZone Current Release QA

Date: 2026-05-09
Scope: live local CivicZone runtime at `http://127.0.0.1:18152`

## Summary

Live browser QA passed for the current CivicZone recovery pass.

| Scenario | Viewport | Path | Status | Overflow | Console | Page errors | Focus evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| resident-desktop | 1440x1000 | `/civiczone` | 200 | no | 0 | 0 | Skip to main content |
| resident-mobile | 390x844 | `/civiczone` | 200 | no | 0 | 0 | Skip to main content |
| docs-desktop | 1440x1000 | `/docs` | 200 | no | 0 | 0 | `/openapi.json` |
| health-json | 800x600 | `/health` | 200 | no | 0 | 0 | response content rendered |

## Evidence Files

- `docs/qa/current-civiczone-release-qa/resident-desktop.png`
- `docs/qa/current-civiczone-release-qa/resident-mobile.png`
- `docs/qa/current-civiczone-release-qa/docs-desktop.png`
- `docs/qa/current-civiczone-release-qa/health-json.png`
- `docs/qa/current-civiczone-release-qa/summary.json`

## Boundaries Checked

- Resident UI states remain visible: loading, success, empty, error, and partial.
- The page keeps the informational-only boundary and planner escalation copy visible.
- No browser console messages or page errors were observed.
- No horizontal overflow was observed at desktop or mobile widths.
- Keyboard focus reached the skip link or expected rendered browser content.
