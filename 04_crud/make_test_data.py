import json
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# ORMの基底クラス
class Base(DeclarativeBase):
    pass


# テーブル定義
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


# DB接続用のEngineを作成
engine = create_engine("sqlite:///test.db", echo=True)

# 既存テーブルを削除
Base.metadata.drop_all(engine)

# テーブル作成
Base.metadata.create_all(engine)


path = Path(__file__).parent


def main():
    # データ追加
    with Session(engine) as session:
        items = json.loads(Path(path / "test.json").read_text(encoding="utf-8"))
        for d in items:
            user = User(name=d["name"], age=d["age"])
            session.add(user)
            session.commit()

    # データ印字
    with Session(engine) as session:
        stmt = select(User)
        users = session.scalars(stmt).all()
        for user in users:
            print(user.id, user.name, user.age)


if __name__ == "__main__":
    main()
