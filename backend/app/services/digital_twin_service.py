from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.business_profile import BusinessProfile
from app.models.expense import Expense
from app.models.document import Document
from app.models.decision import Decision
from app.models.risk_anomaly import Anomaly

class TaxDigitalTwinService:
    """
    Tax Digital Twin: A dynamic, continuously synchronized financial representation
    of the taxpayer's business operations, evidence strength, and audit readiness.
    """

    def get_user_digital_twin(self, db: Session, user_id: str) -> Dict[str, Any]:
        user = db.query(User).filter(User.id == user_id).first()
        profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == user_id).first()
        expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
        documents = db.query(Document).filter(Document.user_id == user_id).all()
        
        # Aggregations
        income = profile.estimated_annual_income if profile else 1500000.0
        total_expenses = sum(e.amount for e in expenses)
        total_eligible = sum(e.eligible_deductible_amount for e in expenses)
        
        # Decisions and evidence scores
        decisions = [e.decision for e in expenses if e.decision]
        avg_evidence_score = (
            sum(d.evidence_strength_score for d in decisions) / len(decisions)
        ) if decisions else 0.70

        # Status counts
        auto_count = sum(1 for e in expenses if e.status == "AUTO_RECOMMENDED")
        review_count = sum(1 for e in expenses if e.status == "NEEDS_REVIEW")
        insufficient_count = sum(1 for e in expenses if e.status == "INSUFFICIENT_DATA")

        # Anomalies count
        expense_ids = [e.id for e in expenses]
        anomaly_count = db.query(Anomaly).filter(Anomaly.expense_id.in_(expense_ids)).count() if expense_ids else 0

        # Calculate Audit Readiness Score (0 to 100)
        # Weighted by: Evidence Strength (50%), Low Anomaly Rate (25%), High Auto-Confirmation (25%)
        base_readiness = (avg_evidence_score * 50.0)
        anomaly_penalty = min(25.0, anomaly_count * 5.0)
        completion_bonus = (auto_count / max(1, len(expenses))) * 25.0
        audit_readiness_score = round(max(10.0, min(100.0, base_readiness + completion_bonus + 25.0 - anomaly_penalty)), 1)

        # Estimated Tax Savings (approx 31.2% marginal slab on eligible deductions)
        est_tax_savings = round(total_eligible * 0.312, 2)

        # Category Breakdown
        category_totals: Dict[str, float] = {}
        for e in expenses:
            cat = e.category or "other"
            category_totals[cat] = round(category_totals.get(cat, 0.0) + e.amount, 2)

        # Monthly Trends
        monthly_trend = [
            {"month": "Apr", "total_expense": 18500, "deductible": 18500, "savings": 5772},
            {"month": "May", "total_expense": 94200, "deductible": 79150, "savings": 24694},
            {"month": "Jun", "total_expense": 254800, "deductible": 194900, "savings": 60808},
            {"month": "Jul", "total_expense": 12500, "deductible": 12500, "savings": 3900},
            {"month": "Aug", "total_expense": 24900, "deductible": 23400, "savings": 7300},
            {"month": "Sep", "total_expense": 34800, "deductible": 31200, "savings": 9734},
        ]

        # Radar Metrics for Audit Readiness
        radar_metrics = [
            {"subject": "Documentation", "score": int(avg_evidence_score * 100), "fullMark": 100},
            {"subject": "Bank Trail", "score": 92, "fullMark": 100},
            {"subject": "Business Nexus", "score": 78, "fullMark": 100},
            {"subject": "Statutory Grounding", "score": 96, "fullMark": 100},
            {"subject": "Anomaly Cleanliness", "score": max(20, int(100 - anomaly_penalty * 3)), "fullMark": 100},
            {"subject": "Timeliness", "score": 88, "fullMark": 100},
        ]

        # Proactive AI Tax Insights
        proactive_insights = []
        if review_count > 0:
            proactive_insights.append({
                "type": "ACTION_REQUIRED",
                "severity": "WARNING",
                "title": f"{review_count} Expenses Require Human Review",
                "message": "Verify business nexus and attendee logs to unlock potential tax claims."
            })
        if anomaly_count > 0:
            proactive_insights.append({
                "type": "RISK_ALERT",
                "severity": "CRITICAL",
                "title": f"{anomaly_count} Anomalies or Duplicate Invoices Detected",
                "message": "Potential double submission flagged. Review deduplication drawer before audit package export."
            })
        if total_expenses > (income * 0.45):
            proactive_insights.append({
                "type": "STRATEGY_RECOMMENDATION",
                "severity": "INFO",
                "title": "Evaluate Section 44ADA vs Regular PGBP",
                "message": f"Your real business expenses (₹{total_expenses:,.0f}) are approaching 50% of revenue. Check What-If Simulator."
            })

        return {
            "user_id": user_id,
            "profession": profile.profession if profile else "Freelancer",
            "tax_year": profile.tax_year if profile else "2024-2025",
            "current_regime": profile.tax_regime if profile else "Sec 44ADA (Presumptive)",
            "total_income_tracked": income,
            "total_expenses_recorded": round(total_expenses, 2),
            "total_potentially_deductible": round(total_eligible, 2),
            "estimated_tax_savings": est_tax_savings,
            "average_evidence_strength": round(avg_evidence_score, 2),
            "audit_readiness_score": audit_readiness_score,
            "total_receipts_ingested": len(documents),
            "auto_recommended_count": auto_count,
            "needs_review_count": review_count,
            "insufficient_data_count": insufficient_count,
            "flagged_anomalies_count": anomaly_count,
            "category_totals": category_totals,
            "monthly_trend": monthly_trend,
            "radar_metrics": radar_metrics,
            "proactive_insights": proactive_insights
        }

digital_twin_service = TaxDigitalTwinService()
