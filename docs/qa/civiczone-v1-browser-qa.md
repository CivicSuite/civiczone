# CivicZone v1.0.0 Browser QA Evidence

Date: 2026-05-21

## Surfaces

| Surface | Viewport | Result | Evidence |
|---|---:|---|---|
| Resident lookup `/civiczone` | 1440x1000 | PASS | `docs/qa/civiczone-v1-public-desktop-resident-ready.png` |
| Resident success state | 1440x1000 | PASS | `docs/qa/civiczone-v1-public-desktop-resident-success.png` |
| Resident empty state | 1440x1000 | PASS | `docs/qa/civiczone-v1-public-desktop-resident-empty.png` |
| Resident planner-review partial state | 1440x1000 | PASS | `docs/qa/civiczone-v1-public-desktop-resident-partial.png` |
| Resident lookup `/civiczone` | 390x844 | PASS | `docs/qa/civiczone-v1-public-mobile-ready.png` |
| Resident mobile states | 390x844 | PASS | `docs/qa/civiczone-v1-public-mobile-states.png` |
| Staff workspace `/civiczone/staff` | 1440x1000 | PASS | `docs/qa/civiczone-v1-staff-desktop-ready.png` |
| Staff answer workflow | 1440x1000 | PASS | `docs/qa/civiczone-v1-staff-desktop-answer.png` |
| Staff queue, analytics, outline workflows | 1440x1000 | PASS | `docs/qa/civiczone-v1-staff-desktop-workflows.png` |
| Staff unauthorized-role error | 1440x1000 | PASS | `docs/qa/civiczone-v1-staff-desktop-auth-error.png` |
| Staff workspace `/civiczone/staff` | 390x844 | PASS | `docs/qa/civiczone-v1-staff-mobile-ready.png` |
| Staff answer workflow | 390x844 | PASS | `docs/qa/civiczone-v1-staff-mobile-answer.png` |

## State Matrix

| State | Evidence | Result |
|---|---|---|
| Loading | Buttons disable and status text changes during fetch | PASS |
| Success | Parcel `100-200-300`, zone `R-2`, ADU answer, citation `CMC 18.42.030` render | PASS |
| Empty | Missing parcel returns actionable "load local records or use sample parcel" fix path | PASS |
| Error | Staff role changed to `resident` returns actionable allowed-role error | PASS |
| Partial/degraded | Determination request routes to planner review with non-determination boundary | PASS |

## Console, Keyboard, Layout

- Desktop resident console: `docs/qa/civiczone-v1-public-desktop-console.json`, zero errors/warnings.
- Desktop staff console: `docs/qa/civiczone-v1-staff-desktop-console.json`, zero errors/warnings.
- Mobile console: `docs/qa/civiczone-v1-mobile-console.json`, zero errors/warnings after favicon fix.
- Keyboard/focus/layout: `docs/qa/civiczone-v1-keyboard-focus-layout.json`.
- Public and staff pages had no horizontal overflow at desktop checks.
- Focus reached skip link, fields, workflow buttons, and staff workspace link in visible order.

## Copy Review

- Resident copy states that CivicZone provides information only and does not make zoning determinations or provide legal advice.
- Empty and error states include a concrete fix path.
- Staff page states that staff API actions require trusted municipal access headers from an approved proxy.
- Staff workflow output remains review support; official determinations stay with planning staff.
