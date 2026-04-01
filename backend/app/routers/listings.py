from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.canonical_listing import CanonicalListing
from app.schemas.canonical_listing import CanonicalListingOut

router = APIRouter(prefix="/api/listings", tags=["listings"])


@router.get("/", response_model=list[CanonicalListingOut])
def get_listings(
    city: str | None = Query(default=None),
    country: str | None = Query(default=None),
    max_rent: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(CanonicalListing).filter(CanonicalListing.is_active == True)

    if city:
        query = query.filter(CanonicalListing.city.ilike(f"%{city}%"))

    if country:
        query = query.filter(CanonicalListing.country.ilike(f"%{country}%"))

    if max_rent is not None:
        query = query.filter(CanonicalListing.monthly_rent <= max_rent)

    return query.order_by(CanonicalListing.monthly_rent.asc()).all()