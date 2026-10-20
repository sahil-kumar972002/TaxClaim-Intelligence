# TaxClaim AI — Intelligent Tax Deduction & Evidence Platform

> **Evidence-backed, explainable, jurisdiction-aware tax intelligence for freelancers & gig workers.**  
> *Zero legal hallucination architecture separating AI predictions, statutory tax rules, and cryptographic evidentiary proofs.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React: 18+](https://img.shields.io/badge/Frontend-React_18+-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/UI-TailwindCSS_Dark_Fintech-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose_Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests: 100% Passed](https://img.shields.io/badge/Tests-100%25_Passing-10B981)](tests)
[![Audit Integrity](https://img.shields.io/badge/Integrity-SHA--256_Cryptographic_Seal-10B981)](#)

---

## ⚡ 60-Second Evaluation Guide for Recruiters & Hiring Managers

Welcome! If you are evaluating this repository, you can launch and test the complete end-to-end full-stack platform in under a minute.

### 🌟 Quick Launch Options

#### Option A: 1-Click Launchers (Recommended)
- **Windows:** Double-click [`start.bat`](start.bat) *(or run `.\start.bat` in cmd/PowerShell)*
- **macOS / Linux:** Run `chmod +x start.sh && ./start.sh`

Both scripts automatically configure environments, install missing packages, start backend & frontend, and launch your browser!

#### Option B: Docker Compose (Zero Configuration)
```bash
docker compose up --build
```

#### Option C: Manual Terminal Launch
```bash
# 1. Backend (Terminal 1)
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# 2. Frontend (Terminal 2)
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

---

### 🌐 Direct Access URLs

| Interface | Local URL | Description |
| :--- | :--- | :--- |
| **Command Center UI** | [`http://localhost:5173`](http://localhost:5173) | Dark-fintech interactive dashboard with charts, modals, simulator & copilot |
| **Interactive API Docs** | [`http://localhost:8000/docs`](http://localhost:8000/docs) | Live Swagger OpenAPI explorer to test all 20+ REST endpoints |
| **System Health Check** | [`http://localhost:8000/health`](http://localhost:8000/health) | Real-time service status and component diagnostics |

---

## 🎯 5-Minute Tour: Key Features to Inspect

When testing the running application, we recommend exploring these 5 core engineering highlights:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Zero-Hallucination Legal Reasoning Chain                                 │
│    Click "Why Decision" on any expense card. Notice the complete audit      │
│    trail citing exact statutory codes (Section 32, Section 37(1), CBDT,     │
│    or US IRC) — deterministic logic, not LLM guesses.                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Missing Evidence Copilot (7-Factor Quality Scoring)                      │
│    Click "Provide Info" on items marked for Review. Add business purpose    │
│    or payment proof to watch the Evidence Strength Score climb live.        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Multi-Dimensional Anomaly & Deduplication Engine                         │
│    Click "Upload Receipt" and use preset invoices to see Isolation Forest   │
│    outlier detection and exact duplicate invoice collision alerts.          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Section 44ADA vs Regular PGBP "What-If" Simulator                        │
│    Switch to the Simulator tab. Drag turnover and expense sliders to see    │
│    real-time tax calculations comparing Presumptive (50%) vs Itemized tax.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. Court-Admissible Audit Pack Studio (ReportLab PDF)                       │
│    Go to "Audit Pack" and generate a tamper-proof PDF report with embedded  │
│    SHA-256 cryptographic hashes for every document in the evidence chain.   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 👥 Pre-Seeded Demonstration Personas

The application automatically seeds 6 realistic freelancer personas across jurisdictions and professions with pre-populated transactions, evidence links, and risk states:

| Persona | Country | Profession | Default Profile Highlights |
| :--- | :---: | :--- | :--- |
| **Priya Sharma** | 🇮🇳 India | Software Engineer | Mix of cloud hosting, Coworking rent, MacBook Pro depreciation (Sec 32) |
| **Alex Miller** | 🇺🇸 USA | Full Stack Contractor | AWS servers, home office deduction, mixed client dinners (IRC 274 cap) |
| **Rohan Mehta** | 🇮🇳 India | Tech Content Creator | Sony A7IV camera, studio lighting, editing plugins, high equipment spend |
| **Ananya Iyer** | 🇮🇳 India | UI/UX Consultant | Figma subscriptions, Adobe CC, client site taxi travel, mobile broadband |
| **Vikram Patel** | 🇮🇳 India | Cloud Architect | Multi-cloud lab instances, certification exams, international software |
| **Sarah Jenkins** | 🇺🇸 USA | Technical Writer | SaaS research tools, high-speed fiber, book purchases, desk ergonomics |

*You can switch between personas directly in the top navigation bar with 1 click.*

---

## 🏛️ System Architecture

TaxClaim AI is engineered with a strict **Zero-Hallucination Architecture**, separating statistical AI predictions from deterministic statutory law and cryptographic proof.

```mermaid
flowchart TD
    subgraph INGESTION["1. Document Ingestion & Verification"]
        Doc[Receipt / Invoice / PDF] --> Hash[SHA-256 Checksum]
        Doc --> PII[PII Masker: PAN / SSN / Card]
        PII --> OCR[Financial NER & Entity Extractor]
    end

    subgraph AI_PREDICTIONS["2. AI & Statistical Layer"]
        OCR --> ML[16-Category Classifier: TF-IDF + Calibrated Logistic]
        OCR --> Anomaly[Isolation Forest Anomaly & Duplicate Detector]
    end

    subgraph STATUTORY_RULES["3. Deterministic Statutory Engine (Zero Hallucination)"]
        ML --> RuleMatch[Tax Law Matcher]
        RuleMatch --> CBDT[India: CBDT Sec 32 / 37 / 44ADA / 40A(3)]
        RuleMatch --> IRS[US: IRC Sec 162 / 274 / MACRS]
    end

    subgraph EVIDENCE_SCORE["4. 7-Factor Evidence Strength Engine"]
        Hash --> EvScore[Evidence Quality Scorer: 0-100%]
        Doc --> Graph[Node-Link Evidence Graph]
    end

    subgraph HUMAN_GATING["5. Human-in-the-Loop Decision Gating"]
        RuleMatch --> Gating{Confidence & Evidence Thresholds}
        Anomaly --> Gating
        EvScore --> Gating
        Gating -->|Score >= 80% & High Confidence| Auto[AUTO RECOMMENDED]
        Gating -->|Ambiguous Nexus or Capital Asset| Review[HUMAN REVIEW REQUIRED]
        Gating -->|Missing Invoice / Payment Proof| Incomplete[INSUFFICIENT DATA]
    end

    subgraph OUTPUTS["6. Deliverables & Audit Defense"]
        Auto --> Pack[Audit Pack PDF with SHA-256 Cryptographic Seal]
        Review --> Copilot[Interactive Evidence Completion Modal]
        Incomplete --> Copilot
        Pack --> Twin[Tax Digital Twin & Readiness Radar]
    end

    style INGESTION fill:#0F172A,stroke:#38BDF8,stroke-width:1px,color:#F8FAFC
    style AI_PREDICTIONS fill:#0F172A,stroke:#818CF8,stroke-width:1px,color:#F8FAFC
    style STATUTORY_RULES fill:#0F172A,stroke:#34D399,stroke-width:1px,color:#F8FAFC
    style EVIDENCE_SCORE fill:#0F172A,stroke:#F59E0B,stroke-width:1px,color:#F8FAFC
    style HUMAN_GATING fill:#0F172A,stroke:#EC4899,stroke-width:1px,color:#F8FAFC
    style OUTPUTS fill:#0F172A,stroke:#10B981,stroke-width:2px,color:#F8FAFC
```

---

## 🛠️ Complete Tech Stack

### Frontend Architecture
- **Framework:** React 18+ with TypeScript (Strict Mode)
- **Design System:** Custom Dark Fintech Navy (`#080C14`, `#0F172A`, `#1E293B`) with Glassmorphism accents
- **Styling:** Tailwind CSS 3.4.17
- **Visualizations:** Recharts (Area trends, radial distribution, 6-dimension defense radar)
- **Icons:** Lucide React
- **API Client:** Axios with dynamic base URL support
- **Bundler:** Vite 8.3

### Backend Architecture
- **Framework:** Python 3.11+ / FastAPI
- **Data Persistence:** SQLAlchemy 2.0 ORM with 20+ relational models
- **Database:** SQLite (default, self-contained) / PostgreSQL (production compatible)
- **Validation:** Pydantic v2 schemas
- **PDF Generation:** ReportLab court-ready multi-page engine
- **Security:** Native Bcrypt password hashing, JWT authentication, SHA-256 document hashing, PII sanitization

### Machine Learning & Data Science
- **Text Classification:** TF-IDF Vectorizer + Calibrated Logistic Regression (16 tax categories)
- **Anomaly Detection:** Scikit-Learn Isolation Forest + Statistical Z-Score outlier detection
- **Model Governance:** Population Stability Index (PSI) drift monitoring, Macro F1, precision, recall, and confusion matrix tracking

---

## 🧪 Automated Test Suite

The platform includes automated test coverage validating deterministic statutory tax logic, evidence scoring, deduplication, and PDF generation:

```bash
cd backend
python -m pytest tests -v
```

**Test Results:**
```text
tests/test_rules_engine.py::test_software_expense_section_37 PASSED       [ 14%]
tests/test_rules_engine.py::test_capital_laptop_depreciation PASSED      [ 28%]
tests/test_rules_engine.py::test_cash_disallowance_section_40a3 PASSED   [ 42%]
tests/test_evidence_engine.py::test_complete_evidence_score PASSED       [ 57%]
tests/test_evidence_engine.py::test_missing_evidence_penalty PASSED      [ 71%]
tests/test_anomaly_detector.py::test_duplicate_invoice_anomaly PASSED    [ 85%]
tests/test_audit_pack.py::test_audit_pack_pdf_generation PASSED          [100%]

============================== 7 passed in 3.47s ===============================
```

---

## ☁️ Deployment Guide

### Deploy Backend (Render / Railway)
1. Fork or push this repository to your GitHub account.
2. Link your repository in [Render](https://render.com) using the included [`render.yaml`](render.yaml) or select **New Web Service**:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version:** `3.11.8`

### Deploy Frontend (Vercel / Netlify)
1. Connect the repository to [Vercel](https://vercel.com):
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variable:** Set `VITE_API_BASE_URL` to your deployed backend URL (e.g., `https://taxclaim-backend.onrender.com/api/v1`).

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
