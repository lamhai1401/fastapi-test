from fastapi.testclient import TestClient

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app  # noqa: E402

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
