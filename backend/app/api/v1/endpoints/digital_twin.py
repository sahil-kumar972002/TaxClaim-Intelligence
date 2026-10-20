from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.digital_twin import DigitalTwinSummary
from app.services.digital_twin_service import digital_twin_service

router = APIRouter()

@router.get("/summary", response_model=DigitalTwinSummary)
def get_digital_twin_summary(db: Session = Depends(get_db)):
    """
    Returns the dynamic continuous financial profile, audit readiness radar,
    monthly trends, and proactive AI tax advice.
    """
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not initialized")
    return digital_twin_service.get_user_digital_twin(db, user.id)
