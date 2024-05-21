from fastapi import FastAPI

from api.v1.users import users_v1_api
from api.v1.content import content_v1_api

from api.v1.database.access import GetConnectionString_render  # Доступ к БД
from api.v1.database.connection import DBConnectionManager

practice_app = FastAPI()
practice_app.include_router(users_v1_api)
practice_app.include_router(content_v1_api)


@practice_app.on_event("startup")
def on_startup():
    DBConnectionManager.InitializeDB(GetConnectionString_render())


@practice_app.get("/")
async def index():
    return "It's working!"
