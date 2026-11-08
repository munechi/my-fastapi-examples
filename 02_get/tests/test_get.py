from fastapi.testclient import TestClient

from get.main import app

client = TestClient(app)


def test_get01():
    response = client.get("/1/add/2")
    assert response.status_code == 200
    assert response.json() == {"result": 1 + 2}


def test_get02():
    response = client.get("/1/sub/2")
    assert response.status_code == 200
    assert response.json() == {"result": 1 - 2}


def test_get03():
    response = client.get("/2/mul/3")
    assert response.status_code == 200
    assert response.json() == {"result": 2 * 3}


def test_get04():
    response = client.get("/2/div/3")
    assert response.status_code == 200
    assert response.json() == {"result": 2 / 3}


def test_get05():
    response = client.get("/2/div/0")
    assert response.status_code == 400


def test_get06():
    response = client.get("/2/hoge/3")
    assert response.status_code == 400
