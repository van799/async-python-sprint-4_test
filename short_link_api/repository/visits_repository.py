from sqlalchemy.orm import Session

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import Visits
from short_link_api.shared.model.get_model_base import VisitsModelBase


class VisitsRepository(RepositoryBase):
    """Класс репозитория для сохранения URLs в БД."""

    def __init__(self, engine):
        super().__init__()
        self.__engine = engine

    def add(self, objects):
        VisitsRepository._add_objects(objects, self.__engine)

    def get(self):
        return VisitsRepository._get_objects(self.__engine)

    @staticmethod
    def _get_objects(engine):
        with Session(autoflush=False, bind=engine) as db:
            # получение всех объектов
            return db.query(Visits).all()

    @staticmethod
    def _add_objects(objects: VisitsModelBase, engine):
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Person для добавления в бд
            add_objects = Visits(
                visit_call=objects.visit_call,
                timestamp=objects.visit_call
            )
            db.add(add_objects)  # добавляем в бд
            db.commit()  # сохраняем изменения

    @staticmethod
    def _delete_objects(objects: VisitsModelBase, engine):
        pass
