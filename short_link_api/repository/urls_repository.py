from sqlalchemy import select

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import UrlsPair


class UrlsRepository(RepositoryBase):
    """Класс репозитория для сохранения URLs в БД."""

    def __init__(self, engine):
        super().__init__(engine, UrlsPair)

    async def get_url_by_hash(self, url_hash: str) -> list:
        return (await self._execute_statement(
            select(
                self._get_subquery()).filter(self._get_subquery().hash_url == url_hash).filter(
                self._get_subquery().deleted == False))).scalar_one_or_none()

    async def get_hash_by_url(self, url: str) -> list:
        return (await self._execute_statement(
            select(
                self._get_subquery()).filter(self._get_subquery().origin_url == url).filter(
                self._get_subquery().deleted == False))).scalar_one_or_none()