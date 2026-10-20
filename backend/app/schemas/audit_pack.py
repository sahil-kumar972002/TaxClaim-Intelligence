from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class AuditPackGenerateRequest(BaseModel):
    tax_year: str = "2024-2025"
    include_receipt_images: bool = True
    include_risk_appendix: bool = True
    assumptions_note: Optional[str] = "All expenses incurred exclusively for professional consulting and software development."

class AuditPackResponse(BaseModel):
    id: str
    package_reference: str
    tax_year: str
    total_expenses_evaluated: int
    total_claimed_deductions: float
    average_evidence_strength: float
    pdf_file_path: str
    package_sha256: str
    generated_at: datetime
    summary_stats: Dict[str, Any] = {}

    class Config:
        from_attributes = True

class AuditTimelineEvent(BaseModel):
    timestamp: datetime
    phase: str
    title: str
    detail: str
    status: str
