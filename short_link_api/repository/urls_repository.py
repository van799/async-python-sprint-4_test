from sqlalchemy.orm import Session

from short_link_api.core.repository_base import RepositoryBase
from short_link_api.models.models import UrlsPair
from short_link_api.shared.model.get_model_base import UrlsModelBase


class UrlsRepository(RepositoryBase):
    """Класс репозитория для сохранения URLs в БД."""

    def __init__(self, engine):
        self.__engine = engine

    def add(self, objects: UrlsModelBase):
        UrlsRepository._add_objects(objects, self.__engine)

    def get(self):
        return UrlsRepository._get_objects(self.__engine)

    def delete(self, objects: UrlsModelBase):
        UrlsRepository._delete_objects(objects, self.__engine)

    @staticmethod
    def _get_objects(engine):
        with Session(autoflush=False, bind=engine) as db:
            # получение всех объектов
            return db.query(UrlsPair).all()

    @staticmethod
    def _add_objects(objects: UrlsModelBase, engine):
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Person для добавления в бд
            add_objects = UrlsPair(
                origin_url=objects.origin_url,
                hash_url=objects.hash_url,
                user_id=objects.user_id,
                deleted=objects.deleted,
                users=objects.users,
                visits_id=objects.visits_id,
                visits=objects.visits,
            )
            db.add(add_objects)  # добавляем в бд
            db.commit()  # сохраняем изменения

    @staticmethod
    def _delete_objects(objects: UrlsModelBase, engine):
        with Session(autoflush=False, bind=engine) as db:
            # получаем один объект, у которого id=1
            urls = db.query(UrlsPair).filter(objects.id == 1).first()
            if urls is None:
                # изменениям значения
                urls.deleted = True
                # сохраняем изменения
                db.commit()
