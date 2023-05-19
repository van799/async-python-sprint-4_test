import unittest

from sqlalchemy import insert

from short_link_api.models.models import Users
from short_link_api.repository.user_repository import UserRepository
from short_link_api.tests.common.common_test_base_init import TestDatabase


class TestRepositoryBase(unittest.IsolatedAsyncioTestCase):
    async def test_repository_get_by_name_return_user(self):
        test_database = TestDatabase()

        values_dict = [
            {'id': 1, 'user_name': 'test_user1'},
            {'id': 2, 'user_name': 'test_user2'},
            {'id': 3, 'user_name': 'test_user3'}
        ]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(Users).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = UserRepository(session)

            result = await repository.get_user_by_name('test_user3')

        test_database.dispose()
        self.assertEqual(result.user_name, 'test_user3')

    async def test_repository_get_by_id_return_none(self):
        test_database = TestDatabase()

        values_dict = [
            {'id': 1, 'user_name': 'test_user1'},
            {'id': 2, 'user_name': 'test_user2'},
            {'id': 3, 'user_name': 'test_user3'}
        ]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(Users).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = UserRepository(session)
            result = await repository.get_user_by_name('test_user22')

        test_database.dispose()
        self.assertEqual(result, None)

    async def test_repository_get_by_id_but_user_deleted_return_none(self):
        test_database = TestDatabase()

        values_dict = [
            {'id': 1, 'user_name': 'test_user1'},
            {'id': 2, 'user_name': 'test_user2'},
            {'id': 3, 'user_name': 'test_user3'}
        ]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(Users).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = UserRepository(session)
            await repository.delete_by_id(2)
            result = await repository.get_user_by_name('test_user2')

        test_database.dispose()
        self.assertEqual(result, None)
