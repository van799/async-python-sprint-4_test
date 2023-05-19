from pydantic import BaseModel


class UsersBaseModel(BaseModel):
    user_name: str


class RequestShortUrlBaseModel(BaseModel):
    origin_url: str
    user_name: str


class ResponseShortUrlBaseModel(BaseModel):
    short_url: str


class RequestDeleteUrlBaseModel(BaseModel):
    origin_url: str
    user_name: str


class ResponseDeleteUrlBaseModel(BaseModel):
    message: str


class ResponseFullUrlBaseModel(BaseModel):
    origin_url: str


class VisitsBaseModel(BaseModel):
    visit_call: str
    timestamp: str
