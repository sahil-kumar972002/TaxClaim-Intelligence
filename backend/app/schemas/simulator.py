from pydantic import BaseModel
from typing import Dict, Any

class SimulatorRequest(BaseModel):
    annual_gross_receipts: float = 2000000.0  # Gross revenue e.g. ₹20,00,000
    total_business_expenses: float = 650000.0
    business_use_multiplier: float = 1.0     # 0.5 to 1.0 slider
    tax_regime_override: str = "AUTO_COMPARE"  # AUTO_COMPARE, SEC_44ADA, REGULAR_PGBP, NEW_REGIME_115BAC

class RegimeCalculation(BaseModel):
    regime_name: str
    statutory_basis: str
    taxable_income: float
    estimated_tax_payable: float
    effective_tax_rate_percent: float
    audit_requirement: str
    books_of_accounts_required: bool
    pros_and_cons: Dict[str, Any]

class SimulatorResponse(BaseModel):
    gross_receipts: float
    claimed_expenses: float
    regimes: Dict[str, RegimeCalculation]
    recommended_regime: str
    potential_tax_savings: float
    disclaimer: str
