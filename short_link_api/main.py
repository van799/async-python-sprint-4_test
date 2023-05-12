import uvicorn
from fastapi import FastAPI

from short_link_api.models.models import engine
from short_link_api.repository.urls_repository import UrlsRepository
from short_link_api.shared.model.get_model_base import UrlsModelBase

app = FastAPI()


@app.get("/{user}")
def user_urls(user):
    dict1 = {
        'origin_url': 'youtebe.com',
        'short_url': 'dadadadadaa1',
    }

    dict2 = {
        'origin_url': 'ya.com',
        'short_url': "lalallaalaal2",
    }

    origin_list = [dict1, dict2]

    return origin_list


@app.post("/")
def add_urls(data: UrlsModelBase):
    urls_repository = UrlsRepository(engine)
    urls_repository.add(data)


@app.get("/")
def get_urls():
    urls_repository = UrlsRepository(engine)
    urls_repository.get()


"""Запуск сервера"""
if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8001)
