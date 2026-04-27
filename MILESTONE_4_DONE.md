# Milestone 4 Done

Milestone 4 produced the sample use and dimensional rule foundation:

- `lookup_use_rule()` for sample allowed/conditional/not-listed use checks.
- `lookup_dimensional_rule()` for sample setback and height checks.
- `POST /api/v1/civiczone/rules/use`.
- `POST /api/v1/civiczone/rules/dimensional`.
- Every response carries a citation and zoning-determination disclaimer.
- Unknown rules return actionable 404 responses.

Still not shipped:

- Resident Q&A.
- Live GIS import.
- Zoning determinations.
- Public workflow UI.
