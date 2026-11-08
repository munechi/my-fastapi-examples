from fastapi import status
from fastapi.testclient import TestClient


def test_get_all(client: TestClient, user_data):
    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    actual = [{k: v for k, v in user.items() if k != "id"} for user in response.json()]
    assert actual == user_data


def test_get(client: TestClient, user_data):
    response = client.get("/items/1")
    assert response.status_code == status.HTTP_200_OK
    actual = {"name": response.json()["name"], "age": response.json()["age"]}
    assert actual == user_data[0]


def test_get_id_not_found(client: TestClient):
    response = client.get("/items/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_invalid_id(client: TestClient):
    response = client.get("/items/a")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_add(client: TestClient):
    data = {"name": "高橋", "age": 34}
    response = client.post("/items", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 3} | data


def test_update(client: TestClient, user_data):
    data = {"name": "佐々木", "age": 41}
    response = client.put("/items/2", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 2, "name": data["name"], "age": data["age"]}


def test_delete(client: TestClient):
    response = client.delete("/items/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""
    # 削除されていることを確認
    response = client.get("/items/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_id_not_found(client: TestClient):
    response = client.delete("/items/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_id(client: TestClient):
    response = client.delete("/items/a")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
