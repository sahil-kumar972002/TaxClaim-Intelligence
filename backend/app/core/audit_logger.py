import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

# Standard logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s")
logger = logging.getLogger("taxclaim.audit")

def log_audit_event(
    db: Session,
    user_id: Optional[str],
    action: str,
    resource_type: str,
    resource_id: Optional[str],
    diff_payload: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """
    Appends an immutable audit log entry to the database and system logs.
    Ensures every tax classification, decision, and document action is traceable.
    """
    from app.models.audit_event import AuditEvent
    import uuid

    try:
        event = AuditEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address or "127.0.0.1",
            user_agent=user_agent or "TaxClaim-Agent/1.0",
            diff_payload=diff_payload or {}
        )
        db.add(event)
        db.commit()
        logger.info(f"AUDIT_RECORDED: user={user_id} action={action} resource={resource_type}:{resource_id}")
    except Exception as e:
        logger.error(f"AUDIT_LOG_FAILURE: Failed to write audit event: {str(e)}")
