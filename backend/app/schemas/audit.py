from pydantic import BaseModel
from datetime import datetime


class AuditBase(BaseModel):
    action: str
    performed_by: str
    details: str | None = None


class AuditResponse(AuditBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True