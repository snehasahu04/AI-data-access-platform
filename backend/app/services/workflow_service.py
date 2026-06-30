from typing import Dict, Optional
from sqlalchemy.orm import Session

from .request_intent_service import parse_request_text
from .catalog_service import recommend_datasets
from .governance_service import determine_approval_path


def build_access_request_workflow(
    db: Session,
    request_text: str,
    business_domain: Optional[str] = None,
    tags: Optional[str] = None
) -> Dict:
    intent = parse_request_text(request_text)
    selected_business_domain = business_domain or intent.business_domain

    datasets = recommend_datasets(
        db=db,
        business_domain=selected_business_domain,
        tags=tags,
        top_n=5
    )

    dataset_names = [d.dataset_name for d in datasets]
    selected_dataset = datasets[0] if datasets else None

    metadata = {
        "dataset_name": selected_dataset.dataset_name if selected_dataset else "unknown",
        "sensitivity": selected_dataset.sensitivity if selected_dataset else "public",
        "access_level": selected_dataset.access_level if selected_dataset else "read"
    }

    workflow = determine_approval_path(metadata)

    return {
        "intent": intent.dict(),
        "recommended_datasets": dataset_names,
        "workflow": workflow,
        "dataset_metadata": metadata
    }