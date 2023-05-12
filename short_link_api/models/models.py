from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import Session

from fastapi import FastAPI
from sqlalchemy.orm import relationship, backref, sessionmaker, DeclarativeBase

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


# создаем базовый класс для моделей
class CommonBase(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)


# создаем модель, объекты которой будут храниться в бд
class Users(CommonBase):
    __tablename__ = "users"

    user_name = Column(String, unique=True)
    urls_pair = relationship("UrlsPair", back_populates="users")


class UrlsPair(CommonBase):
    __tablename__ = "urls_pair"

    origin_url = Column(String, unique=True)
    hash_url = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    deleted = Column(Boolean)
    users = relationship('Users', back_populates='urls_pair')
    visits_id = Column(Integer, ForeignKey('visits.id'))
    visits = relationship("Visits", backref=backref("urls_pair", uselist=False))


class Visits(CommonBase):
    __tablename__ = "visits"

    visit_call = Column(Integer)
    timestamp = Column(Time)


Base.metadata.create_all(bind=engine)
