#!/usr/bin/env bash
set -euo pipefail

required=(
  "README.md"
  "README.txt"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "LICENSE-CODE"
  "LICENSE-DOCS"
  ".gitignore"
  "AGENTS.md"
  "USER-MANUAL.md"
  "SECURITY.md"
  "SUPPORT.md"
  "CODE_OF_CONDUCT.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  "docs/RECONCILIATION.md"
  "docs/MILESTONES.md"
  "docs/IMPLEMENTATION_PLAN.md"
  "docs/github-discussions-seed.md"
  "docs/index.html"
  "pyproject.toml"
  "civiczone/__init__.py"
  "civiczone/main.py"
  "civiczone/models.py"
  "civiczone/parcel_lookup.py"
  "civiczone/rule_lookup.py"
  "civiczone/qa.py"
  "civiczone/question_ledger.py"
  "civiczone/staff_context.py"
  "civiczone/public_ui.py"
  "civiczone/migrations/alembic.ini"
  "civiczone/migrations/env.py"
  "civiczone/migrations/guards.py"
  "civiczone/migrations/versions/civiczone_0001_schema.py"
  "civiczone/migrations/versions/civiczone_0002_parcel_rule_lookup_records.py"
  "civiczone/migrations/versions/civiczone_0003_question_ledger.py"
  "civiczone/migrations/versions/civiczone_0004_staff_workflows.py"
  "MILESTONE_7_DONE.md"
  "MILESTONE_8_DONE.md"
  "PRODUCTION_DEPTH_PARCEL_RULE_PERSISTENCE_DONE.md"
  "PRODUCTION_DEPTH_QUESTION_LEDGER_DONE.md"
)

echo "==> Required-artifact check"
for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "FAIL: missing required artifact: $file" >&2
    exit 1
  fi
done

echo "==> Current-facing shipped/planned truth check"
current_files=("README.md" "README.txt" "USER-MANUAL.md" "docs/index.html")
bad_markers=(
  "CivicZone is shipping"
  "Shipping v0.1.0"
  "zoning answers are available"
  "parcel lookup is available"
  "GIS import is available"
  "zoning determinations are available"
  "legal advice is available"
  "planner review queue is available"
  "staff-only precedent is public"
  "v0.2.0 recovery release"
  "0.2.0 recovery release"
  "current product release"
)

for file in "${current_files[@]}"; do
  for marker in "${bad_markers[@]}"; do
    if grep -Fqi "$marker" "$file"; then
      echo "FAIL: stale/planned-as-shipped marker '$marker' found in $file" >&2
      exit 1
    fi
  done
done

echo "VERIFY-DOCS: PASSED"
