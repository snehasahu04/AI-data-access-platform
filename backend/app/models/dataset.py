from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..database.connection import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    dataset_name = Column(String, nullable=False)

    business_domain = Column(String, nullable=False)

    owner = Column(String, nullable=False)

    sensitivity = Column(String, nullable=False)

    access_level = Column(String, nullable=False)

    tags = Column(String)

    created_at = Column(TIMESTAMP)
