import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), unique=True, nullable=False)
    tax_rule_id = Column(String(36), ForeignKey("tax_rules.id", ondelete="SET NULL"), nullable=True)
    
    potential_treatment = Column(String(255), nullable=False)  # "Potentially 100% Business Deductible under Sec 37(1)"
    ai_confidence = Column(Float, nullable=False, default=0.85)  # 0.0 to 1.0
    evidence_strength_score = Column(Float, nullable=False, default=0.70)  # 0.0 to 1.0
    
    # State: AUTO, REVIEW, INSUFFICIENT_DATA
    decision_status = Column(String(50), default="REVIEW", index=True)
    
    reasoning_summary = Column(JSON, default=list)  # ["Merchant verified", "Recurring software", "Matches profession"]
    limitations_applied = Column(Text, nullable=True)
    missing_evidence = Column(JSON, default=list)   # [{"item": "Business purpose", "prompt": "What project was this used for?"}]
    
    human_review_required = Column(Boolean, default=False)
    confirmed_by_user = Column(Boolean, default=False)
    confirmed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    expense = relationship("Expense", back_populates="decision")
    tax_rule = relationship("TaxRule", back_populates="decisions")
