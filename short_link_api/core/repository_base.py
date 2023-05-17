from abc import ABC
from typing import Any

from sqlalchemy import Engine, select, Result, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.expression import Select
from sqlalchemy.engine.base import Connection

from short_link_api.models.models import CommonBase


class RepositoryBase(ABC):
    def __init__(self, session: AsyncSession, repository_type: type(CommonBase)):
        self.__session = session
        self.__repository_type = repository_type

    async def add(self, model: CommonBase) -> None:
        values = dict(filter(lambda x: not x[0].startswith('_'), model.__dict__.items()))
        await self.__execute_statement(insert(self.__repository_type).values(values))

    async def get_all(self) -> list:
        return (await self.__execute_statement(select(self._get_subquery()))).scalars().all()

    async def get_by_id(self, model_id: int) -> list:
        return (await self.__execute_statement(
            select(self._get_subquery()).where(self._get_subquery().id == model_id))).scalar()

    async def delete_by_id(self, model_id: int) -> None:
        await self.__execute_statement(
            update(self._get_subquery()).where(self._get_subquery().id == model_id).values(deleted=True)
        )
    async def count(self):
        return (await self.__execute_statement(
            select(func.count()).select_from(self._get_subquery()))).scalar()

    async def __execute_statement(self, statement: Any) -> list[Any]:

        if type(statement) is Select:
            result = await self.__session.execute(statement)
            return result

        result = await self.__session.execute(statement)
        print(statement)
        if type(statement) is not Select:
            await self.__session.commit()
            return []
        return result

    def _get_subquery(self):
        base_statement = select(self.__repository_type).where(self.__repository_type.deleted == False)
        subquery = aliased(self.__repository_type, base_statement.subquery())
        return subquery

    async def _execute_statement_scalars(self, statement: Any) -> list[Any]:
        return (await self.__execute_statement(statement)).scalars().all()

    async def _execute_statement_scalar(self, statement: Any) -> Any:
        return (await self.__execute_statement(statement)).scalar()

    async def _execute_statement(self, statement: Any) -> None:
        await self.__execute_statement(statement)
