from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# データクラス
class Item(BaseModel):
    name: str
    age: int


# ORMの基底クラス
class Base(DeclarativeBase):
    pass


# DB テーブル定義
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


def get_session():
    with Session(engine) as session:
        yield session


# DB 接続
engine = create_engine("sqlite:///test.db", echo=True)

app = FastAPI()

# DI（依存性の注入）する
DbSession = Annotated[Session, Depends(get_session)]


# データ取得（全件）
@app.get("/items")
def get_all_users(session: DbSession):
    stmt = select(User)
    users = session.scalars(stmt).all()

    return users


# データ取得（id指定）
@app.get("/items/{id}")
def get_user(id: int, session: DbSession):
    user = session.get(User, id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


# データ追加
@app.post("/items", status_code=status.HTTP_201_CREATED)
def add_user(item: Item, session: DbSession):
    user = User(name=item.name, age=item.age)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"id": user.id, "name": user.name, "age": user.age}


# データ更新（id指定）
@app.put("/items/{id}")
def update_user(id: int, item: Item, session: DbSession):
    user = session.get(User, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user.name = item.name
    user.age = item.age
    session.commit()
    session.refresh(user)

    return user


# データ削除（id指定）
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: DbSession):
    user = session.get(User, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(user)
    session.commit()
