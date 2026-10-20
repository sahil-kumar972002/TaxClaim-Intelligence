from typing import Dict, Any

class TaxSimulatorService:
    """
    Dynamic What-If Tax Simulator.
    Simulates statutory tax liability, regime comparisons (Section 44ADA vs Regular PGBP),
    and shows real-time impact as business-use sliders and expense amounts change.
    """

    @staticmethod
    def _calculate_new_regime_tax(taxable_income: float) -> float:
        """New Tax Regime FY 2024-25 (AY 2025-26) Indian Slabs under Sec 115BAC"""
        if taxable_income <= 300000.0:
            return 0.0
        elif taxable_income <= 700000.0:
            # Full rebate u/s 87A if taxable income <= 7 Lakhs in new regime
            return 0.0
        
        tax = 0.0
        # 0 - 3L: Nil
        # 3L - 7L: 5%
        if taxable_income > 300000:
            tax += min(400000, taxable_income - 300000) * 0.05
        # 7L - 10L: 10%
        if taxable_income > 700000:
            tax += min(300000, taxable_income - 700000) * 0.10
        # 10L - 12L: 15%
        if taxable_income > 1000000:
            tax += min(200000, taxable_income - 1000000) * 0.15
        # 12L - 15L: 20%
        if taxable_income > 1200000:
            tax += min(300000, taxable_income - 1200000) * 0.20
        # Above 15L: 30%
        if taxable_income > 1500000:
            tax += (taxable_income - 1500000) * 0.30

        # Health and Education Cess @ 4%
        cess = tax * 0.04
        return round(tax + cess, 2)

    def simulate(
        self,
        gross_receipts: float,
        actual_expenses: float,
        business_use_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        """
        Evaluates tax liability across:
        1. Presumptive Scheme (Section 44ADA)
        2. Regular PGBP (Actual Expense Deductions)
        """
        adj_expenses = actual_expenses * max(0.1, min(1.0, business_use_multiplier))

        # 1. Section 44ADA Presumptive Calculation
        presumptive_taxable_income = gross_receipts * 0.50  # Flat 50% deemed profit
        tax_44ada = self._calculate_new_regime_tax(presumptive_taxable_income)
        effective_rate_44ada = round((tax_44ada / max(1.0, gross_receipts)) * 100, 2)

        # 2. Regular PGBP Actual Expense Calculation
        pgbp_taxable_income = max(0.0, gross_receipts - adj_expenses)
        tax_pgbp = self._calculate_new_regime_tax(pgbp_taxable_income)
        effective_rate_pgbp = round((tax_pgbp / max(1.0, gross_receipts)) * 100, 2)

        # Recommendation & Delta
        tax_difference = abs(tax_44ada - tax_pgbp)
        if tax_44ada <= tax_pgbp:
            recommended = "Sec 44ADA (Presumptive Scheme)"
            savings = round(tax_pgbp - tax_44ada, 2)
        else:
            recommended = "Regular PGBP (Actual Expense Claim)"
            savings = round(tax_44ada - tax_pgbp, 2)

        regimes = {
            "sec_44ada": {
                "regime_name": "Section 44ADA Presumptive Taxation",
                "statutory_basis": "Income Tax Act 1961 Section 44ADA (50% Deemed Profit)",
                "taxable_income": round(presumptive_taxable_income, 2),
                "estimated_tax_payable": tax_44ada,
                "effective_tax_rate_percent": effective_rate_44ada,
                "audit_requirement": "Exempt from Tax Audit under Sec 44AB if turnover <= ₹75 Lakhs (digital)",
                "books_of_accounts_required": False,
                "pros_and_cons": {
                    "pros": ["Zero risk of expense disallowance", "No requirement to maintain formal books of accounts", "No tax audit required"],
                    "cons": ["Cannot claim additional actual expenses if real costs exceed 50% of revenue"]
                }
            },
            "regular_pgbp": {
                "regime_name": "Regular PGBP (Actual Itemized Deductions)",
                "statutory_basis": "Income Tax Act 1961 Section 28 to 44DB",
                "taxable_income": round(pgbp_taxable_income, 2),
                "estimated_tax_payable": tax_pgbp,
                "effective_tax_rate_percent": effective_rate_pgbp,
                "audit_requirement": "Tax audit mandatory if net profit declared is lower than 50% and turnover > basic exemption",
                "books_of_accounts_required": True,
                "pros_and_cons": {
                    "pros": ["Maximizes tax savings when real expenses exceed 50% (e.g. heavy server or hardware investments)"],
                    "cons": ["Mandatory maintenance of books of accounts (Sec 44AA)", "Vulnerable to expense disallowances during scrutiny"]
                }
            }
        }

        return {
            "gross_receipts": gross_receipts,
            "claimed_expenses": round(adj_expenses, 2),
            "regimes": regimes,
            "recommended_regime": recommended,
            "potential_tax_savings": savings,
            "disclaimer": "Calculations are estimates based on standard statutory rates for FY 2024-25. Consult a licensed Chartered Accountant or CPA before final tax filing."
        }

simulator_service = TaxSimulatorService()
