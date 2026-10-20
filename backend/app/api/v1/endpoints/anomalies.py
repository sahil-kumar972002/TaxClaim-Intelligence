from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.risk_anomaly import Anomaly, RiskFlag
from app.schemas.anomaly import AnomalyResponse, RiskSummary

router = APIRouter()

@router.get("/", response_model=List[AnomalyResponse])
def list_anomalies(db: Session = Depends(get_db)):
    return db.query(Anomaly).order_by(Anomaly.created_at.desc()).all()

@router.get("/summary", response_model=RiskSummary)
def get_risk_summary(db: Session = Depends(get_db)):
    anomalies = db.query(Anomaly).all()
    critical = sum(1 for a in anomalies if a.anomaly_score >= 0.90)
    high = sum(1 for a in anomalies if 0.80 <= a.anomaly_score < 0.90)
    medium = sum(1 for a in anomalies if 0.60 <= a.anomaly_score < 0.80)
    low = sum(1 for a in anomalies if a.anomaly_score < 0.60)

    portfolio_risk = "LOW"
    if critical > 0:
        portfolio_risk = "CRITICAL"
    elif high > 0:
        portfolio_risk = "ELEVATED"
    elif medium > 1:
        portfolio_risk = "MODERATE"

    return {
        "total_anomalies": len(anomalies),
        "critical_count": critical,
        "high_count": high,
        "medium_count": medium,
        "low_count": low,
        "portfolio_risk_level": portfolio_risk,
        "recent_anomalies": anomalies[:10]
    }

@router.post("/{anomaly_id}/resolve")
def resolve_anomaly(anomaly_id: str, db: Session = Depends(get_db)):
    anom = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anom:
        raise HTTPException(status_code=404, detail="Anomaly not found")
    anom.resolved = True
    db.commit()
    return {"message": "Anomaly marked as resolved by taxpayer."}
