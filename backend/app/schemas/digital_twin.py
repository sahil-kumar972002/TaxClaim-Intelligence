from pydantic import BaseModel
from typing import List, Dict, Any

class DigitalTwinSummary(BaseModel):
    user_id: str
    profession: str
    tax_year: str
    current_regime: str
    
    # Financial metrics
    total_income_tracked: float
    total_expenses_recorded: float
    total_potentially_deductible: float
    estimated_tax_savings: float
    
    # Evidence & Quality
    average_evidence_strength: float
    audit_readiness_score: float  # 0 to 100
    
    # Counts
    total_receipts_ingested: int
    auto_recommended_count: int
    needs_review_count: int
    insufficient_data_count: int
    flagged_anomalies_count: int
    
    # Dynamic breakdowns
    category_totals: Dict[str, float]
    monthly_trend: List[Dict[str, Any]]
    radar_metrics: List[Dict[str, Any]]
    proactive_insights: List[Dict[str, Any]]
