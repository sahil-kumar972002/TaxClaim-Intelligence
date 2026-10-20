from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.business_profile import BusinessProfile
from app.schemas.business_profile import BusinessProfileResponse, BusinessProfileUpdate
from app.core.audit_logger import log_audit_event

router = APIRouter()

@router.get("/me", response_model=BusinessProfileResponse)
def get_my_profile(db: Session = Depends(get_db)):
    # Default to first user profile for instant zero-friction demo access
    profile = db.query(BusinessProfile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please run seed script.")
    return profile

@router.put("/me", response_model=BusinessProfileResponse)
def update_my_profile(update_data: BusinessProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(BusinessProfile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for field, val in update_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, val)

    db.commit()
    db.refresh(profile)
    log_audit_event(db, profile.user_id, "UPDATE_BUSINESS_PROFILE", "BusinessProfile", profile.id)
    return profile
