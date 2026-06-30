from sqlalchemy.orm import Session
from ..models.audit import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    status: str,
    performed_by: str,
):
    """
    Create an audit log entry.
    """

    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        status=status,
        performed_by=performed_by,
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit
