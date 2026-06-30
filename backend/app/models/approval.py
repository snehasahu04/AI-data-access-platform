from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, text
from ..database.connection import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("access_requests.id"),
        nullable=False
    )

    approver_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    decision = Column(
        String,
        nullable=False
    )

    comments = Column(Text)

    approved_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )