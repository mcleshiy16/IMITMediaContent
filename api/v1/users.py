from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.models import ResponsePattern, UserRequestBody, UserRegistrationBody, Tags

from api.v1.database.connection import DBConnectionManager
from api.v1.database.manager import LogInUser, RegisterUser

users_v1_api = APIRouter(prefix="/api/v1/users", tags=[Tags.users])


@users_v1_api.post("/authorize", response_class=JSONResponse, tags=[Tags.users])
async def API_user_get_info(user: UserRequestBody,
                            session: Session = Depends(DBConnectionManager.GetSession)) -> ResponsePattern:

    UserObject = LogInUser(session, user.login, user.password)

    if UserObject is None:
        result = ResponsePattern(error="Login failed. Check your login and password!")
    else:
        result = UserObject.AsResponsePattern()

    return result


@users_v1_api.post("/register", response_class=JSONResponse, tags=[Tags.users])
def API_user_add(UsersInfo: UserRegistrationBody,
                 session: Session = Depends(DBConnectionManager.GetSession)) -> ResponsePattern:

    return RegisterUser(session, UsersInfo.login, UsersInfo.password, UsersInfo.email).AsResponsePattern()
