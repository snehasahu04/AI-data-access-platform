from datetime import datetime
from pydantic import BaseModel


class AccessRequestCreate(BaseModel):
    user_id: int
    dataset_id: int
    request_text: str


class AccessRequestResponse(BaseModel):
    id: int
    user_id: int
    dataset_id: int
    request_text: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True