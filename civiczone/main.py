"""FastAPI runtime foundation for CivicZone."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from civiczone import __version__
from civiczone.parcel_lookup import ParcelLookupError, lookup_parcel


app = FastAPI(
    title="CivicZone",
    version=__version__,
    description="Parcel-aware zoning and land-use Q&A foundation for CivicSuite.",
)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicZone",
        "version": __version__,
        "status": "parcel lookup foundation",
        "message": (
            "CivicZone package, API foundation, canonical schema, Alembic migrations, and "
            "sample parcel lookup are online; live GIS ingestion, zoning answers, and "
            "planner review workflows are not implemented yet."
        ),
        "next_step": "Milestone 4: use and dimensional rules",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civiczone",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


class ParcelLookupRequest(BaseModel):
    parcel_number: str | None = Field(default=None)
    address: str | None = Field(default=None)


@app.post("/api/v1/civiczone/parcels/lookup")
def parcel_lookup(request: ParcelLookupRequest) -> dict[str, object]:
    if not request.parcel_number and not request.address:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Provide either parcel_number or address.",
                "fix": "Send parcel_number '100-200-300' or address '123 Main St' in this development build.",
            },
        )

    result = lookup_parcel(parcel_number=request.parcel_number, address=request.address)
    if isinstance(result, ParcelLookupError):
        raise HTTPException(status_code=404, detail={"message": result.message, "fix": result.fix})

    return {
        "parcel_number": result.parcel_number,
        "address": result.address,
        "zone": {"code": result.zone_code, "name": result.zone_name},
        "overlays": list(result.overlays),
        "constraints": list(result.constraints),
        "source": result.source,
        "disclaimer": result.disclaimer,
    }
