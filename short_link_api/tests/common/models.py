from tokenize import String

from sqlalchemy import Column, Integer

from short_link_api.models.models import CommonBase


# создаем модель, объекты которой будут храниться в бд
class TestCommon(CommonBase):
    __tablename__ = "test_common"

    test = Column(Integer)

