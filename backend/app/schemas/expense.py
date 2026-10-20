from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.decision import DecisionResponse
from app.schemas.anomaly import RiskFlagResponse, AnomalyResponse

class ExpenseLineItemBase(BaseModel):
    description: str
    quantity: float = 1.0
    unit_price: float = 0.0
    total_price: float = 0.0
    category_tag: Optional[str] = None

class ExpenseLineItemResponse(ExpenseLineItemBase):
    id: str
    expense_id: str

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    merchant: str
    transaction_date: str
    amount: float
    currency: str = "INR"
    tax_amount: float = 0.0
    invoice_number: Optional[str] = None
    category: str
    payment_method: str = "Credit Card"
    business_purpose: Optional[str] = None
    business_use_percentage: float = 1.0

class ExpenseCreate(ExpenseBase):
    document_id: Optional[str] = None
    line_items: Optional[List[ExpenseLineItemBase]] = []

class ExpenseUpdate(BaseModel):
    merchant: Optional[str] = None
    transaction_date: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    invoice_number: Optional[str] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    business_purpose: Optional[str] = None
    business_use_percentage: Optional[float] = None
    status: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    id: str
    user_id: str
    document_id: Optional[str] = None
    eligible_deductible_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    line_items: List[ExpenseLineItemResponse] = []
    decision: Optional[DecisionResponse] = None
    risk_flags: List[RiskFlagResponse] = []
    anomalies: List[AnomalyResponse] = []

    class Config:
        from_attributes = True

class MissingEvidencePatchRequest(BaseModel):
    business_purpose: Optional[str] = None
    business_use_percentage: Optional[float] = None
    payment_proof_reference: Optional[str] = None
    client_or_project_name: Optional[str] = None
