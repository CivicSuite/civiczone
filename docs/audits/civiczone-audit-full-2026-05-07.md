# CivicZone Audit-Full Recovery Packet

Date: 2026-05-07
Repo: `CivicSuite/civiczone`
Branch: `recovery/civiczone-release-truth-gates`
Mode: release-gate recovery cleanup

## 1. Executive Audit

Scope: CivicZone local checkout and live `origin/main` parity at branch
baseline. Local `HEAD` and `origin/main` matched at
`6176fca7f11a6876d62d8f82ed575db14eb2561f`; the remote URL is
`https://github.com/CivicSuite/civiczone.git` with no embedded token.

Overall verdict: CivicZone had the same release-truth problem as the earlier
modules: useful implementation depth, but public docs promoted the v1 label too
strongly for the recovery standard. This branch freezes fresh product-ready
promotion, fixes the WSL interpreter-order defect, adds docs-source guardrails,
and will attach current browser and WSL evidence before push.

Ship posture: do not promote CivicZone as recertified product-ready until this
branch merges and post-merge CI is green.

Severity summary: Critical 2 fixed; Major 2 fixed; unresolved Blocker/Critical
0 in this branch-level recovery scope after verification.

Static audit confidence: high for release-script and docs changes.
Runtime sign-off confidence: medium-high after WSL install, WSL release gate,
and Playwright docs QA; final confidence depends on post-merge CI.

CI/workflow posture: CI exists and runs release verification; final status must
be checked after PR push and merge.

## 2. Audit Coverage Ledger

| Lane | Status | Evidence summary | Blocker |
| --- | --- | --- | --- |
| remote parity | Checked | `HEAD` and `origin/main` matched before edits. | None |
| local-vs-live commit truth | Checked | Divergence count was `0 0` at baseline. | None |
| CI/workflow presence | Checked | CI/release script present. | None |
| Windows install path | Partially checked | Focused local tests planned. | Full Windows release gate not required for this patch. |
| Linux or Unix install path | Checked | WSL native release gate passed. | None |
| platform parity verdict | Checked | Script now prefers `python3` before `python`. | None |
| first boot | Partially checked | Runtime endpoint tests cover FastAPI boot. | Full browser app flow remains for recertification. |
| required post-install steps | Checked | Release script handles package install/build verification. | None |
| migrations | Partially checked | Existing tests cover models/migrations. | No database rehearsal added here. |
| seed/bootstrap requirements | Partially checked | Existing sample data paths remain unchanged. | No new seed path. |
| runtime dependency and model requirements | Checked | `civiccore==1.0.0`; no live vendor calls by default. | None |
| first-boot dependency truth | Checked | Fresh WSL install passed after direct release-wheel dependency fix. | None |
| secrets and credential handling | Checked | Tracked-file secret scan returned no matches. | None |
| auth and session handling | Partially checked | Staff-only protections covered by existing tests. | Full auth browser QA remains. |
| authorization and role boundaries | Partially checked | Existing tests cover staff precedent boundary. | Full role browser pass remains. |
| response-schema sensitive-data exposure | Partially checked | Existing tests remain in suite. | Not expanded here. |
| audit and compliance logging | Partially checked | Existing staff workflow records remain. | No new audit-log drill. |
| external and admin surfaces | Checked | Docs label local adversarial mocks and no live vendor calls by default. | None |
| connector implementation completeness | Partially checked | Boundaries documented; no connector feature work in this patch. | Full recertification remains. |
| connector docs truth | Checked | Mock-vs-production labeling retained. | None |
| background jobs and schedulers | Not applicable | No scheduler changed. | None |
| frontend critical journeys | Checked | Docs landing page Playwright pass completed. | None |
| loading states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| empty states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| error states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| partial states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| accessibility cues | Checked | First `Tab` reaches the recovery-status link. | None |
| docs truthfulness | Checked | Product-release wording replaced and banlist added. | None |
| version consistency | Checked | Version remains `1.0.0`; label is provisional. | None |
| release artifact consistency | Checked | WSL release gate built wheel, sdist, and `SHA256SUMS.txt`. | None |
| test realism | Checked | Regression tests added for interpreter order and docs banlist. | None |
| runtime, build, and test verification | Checked | WSL release gate passed. | None |
| browser verification | Checked | Playwright desktop/mobile screenshots and summary added. | None |
| prior audit or verification challenge | Checked | Prior v1 product-ready posture challenged. | None |

## 3. Claim Verification Matrix

| Claim | Source | Verdict | Evidence |
| --- | --- | --- | --- |
| CivicZone v1 is a published label. | `pyproject.toml`, docs | True | Version remains `1.0.0`. |
| CivicZone is freshly product-ready. | Prior README/manual wording | False as a current claim | Docs now mark v1 provisional during recovery. |
| CivicZone uses local adversarial mocks instead of external deployment proof. | README/manual/docs | True | Product boundaries say live external vendor calls are not default. |
| WSL release verification proves Linux. | Prior script order | True in branch | WSL selected `.venv-wsl/bin/python3`, platform `linux`, and passed release gate. |
| Fresh install can resolve CivicCore. | `pyproject.toml` | True in branch | Dependency now points at the published CivicCore wheel and Hatch allows direct references. |

## 4. What The Dev Team Needs To Do Now

### Must fix before ship

- None remaining before PR push; post-merge CI still gates final recovery status.

### Should fix this sprint

- `CI-001`: Push PR, wait for CI, merge only if green.

### Can defer if consciously accepted

- `UX-002`: Full application Playwright recertification across all resident and
  staff states before any public product-ready announcement.

## 5. Next-Sprint Watchlist

Architecture: preserve CivicZone as a CivicCore/CivicCode consumer only.
Security and compliance debt: expand staff-only precedent browser checks.
UX debt: convert historical screenshot evidence to executable user-flow tests.
Docs debt: keep recovery labels synchronized across README/manual/docs.
Install/bootstrap debt: add fresh WSL first-boot app walkthrough.
Test debt: add regression tests for every release-gate failure class.
Operational and release debt: require post-merge CI proof before status changes.

## 6. Engineering Deep Dive

Verdict: release-script interpreter order and package dependency metadata were
the primary engineering defects.
Strengths: release script centralizes version, tests, docs, ruff, and build.
Findings: `REL-001` and `BOOT-001` fixed. Verification gaps: post-merge CI.

### `[CRITICAL] REL-001 WSL release gate could select Windows Python`

- `Confidence`: High
- `Evidence type`: Static
- `Status`: Durable defect fixed

Why it matters:

A WSL release gate that runs Windows Python is not Linux evidence.

Evidence:

- `scripts/verify-release.sh` previously probed `python` before `python3`.
- The branch reverses that order and adds a regression test.

Blast radius:

- Every release verification run relying on WSL as Linux coverage.

Fix:

- Prefer native `python3` before `python`.

### `[CRITICAL] BOOT-001 Fresh installs could not resolve CivicCore`

- `Confidence`: High
- `Evidence type`: Runtime
- `Status`: Durable defect fixed

Why it matters:

A package that only installs after CI preinstalls a dependency is not a real
first-boot install path.

Evidence:

- WSL `pip install -e .[dev]` failed while `pyproject.toml` used
  `civiccore==1.0.0`.
- The dependency now points at the published CivicCore v1.0.0 release wheel and
  Hatch direct references are enabled.
- Fresh WSL install now succeeds.

Blast radius:

- New developer install, CI reproducibility, and release-package metadata.

Fix:

- Use the release-wheel direct URL and set
  `tool.hatch.metadata.allow-direct-references = true`.

## 7. Security And Authorization Deep Dive

Verdict: tracked-file secret scan returned no matches. Strengths: staff-only
precedent boundary is an explicit product boundary. Verification gaps: full
browser role pass remains for recertification.

## 8. UI/UX Deep Dive

Verdict: docs copy now sets accurate expectations and browser verification
passed. Strengths: docs landing page plainly says no legal advice or zoning
determinations and links to recovery status. Verification gaps: full app
user-flow QA remains for recertification.

## 9. Product/PM Deep Dive

Verdict: product posture is now more honest: v1 exists as a label, not a fresh
announcement-ready certification. Verification gaps: broader suite retest.

## 10. Documentation Deep Dive

Verdict: stale product-release wording was real and fixed in branch. Strengths:
README, text README, manuals, changelog, and docs landing page now use recovery
language.

### `[MAJOR] DOC-001 Public docs overclaimed v1 status`

- `Confidence`: High
- `Evidence type`: Static
- `Status`: Durable defect fixed

Why it matters:

Municipal users and auditors read release language as a trust claim.

Evidence:

- Current-facing docs now say the v1 label is under release-recovery review.

Blast radius:

- README, manuals, changelog, and docs landing page.

Fix:

- Replace product-release wording and add docs gate banlist entries.

## 11. Install / Bootstrap / Seeding Deep Dive

Verdict: fresh WSL install and native WSL release gate both pass after the
dependency metadata fix. Verification gaps: post-merge CI.

## 12. Version And Release Consistency Deep Dive

Verdict: version remains `1.0.0`; release posture is provisional. No version
bump was made because this is recovery truth labeling, not a new product claim.

## 13. Test Engineering Deep Dive

Verdict: regression tests now cover the failure class.

### `[MAJOR] TEST-001 Docs and release gates lacked regression coverage for recovery truth`

- `Confidence`: High
- `Evidence type`: Static
- `Status`: Durable defect fixed

Why it matters:

Without tests, the same overclaim and WSL false-proof can return.

Evidence:

- `tests/test_runtime_foundation.py` now checks interpreter order, docs banlist,
  and current docs recovery language.

Blast radius:

- Future release maintenance.

Fix:

- Add regression tests.

## 14. Runtime QA Deep Dive

Verdict: `[AUDITOR-RUN]` WSL and Playwright evidence passed. Prior historical
QA remains treated as historical evidence only.

## 15. Cross-Cutting Synthesis

The root issue is the same suite-wide pattern: release labels outpaced current
proof. This branch narrows the claim, locks a gate around the exact wording, and
fixes the platform proof so recovery status cannot be inflated by accident.

## 16. Verification Gaps And Sign-Off Limits

- Post-merge CI: required after PR merge.
- Full product recertification: outside this branch; required before public
  product-ready announcement.
