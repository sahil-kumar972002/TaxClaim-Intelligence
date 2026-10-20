import os
import hashlib
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.audit_package import AuditPackage
from app.schemas.audit_pack import AuditPackGenerateRequest, AuditPackResponse
from app.services.audit_pack_generator import audit_pack_generator
from app.core.audit_logger import log_audit_event

router = APIRouter()

@router.post("/generate", response_model=AuditPackResponse)
def generate_audit_package(
    req: AuditPackGenerateRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    pkg = audit_pack_generator.generate_pdf_package(
        db=db,
        user_id=user.id,
        tax_year=req.tax_year,
        assumptions_note=req.assumptions_note or ""
    )
    log_audit_event(db, user.id, "GENERATE_AUDIT_PACK", "AuditPackage", pkg.id, {"sha256": pkg.package_sha256})
    return pkg

@router.get("/", response_model=List[AuditPackResponse])
def list_audit_packages(db: Session = Depends(get_db)):
    return db.query(AuditPackage).order_by(AuditPackage.generated_at.desc()).all()

@router.get("/{package_id}/download")
def download_audit_package(package_id: str, db: Session = Depends(get_db)):
    pkg = db.query(AuditPackage).filter(AuditPackage.id == package_id).first()
    if not pkg or not os.path.exists(pkg.pdf_file_path):
        raise HTTPException(status_code=404, detail="Audit package PDF file not found")

    return FileResponse(
        path=pkg.pdf_file_path,
        media_type="application/pdf",
        filename=f"{pkg.package_reference}.pdf"
    )

@router.get("/{package_id}/verify")
def verify_package_integrity(package_id: str, db: Session = Depends(get_db)):
    pkg = db.query(AuditPackage).filter(AuditPackage.id == package_id).first()
    if not pkg or not os.path.exists(pkg.pdf_file_path):
        raise HTTPException(status_code=404, detail="Package not found")

    hasher = hashlib.sha256()
    with open(pkg.pdf_file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    current_hash = hasher.hexdigest()

    is_tamper_free = (current_hash == pkg.package_sha256)
    return {
        "package_reference": pkg.package_reference,
        "recorded_sha256": pkg.package_sha256,
        "current_sha256": current_hash,
        "integrity_verified": is_tamper_free,
        "status": "VALID_COURT_READY" if is_tamper_free else "INTEGRITY_COMPROMISED"
    }
