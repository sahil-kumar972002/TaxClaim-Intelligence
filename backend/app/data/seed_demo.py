"""
Demo Seed Data for TaxClaim AI
Includes 6 Freelancer & Gig Worker Personas and 8 realistic transactions.
"""

from typing import List, Dict, Any

DEMO_PERSONAS: List[Dict[str, Any]] = [
    {
        "email": "alex.dev@taxclaim.ai",
        "full_name": "Aarav 'Alex' Sharma",
        "role": "taxpayer",
        "profession": "Software Developer",
        "business_type": "Freelance/Self-Employed",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Sec 44ADA (Presumptive)",
        "estimated_annual_income": 3200000.0,
        "business_use_patterns": {"laptop": 0.95, "internet": 0.80, "phone": 0.70, "home_office": 0.30},
        "recurring_expenses": ["AWS Cloud", "GitHub", "JetBrains", "Jio Fiber"],
        "business_description": "Full-stack cloud architect building high-throughput microservices and generative AI tools for global clients."
    },
    {
        "email": "priya.design@taxclaim.ai",
        "full_name": "Priya Patel",
        "role": "taxpayer",
        "profession": "Graphic Designer",
        "business_type": "Freelance/Sole Proprietor",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Sec 44ADA (Presumptive)",
        "estimated_annual_income": 2100000.0,
        "business_use_patterns": {"hardware": 0.90, "internet": 0.75, "software": 1.0},
        "recurring_expenses": ["Adobe Creative Cloud", "Figma", "Envato Elements"],
        "business_description": "Brand identity and UI/UX product designer crafting digital design systems for tech startups."
    },
    {
        "email": "sam.creator@taxclaim.ai",
        "full_name": "Samir 'Sam' Sen",
        "role": "taxpayer",
        "profession": "Content Creator",
        "business_type": "Sole Proprietorship",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Regular PGBP",
        "estimated_annual_income": 2800000.0,
        "business_use_patterns": {"camera": 1.0, "studio": 0.85, "editing_pc": 0.90},
        "recurring_expenses": ["Epidemic Sound", "YouTube Premium", "Canva Pro"],
        "business_description": "Educational tech YouTuber and video editor producing deep dives on AI, robotics, and coding."
    },
    {
        "email": "raj.driver@taxclaim.ai",
        "full_name": "Rajesh 'Raj' Kumar",
        "role": "taxpayer",
        "profession": "Uber / Ride Gig Worker",
        "business_type": "Individual Gig Worker",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Sec 44AD (Presumptive)",
        "estimated_annual_income": 950000.0,
        "business_use_patterns": {"fuel": 0.85, "vehicle_maintenance": 0.90, "phone": 0.75},
        "recurring_expenses": ["Fastag Toll", "Vehicle Insurance", "Airtel Mobile"],
        "business_description": "Rideshare and logistics platform driver operating on Uber and Urban Company."
    },
    {
        "email": "elena.tutor@taxclaim.ai",
        "full_name": "Elena D'Souza",
        "role": "taxpayer",
        "profession": "Online STEM Tutor",
        "business_type": "Freelance Educator",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Sec 44ADA (Presumptive)",
        "estimated_annual_income": 1600000.0,
        "business_use_patterns": {"drawing_tablet": 1.0, "zoom": 1.0, "internet": 0.80},
        "recurring_expenses": ["Zoom Pro", "Miro Board", "Khan Academy Supporter"],
        "business_description": "Online Mathematics and Physics mentor teaching university students across the US and UK."
    },
    {
        "email": "admin@taxclaim.ai",
        "full_name": "TaxClaim Compliance Admin",
        "role": "admin",
        "profession": "Chartered Tax Auditor",
        "business_type": "Platform Admin",
        "country": "India",
        "jurisdiction": "Income Tax Department (CBDT)",
        "tax_year": "2024-2025",
        "tax_regime": "Corporate",
        "estimated_annual_income": 5000000.0,
        "business_use_patterns": {},
        "recurring_expenses": [],
        "business_description": "Admin and AI tax auditor monitoring regulatory compliance and ML pipeline health."
    }
]

# The 7 core requested demo documents + 1 anomaly test expense
DEMO_EXPENSES: List[Dict[str, Any]] = [
    # 1. Laptop Invoice
    {
        "merchant": "Apple India Pvt Ltd",
        "transaction_date": "2024-06-12",
        "amount": 249900.0,
        "currency": "INR",
        "tax_amount": 38120.34,
        "invoice_number": "APL-IN-2024-91823",
        "category": "hardware",
        "payment_method": "Credit Card",
        "business_purpose": "Primary workstation for microservices engineering and local LLM fine-tuning",
        "business_use_percentage": 0.95,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """TAX INVOICE
Apple India Private Limited
UB City, 19th Floor, Concorde Tower C, Vittal Mallya Road, Bengaluru 560001
GSTIN: 29AABCA0123M1Z8
Invoice No: APL-IN-2024-91823
Date: 12-Jun-2024
Customer: Aarav Sharma (Software Consultant)
Item: 16-inch MacBook Pro - Space Black
Apple M3 Max chip with 16-core CPU, 40-core GPU, 36GB Unified Memory, 1TB SSD
Subtotal: ₹2,11,779.66
IGST (18%): ₹38,120.34
Grand Total: ₹2,49,900.00
Payment Method: HDFC Business Regalia Card ending in 4092
Serial No: C02G901ABCDE"""
    },

    # 2. Adobe Subscription
    {
        "merchant": "Adobe Systems India",
        "transaction_date": "2024-07-05",
        "amount": 3499.0,
        "currency": "INR",
        "tax_amount": 533.75,
        "invoice_number": "ADB-INV-883019",
        "category": "software",
        "payment_method": "Credit Card",
        "business_purpose": "UI/UX asset generation and visual wireframing for client projects",
        "business_use_percentage": 1.0,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """Adobe Creative Cloud
Tax Invoice / Payment Receipt
Invoice Number: ADB-INV-883019
Date: 05 July 2024
Plan: Creative Cloud All Apps - 1 Month Subscription
Subtotal: ₹2,965.25
IGST 18%: ₹533.75
Total Amount Paid: ₹3,499.00
Payment Method: Visa ending in 8129
Billed to: Aarav Sharma"""
    },

    # 3. Internet Bill
    {
        "merchant": "Reliance Jio Infocomm Ltd",
        "transaction_date": "2024-08-01",
        "amount": 1499.0,
        "currency": "INR",
        "tax_amount": 228.66,
        "invoice_number": "JIO-FBR-7482910",
        "category": "internet",
        "payment_method": "UPI",
        "business_purpose": "High-speed 300 Mbps fiber broadband for client video calls and remote cluster deployment",
        "business_use_percentage": 0.80,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """JioFiber Tax Invoice
Reliance Jio Infocomm Limited
CIN: U72900GJ2007PLC105869
Invoice #: JIO-FBR-7482910
Bill Date: 01-Aug-2024
Plan: JioFiber 300 Mbps Unlimited Data
Gross Amount: ₹1,270.34
CGST 9%: ₹114.33
SGST 9%: ₹114.33
Total Payable: ₹1,499.00
Payment Mode: UPI Ref 421498102391"""
    },

    # 4. Travel Receipt
    {
        "merchant": "IndiGo Airlines (InterGlobe)",
        "transaction_date": "2024-09-14",
        "amount": 7850.0,
        "currency": "INR",
        "tax_amount": 420.0,
        "invoice_number": "6E-PNR-W8K9LQ",
        "category": "travel",
        "payment_method": "Credit Card",
        "business_purpose": "Domestic round-trip flight from Delhi to Bengaluru to attend AWS Cloud Architecture Summit with client team",
        "business_use_percentage": 1.0,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """InterGlobe Aviation Limited (IndiGo)
Passenger Electronic Ticket Receipt
Booking Ref / PNR: W8K9LQ
Date: 14 Sep 2024
Passenger: SHARMA / AARAV MR
Flight: 6E 214 Delhi (DEL) -> Bengaluru (BLR)
Base Fare: ₹6,930.00
User Development Fee & CGST/SGST: ₹920.00
Total Fare: ₹7,850.00
Payment: Card ending 4092"""
    },

    # 5. Restaurant Receipt (Needs Review / Missing Attendee Evidence)
    {
        "merchant": "The Bombay Canteen",
        "transaction_date": "2024-09-15",
        "amount": 4850.0,
        "currency": "INR",
        "tax_amount": 230.95,
        "invoice_number": "TBC-DIN-0941",
        "category": "meals",
        "payment_method": "Credit Card",
        "business_purpose": "Business dinner meeting with VP of Product at FinTech client company",
        "business_use_percentage": 0.50,
        "status": "NEEDS_REVIEW",
        "raw_text": """The Bombay Canteen
Unit-1, Process House, Kamala Mills, Lower Parel, Mumbai
TAX INVOICE
Bill No: TBC-DIN-0941
Date: 15-Sep-2024  Time: 21:40
Table: 14 (Guests: 2)
1 Canteen Feast Platter: ₹2,400.00
2 Sparkling Mineral: ₹600.00
1 Smoked Pork Tacos: ₹950.00
1 Special Dessert: ₹669.05
Subtotal: ₹4,619.05
CGST 2.5%: ₹115.48
SGST 2.5%: ₹115.47
Total: ₹4,850.00
Payment: Amex ending 1004"""
    },

    # 6. Cloud Hosting Invoice
    {
        "merchant": "Amazon Web Services India",
        "transaction_date": "2024-09-02",
        "amount": 18450.0,
        "currency": "INR",
        "tax_amount": 2814.41,
        "invoice_number": "AWS-IN-9481029",
        "category": "software",
        "payment_method": "Credit Card",
        "business_purpose": "Staging servers, GPU inference instances, and S3 data pipelines for active SaaS clients",
        "business_use_percentage": 1.0,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """Amazon Web Services India Private Limited
Tax Invoice # AWS-IN-9481029
Invoice Date: September 2, 2024
Customer: Aarav Sharma Cloud Solutions
GSTIN: 27AABCA9999M1Z3
Services Summary:
- Amazon Elastic Compute Cloud (EC2): ₹11,200.00
- Amazon Simple Storage Service (S3): ₹1,850.00
- Amazon Relational Database Service (RDS): ₹2,585.59
Total Charges Before Tax: ₹15,635.59
IGST (18%): ₹2,814.41
Total Amount Due: ₹18,450.00
Payment Status: PAID via Corporate Visa ending 4092"""
    },

    # 7. Office Chair Invoice (Ergonomic Capital Item)
    {
        "merchant": "Herman Miller India",
        "transaction_date": "2024-05-20",
        "amount": 89900.0,
        "currency": "INR",
        "tax_amount": 13713.56,
        "invoice_number": "HM-BLR-2024-059",
        "category": "office",
        "payment_method": "Bank Transfer",
        "business_purpose": "Ergonomic Aeron chair for home office workstation setup",
        "business_use_percentage": 0.85,
        "status": "AUTO_RECOMMENDED",
        "raw_text": """Herman Miller Retail India
Tax Invoice
Invoice No: HM-BLR-2024-059
Date: 20-May-2024
Sold to: Aarav Sharma
Description: Herman Miller Aeron Chair - Size B (Graphite)
PostureFit SL with Fully Adjustable Arms & Hard Floor Casters
Net Price: ₹76,186.44
GST @ 18%: ₹13,713.56
Grand Total: ₹89,900.00
Payment: RTGS Ref / UTR: HDFC000123894819"""
    },

    # 8. Anomaly Demo Item: Duplicate Invoice Attempt (flagged for review)
    {
        "merchant": "Adobe Systems India",
        "transaction_date": "2024-07-06",
        "amount": 3499.0,
        "currency": "INR",
        "tax_amount": 533.75,
        "invoice_number": "ADB-INV-883019",  # EXACT DUPLICATE INVOICE NUMBER
        "category": "software",
        "payment_method": "Credit Card",
        "business_purpose": "Duplicate test entry for Adobe Cloud",
        "business_use_percentage": 1.0,
        "status": "NEEDS_REVIEW",
        "raw_text": """Adobe Creative Cloud - Resubmitted Copy
Invoice Number: ADB-INV-883019
Total: ₹3,499.00"""
    }
]
