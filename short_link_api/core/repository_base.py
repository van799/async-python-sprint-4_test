from abc import ABC
from typing import Any

from sqlalchemy import Engine, select, Result, update, insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select

from short_link_api.models.models import CommonBase


class RepositoryBase(ABC):
    def __init__(self, engine: Engine, repository_type: type(CommonBase)):
        self._engine = engine
        self.__repository_type = repository_type

    def add(self, model: CommonBase) -> None:
        key_ = [x for x in model.__dict__ if x.startswith('_')]
        clear_dict = model.__dict__.copy()
        clear_dict.pop(key_[0])
        self.__execute_statement(insert(self.__repository_type).values(clear_dict))

    def get_all(self) -> Result[Any]:
        return self.__execute_statement(select(self.__repository_type))

    def get_by_id(self, model_id: int) -> Result[Any]:
        return self.__execute_statement(select(self.__repository_type).where(self.__repository_type.id == model_id))

    def get_by_filter(self, where_clause) -> Result[Any]:
        return self.__execute_statement(select(self.__repository_type).where(where_clause))

    def delete_by_id(self, model_id: int) -> None:
        self.__execute_statement(
            update(self.__repository_type).where(self.__repository_type.id == model_id).values(deleted=True)
        )

    def delete_by_filter(self, where_clause) -> None:
        self.__execute_statement(
            update(self.__repository_type).where(where_clause).values(deleted=True)
        )

    def __execute_statement(self, statement: Any) -> Result[Any]:
        with self.__get_session() as session:
            result = session.execute(statement)
            s = str(statement)
            if statement is not Select:
                session.commit()
            return result

    def __get_session(self) -> Session:
        return Session(autoflush=False, bind=self._engine)
