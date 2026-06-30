from pydantic import BaseModel
from datetime import datetime


class DatasetBase(BaseModel):
    dataset_name: str
    business_domain: str
    owner: str
    sensitivity: str
    access_level: str
    tags: str | None = None


class DatasetCreate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
