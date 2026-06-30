from sqlalchemy.orm import Session

from ..models.approval import Approval
from ..models.request import AccessRequest
from .audit_service import create_audit_log


def process_approval(
    db: Session,
    request_id: int,
    approver_id: int,
    decision: str,
    comments: str = None
):

    # Find access request
    request = (
        db.query(AccessRequest)
        .filter(AccessRequest.id == request_id)
        .first()
    )

    if not request:
        raise Exception("Access request not found")

    # Save approval decision
    approval = Approval(
        request_id=request_id,
        approver_id=approver_id,
        decision=decision,
        comments=comments
    )

    db.add(approval)

    # Update access request status
    if decision.upper() == "APPROVED":
        request.status = "APPROVED"
    else:
        request.status = "REJECTED"

    db.commit()
    db.refresh(approval)

    # Create audit log
    create_audit_log(
        db=db,
        user_id=request.user_id,
        action="ACCESS_REQUEST_UPDATED",
        entity_type="ACCESS_REQUEST",
        entity_id=request.id,
        status=request.status,
        performed_by=str(approver_id)
    )

    return approval