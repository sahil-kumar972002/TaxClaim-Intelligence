from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.expense import Expense
from app.models.business_profile import BusinessProfile
from app.schemas.simulator import SimulatorRequest, SimulatorResponse
from app.services.simulator_service import simulator_service

router = APIRouter()

@router.post("/evaluate", response_model=SimulatorResponse)
def evaluate_simulator(request_in: SimulatorRequest, db: Session = Depends(get_db)):
    """
    Evaluates dynamic What-If Tax Impact.
    Allows sliding business-use multiplier, gross receipts, and actual expenses
    to compare Section 44ADA vs Regular PGBP.
    """
    return simulator_service.simulate(
        gross_receipts=request_in.annual_gross_receipts,
        actual_expenses=request_in.total_business_expenses,
        business_use_multiplier=request_in.business_use_multiplier
    )

@router.get("/defaults", response_model=SimulatorResponse)
def get_simulator_defaults(db: Session = Depends(get_db)):
    """Pre-fills the simulator with the taxpayer's real aggregated numbers."""
    profile = db.query(BusinessProfile).first()
    expenses = db.query(Expense).all()
    
    income = profile.estimated_annual_income if profile else 2000000.0
    total_expenses = sum(e.amount for e in expenses) or 450000.0

    return simulator_service.simulate(
        gross_receipts=income,
        actual_expenses=total_expenses,
        business_use_multiplier=1.0
    )
