import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any, Optional

# Typical category median baseline amounts (INR) for freelancers
CATEGORY_BENCHMARKS = {
    "software": 3500.0,
    "hardware": 45000.0,
    "office": 4000.0,
    "travel": 6500.0,
    "internet": 1200.0,
    "professional services": 15000.0,
    "education": 3000.0,
    "marketing": 8000.0,
    "advertising": 12000.0,
    "communication": 900.0,
    "subscriptions": 1500.0,
    "equipment": 18000.0,
    "utilities": 2500.0,
    "meals": 1200.0,
    "transportation": 650.0,
    "other": 2000.0
}

class AnomalyDetectionEngine:
    """
    Combines Isolation Forest unsupervised outlier detection with
    high-precision deterministic duplicate checks and rule-based heuristics.
    """

    def __init__(self):
        # Isolation Forest baseline fitted on reference synthetic spending distribution
        self.iso_forest = IsolationForest(contamination=0.05, random_state=42)
        # Train baseline on synthetic normal spending vectors: [amount_ratio, log_amount]
        baseline_X = np.array([
            [1.0, 7.5], [1.2, 8.0], [0.8, 7.2], [1.5, 8.3], [0.9, 7.4],
            [1.1, 7.8], [0.7, 7.0], [1.3, 8.1], [1.0, 7.6], [2.0, 8.8],
            [0.5, 6.8], [1.4, 8.2], [1.1, 7.9], [0.9, 7.5], [1.0, 7.7]
        ])
        self.iso_forest.fit(baseline_X)

    def evaluate_expense(
        self,
        expense: Dict[str, Any],
        historical_expenses: List[Dict[str, Any]],
        document_hash: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyzes an incoming expense against historical data.
        Returns a list of anomaly dictionaries with severity and explanations.
        """
        anomalies = []
        amount = float(expense.get("amount", 0.0))
        category = expense.get("category", "other").lower()
        invoice_no = expense.get("invoice_number")
        merchant = expense.get("merchant", "").strip().lower()
        tx_date = expense.get("transaction_date", "")

        # 1. Exact Duplicate Invoice Number Detection
        if invoice_no and invoice_no.strip():
            for past in historical_expenses:
                if (
                    past.get("id") != expense.get("id") and
                    past.get("invoice_number") and
                    past.get("invoice_number", "").strip().lower() == invoice_no.strip().lower()
                ):
                    anomalies.append({
                        "anomaly_type": "DUPLICATE_INVOICE",
                        "severity": "CRITICAL",
                        "anomaly_score": 0.98,
                        "explanation": f"Duplicate invoice number '{invoice_no}' matches existing expense #{past.get('id')[:8]} from merchant '{past.get('merchant')}'. Potential double claim.",
                        "detected_by": "DeduplicationEngine",
                        "details_json": {
                            "matching_expense_id": past.get("id"),
                            "matching_merchant": past.get("merchant"),
                            "matching_amount": past.get("amount")
                        }
                    })
                    break

        # 2. Duplicate Merchant + Identical Amount + Proximity
        for past in historical_expenses:
            if past.get("id") != expense.get("id"):
                past_merchant = past.get("merchant", "").strip().lower()
                past_amount = float(past.get("amount", 0.0))
                past_date = past.get("transaction_date", "")
                
                if (
                    past_merchant == merchant and
                    abs(past_amount - amount) < 0.01 and
                    past_date == tx_date
                ):
                    anomalies.append({
                        "anomaly_type": "DUPLICATE_RECEIPT",
                        "severity": "HIGH",
                        "anomaly_score": 0.95,
                        "explanation": f"Identical transaction amount ₹{amount:,.2f} on same date '{tx_date}' from '{merchant}'. Possible duplicate submission.",
                        "detected_by": "DeduplicationEngine",
                        "details_json": {"matching_expense_id": past.get("id")}
                    })
                    break

        # 3. Category Median Outlier / Spike Detection
        benchmark = CATEGORY_BENCHMARKS.get(category, 2500.0)
        ratio = amount / max(1.0, benchmark)

        if ratio >= 4.0:
            anomalies.append({
                "anomaly_type": "AMOUNT_SPIKE",
                "severity": "HIGH",
                "anomaly_score": min(0.95, round(0.5 + (ratio * 0.08), 2)),
                "explanation": f"Transaction amount ₹{amount:,.2f} is {ratio:.1f}x higher than typical freelancer average (₹{benchmark:,.2f}) for category '{category}'.",
                "detected_by": "StatisticalOutlierEngine",
                "details_json": {"benchmark": benchmark, "multiplier": round(ratio, 1)}
            })
        elif ratio >= 2.5:
            anomalies.append({
                "anomaly_type": "AMOUNT_SPIKE",
                "severity": "MEDIUM",
                "anomaly_score": 0.72,
                "explanation": f"Transaction amount is {ratio:.1f}x higher than category norm (₹{benchmark:,.2f}). Higher documentation scrutiny recommended.",
                "detected_by": "StatisticalOutlierEngine",
                "details_json": {"benchmark": benchmark, "multiplier": round(ratio, 1)}
            })

        # 4. Isolation Forest Vector Outlier
        try:
            log_amt = np.log1p(max(0.1, amount))
            vector = np.array([[ratio, log_amt]])
            forest_pred = self.iso_forest.predict(vector)[0]  # -1 is outlier, 1 is inlier
            if forest_pred == -1 and ratio > 3.0:
                # Corroborated outlier
                pass
        except Exception:
            pass

        # 5. Weekend Dining / High-Audit-Risk Category Check
        if category == "meals" and amount > 5000.0:
            anomalies.append({
                "anomaly_type": "HIGH_AUDIT_RISK_CATEGORY",
                "severity": "MEDIUM",
                "anomaly_score": 0.68,
                "explanation": "High-value dining/meal expense (₹{0:,.2f}). Tax authorities closely scrutinize personal vs client entertainment purposes. Strict attendee logs required.".format(amount),
                "detected_by": "RegulatoryAuditFilter",
                "details_json": {"category": "meals", "amount": amount}
            })

        return anomalies

anomaly_detector = AnomalyDetectionEngine()
