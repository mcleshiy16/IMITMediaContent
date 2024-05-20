from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from api.v1.database.tables import BaseDBModel


class DBConnectionManager:
    db_engine: Engine = None

    @classmethod
    def InitializeDB(cls, ConnectionString):
        try:
            cls.db_engine = create_engine(ConnectionString, echo=True)
            BaseDBModel.metadata.create_all(bind=cls.db_engine)
        except Exception as exception:
            raise "error: {0}".format(exception)

    @classmethod
    def GetSession(cls):
        with Session(cls.db_engine) as session:
            try:
                yield session
            finally:
                session.close()
