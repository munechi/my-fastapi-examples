import json
from pathlib import Path

from fastapi.testclient import TestClient

from post.main import app

client = TestClient(app)


tests_path = Path(__file__).parent


def test_post01():
    path = Path(tests_path / "data1.json")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"result": data["a"] + data["b"]}


def test_post02():
    path = Path(tests_path / "data2.json")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    response = client.post("/", json=data)
    assert response.status_code == 400
