import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Types: RECEIPT, INVOICE, PAYMENT_PROOF, BUSINESS_PURPOSE, ATTENDEE_LOG, LOGBOOK
    evidence_type = Column(String(50), nullable=False, index=True)
    file_path = Column(String(500), nullable=True)
    sha256_hash = Column(String(64), nullable=True, index=True)
    verification_status = Column(String(50), default="VERIFIED")  # VERIFIED, PENDING_REVIEW, INCOMPLETE
    metadata_json = Column(JSON, default=dict)  # {"bank_ref": "UPI/482910...", "attendees": 2, "odometer": 42}
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    expense = relationship("Expense", back_populates="evidence_items")

class EvidenceLink(Base):
    __tablename__ = "evidence_links"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    rule_id = Column(String(36), ForeignKey("tax_rules.id", ondelete="CASCADE"), nullable=False)
    evidence_id = Column(String(36), ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False)
    relationship_role = Column(String(100), default="STATUTORY_SATISFACTION")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
