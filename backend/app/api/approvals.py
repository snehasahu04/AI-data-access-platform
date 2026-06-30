from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.approval import Approval

from ..schemas.approval import (
    ApprovalCreate,
    ApprovalResponse
)

from ..services.approval_service import process_approval


router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)

@router.get("/")
def get_approvals(db: Session = Depends(get_db)):
    try:
        return db.query(Approval).all()
    except SQLAlchemyError:
        return []

# Approve or reject access request
@router.post("/", response_model=ApprovalResponse)
def approve_request(
    approval: ApprovalCreate,
    db: Session = Depends(get_db)
):

    result = process_approval(
        db=db,
        request_id=approval.request_id,
        approver_id=approval.approver_id,
        decision=approval.decision,
        comments=approval.comments
    )

    return result