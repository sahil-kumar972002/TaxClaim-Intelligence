import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class TaxRule(Base):
    __tablename__ = "tax_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_code = Column(String(50), unique=True, index=True, nullable=False)  # e.g. IN-SEC37-SOFT-01
    
    country = Column(String(50), nullable=False, index=True)          # India, United States
    jurisdiction = Column(String(100), nullable=False, index=True)    # CBDT, IRS Federal, etc.
    tax_year = Column(String(20), nullable=False, index=True)         # 2024-2025, 2024
    taxpayer_type = Column(String(100), default="Freelancer")         # Freelancer, Gig Worker, Sole Proprietor
    profession = Column(String(100), default="All", index=True)       # Software Developer, Graphic Designer, All
    expense_category = Column(String(100), nullable=False, index=True)# software, internet, meals, hardware
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    deductibility_status = Column(String(50), default="DEDUCTIBLE")   # DEDUCTIBLE, PARTIALLY_DEDUCTIBLE, CAPITAL_DEPRECIATION, NON_DEDUCTIBLE
    
    eligibility_conditions = Column(JSON, default=list)    # ["Incurred wholly and exclusively for business", "Valid payment trail"]
    limitations = Column(JSON, default=dict)               # {"cash_limit": 10000, "depreciation_rate": 0.40, "personal_use_exclusion": True}
    evidence_requirements = Column(JSON, default=list)     # ["Tax Invoice with GST/TIN", "Bank payment debit", "Project purpose note"]
    
    effective_date = Column(String(50), default="2024-04-01")
    source_statute = Column(String(255), nullable=False)   # e.g. "Income Tax Act 1961 Section 37(1)"
    statute_citation_url = Column(String(500), nullable=True)
    rule_version = Column(String(20), default="v2024.1")
    last_verified_date = Column(String(50), default="2025-01-15")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    versions = relationship("TaxRuleVersion", back_populates="rule", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="tax_rule")

class TaxRuleVersion(Base):
    __tablename__ = "tax_rule_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = Column(String(36), ForeignKey("tax_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    version_num = Column(String(20), nullable=False)
    changed_by = Column(String(100), default="CBDT_Regulatory_Sync")
    diff_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    rule = relationship("TaxRule", back_populates="versions")
