from pydantic import BaseModel


class UrlsModelBase(BaseModel):
    id: int
    origin_url: str
    hash_url: str
    user_id: int
    deleted: bool
    users: str
    visits_id: int
    visits: str


class UserModelBase(BaseModel):
    id: int
    user_name: str
    urls_pair: str


class VisitsModelBase(BaseModel):
    id: int
    visit_call: int
    timestamp: str
