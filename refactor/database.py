from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(self.engine, checkfirst=True)

    def get_session(self):
        return self.SessionLocal()
