# CivicZone Local Data Import

CivicZone can load municipal parcel and zoning-rule CSV exports into the configured lookup database. This is a local-first path for city-owned data; it does not call live GIS, permitting, or vendor systems.

## Database Target

Use the same SQLAlchemy URL that the runtime reads from `CIVICZONE_PARCEL_RULE_DB_URL`. The importer creates the lookup tables if they do not already exist and does not seed sample rows.

## CSV Contracts

Parcel CSV columns:

| Column | Required value | Notes |
| --- | --- | --- |
| `parcel_number` | Yes | Local parcel identifier. |
| `address` | Yes | Street address used for lookup. |
| `zone_code` | Yes | Normalized to uppercase on import. |
| `zone_name` | Yes | Human-readable zone name. |
| `overlays` | No | Semicolon-separated overlay names. |
| `constraints` | No | Semicolon-separated parcel constraints. |
| `source` | Yes | Data source label, export name, or file reference. |
| `disclaimer` | Yes | Public-facing non-determination boundary. |

Use-rule CSV columns:

| Column | Required value |
| --- | --- |
| `zone_code` | Yes |
| `use` | Yes |
| `status` | Yes |
| `review_path` | Yes |
| `citation` | Yes |
| `disclaimer` | Yes |

Dimensional-rule CSV columns:

| Column | Required value |
| --- | --- |
| `zone_code` | Yes |
| `rule_type` | Yes |
| `value` | Yes |
| `citation` | Yes |
| `disclaimer` | Yes |

## Operator Flow

Run the `civiczone-import-data` console script from an environment where CivicZone is installed. Provide one or more CSV paths and the target database URL. The importer validates every supplied CSV before writing any rows.

Example import summary:

```text
CivicZone import complete: 1 parcels, 1 use rules, 1 dimensional rules.
```

After import, start CivicZone with `CIVICZONE_PARCEL_RULE_DB_URL` set to the same database URL. Parcel, use-rule, dimensional-rule, resident-question ledger, and staff-workflow APIs will use the configured local store.

## Failure Behavior

- Missing required columns fail before any database writes.
- Empty required values fail before any database writes.
- Existing parcel/rule keys are left unchanged so repeated imports are idempotent.
- Sample parcel and zoning rules are not loaded into the target database by the importer.
