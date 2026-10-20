import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.document import Document, OCRResult
from app.models.expense import Expense
from app.models.business_profile import BusinessProfile
from app.schemas.document import DocumentResponse, OCRCorrectionRequest
from app.services.ocr_engine import ocr_service
from app.services.expense_service import expense_service
from app.core.audit_logger import log_audit_event

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    sample_preset: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Get active user & profile
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No active user found in database.")
    profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == user.id).first()

    # 1. Save file and compute SHA-256
    stored_fn, file_path, sha256_hash, file_size = await ocr_service.save_and_hash_upload(file, user.id)

    # 2. Persist Document record
    doc = Document(
        id=str(uuid.uuid4()),
        user_id=user.id,
        original_filename=file.filename,
        stored_filename=stored_fn,
        file_path=file_path,
        file_hash_sha256=sha256_hash,
        mime_type=file.content_type or "application/pdf",
        file_size_bytes=file_size,
        upload_source="WEB_DROPZONE"
    )
    db.add(doc)
    db.flush()

    # 3. OCR & Entity Extraction
    ocr_data = ocr_service.extract_text_and_entities(file_path, file.filename, sample_text=sample_preset)
    
    ocr_result = OCRResult(
        id=str(uuid.uuid4()),
        document_id=doc.id,
        raw_text=ocr_data["raw_text"],
        extracted_merchant=ocr_data["extracted_merchant"],
        extracted_date=ocr_data["extracted_date"],
        extracted_amount=ocr_data["extracted_amount"],
        extracted_currency=ocr_data["extracted_currency"],
        extracted_tax_amount=ocr_data["extracted_tax_amount"],
        extracted_invoice_number=ocr_data["extracted_invoice_number"],
        line_items_json=ocr_data["line_items"],
        ocr_confidence=ocr_data["ocr_confidence"]
    )
    db.add(ocr_result)
    db.flush()

    # 4. Automatically create Expense and evaluate Tax Intelligence
    expense = Expense(
        id=str(uuid.uuid4()),
        user_id=user.id,
        document_id=doc.id,
        merchant=ocr_data["extracted_merchant"] or "Unknown Merchant",
        transaction_date=ocr_data["extracted_date"],
        amount=ocr_data["extracted_amount"] or 1000.0,
        currency=ocr_data["extracted_currency"] or "INR",
        tax_amount=ocr_data["extracted_tax_amount"] or 0.0,
        invoice_number=ocr_data["extracted_invoice_number"],
        category="other",  # Will be classified by ML in expense_service
        payment_method="Credit Card",
        business_purpose=f"Expense associated with {ocr_data['extracted_merchant']}",
        business_use_percentage=1.0
    )
    db.add(expense)
    db.flush()

    # Run AI Tax pipeline
    expense_service.process_and_evaluate_expense(
        db=db,
        expense=expense,
        document=doc,
        profile=profile
    )

    log_audit_event(db, user.id, "UPLOAD_DOCUMENT", "Document", doc.id, {"hash": sha256_hash})
    db.refresh(doc)
    return doc

@router.get("/", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()

@router.patch("/{document_id}/correct")
def correct_ocr_fields(
    document_id: str,
    correction: OCRCorrectionRequest,
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Update corresponding Expense
    expense = db.query(Expense).filter(Expense.document_id == document_id).first()
    if expense:
        expense.merchant = correction.merchant
        expense.transaction_date = correction.transaction_date
        expense.amount = correction.amount
        expense.currency = correction.currency
        if correction.tax_amount is not None:
            expense.tax_amount = correction.tax_amount
        if correction.invoice_number is not None:
            expense.invoice_number = correction.invoice_number
        if correction.category:
            expense.category = correction.category
        if correction.business_purpose:
            expense.business_purpose = correction.business_purpose
        if correction.business_use_percentage is not None:
            expense.business_use_percentage = correction.business_use_percentage

        # Re-run Tax Intelligence Pipeline
        profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == expense.user_id).first()
        expense_service.process_and_evaluate_expense(
            db=db,
            expense=expense,
            document=doc,
            profile=profile
        )

    log_audit_event(db, doc.user_id, "CORRECT_OCR_FIELDS", "Document", doc.id, correction.model_dump())
    return {"message": "OCR fields successfully updated and tax decision re-evaluated."}
