from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import Visits


class VisitsRepository(RepositoryBase):
    """Класс репозитория для сохранения URLs в БД."""

    def __init__(self, engine):
        super().__init__(engine, Visits)
