import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from short_link_api.api.v1.entity import router


app = FastAPI(
    title="Заголовок",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(router, prefix='/api/v1')


"""Запуск сервера"""
if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8001)
