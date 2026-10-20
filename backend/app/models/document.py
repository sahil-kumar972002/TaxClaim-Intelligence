import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_hash_sha256 = Column(String(64), nullable=False, index=True)
    mime_type = Column(String(100), default="application/pdf")
    file_size_bytes = Column(Integer, default=0)
    encryption_status = Column(String(50), default="AES-256-GCM")
    upload_source = Column(String(50), default="WEB_DROPZONE")  # WEB_DROPZONE, CAMERA, EMAIL, MANUAL
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="documents")
    ocr_result = relationship("OCRResult", back_populates="document", uselist=False, cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="document")

class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    raw_text = Column(Text, nullable=True)
    extracted_merchant = Column(String(255), nullable=True)
    extracted_date = Column(String(50), nullable=True)
    extracted_amount = Column(Float, nullable=True)
    extracted_currency = Column(String(10), default="INR")
    extracted_tax_amount = Column(Float, nullable=True)
    extracted_invoice_number = Column(String(100), nullable=True)
    line_items_json = Column(JSON, default=list)
    ocr_confidence = Column(Float, default=0.90)
    parser_version = Column(String(50), default="TaxClaim-HybridOCR-v2.1")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    document = relationship("Document", back_populates="ocr_result")
