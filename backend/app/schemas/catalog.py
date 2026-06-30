from pydantic import BaseModel
from datetime import datetime


class DatasetCatalogBase(BaseModel):
    dataset_name: str
    business_domain: str
    owner: str
    sensitivity: str
    access_level: str
    tags: str | None = None


class DatasetCatalogResponse(DatasetCatalogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
