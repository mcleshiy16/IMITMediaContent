from pydantic import BaseModel, typing
from fastapi import Body
from typing import Annotated
from enum import Enum


class Tags(Enum):
    users = "users"
    content = "content"


class UserRequestBody(BaseModel):
    login: Annotated[str, Body(description="Логин", min_length=4, max_length=32)]
    password: Annotated[str, Body(description="Пароль", min_length=4, max_length=32)]


class UserRegistrationBody(UserRequestBody):
    email: Annotated[str, Body(description="Почтовый адрес", example="some_email@mail.asu.ru")]


class UserInfoBody(UserRegistrationBody):
    api_key: Annotated[str, Body(description="Ключ API")]


class ResponsePattern(BaseModel):
    success: Annotated[bool, Body(description="Успех выполнения запроса")] = False
    result: Annotated[typing.Any, Body(description="Результат выполнения запроса")] = None
    error: Annotated[str, Body(description="Описание ошибки выполнения запроса")] = ""


class FunctionResult:
    success: bool = False
    result: typing.Any = None
    error: str = ""

    def __init__(self, success: bool = False, result: typing.Any = None, error: str = ""):
        self.success = success
        self.result = result
        self.error = error

    def AsResponsePattern(self):
        return ResponsePattern(success=self.success, result=self.result, error=self.error)
