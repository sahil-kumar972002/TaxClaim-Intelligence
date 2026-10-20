import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Text
from app.core.database import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True, index=True)
    
    action = Column(String(100), nullable=False, index=True)  # UPLOAD_DOC, OCR_RUN, RULE_EVAL, USER_CONFIRM, EXPORT_PACK
    resource_type = Column(String(50), nullable=False)        # Document, Expense, Decision, AuditPackage
    resource_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    user_agent = Column(String(255), default="TaxClaim-Client")
    diff_payload = Column(JSON, default=dict)
    
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
