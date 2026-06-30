from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services.request_intent_service import parse_request_text
from ..services.catalog_service import recommend_datasets
from ..services.workflow_service import build_access_request_workflow
from ..database.connection import get_db
from sqlalchemy.orm import Session


class RequestIntentInput(BaseModel):
    request_text: str
    business_domain: str | None = None
    tags: str | None = None


class RequestIntentResponse(BaseModel):
    business_domain: str
    requested_resource: str
    time_granularity: str | None = None
    customer_type: str | None = None
    recommended_datasets: list[str] = []
    suggested_query: str | None = None


router = APIRouter(prefix="/ai", tags=["AI Request Understanding"])


@router.post("/classify", response_model=RequestIntentResponse)
def classify_request(input: RequestIntentInput, db: Session = Depends(get_db)):
    workflow = build_access_request_workflow(
        db=db,
        request_text=input.request_text,
        business_domain=input.business_domain,
        tags=input.tags,
    )

    return RequestIntentResponse(
        business_domain=workflow["intent"]["business_domain"],
        requested_resource=workflow["intent"]["requested_resource"],
        time_granularity=workflow["intent"]["time_granularity"],
        customer_type=workflow["intent"]["customer_type"],
        recommended_datasets=workflow["recommended_datasets"],
        suggested_query=workflow["intent"]["suggested_query"],
    )
