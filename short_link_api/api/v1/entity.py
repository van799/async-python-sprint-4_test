from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from short_link_api.api.v1.models.api_model import RequestShortUrlBaseModel, \
    ResponseShortUrlBaseModel, ResponseFullUrlBaseModel, RequestDeleteUrlBaseModel, ResponseDeleteUrlBaseModel
from short_link_api.models.database_init import Database
from short_link_api.models.models import Users, UrlsPair
from short_link_api.repository.urls_repository import UrlsRepository
from short_link_api.repository.user_repository import UserRepository

database = Database()
router = APIRouter()


@router.get('/ping', tags=['main'])
async def ping_db(
        db: AsyncSession = Depends(database.get_session)) -> Any:
    """
    Check DB connection status
    """
    try:
        await db.connection()
        connection_status = True
    except Exception:
        connection_status = False

    return {'Connected': connection_status}


@router.post("/")
async def create_url(*,
                     session: AsyncSession = Depends(database.get_session),
                     request: RequestShortUrlBaseModel
                     ) -> Any:
    user_repository = UserRepository(session)
    urls_repository = UrlsRepository(session)
    url = UrlsPair()

    find_user = await user_repository.get_user_by_name(request.user_name)
    find_url = await urls_repository.get_hash_by_url(request.origin_url)

    if find_user is None:
        user = Users()
        user.user_name = request.user_name
        await user_repository.add(user)
        url.user_id = (await user_repository.get_user_by_name(request.user_name)).id
    else:
        url.user_id = find_user.id

    url.origin_url = request.origin_url
    url.hash_url = hash(request.origin_url)
    if find_url is None:
        await urls_repository.add(url)
        result = url.hash_url
    else:
        result = (await urls_repository.get_hash_by_url(request.origin_url)).hash_url

    return ResponseShortUrlBaseModel(short_url=result)


@router.get("/{shorten_url_id}")
async def get_url(*,
                  session: AsyncSession = Depends(database.get_session),
                  shorten_url_id: str
                  ) -> Any:
    urls_repository = UrlsRepository(session)
    url = await urls_repository.get_url_by_hash(shorten_url_id)
    if url is None:
        result = "URL не найден"
    else:
        result = url.origin_url
    return ResponseFullUrlBaseModel(origin_url=result)


@router.post("/delete")
async def delete_url(*,
                     session: AsyncSession = Depends(database.get_session),
                     request: RequestDeleteUrlBaseModel
                     ) -> Any:
    user_repository = UserRepository(session)
    urls_repository = UrlsRepository(session)

    find_user = await user_repository.get_user_by_name(request.user_name)
    find_url = await urls_repository.get_hash_by_url(request.origin_url)

    if find_user is None:
        user_message = "Удалить может только пользователь"
        return ResponseDeleteUrlBaseModel(message=user_message)
    if find_url is None:
        url_message = "Неверный URL"
        return ResponseDeleteUrlBaseModel(message=url_message)
    await urls_repository.delete_by_id(find_url.id)
    return ResponseShortUrlBaseModel(short_url="URL Удален")

# Список возможных эндпойнтов (можно изменять)
#
# 1. Получить сокращённый вариант переданного URL.
# POST /
#  Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом 201.

# 2.Вернуть оригинальный URL.
# GET /<shorten-url-id>

# 3. Метод принимает в качестве параметра идентификатор сокращённого URL
# и возвращает ответ с кодом 307 и оригинальным URL в заголовке Location.
# Вернуть статус использования URL.
# GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]

# 4. Реализуйте метод GET /ping, который возвращает информацию
# о статусе доступности БД.

# 5. Реализуйте возможность «удаления» сохранённого URL.
# Запись должна остаться, но помечаться как удалённая.
# При попытке получения полного URL возвращать ответ с кодом 410 Gone

# 6. Реализуйте взаимодействие с сервисом авторизованного пользователя.
# Пользователь может создавать как приватные, так и публичные ссылки или изменять видимость ссылок.
# Вызов метода GET /user/status возвращает все созданные ранее ссылки в формате:
