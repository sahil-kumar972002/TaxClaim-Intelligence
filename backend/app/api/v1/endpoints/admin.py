from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.business_profile import BusinessProfile
from app.models.expense import Expense
from app.models.tax_rule import TaxRule
from app.models.audit_event import AuditEvent
from app.models.model_metrics import ModelPrediction
from app.ml.model_monitor import model_monitor
from app.data.seed_rules import STATUTORY_TAX_RULES
from app.data.seed_demo import DEMO_PERSONAS, DEMO_EXPENSES
from app.services.expense_service import expense_service
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/metrics")
def get_model_metrics(db: Session = Depends(get_db)):
    predictions = db.query(ModelPrediction).all()
    pred_dicts = [
        {"predicted": p.predicted_category, "actual": p.ground_truth_category}
        for p in predictions if p.ground_truth_category
    ]
    return model_monitor.compute_metrics(pred_dicts)

@router.get("/audit-logs")
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    events = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "action": e.action,
            "resource_type": e.resource_type,
            "resource_id": e.resource_id,
            "ip_address": e.ip_address,
            "user_agent": e.user_agent,
            "diff_payload": e.diff_payload,
            "timestamp": e.timestamp
        }
        for e in events
    ]

@router.post("/seed-demo")
def seed_demo_database(db: Session = Depends(get_db)):
    """
    Seeds verified statutory tax rules, 6 personas, and 8 realistic transactions.
    """
    # 1. Seed Tax Rules
    for r in STATUTORY_TAX_RULES:
        existing_rule = db.query(TaxRule).filter(TaxRule.rule_code == r["rule_code"]).first()
        if not existing_rule:
            db_rule = TaxRule(
                id=str(uuid.uuid4()),
                rule_code=r["rule_code"],
                country=r["country"],
                jurisdiction=r["jurisdiction"],
                tax_year=r["tax_year"],
                taxpayer_type=r["taxpayer_type"],
                profession=r["profession"],
                expense_category=r["expense_category"],
                title=r["title"],
                description=r["description"],
                deductibility_status=r["deductibility_status"],
                eligibility_conditions=r["eligibility_conditions"],
                limitations=r["limitations"],
                evidence_requirements=r["evidence_requirements"],
                effective_date=r["effective_date"],
                source_statute=r["source_statute"],
                statute_citation_url=r.get("statute_citation_url"),
                rule_version=r["rule_version"],
                last_verified_date=r["last_verified_date"]
            )
            db.add(db_rule)
    db.commit()

    # 2. Seed Primary User (Aarav Sharma - Software Developer)
    primary_persona = DEMO_PERSONAS[0]
    user = db.query(User).filter(User.email == primary_persona["email"]).first()
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=primary_persona["email"],
            password_hash=get_password_hash("password123"),
            full_name=primary_persona["full_name"],
            role=primary_persona["role"],
            is_verified=True
        )
        db.add(user)
        db.flush()

        profile = BusinessProfile(
            id=str(uuid.uuid4()),
            user_id=user.id,
            profession=primary_persona["profession"],
            business_type=primary_persona["business_type"],
            country=primary_persona["country"],
            jurisdiction=primary_persona["jurisdiction"],
            tax_year=primary_persona["tax_year"],
            tax_regime=primary_persona["tax_regime"],
            business_use_patterns=primary_persona["business_use_patterns"],
            recurring_expenses=primary_persona["recurring_expenses"],
            business_description=primary_persona["business_description"],
            estimated_annual_income=primary_persona["estimated_annual_income"]
        )
        db.add(profile)
        db.commit()

    # 3. Seed the 8 realistic demo expenses if none exist
    existing_expenses_count = db.query(Expense).filter(Expense.user_id == user.id).count()
    if existing_expenses_count == 0:
        profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == user.id).first()
        for item in DEMO_EXPENSES:
            expense = Expense(
                id=str(uuid.uuid4()),
                user_id=user.id,
                merchant=item["merchant"],
                transaction_date=item["transaction_date"],
                amount=item["amount"],
                currency=item["currency"],
                tax_amount=item["tax_amount"],
                invoice_number=item["invoice_number"],
                category=item["category"],
                payment_method=item["payment_method"],
                business_purpose=item["business_purpose"],
                business_use_percentage=item["business_use_percentage"]
            )
            db.add(expense)
            db.flush()

            # Run full AI Tax intelligence pipeline on each expense
            expense_service.process_and_evaluate_expense(
                db=db,
                expense=expense,
                document=None,
                profile=profile
            )

    return {
        "status": "SUCCESS",
        "message": "Demo data initialized: statutory tax rules, active persona, and 8 realistic transactions seeded."
    }
