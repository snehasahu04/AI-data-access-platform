from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from ..database.connection import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    action = Column(String(200), nullable=False)

    entity_type = Column(String(100))

    entity_id = Column(Integer)

    status = Column(String(50))

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    performed_by = Column(String(255))
