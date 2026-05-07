# Browser QA - CivicZone v0.1.2 Question Ledger

Run date: 2026-05-07

Target surfaces:

- `docs/index.html`
- `http://127.0.0.1:18131/civiczone`

| Scenario | Viewport | Status | Expected copy | Overflow | Console errors | Page errors | Result |
|---|---:|---:|---|---:|---:|---:|---|
| docs-index-desktop | 1440x1000 | 200 | question persistence | false | 0 | 0 | PASS |
| docs-index-mobile | 390x900 | 200 | question persistence | false | 0 | 0 | PASS |
| public-sample-desktop | 1440x1000 | 200 | does not provide legal advice | false | 0 | 0 | PASS |
| public-sample-mobile | 390x900 | 200 | does not provide legal advice | false | 0 | 0 | PASS |

Additional checks:

- `/civiczone` badge shows `v0.1.2 public UI foundation + parcel/rule and question persistence`.
- The prior no-op `Show sample zoning context` button is removed; the sample is presented as static pre-filled evidence.
- Keyboard focus reaches the skip link and API docs link.
- No horizontal overflow at desktop or mobile widths.

Result: PASS.
