from pydantic import BaseModel
from datetime import datetime


class ApprovalBase(BaseModel):
    request_id: int
    approver_id: int
    decision: str
    comments: str | None = None


class ApprovalCreate(ApprovalBase):
    pass


class ApprovalResponse(ApprovalBase):
    id: int
    approved_at: datetime

    class Config:
        from_attributes = True