from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class EvidenceItemResponse(BaseModel):
    id: str
    expense_id: str
    evidence_type: str
    file_path: Optional[str] = None
    sha256_hash: Optional[str] = None
    verification_status: str
    metadata_json: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceStrengthFactor(BaseModel):
    name: str
    weight: float
    satisfied: bool
    description: str

class EvidenceScoreBreakdown(BaseModel):
    overall_score: float
    status: str  # STRONG, MODERATE, WEAK
    factors: List[EvidenceStrengthFactor]
    missing_items: List[str]
    audit_risk_level: str
