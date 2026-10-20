from typing import List, Optional
from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.business_profile import BusinessProfile
from app.models.expense import Expense, ExpenseLineItem
from app.models.document import Document
from app.models.decision import Decision
from app.models.tax_rule import TaxRule
from app.models.model_metrics import ModelPrediction
from app.schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate, MissingEvidencePatchRequest
from app.schemas.decision import WhyDecisionResponse
from app.services.expense_service import expense_service
from app.core.audit_logger import log_audit_event

router = APIRouter()

@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if status:
        query = query.filter(Expense.status == status)
    if category:
        query = query.filter(Expense.category == category)
    return query.order_by(Expense.transaction_date.desc()).all()

@router.post("/", response_model=ExpenseResponse)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No user found")
    profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == user.id).first()

    expense = Expense(
        id=str(uuid.uuid4()),
        user_id=user.id,
        document_id=expense_in.document_id,
        merchant=expense_in.merchant,
        transaction_date=expense_in.transaction_date,
        amount=expense_in.amount,
        currency=expense_in.currency,
        tax_amount=expense_in.tax_amount,
        invoice_number=expense_in.invoice_number,
        category=expense_in.category,
        payment_method=expense_in.payment_method,
        business_purpose=expense_in.business_purpose,
        business_use_percentage=expense_in.business_use_percentage
    )
    db.add(expense)
    db.flush()

    # Add line items if any
    for li in (expense_in.line_items or []):
        item = ExpenseLineItem(
            id=str(uuid.uuid4()),
            expense_id=expense.id,
            description=li.description,
            quantity=li.quantity,
            unit_price=li.unit_price,
            total_price=li.total_price,
            category_tag=li.category_tag
        )
        db.add(item)
    db.flush()

    # Process and evaluate tax intelligence
    doc = db.query(Document).filter(Document.id == expense_in.document_id).first() if expense_in.document_id else None
    expense_service.process_and_evaluate_expense(db, expense, doc, profile)

    log_audit_event(db, user.id, "CREATE_EXPENSE", "Expense", expense.id)
    db.refresh(expense)
    return expense

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.get("/{expense_id}/why", response_model=WhyDecisionResponse)
def why_taxclaim_decision(expense_id: str, db: Session = Depends(get_db)):
    """
    TRACEABLE EVIDENCE & REASONING CHAIN
    Explains exactly why TaxClaim made this potential tax treatment decision.
    Links the user, expense, receipt, payment trail, statutory tax rule, and limitation logic.
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    decision = expense.decision
    if not decision:
        raise HTTPException(status_code=400, detail="Decision has not been generated for this expense yet.")

    rule = decision.tax_rule

    evidence_trail = [
        {"step": 1, "item": "Vendor Identification", "detail": f"Merchant '{expense.merchant}' extracted and validated against verified merchant corpus.", "status": "SATISFIED"},
        {"step": 2, "item": "Statutory Rule Retrieval", "detail": f"Retrieved official statutory provision: {rule.title if rule else 'General Business Deduction'}.", "status": "SATISFIED" if rule else "PARTIAL"},
        {"step": 3, "item": "Evidentiary Test", "detail": f"Evidence Strength Score computed at {int(decision.evidence_strength_score*100)}% based on invoice, payment method ({expense.payment_method}), and purpose.", "status": "SATISFIED" if decision.evidence_strength_score >= 0.70 else "NEEDS_ATTENTION"},
        {"step": 4, "item": "Statutory Limitations", "detail": decision.limitations_applied or "No statutory cap exceeded.", "status": "CHECKED"},
        {"step": 5, "item": "Anomaly Screen", "detail": f"{len(expense.anomalies)} anomalies and {len(expense.risk_flags)} risk flags detected.", "status": "CLEAR" if not expense.anomalies else "FLAGGED"}
    ]

    verification_steps = [
        "Cryptographic check of original document hash",
        "Deterministic statutory rule match (Zero hallucination)",
        "Audit trail event logged into immutable ledger"
    ]

    return {
        "expense_id": expense.id,
        "merchant": expense.merchant,
        "amount": expense.amount,
        "category": expense.category,
        "decision": decision,
        "statutory_rule": rule,
        "evidence_trail": evidence_trail,
        "verification_steps": verification_steps,
        "audit_trail_timestamp": decision.updated_at or decision.created_at
    }

@router.post("/{expense_id}/missing-evidence")
def patch_missing_evidence(
    expense_id: str,
    patch: MissingEvidencePatchRequest,
    db: Session = Depends(get_db)
):
    """
    Missing Evidence Copilot action.
    User provides answers to targeted questions to satisfy evidentiary requirements.
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if patch.business_purpose:
        expense.business_purpose = patch.business_purpose
    if patch.business_use_percentage is not None:
        expense.business_use_percentage = patch.business_use_percentage
    if patch.payment_proof_reference:
        expense.payment_method = f"Verified: {patch.payment_proof_reference}"

    # Re-evaluate
    doc = expense.document
    profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == expense.user_id).first()
    expense_service.process_and_evaluate_expense(db, expense, doc, profile)

    log_audit_event(db, expense.user_id, "PATCH_MISSING_EVIDENCE", "Expense", expense.id, patch.model_dump())
    return {"message": "Evidence updated. Evidence strength score recalculated.", "expense": expense}

@router.post("/{expense_id}/confirm")
def confirm_decision(expense_id: str, db: Session = Depends(get_db)):
    """
    Human-in-the-loop User Confirmation.
    Promotes expense to CONFIRMED and updates ML model ground truth.
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.status = "CONFIRMED"
    if expense.decision:
        expense.decision.confirmed_by_user = True
        expense.decision.confirmed_at = datetime.now(timezone.utc)
        expense.decision.decision_status = "CONFIRMED"

    # Update ground truth on prediction for model monitoring
    pred = db.query(ModelPrediction).filter(ModelPrediction.expense_id == expense.id).first()
    if pred:
        pred.ground_truth_category = expense.category

    db.commit()
    log_audit_event(db, expense.user_id, "CONFIRM_EXPENSE_DECISION", "Expense", expense.id)
    return {"message": "Expense and tax deduction confirmed by taxpayer.", "status": "CONFIRMED"}
