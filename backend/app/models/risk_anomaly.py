import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class RiskFlag(Base):
    __tablename__ = "risk_flags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    risk_type = Column(String(100), nullable=False)   # e.g. PERSONAL_EXPENSE_RISK, CASH_LIMIT_EXCEEDED, AUDIT_TARGET_CATEGORY
    severity = Column(String(20), default="MEDIUM")   # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text, nullable=False)
    triggered_rule = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    expense = relationship("Expense", back_populates="risk_flags")

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Types: DUPLICATE_INVOICE, DUPLICATE_RECEIPT, AMOUNT_SPIKE, UNUSUAL_MERCHANT, DATE_CONFLICT, CATEGORY_MISMATCH
    anomaly_type = Column(String(100), nullable=False, index=True)
    anomaly_score = Column(Float, default=0.75)  # Outlier score (0.0 to 1.0)
    explanation = Column(Text, nullable=False)   # e.g. "Transaction is 4.7x normal average for category 'meals'"
    detected_by = Column(String(100), default="IsolationForest+Deduplicator")
    details_json = Column(JSON, default=dict)
    resolved = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    expense = relationship("Expense", back_populates="anomalies")
