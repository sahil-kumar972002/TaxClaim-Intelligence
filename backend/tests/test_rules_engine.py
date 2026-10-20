import pytest
from app.services.rules_engine import StatutoryRulesEngine
from app.models.tax_rule import TaxRule
from app.models.business_profile import BusinessProfile

def test_software_deduction_evaluation():
    engine = StatutoryRulesEngine()
    rule = TaxRule(
        rule_code="IN-SEC37-SOFT-01",
        country="India",
        jurisdiction="CBDT",
        tax_year="2024-2025",
        taxpayer_type="Freelancer",
        profession="Software Developer",
        expense_category="software",
        title="Software Licenses",
        description="Full revenue deduction for periodic SaaS subscriptions",
        deductibility_status="DEDUCTIBLE",
        eligibility_conditions=["Incurred wholly and exclusively for profession"],
        limitations={"max_deduction_percentage": 100.0, "cash_payment_limit": 10000.0},
        evidence_requirements=["Tax Invoice", "Payment proof"],
        effective_date="2024-04-01",
        source_statute="Income Tax Act 1961 Section 37(1)",
        rule_version="v2024.1",
        last_verified_date="2025-01-15"
    )
    res = engine.evaluate_deduction(
        rule=rule,
        amount=3499.0,
        business_use_pct=1.0,
        payment_method="Credit Card",
        profile=None
    )
    assert res["deductibility_status"] == "DEDUCTIBLE"
    assert res["eligible_amount"] == 3499.0
    assert "Section 37(1)" in res["potential_treatment"]

def test_cash_disallowance_under_sec_40a3():
    engine = StatutoryRulesEngine()
    rule = TaxRule(
        rule_code="IN-SEC37-SOFT-01",
        country="India",
        jurisdiction="CBDT",
        tax_year="2024-2025",
        taxpayer_type="Freelancer",
        profession="All",
        expense_category="software",
        title="Software",
        description="Software",
        deductibility_status="DEDUCTIBLE",
        eligibility_conditions=[],
        limitations={"cash_payment_limit": 10000.0},
        evidence_requirements=[],
        effective_date="2024-04-01",
        source_statute="Income Tax Act 1961 Section 37(1)",
        rule_version="v2024.1",
        last_verified_date="2025-01-15"
    )
    # Cash payment of ₹15,000 > ₹10,000 threshold
    res = engine.evaluate_deduction(
        rule=rule,
        amount=15000.0,
        business_use_pct=1.0,
        payment_method="Cash",
        profile=None
    )
    assert res["deductibility_status"] == "NON_DEDUCTIBLE"
    assert res["eligible_amount"] == 0.0
    assert "Section 40A(3)" in res["potential_treatment"]
