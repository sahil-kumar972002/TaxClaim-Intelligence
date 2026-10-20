from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class OCRResultResponse(BaseModel):
    id: str
    extracted_merchant: Optional[str]
    extracted_date: Optional[str]
    extracted_amount: Optional[float]
    extracted_currency: Optional[str]
    extracted_tax_amount: Optional[float]
    extracted_invoice_number: Optional[str]
    line_items_json: List[Dict[str, Any]] = []
    ocr_confidence: float
    parser_version: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    user_id: str
    original_filename: str
    stored_filename: str
    file_path: str
    file_hash_sha256: str
    mime_type: str
    file_size_bytes: int
    encryption_status: str
    upload_source: str
    created_at: datetime
    ocr_result: Optional[OCRResultResponse] = None

    class Config:
        from_attributes = True

class OCRCorrectionRequest(BaseModel):
    merchant: str
    transaction_date: str
    amount: float
    currency: str = "INR"
    tax_amount: Optional[float] = 0.0
    invoice_number: Optional[str] = None
    category: Optional[str] = None
    business_purpose: Optional[str] = None
    business_use_percentage: Optional[float] = 1.0
