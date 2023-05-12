from sqlalchemy.orm import Session

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import Users, engine
from short_link_api.shared.model.get_model_base import UserModelBase


class UserRepository:
    """Класс репозитория для сохранения user в БД."""

    def __init__(self, engine):
        super().__init__()
        self.__engine = engine

    def add(self, objects):
        UserRepository._add_objects(objects, self.__engine)

    def get(self):
        return UserRepository._get_objects(self.__engine)

    @staticmethod
    def _get_objects(engine):
        with Session(autoflush=False, bind=engine) as db:
            # получение всех объектов
            return db.query(Users).all()

    @staticmethod
    def _add_objects(objects: UserModelBase, engine):
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Person для добавления в бд
            add_objects = Users(user_name=objects.user_name)
            db.add(add_objects)  # добавляем в бд
            db.commit()  # сохраняем изменения

    def _delete_objects(self):
        pass
