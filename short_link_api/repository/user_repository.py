from sqlalchemy import select

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import Users


class UserRepository(RepositoryBase):
    """Класс репозитория для сохранения user в БД."""

    def __init__(self, engine):
        super().__init__(engine, Users)

    async def get_user_by_name(self, user_name: str) -> list:
        return (await self._execute_statement(
            select(
                self._get_subquery()).filter(self._get_subquery().user_name == user_name).filter(
                self._get_subquery().deleted == False))).scalar_one_or_none()
