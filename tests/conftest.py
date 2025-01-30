import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
