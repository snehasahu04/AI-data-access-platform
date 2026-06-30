from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import settings


Base = declarative_base()


def create_engine_from_settings():
    database_url = settings.DATABASE_URL or "sqlite:///./app.db"

    if database_url.startswith("postgresql"):
        try:
            engine = create_engine(database_url, echo=True)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return engine
        except SQLAlchemyError:
            fallback_engine = create_engine("sqlite:///./app.db", echo=True)
            initialize_database(fallback_engine)
            return fallback_engine

    engine = create_engine(database_url, echo=True)
    initialize_database(engine)
    return engine


def initialize_database(engine):
    from ..models.approval import Approval
    from ..models.dataset import Dataset
    from ..models.request import AccessRequest
    from ..models.user import User

    Base.metadata.create_all(bind=engine)


engine = create_engine_from_settings()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()