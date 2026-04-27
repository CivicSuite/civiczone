"""FastAPI runtime foundation for CivicZone."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI

from civiczone import __version__


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
        "status": "schema foundation",
        "message": (
            "CivicZone package, API foundation, canonical schema, and Alembic migrations are online; parcel lookup, GIS ingestion, "
            "zoning answers, and planner review workflows are not implemented yet."
        ),
        "next_step": "Milestone 3: parcel and zone lookup",
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
