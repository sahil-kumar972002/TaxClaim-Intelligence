import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    profession = Column(String(100), nullable=False)  # Software Developer, Graphic Designer, Content Creator, Gig Driver, etc.
    business_type = Column(String(100), default="Freelance/Self-Employed")
    country = Column(String(50), default="India")     # India, United States, etc.
    jurisdiction = Column(String(100), default="Income Tax Department (CBDT)")
    tax_year = Column(String(20), default="2024-2025")
    tax_regime = Column(String(50), default="Sec 44ADA (Presumptive)")  # Sec 44ADA, Regular PGBP, US Schedule C
    
    business_use_patterns = Column(JSON, default=dict)   # {"laptop": 0.90, "internet": 0.75, "phone": 0.60}
    recurring_expenses = Column(JSON, default=list)       # ["Adobe Cloud", "Github", "AWS", "Jio Fiber"]
    business_description = Column(Text, nullable=True)
    estimated_annual_income = Column(Float, default=1500000.0)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    user = relationship("User", back_populates="profile")
