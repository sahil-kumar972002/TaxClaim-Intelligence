from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TaxRuleBase(BaseModel):
    rule_code: str
    country: str
    jurisdiction: str
    tax_year: str
    taxpayer_type: str
    profession: str
    expense_category: str
    title: str
    description: str
    deductibility_status: str
    eligibility_conditions: List[str]
    limitations: Dict[str, Any]
    evidence_requirements: List[str]
    effective_date: str
    source_statute: str
    statute_citation_url: Optional[str] = None
    rule_version: str
    last_verified_date: str

class TaxRuleResponse(TaxRuleBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class TaxRuleFilter(BaseModel):
    country: Optional[str] = None
    jurisdiction: Optional[str] = None
    tax_year: Optional[str] = None
    profession: Optional[str] = None
    expense_category: Optional[str] = None
