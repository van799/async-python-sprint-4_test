import unittest

from sqlalchemy import select, insert, Select

from short_link_api.tests.common.common_test_base_init import TestDatabase
from short_link_api.tests.common.models import TestCommon
from short_link_api.tests.common.test_repository import TestRepository


class TestRepositoryBase(unittest.IsolatedAsyncioTestCase):

    async def test_repository_add(self):
        test_database = TestDatabase()
        test_common = TestCommon()
        test_common.test_str = 'test'

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            await repository.add(test_common)

        async with test_database.get_engine().begin() as conn:
            await repository.add(test_common)
            result = [row for row in await conn.execute(select(TestCommon))]

        test_database.dispose()
        self.assertEqual(result[0][0], test_common.test_str)

    async def test_repository_get_all(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': False, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            result = await repository.get_all()

        test_database.dispose()
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[2].id, 3)

    async def test_repository_get_by_id(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': False, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)

            result = await repository.get_by_id(2)

        test_database.dispose()
        self.assertEqual(result.id, 2)

    async def test_repository_delete_by_id(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': False, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            await repository.delete_by_id(1)

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            result = await repository.get_all()

        test_database.dispose()
        self.assertEqual(len(result), 2)

    async def test_repository_get_all_does_not_return_deleted_objects(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': True, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)

            result = await repository.get_all()

        test_database.dispose()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)

    async def test_repository_count(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': True, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            result = await repository.count()

        test_database.dispose()
        self.assertEqual(result, 2)

    async def test_repository_execute_statement_scalars(self):
        test_database = TestDatabase()

        values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
                       {'id': 2, 'deleted': False, 'test_str': 'test2'},
                       {'id': 3, 'deleted': False, 'test_str': 'test3'}]

        await test_database.create_session()

        async with test_database.get_engine().begin() as conn:
            await conn.execute(insert(TestCommon).values(values_dict))
            await conn.commit()

        async with await test_database.create_session() as session:
            repository = TestRepository(session)
            statement = Select(TestCommon).where(TestCommon.test_str == "test2")
            result = await repository._execute_statement_scalars(statement)

        test_database.dispose()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].test_str, "test2")

    # async def test_repository_execute_statement_scalar(self):
    #     values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
    #                    {'id': 2, 'deleted': False, 'test_str': 'test2'},
    #                    {'id': 3, 'deleted': False, 'test_str': 'test3'}]
    #
    #     async with test_engine.begin() as conn:
    #         await conn.execute(insert(TestCommon).values(values_dict))
    #         await conn.commit()
    #
    #     async with get_session() as session:
    #         repository = TestRepository(session)
    #         statement = select(func.count()).select_from(select(repository._get_subquery()).where(repository._get_subquery().test_str == "test2"))
    #         print(statement)
    #         result = await repository._execute_statement_scalar(statement)
    #
    #     self.assertEqual(result, 1)

    # async def test_repository_alias_approach(self):
    #     values_dict = [{'id': 1, 'deleted': False, 'test_str': 'test1'},
    #                    {'id': 2, 'deleted': False, 'test_str': 'test2'},
    #                    {'id': 3, 'deleted': False, 'test_str': 'test3'}]
    #
    #     async with test_engine.begin() as conn:
    #         await conn.execute(insert(TestCommon).values(values_dict))
    #         await conn.commit()
    #
    #     async with get_session() as session:
    #         repository = TestRepository(session)
    #
    #         base_statement = select(TestCommon).where(TestCommon.deleted == False)
    #         base_alias = aliased(TestCommon, base_statement.subquery())
    #         statement = select(base_alias).where(base_alias.id == 1)
    #         result = (await session.execute(statement)).scalars().all()
    #         print(result)
    #         statement = select(func.count()).select_from(base_alias).where(base_alias.test_str == "test2")
    #         result = (await session.execute(statement)).scalar()
    #         print(result)
    #         # statement = select(func.count()).select_from(TestCommon)
    #         # print(statement)
    #         # result = await repository._execute_statement_scalar(statement)
    #
    #     self.assertEqual(result, 1)
