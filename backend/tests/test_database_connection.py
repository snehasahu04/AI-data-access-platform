import backend.app.database.connection as connection_module
from sqlalchemy.exc import SQLAlchemyError


class DummyEngine:
    def __init__(self, url):
        self.url = type("URL", (), {"drivername": url.split(":", 1)[0]})()

    def connect(self):
        return self

    def execute(self, statement):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def _run_ddl_visitor(self, *args, **kwargs):
        return None


def test_create_engine_from_settings_falls_back_to_sqlite(monkeypatch):
    monkeypatch.setattr(
        connection_module.settings,
        "DATABASE_URL",
        "postgresql://user:pass@localhost:5432/app",
    )

    def fake_create_engine(url, echo=True):
        if url.startswith("postgresql"):
            raise SQLAlchemyError("connection refused")
        return DummyEngine(url)

    monkeypatch.setattr(connection_module, "create_engine", fake_create_engine)

    engine = connection_module.create_engine_from_settings()

    assert engine.url.drivername == "sqlite"
