import os
import unittest
import os.path

from sqlalchemy import select, create_engine, insert
from sqlalchemy.orm import Session

from short_link_api.models.models import CommonBase
from short_link_api.tests.common.models import TestCommon
from short_link_api.tests.common.test_repository import TestRepository


class TestRepositoryBase(unittest.TestCase):

    def setUp(self):
        path = 'test_sql_app.db'
        if os.path.exists(path):
            os.remove(path)

        SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

        self.test_engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        CommonBase.metadata.create_all(bind=self.test_engine)

        self.repository_base = TestRepository(self.test_engine)

    def test_repository_add(self):
        test_common = TestCommon()
        self.repository_base.add(test_common)

        with self.test_engine.connect() as con:
            for row in con.execute(select(TestCommon)):
                print(row)
                a = 1

            # row = session.query(TestCommon).all()
            # for result in row:
            #     print(result.id, result.deleted, result.test)

        # results = session.execute(select(TestCommon))
        # for result in results:
        #     print(result.id)
        # a = 1
