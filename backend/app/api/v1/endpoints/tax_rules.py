from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tax_rule import TaxRule
from app.schemas.tax_rule import TaxRuleResponse

router = APIRouter()

@router.get("/", response_model=List[TaxRuleResponse])
def list_tax_rules(
    country: Optional[str] = None,
    expense_category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TaxRule)
    if country:
        query = query.filter(TaxRule.country == country)
    if expense_category:
        query = query.filter(TaxRule.expense_category == expense_category)
    return query.all()

@router.get("/{rule_code}", response_model=TaxRuleResponse)
def get_tax_rule(rule_code: str, db: Session = Depends(get_db)):
    rule = db.query(TaxRule).filter(TaxRule.rule_code == rule_code).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Statutory Tax Rule not found")
    return rule
