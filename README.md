# TaxClaim AI — Intelligent Tax Intelligence & Evidence Management Platform

> **"Evidence-backed, explainable, jurisdiction-aware tax intelligence for freelancers & gig workers."**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React: 18+](https://img.shields.io/badge/Frontend-React_18+-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/UI-TailwindCSS_Dark_Fintech-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Audit Integrity](https://img.shields.io/badge/Integrity-SHA--256_Cryptographic_Seal-10B981)](#)

---

## 🌟 Executive Overview

**TaxClaim AI** is a production-grade tax intelligence platform that bridges financial documents and tax laws. Rather than acting as a simple receipt classifier, TaxClaim AI ingests receipts, invoices, PDFs, broadband bills, and bank statements and converts them into **statutorily substantiated, audit-ready deductions**.

### 🛡️ Zero-Hallucination Architectural Separation
The system strictly enforces separation between:
1. **AI Predictions:** OCR entity extraction, 16-category ML classification, and anomaly outlier detection.
2. **Statutory Tax Rules:** Deterministic legal rules with verified citations from official authorities (Indian Income Tax Act 1961, CBDT circulars, Section 37(1), Section 32, Section 44ADA, and US IRC 162/274).
3. **Evidentiary Proofs:** Cryptographic SHA-256 document hashing and 7-factor Evidence Strength scoring.
4. **Human-in-the-Loop Confirmation:** High-confidence routine cases can be auto-recommended, while ambiguous items require taxpayer verification.

---

## 🎯 Key Platform Capabilities

1. **Smart Multi-Format Ingestion & OCR:**
   - Drag & drop PDFs, receipt images, flight tickets, and bills.
   - Computes SHA-256 digital fingerprint for audit chain of custody.
   - Extracts merchant, date, amount, currency, tax breakdowns (GST/CGST/SGST/VAT), and invoice numbers with PII redaction (PAN/SSN/Card masking).

2. **Jurisdiction-Aware Statutory Tax Engine:**
   - Retrieves applicable tax laws based on country, jurisdiction, tax year, profession, and category.
   - Evaluates capital depreciation (e.g. Laptops @ 40% WDV under Section 32) vs 100% revenue deductions under Section 37(1).
   - Enforces statutory caps like Section 40A(3) cash payment disallowance (>₹10,000) and business-use apportionments (Section 38(2)).

3. **7-Factor Evidence Strength Index:**
   - Calculates weighted evidence quality: Receipt Document (20%), Merchant (15%), Date (10%), Amount & Tax (15%), Payment Trail (15%), Business Nexus (15%), Business-Use Allocation (10%).

4. **Missing Evidence Copilot:**
   - Doesn't simply reject expenses with partial data.
   - Asks targeted interactive questions (business purpose justification, business-use %, proof of payment reference) and previews score boosts in real-time.

5. **Multi-Dimensional Anomaly & Deduplication Engine:**
   - Scikit-learn **Isolation Forest** detects numerical spikes and category median outliers.
   - Real-time deduplication flags exact invoice number collisions and duplicate receipt submissions to prevent penalty under tax scrutiny.

6. **Dynamic Tax What-If Simulator:**
   - Interactive sliders for annual turnover, actual expenses, and business-use percentage.
   - Live side-by-side comparison between **Section 44ADA (Presumptive 50% Deemed Profit Scheme)** and **Regular PGBP (Itemized Actual Expenses)**.

7. **Tax Digital Twin:**
   - Continuously updated representation of the taxpayer's financial health, audit defense readiness radar, and proactive year-end advice.

8. **1-Click Audit Pack Studio (PDF Generator):**
   - Compiles court-admissible, multi-page PDF audit evidence packages using ReportLab.
   - Includes executive summaries, itemized ledgers, statutory citations, and an embedded tamper-proof SHA-256 cryptographic seal.

9. **TaxClaim Copilot:**
   - Grounded conversational assistant that answers freelancer tax questions citing exact legal codes with zero legal hallucination.

10. **ML Governance & Model Monitoring:**
    - Live tracking of classification accuracy, precision, recall, macro F1, confusion matrix, and Population Stability Index (PSI) drift detection.

---

## 🏗️ Tech Stack

### Frontend
- **Framework:** React 18 / 19 + TypeScript
- **Styling:** Tailwind CSS (Fintech Dark Navy & Glassmorphism theme)
- **Charts:** Recharts (Area trends, radial distributions, 6-dimension defense radar)
- **Icons:** Lucide React
- **API Client:** Axios
- **Bundler:** Vite

### Backend
- **Framework:** Python 3.11 + FastAPI
- **ASGI Server:** Uvicorn
- **ORM:** SQLAlchemy 2.0 (PostgreSQL & SQLite compatible)
- **Data Validation:** Pydantic v2
- **Document PDF Engine:** ReportLab
- **Security:** Native Bcrypt, Python-Jose (JWT), SHA-256 Hashing, PII Sanitizer

### Machine Learning & Data Science
- **Classification:** Scikit-Learn (TF-IDF Vectorizer + Calibrated Logistic Regression)
- **Anomaly Detection:** Scikit-Learn Isolation Forest + Statistical Z-Score
- **Entity Extraction:** Financial Regex NER & Pattern Matcher

---

## 📁 Repository Structure

```
TaxClaim-Intelligence/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/      # REST API endpoints (auth, expenses, ocr, simulator, etc.)
│   │   ├── core/                  # Security, database, config, PII sanitizer, audit logger
│   │   ├── data/                  # Statutory tax rules (CBDT & IRS) and demo seeds
│   │   ├── ml/                    # Classifier, anomaly detector, NER, model monitor
│   │   ├── models/                # 20+ SQLAlchemy ORM models
│   │   ├── schemas/               # Pydantic v2 request/response schemas
│   │   └── services/              # Rules engine, evidence engine, PDF generator, simulator
│   ├── tests/                     # Pytest suite (rules, evidence, anomaly, PDF tests)
│   ├── main.py                    # FastAPI entrypoint with lifespan auto-seeding
│   └── requirements.txt           # Backend Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/            # Command center, expenses, ingestion, simulator, etc.
│   │   ├── services/api.ts        # Axios API client
│   │   ├── types/index.ts         # TypeScript definitions
│   │   ├── App.tsx                # Master Command Center View
│   │   └── index.css              # Custom fintech glassmorphism styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 18+ & npm**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/sahil-kumar972002/TaxClaim-Intelligence.git
cd TaxClaim-Intelligence
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend test suite
python -m pytest tests

# Start FastAPI server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Backend will be available at:
- **API Base:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev -- --host 127.0.0.1 --port 5173
```
Frontend Web Command Center will be live at:
- **Web App:** `http://localhost:5173`

---

## 🧪 Automated Testing

The backend includes a comprehensive test suite verifying the deterministic statutory rules engine, evidence math, deduplication, and PDF generation:

```bash
cd backend
.venv\Scripts\pytest tests
```
*Output: 7 passed in 3.47s (100% pass rate)*

---

## 📄 License
This project is licensed under the MIT License.
