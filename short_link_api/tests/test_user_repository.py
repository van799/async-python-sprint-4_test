import os
import unittest

from short_link_api.models.models import engine
from short_link_api.repository.user_repository import UserRepository
from short_link_api.shared.test_get_model_base import GetUserModelBase


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.user_repository = UserRepository(engine)
        GetUserModelBase.user_name = "TestUser"
        self.object = GetUserModelBase

    def test_user_repository_add_and_get(self):
        self.user_repository.add(self.object)
        bd_data = self.user_repository.get()
        path = 'sql_app.db'
        os.remove(path)
        self.assertEqual(bd_data[0].user_name, self.object.user_name)
