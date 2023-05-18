import unittest

from sqlalchemy import insert

from short_link_api.models.models import UrlsPair, Users
from short_link_api.repository.urls_repository import UrlsRepository
from short_link_api.tests.common.common_test_base_init import TestDatabase


class TestRepositoryBase(unittest.IsolatedAsyncioTestCase):
    async def test_repository_get_by_hash_return_url(self):
        test_database = TestDatabase()

        values_dict_user = [
            {'id': 1, 'user_name': 'test_user1'},
            {'id': 2, 'user_name': 'test_user2'},
            {'id': 3, 'user_name': 'test_user3'}
        ]

        values_dict_urls = [
            {'id': 1, 'origin_url': 'ya.ru', 'hash_url': 'dafaagadaag', 'user_id': 1},
            {'id': 2, 'origin_url': 'google.ru', 'hash_url': 'faafsdg', 'user_id': 2},
            {'id': 3, 'origin_url': 'youtube.com', 'hash_url': 'wfarg', 'user_id': 3},
        ]

    #     user_name = Column(String, unique=True)
    #     urls_pair = relationship("UrlsPair", back_populates="users")
    #
    #     __tablename__ = "urls_pair"
    #
    #     origin_url = Column(String, unique=True)
    #     hash_url = Column(String, unique=True)
    #     user_id = Column(Integer, ForeignKey("users.id"))
    #     users = relationship('Users', back_populates='urls_pair')
    #     visits_id = Column(Integer, ForeignKey('visits.id'), default=None)
    #     visits = relationship("Visits", backref=backref("urls_pair", uselist=False))



        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(Users).values(values_dict_user))
            await conn.commit()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(UrlsPair).values(values_dict_urls))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = UrlsRepository(session)

            result = await repository.get_url_by_hash('dafaagadaag')

        self.assertEqual(result.origin_url, 'ya.ru')
        test_database.dispose()
