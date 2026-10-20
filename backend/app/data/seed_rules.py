"""
Jurisdiction-Aware Statutory Tax Knowledge Base
Verified statutory provisions from Indian Income Tax Act 1961 and US Internal Revenue Code.
Every rule contains official citations, versioning, verified dates, and exact evidence requirements.
"""

from typing import List, Dict, Any

STATUTORY_TAX_RULES: List[Dict[str, Any]] = [
    # 1. Software & Subscriptions (India)
    {
        "rule_code": "IN-SEC37-SOFT-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "software",
        "title": "Software Licenses, SaaS Subscriptions & Cloud Hosting",
        "description": "Full revenue deduction for periodic SaaS subscriptions (Adobe, GitHub, JetBrains, AWS, Google Cloud) under Section 37(1) as revenue expenditure incurred wholly and exclusively for business/profession.",
        "deductibility_status": "DEDUCTIBLE",
        "eligibility_conditions": [
            "Incurred wholly and exclusively for profession/freelance work",
            "Periodic/annual recurring license or pay-as-you-go cloud service (not perpetual capital asset)",
            "Payment processed through banking channels (Credit Card, Net Banking, UPI)"
        ],
        "limitations": {
            "max_deduction_percentage": 100.0,
            "cash_payment_limit": 10000.0,
            "depreciation_applicable": False
        },
        "evidence_requirements": [
            "Vendor Tax Invoice showing user or freelance entity name",
            "Payment proof (Credit card statement line item or bank debit)",
            "Brief justification of software tool role in professional workflow"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 37(1)",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.2",
        "last_verified_date": "2025-01-15"
    },

    # 2. Hardware / Computers / Laptops (India)
    {
        "rule_code": "IN-SEC32-COMP-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "hardware",
        "title": "Computers, Laptops & Peripherals Depreciation (Block of Assets)",
        "description": "Capital expenditure on laptops, desktops, monitors, and servers is capitalized under 'Block of Assets - Computers including computer software' and eligible for 40% Written Down Value (WDV) depreciation under Section 32.",
        "deductibility_status": "CAPITAL_DEPRECIATION",
        "eligibility_conditions": [
            "Asset owned and utilized for professional practice during the tax year",
            "If put to use for less than 180 days in the financial year, 50% of depreciation rate (20%) is allowable in Year 1",
            "Full 40% depreciation allowed if put to use >= 180 days"
        ],
        "limitations": {
            "depreciation_rate": 0.40,
            "less_than_180_days_depreciation_rate": 0.20,
            "immediate_full_expensing_allowed": False
        },
        "evidence_requirements": [
            "Original Tax Invoice with serial number and GST details",
            "Proof of payment through non-cash banking channel",
            "Date of acquisition and date 'put to use' log",
            "Business-use percentage allocation if used partly for personal purposes"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 32(1)(ii) read with Rule 5",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-15"
    },

    # 3. Internet & Telecommunications (India)
    {
        "rule_code": "IN-SEC37-INET-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "internet",
        "title": "Broadband, Fiber & Mobile Cellular Connectivity",
        "description": "Internet broadband and mobile business calls are deductible in proportion to business utilization. When working from home, a reasonable apportionment (typically 70%-80%) is accepted.",
        "deductibility_status": "PARTIALLY_DEDUCTIBLE",
        "eligibility_conditions": [
            "Connection utilized for conducting remote work, client calls, code pushes, and research",
            "Reasonable apportionment between personal and professional usage"
        ],
        "limitations": {
            "default_business_use_cap": 0.80,
            "cash_limit": 10000.0
        },
        "evidence_requirements": [
            "Monthly telecommunications invoice (Jio, Airtel, etc.)",
            "Proof of payment debit",
            "Written declaration of business-use percentage (e.g. 75% business / 25% personal)"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 37(1) read with Section 38(2)",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-15"
    },

    # 4. Meals & Client Meetings (India)
    {
        "rule_code": "IN-SEC37-MEAL-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "meals",
        "title": "Business Meals, Client Meetings & Travel Subsistence",
        "description": "Meals and dining are deductible only when directly connected to professional discussions, prospective client acquisition, or travel away from standard tax home. Purely personal food is expressly non-deductible.",
        "deductibility_status": "PARTIALLY_DEDUCTIBLE",
        "eligibility_conditions": [
            "Must have a bona fide business purpose (client meeting, contract review, project pitch)",
            "Must not be lavish or extravagant under circumstances",
            "Must document names of attendees and specific business objective"
        ],
        "limitations": {
            "disallowance_of_personal_meals": True,
            "cash_limit": 10000.0
        },
        "evidence_requirements": [
            "Itemized restaurant receipt (not just credit card summary slip)",
            "List of attendees and client company",
            "Meeting agenda or business purpose summary"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 37(1)",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-15"
    },

    # 5. Travel & Local Transportation (India)
    {
        "rule_code": "IN-SEC37-TRAV-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "transportation",
        "title": "Cabs, Rideshare & Local Travel for Client Visits",
        "description": "Cab rides (Uber, Ola) and transit incurred for traveling to client sites, coworking hubs, airport travel for client meetings are 100% deductible.",
        "deductibility_status": "DEDUCTIBLE",
        "eligibility_conditions": [
            "Travel undertaken solely for business or client appointment",
            "Trip destination matches client office or business venue"
        ],
        "limitations": {
            "commute_to_permanent_office_non_deductible": False
        },
        "evidence_requirements": [
            "Rideshare electronic invoice showing pickup, destination, and fare",
            "Purpose of trip (client appointment or conference)"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 37(1)",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-15"
    },

    # 6. Presumptive Taxation Scheme Sec 44ADA (India)
    {
        "rule_code": "IN-SEC44ADA-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "Software Developer, Consultant, Designer, Doctor, Engineer",
        "expense_category": "all",
        "title": "Presumptive Taxation for Specified Professionals (Section 44ADA)",
        "description": "Specified professionals with gross receipts up to ₹75 Lakhs (where digital receipts >= 95%) can declare 50% of gross revenue as taxable net profit without maintaining extensive detailed books of accounts or undergoing tax audit under Sec 44AB.",
        "deductibility_status": "PRESUMPTIVE_DEEMED_EXPENSE",
        "eligibility_conditions": [
            "Profession belongs to specified categories: Technical Consultancy, IT, Engineering, Architecture, Accountancy, Legal",
            "Total gross receipts in financial year do not exceed ₹75 Lakhs (or ₹50 Lakhs if cash > 5%)",
            "50% of gross receipts deemed as expenses automatically"
        ],
        "limitations": {
            "max_gross_turnover": 7500000.0,
            "presumptive_profit_rate": 0.50,
            "further_expense_deductions_prohibited": True
        },
        "evidence_requirements": [
            "Annual Bank statement demonstrating total client inflow",
            "Invoices issued to clients",
            "Verification of 95%+ digital payments via banking channels"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 44ADA read with Section 44AA & 44AB",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.2",
        "last_verified_date": "2025-01-15"
    },

    # 7. Office Furniture & Ergonomic Equipment (India)
    {
        "rule_code": "IN-SEC32-FURN-01",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "office",
        "title": "Office Furniture & Ergonomic Chairs (Block of Assets - Furniture)",
        "description": "Ergonomic chairs (Herman Miller, etc.) and motorized desks utilized for professional work qualify as 'Furniture and Fittings' subject to 10% Written Down Value (WDV) depreciation.",
        "deductibility_status": "CAPITAL_DEPRECIATION",
        "eligibility_conditions": [
            "Asset purchased and installed in primary home office or studio",
            "Invoice in taxpayer name"
        ],
        "limitations": {
            "depreciation_rate": 0.10,
            "less_than_180_days_depreciation_rate": 0.05
        },
        "evidence_requirements": [
            "Tax Invoice with GST details",
            "Payment proof",
            "Home office allocation documentation"
        ],
        "effective_date": "2024-04-01",
        "source_statute": "Income Tax Act 1961, Section 32(1)(ii)",
        "statute_citation_url": "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-15"
    },

    # 8. US IRS Schedule C - Ordinary & Necessary Expenses
    {
        "rule_code": "US-IRC162-GEN-01",
        "country": "United States",
        "jurisdiction": "Internal Revenue Service (IRS)",
        "tax_year": "2024",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "software",
        "title": "Ordinary and Necessary Trade or Business Expenses",
        "description": "Software, web hosting, domain registrations, and cloud compute used in your trade or business are 100% deductible as ordinary and necessary business expenses under IRC Section 162.",
        "deductibility_status": "DEDUCTIBLE",
        "eligibility_conditions": [
            "Ordinary: common and accepted in your trade of business",
            "Necessary: helpful and appropriate for your business",
            "Documented with contemporaneous receipt or electronic statement"
        ],
        "limitations": {
            "personal_portion_non_deductible": True
        },
        "evidence_requirements": [
            "Electronic invoice or receipt with vendor name and amount",
            "Credit card or bank statement proof of debit",
            "Business justification"
        ],
        "effective_date": "2024-01-01",
        "source_statute": "Internal Revenue Code (IRC) Section 162 / IRS Publication 535",
        "statute_citation_url": "https://www.irs.gov/publications/p535",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-10"
    },

    # 9. US IRS Business Meals (50% limitation)
    {
        "rule_code": "US-IRC274-MEAL-01",
        "country": "United States",
        "jurisdiction": "Internal Revenue Service (IRS)",
        "tax_year": "2024",
        "taxpayer_type": "Freelancer",
        "profession": "All",
        "expense_category": "meals",
        "title": "Business Meals with Clients (50% Limit Rule)",
        "description": "Meals with clients or prospects during business discussions are subject to a strict 50% statutory deduction limit under IRC Section 274(n). Lavish meals are disallowed.",
        "deductibility_status": "PARTIALLY_DEDUCTIBLE",
        "eligibility_conditions": [
            "Direct business discussion took place before, during, or immediately after meal",
            "Taxpayer or employee must be present at the meal",
            "Not lavish or extravagant"
        ],
        "limitations": {
            "statutory_deduction_limit": 0.50
        },
        "evidence_requirements": [
            "Itemized receipt with date, location, amount",
            "Name of business associates present",
            "Business topic discussed"
        ],
        "effective_date": "2024-01-01",
        "source_statute": "Internal Revenue Code (IRC) Section 274(n) / IRS Publication 463",
        "statute_citation_url": "https://www.irs.gov/publications/p463",
        "rule_version": "v2024.1",
        "last_verified_date": "2025-01-10"
    }
]
