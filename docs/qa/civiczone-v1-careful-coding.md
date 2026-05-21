# CivicZone v1.0.0 Careful-Coding Evidence

Date: 2026-05-21

Scope: CivicZone active module only.

## Pre-Edit Trace

1. Callers read: `GET /civiczone`, new `GET /civiczone/staff`, every `/api/v1/civiczone/staff/*` route, resident Q&A routes, public UI tests, staff workflow tests, release verifier, docs verifier, and GitHub workflows.
2. Runtime context traced: FastAPI sync route handlers under Uvicorn/TestClient; staff routes run behind trusted municipal headers and now validate source through CivicCore trusted-proxy helpers; resident UI uses same-origin browser `fetch`; optional persistence remains behind `CIVICZONE_PARCEL_RULE_DB_URL`.
3. Fan-out search: `0.2.0`, `1.0.1`, `v0.2.0`, recovery labels, CivicCore placeholder import guard, public UI static-state claims, staff-header docs, release workflows, and test expectations.
4. Data contract identified: package version, CivicCore wheel URL/hash, root/health version payloads, staff auth failure semantics, public/staff HTML render paths, browser state evidence, and release artifact names.
5. Blast radius: CivicZone API responses, staff route authorization, resident and staff browser UX, docs, release verifier, GitHub verify/release workflows, package artifacts, and future suite truth.

## Post-Edit Proof

6. Changed files re-read: `civiczone/main.py`, `civiczone/public_ui.py`, `civiczone/staff_ui.py`, tests, release scripts, README/manual/security/changelog/docs, and QA evidence.
7. Code path narrated: resident submits parcel/question -> `/api/v1/civiczone/parcels/lookup` returns cited parcel context -> `/api/v1/civiczone/questions/answer` returns answer/refusal/escalation -> UI renders success, empty, error, or planner-review partial state with actionable copy and non-determination boundary.
8. Staff path narrated: staff enters principal/role -> browser calls staff API with trusted headers -> FastAPI enforces trusted proxy/source and role -> staff Q&A, ambiguity queue, analytics, and report outline return staff-only records or actionable auth errors.
9. Render/data path proved: browser screenshots and console logs are saved under `docs/qa/`; desktop and mobile resident/staff surfaces passed; keyboard focus and no-horizontal-overflow checks are recorded.

## Five-Lens Self-Audit

- Engineering: full release verifier passes with 71 tests, docs gate, placeholder import gate, Ruff, build artifacts, and SHA256SUMS.
- UX: resident and staff browser flows have loading, success, empty, error, and partial states; copy gives concrete next steps.
- QA: desktop/mobile screenshots, console logs, keyboard/focus, layout, and adversarial mock coverage are recorded.
- Tests: staff route tests cover missing auth, underprivileged roles, trusted-source rejection, persistence, and resident/staff leakage boundaries.
- Docs: current-facing docs now say CivicZone v1.0.0, CivicCore v1.1.0, trusted-proxy staff access, and no legal/determination/live-vendor overclaims.
