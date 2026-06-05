# QA Deep Dive

## Scope

Ran runtime API, release gate, CLI smoke, and browser walkthrough checks.

## Findings

None.

## Evidence

- `/health` returned `{"status":"ok","service":"civiczone","version":"0.2.2","civiccore_version":"1.2.0"}`.
- CLI smoke returned `CivicZone import complete: 1 parcels, 0 use rules, 0 dimensional rules.`
- Browser walkthrough passed resident success, empty, and planner-review states on desktop and mobile.
- Staff page rendered on desktop and mobile with trusted header guidance.

## Notes

The resident empty-state walkthrough intentionally triggers a 404 from `/api/v1/civiczone/parcels/lookup`; the UI catches it and renders the empty state. Playwright records that expected 404 as a console resource entry, not a JavaScript exception or request failure.
