from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class RiskFlagResponse(BaseModel):
    id: str
    expense_id: str
    risk_type: str
    severity: str
    description: str
    triggered_rule: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class AnomalyResponse(BaseModel):
    id: str
    expense_id: str
    anomaly_type: str
    anomaly_score: float
    explanation: str
    detected_by: str
    details_json: Dict[str, Any] = {}
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RiskSummary(BaseModel):
    total_anomalies: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    portfolio_risk_level: str  # LOW, MODERATE, ELEVATED, CRITICAL
    recent_anomalies: List[AnomalyResponse]
