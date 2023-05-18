from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time

from sqlalchemy.orm import relationship, backref, sessionmaker, DeclarativeBase


# создаем базовый класс для моделей
class CommonBase(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    deleted = Column(Boolean, default=False)


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
    users = relationship('Users', back_populates='urls_pair')
    visits_id = Column(Integer, ForeignKey('visits.id'), default=None)
    visits = relationship("Visits", backref=backref("urls_pair", uselist=False))


class Visits(CommonBase):
    __tablename__ = "visits"

    visit_call = Column(Integer)
    timestamp = Column(Time)
