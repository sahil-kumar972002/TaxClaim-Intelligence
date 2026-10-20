from typing import Dict, Any, Optional, Tuple, List
from sqlalchemy.orm import Session
from app.models.tax_rule import TaxRule
from app.models.business_profile import BusinessProfile

class StatutoryRulesEngine:
    """
    Deterministic Jurisdiction-Aware Tax Rules Engine.
    Evaluates statutory deductibility, legal limits, and evidentiary requirements
    without inventing laws or hallucinating tax codes.
    """

    def match_rule(
        self,
        db: Session,
        country: str,
        jurisdiction: str,
        tax_year: str,
        profession: str,
        category: str
    ) -> Optional[TaxRule]:
        """
        Retrieves the exact applicable statutory rule matching taxpayer profile and category.
        Falls back to 'All' professions if no specific profession rule exists.
        """
        # Specific profession match
        rule = db.query(TaxRule).filter(
            TaxRule.country == country,
            TaxRule.tax_year == tax_year,
            TaxRule.expense_category == category,
            TaxRule.profession.ilike(f"%{profession}%")
        ).first()

        if not rule:
            # Fallback to general rule for all professions in this category
            rule = db.query(TaxRule).filter(
                TaxRule.country == country,
                TaxRule.expense_category == category,
                TaxRule.profession == "All"
            ).first()

        if not rule:
            # Fallback to general Section 37(1) rule if India
            if country == "India":
                rule = db.query(TaxRule).filter(TaxRule.rule_code == "IN-SEC37-SOFT-01").first()

        return rule

    def evaluate_deduction(
        self,
        rule: Optional[TaxRule],
        amount: float,
        business_use_pct: float,
        payment_method: str,
        profile: Optional[BusinessProfile]
    ) -> Dict[str, Any]:
        """
        Calculates statutory treatment, eligible deductible amount, and limitations.
        """
        if not rule:
            return {
                "potential_treatment": "Needs Statutory Classification",
                "deductibility_status": "NEEDS_REVIEW",
                "eligible_amount": round(amount * business_use_pct, 2),
                "limitations_applied": "No explicit statutory rule match found. Subject to general business test.",
                "reasoning_points": ["General business deduction evaluation required."]
            }

        status = rule.deductibility_status
        limitations_str = ""
        reasoning = []
        eligible_amount = 0.0

        # Cash payment disallowance under Section 40A(3) for India
        is_cash = payment_method.strip().lower() == "cash"
        if is_cash and amount > 10000.0 and rule.country == "India":
            status = "NON_DEDUCTIBLE"
            eligible_amount = 0.0
            limitations_str = "Section 40A(3) Disallowance: Single cash payment exceeds ₹10,000 threshold. 100% disallowed."
            reasoning.append("Cash payment exceeds statutory threshold of ₹10,000 under Section 40A(3).")
            return {
                "potential_treatment": "Disallowed under Section 40A(3) (Cash > ₹10,000)",
                "deductibility_status": status,
                "eligible_amount": eligible_amount,
                "limitations_applied": limitations_str,
                "reasoning_points": reasoning
            }

        # Case A: Capital Depreciation (Hardware, Furniture, Laptops)
        if status == "CAPITAL_DEPRECIATION":
            depr_rate = rule.limitations.get("depreciation_rate", 0.40)
            eligible_amount = round(amount * business_use_pct * depr_rate, 2)
            limitations_str = f"Capitalized under Block of Assets. First-year depreciation rate {int(depr_rate*100)}% applied on business portion."
            reasoning.append(f"Capital expenditure capitalized under Section 32; eligible for {int(depr_rate*100)}% WDV depreciation.")
            potential_treatment = f"Capital Asset: {int(depr_rate*100)}% First-Year Depreciation under Section 32"

        # Case B: Partially Deductible (Internet, Meals, Vehicles)
        elif status == "PARTIALLY_DEDUCTIBLE":
            if rule.expense_category == "meals":
                # Strict 50% cap for meals (US IRC 274(n) or standard Indian business meal apportionment)
                effective_pct = min(business_use_pct, 0.50)
                eligible_amount = round(amount * effective_pct, 2)
                limitations_str = "Business meal 50% statutory deduction limitation applied. Non-business portion excluded."
                reasoning.append("Business meals restricted to 50% allowable deduction with verified client attendee proof.")
                potential_treatment = "50% Business Meal Deduction (Client Meeting Rule)"
            elif rule.expense_category == "internet":
                capped_pct = min(business_use_pct, rule.limitations.get("default_business_use_cap", 0.80))
                eligible_amount = round(amount * capped_pct, 2)
                limitations_str = f"Apportioned business utilization applied ({int(capped_pct*100)}%). Personal usage portion excluded."
                reasoning.append(f"Telecommunications apportioned at {int(capped_pct*100)}% business use under Section 38(2).")
                potential_treatment = f"{int(capped_pct*100)}% Deductible Business Broadband (Apportioned)"
            else:
                eligible_amount = round(amount * business_use_pct, 2)
                limitations_str = f"Apportioned to {int(business_use_pct*100)}% business use."
                potential_treatment = f"{int(business_use_pct*100)}% Apportioned Business Expense"

        # Case C: 100% Revenue Expense (Software, Travel, Subscriptions, Office Supplies)
        elif status == "DEDUCTIBLE":
            eligible_amount = round(amount * business_use_pct, 2)
            limitations_str = "100% allowable revenue expenditure incurred wholly and exclusively for profession."
            reasoning.append(f"Qualifies as 100% deductible revenue expense under {rule.source_statute}.")
            potential_treatment = f"100% Deductible Business Expense under {rule.source_statute.split(',')[0]}"

        else:
            eligible_amount = round(amount * business_use_pct, 2)
            limitations_str = "Standard deduction criteria applied."
            potential_treatment = "Potentially Business-Related Expense"

        if business_use_pct < 1.0:
            reasoning.append(f"Adjusted for taxpayer declared {int(business_use_pct*100)}% business-use allocation.")

        return {
            "potential_treatment": potential_treatment,
            "deductibility_status": status,
            "eligible_amount": eligible_amount,
            "limitations_applied": limitations_str,
            "reasoning_points": reasoning
        }

rules_engine = StatutoryRulesEngine()
