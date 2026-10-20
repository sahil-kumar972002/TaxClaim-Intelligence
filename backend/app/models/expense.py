import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    merchant = Column(String(255), nullable=False, index=True)
    transaction_date = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    tax_amount = Column(Float, default=0.0)
    invoice_number = Column(String(100), nullable=True, index=True)
    
    # Categories: software, hardware, office, travel, internet, professional services,
    # education, marketing, advertising, communication, subscriptions, equipment, utilities, meals, transportation, other
    category = Column(String(100), nullable=False, index=True)
    payment_method = Column(String(50), default="Credit Card")  # Credit Card, Bank Transfer, UPI, Debit Card, Cash
    business_purpose = Column(Text, nullable=True)
    business_use_percentage = Column(Float, default=1.0)  # 0.0 to 1.0 (e.g. 0.8 = 80%)
    eligible_deductible_amount = Column(Float, default=0.0)
    
    # Status: AUTO_RECOMMENDED, NEEDS_REVIEW, INSUFFICIENT_DATA, CONFIRMED, REJECTED
    status = Column(String(50), default="NEEDS_REVIEW", index=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="expenses")
    document = relationship("Document", back_populates="expenses")
    line_items = relationship("ExpenseLineItem", back_populates="expense", cascade="all, delete-orphan")
    decision = relationship("Decision", back_populates="expense", uselist=False, cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="expense", cascade="all, delete-orphan")
    risk_flags = relationship("RiskFlag", back_populates="expense", cascade="all, delete-orphan")
    anomalies = relationship("Anomaly", back_populates="expense", cascade="all, delete-orphan")

class ExpenseLineItem(Base):
    __tablename__ = "expense_line_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    description = Column(String(255), nullable=False)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)
    category_tag = Column(String(100), nullable=True)

    # Relationship
    expense = relationship("Expense", back_populates="line_items")
