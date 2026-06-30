from sqlalchemy.orm import Session

from ..models.request import AccessRequest
from ..models.dataset import Dataset
from .audit_service import create_audit_log


def create_access_request(
    db: Session, user_id: int, dataset_id: int, request_text: str
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise Exception("Dataset not found")

    if dataset.sensitivity.lower() == "public":
        status = "APPROVED"
    else:
        status = "PENDING_APPROVAL"

    request = AccessRequest(
        user_id=user_id, dataset_id=dataset_id, request_text=request_text, status=status
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    print("Request ID:", request.id)
    print("Created At:", request.created_at)

    create_audit_log(
        db=db,
        user_id=user_id,
        action="ACCESS_REQUEST_CREATED",
        entity_type="DATASET",
        entity_id=dataset_id,
        status=status,
        performed_by=str(user_id),
    )

    db.refresh(request)

    return request
