from sqlalchemy import Column, Integer, String

from short_link_api.models.models import CommonBase


# создаем модель, объекты которой будут храниться в бд
class TestCommon(CommonBase):
    __tablename__ = "test_common"

    test_str = Column(String)
