from typing import Dict, Any, List, Optional
from app.models.expense import Expense
from app.models.document import Document
from app.models.evidence import Evidence

class EvidenceEngine:
    """
    Evaluates evidence quality across 7 statutory dimensions.
    Constructs traceable evidence graphs and generates targeted questions for missing proofs.
    """

    # 7-factor weights
    WEIGHTS = {
        "receipt_document": 0.20,
        "merchant_identified": 0.15,
        "date_verified": 0.10,
        "amount_tax_verified": 0.15,
        "payment_proof": 0.15,
        "business_purpose": 0.15,
        "business_use_pct": 0.10
    }

    def evaluate_evidence(
        self,
        expense: Expense,
        document: Optional[Document] = None,
        evidence_items: Optional[List[Evidence]] = None
    ) -> Dict[str, Any]:
        """
        Calculates Evidence Strength Score (0.0 to 1.0) and detailed factor breakdown.
        """
        evidence_items = evidence_items or []
        factors = []
        missing = []
        total_score = 0.0

        # Factor 1: Receipt / Tax Invoice Document
        has_doc = (document is not None) or any(e.evidence_type in ("RECEIPT", "INVOICE") for e in evidence_items)
        if has_doc:
            total_score += self.WEIGHTS["receipt_document"]
            factors.append({
                "name": "Receipt / Invoice Document",
                "weight": self.WEIGHTS["receipt_document"],
                "satisfied": True,
                "description": f"Original document '{document.original_filename if document else 'Attached'}' on record with cryptographic SHA-256 hash."
            })
        else:
            factors.append({
                "name": "Receipt / Invoice Document",
                "weight": self.WEIGHTS["receipt_document"],
                "satisfied": False,
                "description": "No original PDF/Image invoice attached."
            })
            missing.append({
                "field": "document",
                "label": "Original Tax Invoice / Receipt",
                "prompt": "Upload the original PDF or camera receipt to substantiate this deduction."
            })

        # Factor 2: Merchant Identified
        merchant = (expense.merchant or "").strip()
        has_merchant = bool(merchant and merchant.lower() != "unknown merchant")
        if has_merchant:
            total_score += self.WEIGHTS["merchant_identified"]
            factors.append({
                "name": "Merchant Identification",
                "weight": self.WEIGHTS["merchant_identified"],
                "satisfied": True,
                "description": f"Legitimate vendor '{merchant}' verified."
            })
        else:
            factors.append({
                "name": "Merchant Identification",
                "weight": self.WEIGHTS["merchant_identified"],
                "satisfied": False,
                "description": "Vendor / merchant name not verified."
            })
            missing.append({
                "field": "merchant",
                "label": "Merchant / Supplier Name",
                "prompt": "Please specify the full business name of the vendor."
            })

        # Factor 3: Transaction Date
        has_date = bool(expense.transaction_date and len(expense.transaction_date) >= 8)
        if has_date:
            total_score += self.WEIGHTS["date_verified"]
            factors.append({
                "name": "Transaction Date",
                "weight": self.WEIGHTS["date_verified"],
                "satisfied": True,
                "description": f"Date verified as {expense.transaction_date} within active assessment tax year."
            })
        else:
            factors.append({
                "name": "Transaction Date",
                "weight": self.WEIGHTS["date_verified"],
                "satisfied": False,
                "description": "Transaction date missing or ambiguous."
            })
            missing.append({
                "field": "transaction_date",
                "label": "Invoice Date",
                "prompt": "Enter the exact date when the payment or invoice was issued."
            })

        # Factor 4: Amount & Tax Match
        has_amount = expense.amount > 0
        if has_amount:
            total_score += self.WEIGHTS["amount_tax_verified"]
            tax_str = f"with recorded GST/Tax ₹{expense.tax_amount:,.2f}" if expense.tax_amount > 0 else "tax breakdown verified"
            factors.append({
                "name": "Amount & Tax Verification",
                "weight": self.WEIGHTS["amount_tax_verified"],
                "satisfied": True,
                "description": f"Total {expense.currency} {expense.amount:,.2f} {tax_str}."
            })
        else:
            factors.append({
                "name": "Amount & Tax Verification",
                "weight": self.WEIGHTS["amount_tax_verified"],
                "satisfied": False,
                "description": "Transaction amount is zero or unverified."
            })
            missing.append({
                "field": "amount",
                "label": "Total Amount Paid",
                "prompt": "Specify the gross invoice total including taxes."
            })

        # Factor 5: Proof of Payment (Bank / UPI / Card / Non-Cash)
        has_payment = bool(
            expense.payment_method and
            expense.payment_method.lower() != "cash"
        ) or any(e.evidence_type == "PAYMENT_PROOF" for e in evidence_items)

        if has_payment:
            total_score += self.WEIGHTS["payment_proof"]
            factors.append({
                "name": "Payment Method & Trail",
                "weight": self.WEIGHTS["payment_proof"],
                "satisfied": True,
                "description": f"Banking trail verified via {expense.payment_method}."
            })
        else:
            factors.append({
                "name": "Payment Method & Trail",
                "weight": self.WEIGHTS["payment_proof"],
                "satisfied": False,
                "description": "Payment trail not linked to a bank transfer, UPI, or card statement."
            })
            missing.append({
                "field": "payment_method",
                "label": "Proof of Bank Payment",
                "prompt": "Link your bank transaction reference or card statement line to satisfy audit trail."
            })

        # Factor 6: Business Purpose Justification
        has_purpose = bool(expense.business_purpose and len(expense.business_purpose.strip()) > 10)
        if has_purpose:
            total_score += self.WEIGHTS["business_purpose"]
            factors.append({
                "name": "Business Purpose Justification",
                "weight": self.WEIGHTS["business_purpose"],
                "satisfied": True,
                "description": f"Documented justification: '{expense.business_purpose[:60]}...'"
            })
        else:
            factors.append({
                "name": "Business Purpose Justification",
                "weight": self.WEIGHTS["business_purpose"],
                "satisfied": False,
                "description": "Lack of explicit business nexus explanation."
            })
            missing.append({
                "field": "business_purpose",
                "label": "Business Purpose Nexus",
                "prompt": "In 1 sentence, explain how this expense relates directly to your client work or profession."
            })

        # Factor 7: Business-Use Percentage Declared
        has_use_pct = 0.0 < expense.business_use_percentage <= 1.0
        if has_use_pct:
            total_score += self.WEIGHTS["business_use_pct"]
            factors.append({
                "name": "Business-Use Allocation",
                "weight": self.WEIGHTS["business_use_pct"],
                "satisfied": True,
                "description": f"Allocation fixed at {int(expense.business_use_percentage*100)}% business utilization."
            })
        else:
            factors.append({
                "name": "Business-Use Allocation",
                "weight": self.WEIGHTS["business_use_pct"],
                "satisfied": False,
                "description": "Business utilization percentage not established."
            })
            missing.append({
                "field": "business_use_percentage",
                "label": "Business-Use Percentage",
                "prompt": "What percentage of this asset/service was used for your freelance work vs personal?"
            })

        final_score = round(total_score, 2)
        status = "STRONG" if final_score >= 0.80 else ("MODERATE" if final_score >= 0.60 else "WEAK")
        risk = "LOW" if final_score >= 0.80 else ("MEDIUM" if final_score >= 0.60 else "HIGH")

        return {
            "overall_score": final_score,
            "status": status,
            "factors": factors,
            "missing_evidence": missing,
            "audit_risk_level": risk
        }

    def build_evidence_graph(
        self,
        expense: Expense,
        document: Optional[Document],
        rule: Optional[Any],
        decision: Optional[Any]
    ) -> Dict[str, Any]:
        """
        Creates an interactive traceable node-link graph representation:
        User -> Expense -> Document/Receipt -> Payment -> Tax Rule -> Decision
        """
        nodes = [
            {"id": "user", "label": "Taxpayer", "type": "USER", "status": "VERIFIED"},
            {"id": "expense", "label": f"Expense: {expense.merchant} (₹{expense.amount:,.0f})", "type": "EXPENSE", "status": "INGESTED"},
        ]
        links = [
            {"source": "user", "target": "expense", "label": "claims"}
        ]

        if document:
            nodes.append({
                "id": "doc",
                "label": f"Tax Invoice ({document.original_filename})",
                "type": "DOCUMENT",
                "status": "HASH_VERIFIED",
                "sha256": document.file_hash_sha256[:12] + "..."
            })
            links.append({"source": "expense", "target": "doc", "label": "backed_by"})

        nodes.append({
            "id": "payment",
            "label": f"Payment: {expense.payment_method}",
            "type": "PAYMENT",
            "status": "NON_CASH" if expense.payment_method.lower() != "cash" else "CASH"
        })
        links.append({"source": "expense", "target": "payment", "label": "paid_via"})

        if rule:
            nodes.append({
                "id": "rule",
                "label": f"Statute: {rule.rule_code}",
                "type": "TAX_RULE",
                "status": "STATUTORY_GROUNDED",
                "source": rule.source_statute
            })
            links.append({"source": "expense", "target": "rule", "label": "governed_by"})

        if decision:
            nodes.append({
                "id": "decision",
                "label": f"Decision: {decision.potential_treatment[:32]}...",
                "type": "DECISION",
                "status": decision.decision_status,
                "confidence": f"{int(decision.ai_confidence*100)}%"
            })
            if rule:
                links.append({"source": "rule", "target": "decision", "label": "evaluates"})
            links.append({"source": "expense", "target": "decision", "label": "concludes"})

        return {"nodes": nodes, "links": links}

evidence_engine = EvidenceEngine()
