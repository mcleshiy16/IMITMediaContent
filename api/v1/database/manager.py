from sqlalchemy.orm import Session
import uuid

from api.v1.database.tables import TableUsers, TableContent

from api.v1.models import FunctionResult


def LogInUser(session: Session, login: str, password: str) -> FunctionResult:
    result = FunctionResult(error="User is not exist!")

    User = session.query(TableUsers).filter(TableUsers.login == login, TableUsers.password == password).first()

    if User is not None:
        result = FunctionResult(success=True, result={"api_key": User.api_key, "active": User.active, "id": User.id})

    return result


def AuthorizeUser(session: Session, api_key: str) -> FunctionResult:
    User = session.query(TableUsers).filter(TableUsers.api_key == api_key).first()

    if User is None:
        result = FunctionResult(error="API key is invalid!")
    else:
        result = FunctionResult(success=True, result=User.id)

    return result


def RegisterUser(session: Session, login: str, password: str, email: str) -> FunctionResult:
    User = session.query(TableUsers).filter(TableUsers.login == login).first()

    if User is not None:
        result = FunctionResult(error="Such user already exist!")
    else:
        new_user = TableUsers(id=None, login=login, password=password, email=email, active=True, api_key=str(uuid.uuid4()))

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        result = FunctionResult(success=True, result="Registration success! You're able to login now")

    return result


def GetContentList(session: Session, api_key: str) -> FunctionResult:
    AuthorizationResult = AuthorizeUser(session, api_key)

    if AuthorizationResult.success:
        owner_id: int = AuthorizationResult.result
        AllContent = session.query(TableContent).filter(TableContent.owner_id == owner_id, ).all()

        ContentList = [{"id": content.id, "comment": content.comment, "private": content.private} for content in AllContent]

        result = FunctionResult(success=True, result=ContentList)
    else:
        result = AuthorizationResult

    return result


def WriteContent(session: Session, api_key: str, content_id: int | None, content: bytes, content_type: str, private: bool, comment: str) -> FunctionResult:
    AuthorizationResult = AuthorizeUser(session, api_key)

    if AuthorizationResult.success:
        owner_id: int = AuthorizationResult.result

        if content_id is None:
            content_id = 0

        ContentObject = session.query(TableContent).filter(TableContent.id == content_id).first()
        if ContentObject is None:
            ContentObject = TableContent(id=None, content=content, owner_id=owner_id, private=private, comment=comment, content_type=content_type)
            session.add(ContentObject)
        else:
            ContentObject.private = private
            ContentObject.comment = comment
            ContentObject.content_type = content_type
            ContentObject.content = content

        session.commit()
        session.refresh(ContentObject)

        result = FunctionResult(success=True, result=ContentObject.id)
    else:
        result = AuthorizationResult

    return result


def GetContent(session: Session, api_key: str, content_id: int) -> FunctionResult:
    allow_private_content = False

    if api_key is not None:
        if len(api_key) > 0:
            AuthorizationResult = AuthorizeUser(session, api_key)
            if AuthorizationResult.success:
                allow_private_content = True

    content = session.query(TableContent).filter(TableContent.id == content_id).first()
    if content is None:
        result = FunctionResult(error="Content is not exist!")
    else:
        if (content.private and allow_private_content) or not content.private:
            content_info = {"content": content.content, "content_type": content.content_type}
            result = FunctionResult(success=True, result=content_info)
        else:
            result = FunctionResult(error="Access denied!")

    return result


def DeleteContent(session: Session, api_key: str, content_id: int) -> FunctionResult:
    AuthorizationResult = AuthorizeUser(session, api_key)
    if AuthorizationResult.success:
        content = session.query(TableContent).filter(TableContent.id == content_id).first()
        if content is None:
            result = FunctionResult(error="Content is not exist!")
        else:
            session.delete(content)
            session.commit()
            result = FunctionResult(success=True)
    else:
        result = AuthorizationResult

    return result
