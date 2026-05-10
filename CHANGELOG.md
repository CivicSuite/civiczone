# Changelog

## [0.2.0] - 2026-05-10

- Demoted the false v1.0.0 release label after the external CivicSuite audit found this module is a recovery/foundation module, not a canonical spec-complete v1 product.
- Preserved the useful recovery work while resetting the public package version to 0.2.0.
- Kept the CivicCore v1.0.0 wheel dependency and pinned it with SHA256 for release integrity.
- Supersedes the prior public v1.0.0 posture; do not treat v1.0.0 as production-ready or spec-complete.

All notable changes to CivicZone will be documented in this file.

The format follows Keep a Changelog, and this project follows Semantic Versioning.

## [1.0.0] - 2026-05-07

### Recovery note

- The `1.0.0` label was checked through the suite release-recovery pass with a
  fresh local release gate and live browser QA. Treat the original release date
  as historical; the recovery evidence is recorded in
  `docs/release-recovery-status.md`.

### Added

- v1 resident zoning Q&A runtime with deterministic cited answers, refusal and escalation reasons, confidence metadata, and actionable next steps.
- Staff workflow APIs for planner Q&A, ambiguity review queue, high-volume question analytics, staff-report outline support, and flagged-answer review.
- Database-backed staff workflow records for planner questions, ambiguity queue items, and flagged answer reviews when `CIVICZONE_PARCEL_RULE_DB_URL` is configured.
- Local adversarial integration mocks for Esri ArcGIS REST, GeoJSON fallback, CivicCode, CivicClerk, CivicPlan, CivicAccess, county assessor, and CKAN boundary validation.
- Resident UI copy and visible state guidance for loading, success, empty, error, and partial outcomes.

### Changed

- Published CivicZone release surfaces at `1.0.0`; the later suite
  release-recovery pass records fresh verification evidence.
- Updated runtime and documentation boundaries to describe the v1 product without claiming legal advice, official zoning determinations, or live external vendor calls by default.

## [0.1.2] - 2026-05-07

### Added

- Production-depth parcel/rule lookup persistence slice with `CIVICZONE_PARCEL_RULE_DB_URL`, seeded sample parcel/use/dimensional records, and Alembic revision `civiczone_0002_parcel_rules`.
- Production-depth resident question ledger persistence for deterministic cited Q&A, including Alembic revision `civiczone_0003_question_ledger`.

### Changed

- Aligned CivicZone's release gate, CI install path, docs, and health-contract test with the published CivicCore v1.0.0 wheel before the next production-depth sprint.

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicZone to `civiccore==0.3.0` while preserving the v0.1 public UI foundation behavior.
- Updated version surfaces, release gate, CI CivicCore wheel install, documentation, and health-contract tests for the v0.1.1 dependency-alignment release.

## [0.1.0] - 2026-04-27

### Added

- Milestone 0 professional scaffold and reconciliation documents.
- Milestone 1 runtime foundation with package shell, root endpoint, health endpoint, tests, and release/documentation gates.
- Milestone 2 canonical zoning schema with SQLAlchemy models, Alembic scaffold, real pgvector migration test, and schema documentation.
- Milestone 3 sample parcel/zone lookup API with actionable unknown-parcel errors and zoning-determination disclaimer.
- Milestone 4 sample use and dimensional rule APIs with citations, disclaimers, and actionable 404s.
- Milestone 5 citation-grounded sample resident Q&A with escalation/refusal for determination or uncited questions.
- Milestone 6 planner-escalation classifier and staff-only precedent context sample, with leakage guard tests.
- Milestone 7 accessible public sample UI at `/civiczone`, with parcel context, cited rule cards, planner-escalation guidance, and browser QA evidence.
- Milestone 8 v0.1.0 release packaging, version synchronization, and GitHub release artifacts.
