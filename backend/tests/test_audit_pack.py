import os
import pytest
from app.core.database import SessionLocal, Base, engine
from app.services.audit_pack_generator import audit_pack_generator
from app.api.v1.endpoints.admin import seed_demo_database

def test_audit_pack_generation():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_database(db)
        from app.models.user import User
        user = db.query(User).first()
        assert user is not None

        pkg = audit_pack_generator.generate_pdf_package(
            db=db,
            user_id=user.id,
            tax_year="2024-2025",
            assumptions_note="Automated test generation"
        )
        assert pkg is not None
        assert os.path.exists(pkg.pdf_file_path)
        assert len(pkg.package_sha256) == 64  # Valid SHA-256
        assert pkg.total_claimed_deductions > 0
    finally:
        db.close()
