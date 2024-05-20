from fastapi import APIRouter, Depends, Security, UploadFile, File, Body
from typing import Annotated
from fastapi.responses import JSONResponse, Response
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from api.v1.models import ResponsePattern, Tags

from api.v1.database.connection import DBConnectionManager
import api.v1.database.manager as DBManager

content_v1_api = APIRouter(prefix="/api/v1/content", tags=[Tags.content])

api_key_header = APIKeyHeader(name="Authorization")
api_key_header_optional = APIKeyHeader(name="Authorization", auto_error=False)


@content_v1_api.get("/", response_class=JSONResponse, tags=[Tags.content])
def GetContentList(api_key: str = Security(api_key_header),
                   session: Session = Depends(DBConnectionManager.GetSession)) -> ResponsePattern:

    return DBManager.GetContentList(session, api_key).AsResponsePattern()


@content_v1_api.post("/", response_class=JSONResponse, tags=[Tags.content])
def WriteContent(comment: Annotated[str, Body()] = "",
                 private: Annotated[bool, Body()] = True,
                 content_id: Annotated[int, Body()] = 0,
                 file: UploadFile = File(...),
                 api_key: str = Security(api_key_header),
                 session: Session = Depends(DBConnectionManager.GetSession)) -> ResponsePattern:

    ContentAddingResult = DBManager.WriteContent(session, api_key, content_id, file.file.read(), file.content_type,
                                                 private, comment)

    return ContentAddingResult.AsResponsePattern()


@content_v1_api.get("/{content_id}", tags=[Tags.content])
def GetContent(content_id: int,
               api_key: str | None = Security(api_key_header_optional),
               session: Session = Depends(DBConnectionManager.GetSession)):

    GetContentResult = DBManager.GetContent(session, api_key, content_id)
    if GetContentResult.success:
        content_info = GetContentResult.result
        return Response(content=content_info["content"], media_type=content_info["content_type"])
    else:
        return GetContentResult.AsResponsePattern()


@content_v1_api.delete("/{content_id}", tags=[Tags.content])
def DeleteContent(content_id: int,
                  api_key: str | None = Security(api_key_header_optional),
                  session: Session = Depends(DBConnectionManager.GetSession)) -> ResponsePattern:

    return DBManager.DeleteContent(session, api_key, content_id).AsResponsePattern()
