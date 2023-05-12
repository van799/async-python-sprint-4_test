from pydantic import BaseModel


class GetUrlsModelBase(BaseModel):
    id: int
    origin_url: str
    hash_url: str
    user_id: int
    deleted: bool
    users: str
    visits_id: int
    visits: str


class GetUserModelBase(BaseModel):
    id: int
    user_name: str
    urls_pair: str


class GetVisitsModelBase(BaseModel):
    id: int
    visit_call: int
    timestamp: str
