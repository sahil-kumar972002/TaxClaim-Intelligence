from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class BusinessProfileBase(BaseModel):
    profession: str
    business_type: str = "Freelance/Self-Employed"
    country: str = "India"
    jurisdiction: str = "Income Tax Department (CBDT)"
    tax_year: str = "2024-2025"
    tax_regime: str = "Sec 44ADA (Presumptive)"
    business_use_patterns: Dict[str, float] = {
        "laptop": 0.90,
        "internet": 0.75,
        "phone": 0.60,
        "meals": 0.50,
        "vehicle": 0.40
    }
    recurring_expenses: List[str] = [
        "Adobe Creative Cloud",
        "GitHub",
        "AWS Cloud",
        "Jio Fiber Broadband"
    ]
    business_description: Optional[str] = "Independent software engineer and cloud consultant specializing in distributed systems and AI applications."
    estimated_annual_income: float = 1500000.0

class BusinessProfileCreate(BusinessProfileBase):
    pass

class BusinessProfileUpdate(BaseModel):
    profession: Optional[str] = None
    business_type: Optional[str] = None
    country: Optional[str] = None
    jurisdiction: Optional[str] = None
    tax_year: Optional[str] = None
    tax_regime: Optional[str] = None
    business_use_patterns: Optional[Dict[str, float]] = None
    recurring_expenses: Optional[List[str]] = None
    business_description: Optional[str] = None
    estimated_annual_income: Optional[float] = None

class BusinessProfileResponse(BusinessProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
