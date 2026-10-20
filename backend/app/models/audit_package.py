import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class AuditPackage(Base):
    __tablename__ = "audit_packages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    tax_year = Column(String(20), nullable=False)
    package_reference = Column(String(100), unique=True, nullable=False, index=True)  # e.g. "TC-AUDIT-2024-8F92"
    
    total_expenses_evaluated = Column(Integer, default=0)
    total_claimed_deductions = Column(Float, default=0.0)
    average_evidence_strength = Column(Float, default=0.0)
    
    pdf_file_path = Column(String(500), nullable=False)
    package_sha256 = Column(String(64), nullable=False, index=True)  # Tamper-proof cryptographic checksum
    summary_stats_json = Column(JSON, default=dict)
    
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    user = relationship("User", back_populates="audit_packages")
