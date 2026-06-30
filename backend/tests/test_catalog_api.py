import sys
import os
from fastapi.testclient import TestClient

# Ensure repository root is on sys.path so 'backend' package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.app.main import app

# Also ensure the backend directory is on sys.path so `import app` works
BACKEND_DIR = os.path.abspath(os.path.join(ROOT, 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

client = TestClient(app)

# Provide a stub DB to avoid real DB connections in CI/local tests
import importlib
_db_mod = importlib.import_module('app.database.connection')
real_get_db = _db_mod.get_db


class _DummyQuery:
    def order_by(self, *args, **kwargs):
        return self

    def limit(self, n):
        return self

    def all(self):
        return []

    def filter(self, *args, **kwargs):
        return self


class _DummyDB:
    def query(self, *args, **kwargs):
        return _DummyQuery()


def _override_get_db():
    db = _DummyDB()
    try:
        yield db
    finally:
        pass


app.dependency_overrides[real_get_db] = _override_get_db


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Data Access Platform is running successfully"
