from pydantic import BaseModel


class UsersBaseModel(BaseModel):
    user_name: str


class RequestShortUrlBaseModel(BaseModel):
    origin_url: str
    is_public: bool


class ResponseShortUrlBaseModel(BaseModel):
    short_url: str


class RequestDeleteUrlBaseModel(BaseModel):
    origin_url: str


class ResponseDeleteUrlBaseModel(BaseModel):
    message: str


class ResponseFullUrlBaseModel(BaseModel):
    origin_url: str


class UserUrl(BaseModel):
    short_id: str
    short_url: str
    origin_url: str
    is_public: bool


class ResponseStatusUrlBaseModel(BaseModel):
    user_url: list[UserUrl]


class VisitsBaseModel(BaseModel):
    visit_call: str
    timestamp: str
