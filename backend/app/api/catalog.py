from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database.connection import get_db
from ..services.catalog_service import search_datasets, recommend_datasets
from ..schemas.catalog import DatasetCatalogResponse

router = APIRouter(
    prefix="/catalog",
    tags=["Metadata Catalog"]
)


@router.get("/search", response_model=list[DatasetCatalogResponse])
def catalog_search(
    q: Optional[str] = Query(None, description="Search term for datasets"),
    business_domain: Optional[str] = Query(None),
    sensitivity: Optional[str] = Query(None),
    access_level: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return search_datasets(
        db=db,
        term=q,
        business_domain=business_domain,
        sensitivity=sensitivity,
        access_level=access_level,
        tags=tags
    )


@router.get("/recommend", response_model=list[DatasetCatalogResponse])
def catalog_recommend(
    business_domain: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    return recommend_datasets(
        db=db,
        business_domain=business_domain,
        tags=tags,
        top_n=top_n
    )
