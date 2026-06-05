from __future__ import annotations

import pytest

from civiczone.data_import import import_local_dataset
from civiczone.parcel_lookup import ParcelLookupRepository, ParcelLookupResult
from civiczone.rule_lookup import DimensionalRuleResult, RuleLookupRepository, UseRuleResult


def test_local_dataset_import_loads_parcels_and_rules_without_samples(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'municipal.db'}"
    parcels_csv = tmp_path / "parcels.csv"
    use_rules_csv = tmp_path / "use-rules.csv"
    dimensional_rules_csv = tmp_path / "dimensional-rules.csv"
    parcels_csv.write_text(
        "\n".join(
            [
                "parcel_number,address,zone_code,zone_name,overlays,constraints,source,disclaimer",
                (
                    "200-300-400,45 Oak Ave,R-3,Neighborhood Residential,"
                    "Floodplain;Design Review,Planner review for floodplain work,"
                    "City zoning export 2026-06-01,Informational only; not a zoning determination."
                ),
            ]
        ),
        encoding="utf-8",
    )
    use_rules_csv.write_text(
        "\n".join(
            [
                "zone_code,use,status,review_path,citation,disclaimer",
                (
                    "R-3,duplex,allowed,Confirm overlays before permitting,"
                    "CMC 18.22.020,Informational only; not a zoning determination."
                ),
            ]
        ),
        encoding="utf-8",
    )
    dimensional_rules_csv.write_text(
        "\n".join(
            [
                "zone_code,rule_type,value,citation,disclaimer",
                (
                    "R-3,height,32 feet maximum,CMC 18.22.050(B),"
                    "Informational only; not a zoning determination."
                ),
            ]
        ),
        encoding="utf-8",
    )

    summary = import_local_dataset(
        db_url=db_url,
        parcels_csv=parcels_csv,
        use_rules_csv=use_rules_csv,
        dimensional_rules_csv=dimensional_rules_csv,
    )
    parcels = ParcelLookupRepository(db_url=db_url, seed_defaults=False)
    rules = RuleLookupRepository(db_url=db_url, seed_defaults=False)

    parcel = parcels.lookup(address="45 oak ave")
    use_rule = rules.lookup_use_rule(zone_code="r-3", use="Duplex")
    dimensional = rules.lookup_dimensional_rule(zone_code="R-3", rule_type="HEIGHT")

    assert summary.parcels == 1
    assert summary.use_rules == 1
    assert summary.dimensional_rules == 1
    assert isinstance(parcel, ParcelLookupResult)
    assert parcel.parcel_number == "200-300-400"
    assert parcel.overlays == ("Floodplain", "Design Review")
    assert isinstance(use_rule, UseRuleResult)
    assert use_rule.status == "allowed"
    assert isinstance(dimensional, DimensionalRuleResult)
    assert dimensional.value == "32 feet maximum"
    assert not isinstance(parcels.lookup(parcel_number="100-200-300"), ParcelLookupResult)


def test_local_dataset_import_validates_all_csvs_before_writing(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'invalid.db'}"
    parcels_csv = tmp_path / "parcels.csv"
    use_rules_csv = tmp_path / "use-rules.csv"
    parcels_csv.write_text(
        "\n".join(
            [
                "parcel_number,address,zone_code,zone_name,overlays,constraints,source,disclaimer",
                (
                    "200-300-400,45 Oak Ave,R-3,Neighborhood Residential,"
                    ",,City zoning export,Informational only."
                ),
            ]
        ),
        encoding="utf-8",
    )
    use_rules_csv.write_text(
        "\n".join(
            [
                "zone_code,use,status,review_path,citation",
                "R-3,duplex,allowed,Confirm overlays before permitting,CMC 18.22.020",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required columns: disclaimer"):
        import_local_dataset(db_url=db_url, parcels_csv=parcels_csv, use_rules_csv=use_rules_csv)

    parcels = ParcelLookupRepository(db_url=db_url, seed_defaults=False)
    assert not isinstance(parcels.lookup(parcel_number="200-300-400"), ParcelLookupResult)


def test_local_dataset_import_requires_at_least_one_csv(tmp_path) -> None:
    with pytest.raises(ValueError, match="at least one CSV"):
        import_local_dataset(db_url=f"sqlite:///{tmp_path / 'empty.db'}")
