from sqlalchemy import select

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import UrlsPair


class UrlsRepository(RepositoryBase):
    """Класс репозитория для сохранения URLs в БД."""

    def __init__(self, engine):
        super().__init__(engine, UrlsPair)

    async def get_url_by_hash(self, url_hash: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(UrlsPair.hash_url == url_hash))).scalar_one_or_none()

    async def get_hash_by_url(self, url: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(UrlsPair.origin_url == url))).scalar_one_or_none()
