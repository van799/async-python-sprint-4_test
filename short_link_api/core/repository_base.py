from abc import ABC, abstractmethod
from typing import Callable

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlalchemy.orm import Session


class RepositoryBase(ABC):
    def __init__(self, engine: Engine, repository_type: type):
        self._engine = engine
        self.__repository_type = repository_type

    def add(self, model: BaseModel) -> None:
        with self.__get_session() as db:
            self._add_object(db, model)
            db.commit()

    def get_all(self) -> list:
        with self.__get_session() as db:
            return self._get_all(db)

    def get_by_id(self, model_id: int) -> list:
        with self.__get_session() as db:
            return self._get_by_id(db, model_id)

    def get_by_filter(self, condition: Callable[[BaseModel], bool]) -> list:
        with self.__get_session() as db:
            return self._get_by_filter(db, condition)

    def delete(self, model_id: int) -> None:
        with self.__get_session() as db:
            self._get_by_filter(db, model_id)

    def __get_session(self) -> Session:
        return Session(autoflush=False, bind=self._engine)

    def _get_all(self, db: Session):
        return db.query(self.__repository_type).all()

    @abstractmethod
    def _get_by_id(self, db: Session, model_id):
        db.query(self.__repository_type).sel
        return db.query(self.__repository_type).filter(self.__repository_type.id==model_id)

    @abstractmethod
    def _get_by_filter(self, db: Session, model):
        pass

    @abstractmethod
    def _add_object(self, db: Session, model):
        pass

    @abstractmethod
    def _delete_objects(self, db: Session, model_id):
        pass
