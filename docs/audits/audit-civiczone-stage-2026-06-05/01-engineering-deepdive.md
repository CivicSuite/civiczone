# Engineering Deep Dive

## Scope

Reviewed dependency metadata, release gate behavior, local data import, Q&A routing, database repository use, and FastAPI runtime paths.

## Findings

None.

## Evidence

- `pyproject.toml` pins CivicCore v1.2.0 by release wheel URL and SHA256.
- `civiczone/data_import.py` validates CSVs before creating repositories and uses `seed_defaults=False`.
- `civiczone/qa.py` keeps refusal/escalation guards before cited answer paths.
- Full release gate passed after all stage changes.

## What's Working

The source changes respect existing repository boundaries: import code reuses repository seed APIs, Q&A reuses lookup callables, and no new global runtime state was added.
