from sqlalchemy import Column, String, Integer, Boolean, LargeBinary
from sqlalchemy.orm import declarative_base

BaseDBModel = declarative_base()


class TableContent(BaseDBModel):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(LargeBinary, nullable=False)
    owner_id = Column(Integer, nullable=False)
    comment = Column(String(256), nullable=False, default="")
    private = Column(Boolean, nullable=False, default=True)
    content_type = Column(String, nullable=False)


class TableUsers(BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, nullable=False, default=True)
    login = Column(String(32), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False)
    api_key = Column(String(36), nullable=False)

