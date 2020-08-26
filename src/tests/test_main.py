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


def test_read_main_token():
    resp = client.get(
        "/items/foo",
        headers={"X-Token": "coneofsilence"}
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "name": "foo",
        "title": "Foo",
        'image': None,
        "tax": None,
        "price": 0.1,
        "description": "There goes my hero",
        "tags": ["tags"]
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foobar",
            "name": "foobar",
            "price": 0.1,
            "tags": ["tags"],
            "title": "Foo Bar",
            "description": "The Foo Barters"},
    )
    assert response.status_code == 200
