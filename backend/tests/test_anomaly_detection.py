import pytest
from app.ml.anomaly_detector import AnomalyDetectionEngine

def test_duplicate_invoice_detection():
    detector = AnomalyDetectionEngine()
    historical = [
        {
            "id": "exp-1",
            "merchant": "Adobe Systems India",
            "amount": 3499.0,
            "invoice_number": "ADB-INV-883019",
            "transaction_date": "2024-07-05",
            "category": "software"
        }
    ]
    new_expense = {
        "id": "exp-2",
        "merchant": "Adobe Systems India",
        "amount": 3499.0,
        "invoice_number": "ADB-INV-883019",  # Duplicate invoice number
        "transaction_date": "2024-07-06",
        "category": "software"
    }
    anomalies = detector.evaluate_expense(new_expense, historical)
    types = [a["anomaly_type"] for a in anomalies]
    assert "DUPLICATE_INVOICE" in types
    dup = next(a for a in anomalies if a["anomaly_type"] == "DUPLICATE_INVOICE")
    assert dup["severity"] == "CRITICAL"

def test_amount_spike_detection():
    detector = AnomalyDetectionEngine()
    new_expense = {
        "id": "exp-3",
        "merchant": "Luxury Dining Place",
        "amount": 15000.0,  # 15,000 is > 10x typical meal benchmark (1200)
        "invoice_number": "LDP-991",
        "transaction_date": "2024-08-10",
        "category": "meals"
    }
    anomalies = detector.evaluate_expense(new_expense, [])
    types = [a["anomaly_type"] for a in anomalies]
    assert "AMOUNT_SPIKE" in types
