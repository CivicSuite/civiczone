from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from civiczone.parcel_lookup import ParcelLookupRepository, ParcelLookupResult
from civiczone.rule_lookup import DimensionalRuleResult, RuleLookupRepository, UseRuleResult


PARCEL_COLUMNS = {
    "parcel_number",
    "address",
    "zone_code",
    "zone_name",
    "overlays",
    "constraints",
    "source",
    "disclaimer",
}
USE_RULE_COLUMNS = {"zone_code", "use", "status", "review_path", "citation", "disclaimer"}
DIMENSIONAL_RULE_COLUMNS = {"zone_code", "rule_type", "value", "citation", "disclaimer"}
PARCEL_REQUIRED_VALUES = PARCEL_COLUMNS - {"overlays", "constraints"}


@dataclass(frozen=True)
class ImportSummary:
    parcels: int = 0
    use_rules: int = 0
    dimensional_rules: int = 0


def import_local_dataset(
    *,
    db_url: str,
    parcels_csv: Path | None = None,
    use_rules_csv: Path | None = None,
    dimensional_rules_csv: Path | None = None,
) -> ImportSummary:
    """Validate and import local municipal parcel/rule CSVs into CivicZone lookup tables."""

    if parcels_csv is None and use_rules_csv is None and dimensional_rules_csv is None:
        raise ValueError("Provide at least one CSV path to import.")

    parcels = _read_parcels(parcels_csv) if parcels_csv is not None else []
    use_rules = _read_use_rules(use_rules_csv) if use_rules_csv is not None else []
    dimensional_rules = (
        _read_dimensional_rules(dimensional_rules_csv)
        if dimensional_rules_csv is not None
        else []
    )

    if parcels:
        ParcelLookupRepository(db_url=db_url, seed_defaults=False).seed(parcels)
    if use_rules or dimensional_rules:
        repository = RuleLookupRepository(db_url=db_url, seed_defaults=False)
        if use_rules:
            repository.seed_use_rules(use_rules)
        if dimensional_rules:
            repository.seed_dimensional_rules(dimensional_rules)

    return ImportSummary(
        parcels=len(parcels),
        use_rules=len(use_rules),
        dimensional_rules=len(dimensional_rules),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import local municipal parcel and zoning-rule CSV files into CivicZone."
    )
    parser.add_argument("--db-url", required=True, help="SQLAlchemy database URL for CivicZone lookup tables.")
    parser.add_argument("--parcels-csv", type=Path, help="CSV with parcel lookup rows.")
    parser.add_argument("--use-rules-csv", type=Path, help="CSV with zoning use-rule rows.")
    parser.add_argument("--dimensional-rules-csv", type=Path, help="CSV with dimensional-rule rows.")
    args = parser.parse_args(argv)

    summary = import_local_dataset(
        db_url=args.db_url,
        parcels_csv=args.parcels_csv,
        use_rules_csv=args.use_rules_csv,
        dimensional_rules_csv=args.dimensional_rules_csv,
    )
    print(
        "CivicZone import complete: "
        f"{summary.parcels} parcels, "
        f"{summary.use_rules} use rules, "
        f"{summary.dimensional_rules} dimensional rules."
    )
    return 0


def _read_parcels(path: Path) -> list[ParcelLookupResult]:
    return [
        ParcelLookupResult(
            parcel_number=_required(row, "parcel_number"),
            address=_required(row, "address"),
            zone_code=_required(row, "zone_code").upper(),
            zone_name=_required(row, "zone_name"),
            overlays=_split_list(row.get("overlays", "")),
            constraints=_split_list(row.get("constraints", "")),
            source=_required(row, "source"),
            disclaimer=_required(row, "disclaimer"),
        )
        for row in _read_rows(path, PARCEL_COLUMNS, PARCEL_REQUIRED_VALUES)
    ]


def _read_use_rules(path: Path) -> list[UseRuleResult]:
    return [
        UseRuleResult(
            zone_code=_required(row, "zone_code").upper(),
            use=_required(row, "use"),
            status=_required(row, "status"),
            review_path=_required(row, "review_path"),
            citation=_required(row, "citation"),
            disclaimer=_required(row, "disclaimer"),
        )
        for row in _read_rows(path, USE_RULE_COLUMNS, USE_RULE_COLUMNS)
    ]


def _read_dimensional_rules(path: Path) -> list[DimensionalRuleResult]:
    return [
        DimensionalRuleResult(
            zone_code=_required(row, "zone_code").upper(),
            rule_type=_required(row, "rule_type").casefold(),
            value=_required(row, "value"),
            citation=_required(row, "citation"),
            disclaimer=_required(row, "disclaimer"),
        )
        for row in _read_rows(path, DIMENSIONAL_RULE_COLUMNS, DIMENSIONAL_RULE_COLUMNS)
    ]


def _read_rows(
    path: Path,
    required_columns: set[str],
    required_values: set[str],
) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(required_columns - fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        rows = list(reader)
    for index, row in enumerate(rows, start=2):
        for column in required_values:
            if row.get(column, "").strip() == "":
                raise ValueError(f"{path}:{index} has an empty required value for {column}")
    return rows


def _required(row: dict[str, str], column: str) -> str:
    return row[column].strip()


def _split_list(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(";") if part.strip())


if __name__ == "__main__":
    raise SystemExit(main())
