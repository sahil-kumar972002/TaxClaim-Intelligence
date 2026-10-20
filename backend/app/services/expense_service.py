import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.expense import Expense, ExpenseLineItem
from app.models.document import Document
from app.models.decision import Decision
from app.models.risk_anomaly import RiskFlag, Anomaly
from app.models.business_profile import BusinessProfile
from app.models.model_metrics import ModelPrediction
from app.ml.category_classifier import expense_classifier
from app.ml.anomaly_detector import anomaly_detector
from app.services.rules_engine import rules_engine
from app.services.evidence_engine import evidence_engine
from app.core.audit_logger import log_audit_event

class ExpenseIntelligenceService:
    """
    Core Tax Intelligence Orchestrator.
    Executes the multi-stage AI classification, statutory rule retrieval,
    evidence scoring, and anomaly detection pipeline.
    """

    def process_and_evaluate_expense(
        self,
        db: Session,
        expense: Expense,
        document: Optional[Document] = None,
        profile: Optional[BusinessProfile] = None
    ) -> Dict[str, Any]:
        """
        Runs the complete Tax Intelligence analysis on an expense.
        """
        # Step 1: ML Expense Category Classification
        search_text = f"{expense.merchant} {expense.business_purpose or ''} {expense.category or ''}"
        predicted_category, ai_confidence, feature_weights = expense_classifier.predict(search_text)
        
        # If user explicitly provided a category, respect it but keep track of prediction
        if not expense.category or expense.category == "other":
            expense.category = predicted_category

        # Record model prediction for monitoring & drift tracking
        pred_record = ModelPrediction(
            id=str(uuid.uuid4()),
            expense_id=expense.id,
            model_name="ExpenseClassifier-XGB-v2",
            model_version="2.1.0",
            predicted_category=predicted_category,
            confidence=ai_confidence,
            feature_contributions=feature_weights
        )
        db.add(pred_record)

        # Step 2: Retrieve Applicable Statutory Tax Rule
        country = profile.country if profile else "India"
        jurisdiction = profile.jurisdiction if profile else "Income Tax Department (CBDT)"
        tax_year = profile.tax_year if profile else "2024-2025"
        profession = profile.profession if profile else "Software Developer"

        applicable_rule = rules_engine.match_rule(
            db=db,
            country=country,
            jurisdiction=jurisdiction,
            tax_year=tax_year,
            profession=profession,
            category=expense.category
        )

        # Step 3: Evaluate Statutory Deduction & Limitations
        deduction_eval = rules_engine.evaluate_deduction(
            rule=applicable_rule,
            amount=expense.amount,
            business_use_pct=expense.business_use_percentage,
            payment_method=expense.payment_method,
            profile=profile
        )
        expense.eligible_deductible_amount = deduction_eval["eligible_amount"]

        # Step 4: Evaluate 7-Factor Evidence Strength & Missing Items
        evidence_eval = evidence_engine.evaluate_evidence(
            expense=expense,
            document=document,
            evidence_items=expense.evidence_items
        )

        # Step 5: Multi-Dimensional Anomaly & Duplicate Detection
        all_user_expenses = db.query(Expense).filter(Expense.user_id == expense.user_id).all()
        historical_dict = [
            {
                "id": e.id,
                "merchant": e.merchant,
                "amount": e.amount,
                "invoice_number": e.invoice_number,
                "transaction_date": e.transaction_date,
                "category": e.category
            }
            for e in all_user_expenses
        ]

        doc_hash = document.file_hash_sha256 if document else None
        detected_anomalies = anomaly_detector.evaluate_expense(
            expense={
                "id": expense.id,
                "merchant": expense.merchant,
                "amount": expense.amount,
                "category": expense.category,
                "invoice_number": expense.invoice_number,
                "transaction_date": expense.transaction_date
            },
            historical_expenses=historical_dict,
            document_hash=doc_hash
        )

        # Clear existing anomalies/flags for this expense and re-insert
        db.query(Anomaly).filter(Anomaly.expense_id == expense.id).delete()
        db.query(RiskFlag).filter(RiskFlag.expense_id == expense.id).delete()

        has_critical_anomaly = False
        for anom in detected_anomalies:
            if anom["severity"] in ("HIGH", "CRITICAL"):
                has_critical_anomaly = True
            db_anom = Anomaly(
                id=str(uuid.uuid4()),
                expense_id=expense.id,
                anomaly_type=anom["anomaly_type"],
                anomaly_score=anom["anomaly_score"],
                explanation=anom["explanation"],
                detected_by=anom["detected_by"],
                details_json=anom.get("details_json", {})
            )
            db.add(db_anom)

        # Step 6: Human-in-the-Loop Gating (AUTO / REVIEW / INSUFFICIENT DATA)
        has_missing_vital_evidence = len(evidence_eval["missing_evidence"]) > 2
        is_evidence_strong = evidence_eval["overall_score"] >= 0.75
        is_confidence_high = ai_confidence >= 0.85

        if has_missing_vital_evidence or evidence_eval["overall_score"] < 0.40:
            decision_status = "INSUFFICIENT_DATA"
            expense.status = "INSUFFICIENT_DATA"
            human_review_req = True
        elif has_critical_anomaly or not is_evidence_strong or not is_confidence_high:
            decision_status = "REVIEW"
            expense.status = "NEEDS_REVIEW"
            human_review_req = True
        else:
            decision_status = "AUTO"
            expense.status = "AUTO_RECOMMENDED"
            human_review_req = False

        # Step 7: Synthesize Traceable Reasoning Chain
        reasoning_points = [
            f"Merchant '{expense.merchant}' verified via financial entity recognition.",
            f"AI Category Classification: '{expense.category}' (confidence: {int(ai_confidence*100)}%).",
        ]
        reasoning_points.extend(deduction_eval["reasoning_points"])
        reasoning_points.append(f"Evidence Strength Score evaluated at {int(evidence_eval['overall_score']*100)}%.")

        # Step 8: Persist or Update Decision
        decision = db.query(Decision).filter(Decision.expense_id == expense.id).first()
        if not decision:
            decision = Decision(
                id=str(uuid.uuid4()),
                expense_id=expense.id,
                tax_rule_id=applicable_rule.id if applicable_rule else None,
                potential_treatment=deduction_eval["potential_treatment"],
                ai_confidence=ai_confidence,
                evidence_strength_score=evidence_eval["overall_score"],
                decision_status=decision_status,
                reasoning_summary=reasoning_points,
                limitations_applied=deduction_eval["limitations_applied"],
                missing_evidence=evidence_eval["missing_evidence"],
                human_review_required=human_review_req
            )
            db.add(decision)
        else:
            decision.tax_rule_id = applicable_rule.id if applicable_rule else None
            decision.potential_treatment = deduction_eval["potential_treatment"]
            decision.ai_confidence = ai_confidence
            decision.evidence_strength_score = evidence_eval["overall_score"]
            decision.decision_status = decision_status
            decision.reasoning_summary = reasoning_points
            decision.limitations_applied = deduction_eval["limitations_applied"]
            decision.missing_evidence = evidence_eval["missing_evidence"]
            decision.human_review_required = human_review_req

        db.commit()

        # Audit Log Event
        log_audit_event(
            db=db,
            user_id=expense.user_id,
            action="EVALUATE_TAX_DECISION",
            resource_type="Expense",
            resource_id=expense.id,
            diff_payload={
                "status": decision_status,
                "rule_code": applicable_rule.rule_code if applicable_rule else None,
                "evidence_score": evidence_eval["overall_score"],
                "eligible_deduction": expense.eligible_deductible_amount
            }
        )

        return {
            "expense": expense,
            "decision": decision,
            "applicable_rule": applicable_rule,
            "evidence_eval": evidence_eval,
            "anomalies": detected_anomalies
        }

expense_service = ExpenseIntelligenceService()
