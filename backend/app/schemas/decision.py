from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.tax_rule import TaxRuleResponse

class DecisionResponse(BaseModel):
    id: str
    expense_id: str
    tax_rule_id: Optional[str]
    potential_treatment: str
    ai_confidence: float
    evidence_strength_score: float
    decision_status: str
    reasoning_summary: List[str]
    limitations_applied: Optional[str]
    missing_evidence: List[Dict[str, Any]]
    human_review_required: bool
    confirmed_by_user: bool
    confirmed_at: Optional[datetime]
    created_at: datetime
    tax_rule: Optional[TaxRuleResponse] = None

    class Config:
        from_attributes = True

class WhyDecisionResponse(BaseModel):
    expense_id: str
    merchant: str
    amount: float
    category: str
    decision: DecisionResponse
    statutory_rule: Optional[TaxRuleResponse]
    evidence_trail: List[Dict[str, Any]]
    verification_steps: List[str]
    audit_trail_timestamp: datetime
