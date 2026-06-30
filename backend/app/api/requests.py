from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.request import AccessRequest
from ..schemas.request import AccessRequestCreate, AccessRequestResponse
from ..services.access_service import create_access_request

router = APIRouter(prefix="/requests", tags=["Access Requests"])


@router.get("/")
def get_requests(db: Session = Depends(get_db)):
    try:
        return db.query(AccessRequest).all()
    except SQLAlchemyError:
        return []


@router.post("/", response_model=AccessRequestResponse)
def create_request(request: AccessRequestCreate, db: Session = Depends(get_db)):
    access_request = create_access_request(
        db=db,
        user_id=request.user_id,
        dataset_id=request.dataset_id,
        request_text=request.request_text,
    )

    return access_request
