from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import Users


class UserRepository(RepositoryBase):
    """Класс репозитория для сохранения user в БД."""

    def __init__(self, engine):
        super().__init__(engine, Users)
