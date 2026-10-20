from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    business_profiles,
    documents,
    expenses,
    tax_rules,
    anomalies,
    simulator,
    digital_twin,
    audit_pack,
    copilot,
    admin
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(business_profiles.router, prefix="/profiles", tags=["Business Profiles"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents & OCR"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["Expense Intelligence"])
api_router.include_router(tax_rules.router, prefix="/tax-rules", tags=["Statutory Tax Rules"])
api_router.include_router(anomalies.router, prefix="/anomalies", tags=["Risk & Anomaly Detection"])
api_router.include_router(simulator.router, prefix="/simulator", tags=["Tax What-If Simulator"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["Tax Digital Twin"])
api_router.include_router(audit_pack.router, prefix="/audit-pack", tags=["Audit Evidence Pack"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["TaxClaim Copilot Assistant"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin & Model Monitoring"])
