import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON
from app.core.database import Base

class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), nullable=True, index=True)
    
    model_name = Column(String(100), default="ExpenseClassifier-XGB-v2")
    model_version = Column(String(50), default="2.1.0")
    predicted_category = Column(String(100), nullable=False)
    ground_truth_category = Column(String(100), nullable=True)  # Populated after user confirmation
    confidence = Column(Float, nullable=False)
    feature_contributions = Column(JSON, default=dict)  # Top contributing tokens / factors
    latency_ms = Column(Float, default=12.5)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DriftMetric(Base):
    __tablename__ = "drift_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(100), nullable=False)  # e.g. "KS_Drift_Amount", "PSI_Category_Distribution"
    drift_score = Column(Float, nullable=False)
    threshold = Column(Float, default=0.25)
    status = Column(String(50), default="NORMAL")       # NORMAL, WARNING, DRIFT_DETECTED
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
