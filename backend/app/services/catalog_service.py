from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models.dataset import Dataset
from ..utils import normalize_text


def search_datasets(
    db: Session,
    term: Optional[str] = None,
    business_domain: Optional[str] = None,
    sensitivity: Optional[str] = None,
    access_level: Optional[str] = None,
    tags: Optional[str] = None
) -> List[Dataset]:
    query = db.query(Dataset)

    if term:
        normalized = f"%{normalize_text(term)}%"
        query = query.filter(
            or_(
                Dataset.dataset_name.ilike(normalized),
                Dataset.owner.ilike(normalized),
                Dataset.tags.ilike(normalized),
                Dataset.business_domain.ilike(normalized)
            )
        )

    if business_domain:
        query = query.filter(Dataset.business_domain.ilike(f"%{normalize_text(business_domain)}%"))

    if sensitivity:
        query = query.filter(Dataset.sensitivity.ilike(f"%{normalize_text(sensitivity)}%"))

    if access_level:
        query = query.filter(Dataset.access_level.ilike(f"%{normalize_text(access_level)}%"))

    if tags:
        query = query.filter(Dataset.tags.ilike(f"%{normalize_text(tags)}%"))

    return query.order_by(Dataset.business_domain, Dataset.sensitivity).all()


def recommend_datasets(
    db: Session,
    business_domain: Optional[str] = None,
    tags: Optional[str] = None,
    top_n: int = 5
) -> List[Dataset]:
    query = db.query(Dataset)

    if business_domain:
        query = query.filter(Dataset.business_domain.ilike(f"%{normalize_text(business_domain)}%"))

    if tags:
        query = query.filter(Dataset.tags.ilike(f"%{normalize_text(tags)}%"))

    return query.order_by(Dataset.sensitivity, Dataset.dataset_name).limit(top_n).all()
