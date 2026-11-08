import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crud.main import Base, User, app, get_session


@pytest.fixture
def user_data():
    # 初期テストデータ読込
    data_path = Path(__file__).parent / "data" / "test.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


@pytest.fixture
def client(tmp_path: Path, user_data):
    # 初期テストデータ DB 作成
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        for d in user_data:
            user = User(name=d["name"], age=d["age"])
            session.add(user)
            session.commit()

    # pytest 用 DB session
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
