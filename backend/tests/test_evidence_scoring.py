import pytest
from app.services.evidence_engine import EvidenceEngine
from app.models.expense import Expense
from app.models.document import Document

def test_evidence_strength_score_full():
    engine = EvidenceEngine()
    doc = Document(
        original_filename="receipt.pdf",
        stored_filename="receipt_uuid.pdf",
        file_path="/tmp/test.pdf",
        file_hash_sha256="abc12345"
    )
    expense = Expense(
        merchant="Adobe Systems",
        transaction_date="2024-07-05",
        amount=3499.0,
        currency="INR",
        tax_amount=533.75,
        payment_method="Credit Card",
        business_purpose="Design asset creation for client wireframes and UI components",
        business_use_percentage=1.0
    )
    eval_res = engine.evaluate_evidence(expense, doc)
    assert eval_res["overall_score"] == 1.0
    assert eval_res["status"] == "STRONG"
    assert len(eval_res["missing_evidence"]) == 0

def test_evidence_strength_score_missing_purpose_and_doc():
    engine = EvidenceEngine()
    expense = Expense(
        merchant="Adobe Systems",
        transaction_date="2024-07-05",
        amount=3499.0,
        currency="INR",
        tax_amount=0.0,
        payment_method="Cash",
        business_purpose="",
        business_use_percentage=1.0
    )
    eval_res = engine.evaluate_evidence(expense, None)
    # Missing document (0.20), missing payment trail (0.15), missing purpose (0.15)
    assert eval_res["overall_score"] < 0.60
    assert eval_res["status"] == "WEAK"
    assert len(eval_res["missing_evidence"]) >= 2
