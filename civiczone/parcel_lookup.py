from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParcelLookupResult:
    parcel_number: str
    address: str
    zone_code: str
    zone_name: str
    overlays: tuple[str, ...]
    constraints: tuple[str, ...]
    source: str
    disclaimer: str


@dataclass(frozen=True)
class ParcelLookupError:
    message: str
    fix: str


SAMPLE_PARCELS: dict[str, ParcelLookupResult] = {
    "100-200-300": ParcelLookupResult(
        parcel_number="100-200-300",
        address="123 Main St",
        zone_code="R-2",
        zone_name="Medium Density Residential",
        overlays=("Historic District",),
        constraints=("Planner review required for exterior changes in the historic overlay.",),
        source="Sample fixture: city zoning map extract 2026-04-27",
        disclaimer="Informational only; this is not a zoning determination.",
    )
}

ADDRESS_INDEX = {value.address.casefold(): key for key, value in SAMPLE_PARCELS.items()}


def lookup_parcel(*, parcel_number: str | None = None, address: str | None = None) -> ParcelLookupResult | ParcelLookupError:
    """Return a sample parcel lookup without claiming live GIS integration."""

    if parcel_number:
        key = parcel_number.strip()
        if key in SAMPLE_PARCELS:
            return SAMPLE_PARCELS[key]

    if address:
        key = ADDRESS_INDEX.get(address.strip().casefold())
        if key:
            return SAMPLE_PARCELS[key]

    return ParcelLookupError(
        message="Parcel not found in the CivicZone sample dataset.",
        fix=(
            "Use parcel_number '100-200-300' or address '123 Main St' in this "
            "development build; live GIS import is planned for a later milestone."
        ),
    )
