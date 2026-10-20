import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaxClaim AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "taxclaim_super_secret_jwt_key_development_2026_99x")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: SQLite fallback for instant zero-friction local run, PostgreSQL production ready
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./taxclaim.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*"
    ]
    
    # Document storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./storage/documents")
    AUDIT_DIR: str = os.getenv("AUDIT_DIR", "./storage/audit_packages")
    MAX_UPLOAD_SIZE_BYTES: int = 25 * 1024 * 1024  # 25 MB
    
    # AI Engine Thresholds
    AUTO_CONFIRM_CONFIDENCE_THRESHOLD: float = 0.88
    EVIDENCE_STRENGTH_GOOD_THRESHOLD: float = 0.75
    ANOMALY_CONTAMINATION_RATE: float = 0.05
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Ensure storage directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.AUDIT_DIR, exist_ok=True)
